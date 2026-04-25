#!/usr/bin/env bash
# Publish Godogen runtime files into a target game repo.
#
# Usage:
#   ./publish.sh --engine godot|bevy --agent claude|codex --out <target_dir> [--force]
#   ./publish.sh --engine godot|bevy --agent claude|codex <target_dir> [--force]
#
# The Stop hook is best-effort: when `tg-push` and TG_* env vars are present at runtime
# it pushes the latest screenshots/result/{N}/video.mp4 to Telegram, otherwise it no-ops.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

ENGINE=""
AGENT=""
OUT=""
FORCE=0

usage() {
    sed -n '1,9p' "$0" >&2
}

resolve_path() {
    local raw_path="$1"
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$raw_path"
}

render_dir() {
    local root="$1"
    shift
    python3 - "$root" "$@" <<'PY'
from pathlib import Path
import os
import sys

root = Path(sys.argv[1])
pairs = sys.argv[2:]
replacements = {}
for pair in pairs:
    key, value = pair.split("=", 1)
    replacements["${" + key + "}"] = value

for path in root.rglob("*"):
    if not path.is_file() or path.is_symlink():
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    original = text
    for token, value in replacements.items():
        text = text.replace(token, value)
    if text != original:
        path.write_text(text)
PY
}

generate_codex_metadata() {
    local skills_root="$1"
    python3 - "$skills_root" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

skills_root = Path(sys.argv[1])


def parse_frontmatter(path: Path) -> dict[str, str | bool]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    lines = text[4:end].splitlines()
    data: dict[str, str | bool] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if not line.strip() or ":" not in line:
            idx += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "|":
            idx += 1
            block: list[str] = []
            while idx < len(lines):
                candidate = lines[idx]
                if candidate and not candidate.startswith(" ") and ":" in candidate:
                    break
                block.append(candidate[2:] if candidate.startswith("  ") else candidate)
                idx += 1
            data[key] = "\n".join(block).strip()
            continue
        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip('"').strip("'")
        idx += 1
    return data


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", name) if part)


for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        continue
    meta = parse_frontmatter(skill_file)
    name = str(meta.get("name") or skill_dir.name)
    description = str(meta.get("description") or "").strip()
    first_description = " ".join(description.split())
    if len(first_description) > 120:
        first_description = first_description[:117].rstrip() + "..."
    display_name = str(meta.get("display_name") or title_from_name(name))
    short_description = str(meta.get("short_description") or first_description or display_name)
    default_prompt = str(meta.get("default_prompt") or f"Use ${name} when this skill is relevant.")

    lines = [
        "interface:",
        f"  display_name: {json.dumps(display_name)}",
        f"  short_description: {json.dumps(short_description)}",
        f"  default_prompt: {json.dumps(default_prompt)}",
    ]
    if "allow_implicit_invocation" in meta:
        value = "true" if bool(meta["allow_implicit_invocation"]) else "false"
        lines.extend(["", "policy:", f"  allow_implicit_invocation: {value}"])

    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "openai.yaml").write_text("\n".join(lines) + "\n")
PY
}

merge_claude_stop_hook() {
    local settings_path="$1"

    python3 - "$settings_path" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)

data = {}
if path.exists():
    raw = path.read_text().strip()
    if raw:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise SystemExit(f"error: {path} is not a JSON object")

hooks = data.setdefault("hooks", {})
stop_entries = hooks.setdefault("Stop", [])

command = 'python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/stop_post_task_gate.py'
gate_entry = {
    "type": "command",
    "command": command,
    "timeout": 60,
}

for entry in stop_entries:
    inner = entry.get("hooks") if isinstance(entry, dict) else None
    if not isinstance(inner, list):
        continue
    for idx, hook in enumerate(inner):
        if isinstance(hook, dict) and hook.get("command") == command:
            inner[idx] = gate_entry
            path.write_text(json.dumps(data, indent=2) + "\n")
            raise SystemExit

stop_entries.append({"hooks": [gate_entry]})
path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

ensure_codex_hooks_feature() {
    local config_path="$1"

    python3 - "$config_path" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)

text = path.read_text() if path.exists() else ""
if not text.strip():
    path.write_text("[features]\ncodex_hooks = true\n")
    raise SystemExit

lines = text.splitlines()
features_start = None
for idx, line in enumerate(lines):
    if line.strip() == "[features]":
        features_start = idx
        break

if features_start is None:
    suffix = "" if text.endswith("\n") else "\n"
    path.write_text(text + suffix + "[features]\ncodex_hooks = true\n")
    raise SystemExit

features_end = len(lines)
for idx in range(features_start + 1, len(lines)):
    stripped = lines[idx].strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        features_end = idx
        break

for idx in range(features_start + 1, features_end):
    stripped = lines[idx].lstrip()
    if stripped.startswith("codex_hooks"):
        indent = lines[idx][: len(lines[idx]) - len(stripped)]
        lines[idx] = f"{indent}codex_hooks = true"
        path.write_text("\n".join(lines) + "\n")
        raise SystemExit

lines.insert(features_start + 1, "codex_hooks = true")
path.write_text("\n".join(lines) + "\n")
PY
}

inject_claude_lookup_frontmatter() {
    local skill_file="$1"
    python3 - "$skill_file" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
if not text.startswith("---\n"):
    raise SystemExit
end = text.find("\n---", 4)
if end == -1:
    raise SystemExit
frontmatter = text[4:end]
body = text[end:]

claude_keys = ("context:", "model:", "agent:")
lines = frontmatter.splitlines()
keep = [line for line in lines if not any(line.lstrip().startswith(key) for key in claude_keys)]
keep.extend(["context: fork", "model: sonnet", "agent: Explore"])
path.write_text("---\n" + "\n".join(keep) + body)
PY
}

link_bevy_docs() {
    local target_docs_dir="$1"
    local source_docs_dir="$REPO_ROOT/bevy/skills/bevy-help/docs"
    local name

    mkdir -p "$target_docs_dir"
    if [ -f "$source_docs_dir/.gitignore" ]; then
        cp "$source_docs_dir/.gitignore" "$target_docs_dir/.gitignore"
    fi

    for name in rustdoc bevy bevy-website; do
        local source_link="$source_docs_dir/$name"
        local target_link="$target_docs_dir/$name"
        local source_target

        if [ ! -L "$source_link" ]; then
            echo "error: $source_link is not configured." >&2
            echo "Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> in this source repo before publishing." >&2
            exit 1
        fi

        source_target="$(resolve_path "$source_link")"
        if [ ! -d "$source_target" ]; then
            echo "error: $source_link points to missing docs at $source_target." >&2
            echo "Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> again with a valid Bevy docs folder before publishing." >&2
            exit 1
        fi

        rm -rf "$target_link"
        ln -s "$source_target" "$target_link"
    done
}

while [ $# -gt 0 ]; do
    case "$1" in
        --engine)
            ENGINE="${2:-}"
            shift 2
            ;;
        --agent)
            AGENT="${2:-}"
            shift 2
            ;;
        --out)
            OUT="${2:-}"
            shift 2
            ;;
        --force)
            FORCE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo "error: unknown option $1" >&2
            usage
            exit 1
            ;;
        *)
            if [ -n "$OUT" ]; then
                echo "error: target specified more than once" >&2
                exit 1
            fi
            OUT="$1"
            shift
            ;;
    esac
done

case "$ENGINE" in
    godot|bevy) ;;
    *)
        echo "error: --engine must be godot or bevy" >&2
        usage
        exit 1
        ;;
esac

case "$AGENT" in
    claude)
        MANIFEST="CLAUDE.md"
        SKILLS_DIR_REL=".claude/skills"
        HOOK_CONFIG_DIR=".claude"
        AGENT_NAME="Claude"
        GODOGEN_COMMAND="/godogen"
        GODOT_API_COMMAND="/godot-api"
        BEVY_HELP_COMMAND="/bevy-help"
        ;;
    codex)
        MANIFEST="AGENTS.md"
        SKILLS_DIR_REL=".agents/skills"
        HOOK_CONFIG_DIR=".codex"
        AGENT_NAME="Codex"
        GODOGEN_COMMAND="\$godogen"
        GODOT_API_COMMAND="\$godot-api"
        BEVY_HELP_COMMAND="\$bevy-help"
        ;;
    *)
        echo "error: --agent must be claude or codex" >&2
        usage
        exit 1
        ;;
esac

if [ -z "$OUT" ]; then
    echo "error: --out <target_dir> is required" >&2
    usage
    exit 1
fi

TARGET="$(cd "$OUT" 2>/dev/null && pwd || (mkdir -p "$OUT" && cd "$OUT" && pwd))"

if [ "$FORCE" -eq 1 ] && [ -d "$TARGET" ]; then
    echo "Force: cleaning $TARGET"
    rm -rf "${TARGET:?}"
    mkdir -p "$TARGET"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/skills/godogen"
rsync -a --delete --exclude='__pycache__/' "$REPO_ROOT/shared/skills/godogen/" "$TMP/skills/godogen/"
rsync -a --exclude='__pycache__/' "$REPO_ROOT/$ENGINE/skills/godogen/" "$TMP/skills/godogen/"

if [ "$ENGINE" = "godot" ]; then
    rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' \
        "$REPO_ROOT/godot/skills/godot-api" "$TMP/skills/"
else
    rsync -a --delete --exclude='docs/' --exclude='__pycache__/' \
        "$REPO_ROOT/bevy/skills/bevy-help" "$TMP/skills/"
fi

render_dir "$TMP" \
    "AGENT_ID=$AGENT" \
    "AGENT_NAME=$AGENT_NAME" \
    "SKILLS_DIR=$SKILLS_DIR_REL" \
    "GODOGEN_SKILL_DIR=$SKILLS_DIR_REL/godogen" \
    "GODOT_API_SKILL_DIR=$SKILLS_DIR_REL/godot-api" \
    "BEVY_HELP_SKILL_DIR=$SKILLS_DIR_REL/bevy-help" \
    "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
    "ENGINE_NAME=${ENGINE^}" \
    "GODOGEN_COMMAND=$GODOGEN_COMMAND" \
    "GODOT_API_COMMAND=$GODOT_API_COMMAND" \
    "BEVY_HELP_COMMAND=$BEVY_HELP_COMMAND"

if [ "$AGENT" = "codex" ]; then
    generate_codex_metadata "$TMP/skills"
else
    if [ "$ENGINE" = "godot" ]; then
        inject_claude_lookup_frontmatter "$TMP/skills/godot-api/SKILL.md"
    else
        inject_claude_lookup_frontmatter "$TMP/skills/bevy-help/SKILL.md"
    fi
fi

echo "Publishing $ENGINE/$AGENT to: $TARGET"

mkdir -p "$TARGET/$SKILLS_DIR_REL"
rsync -a --delete "$TMP/skills/" "$TARGET/$SKILLS_DIR_REL/"

if [ "$ENGINE" = "bevy" ]; then
    link_bevy_docs "$TARGET/$SKILLS_DIR_REL/bevy-help/docs"
    echo "Linked bevy-help docs from source repo"
fi

mkdir -p "$TMP/game"
cp "$REPO_ROOT/$ENGINE/game-engine.md" "$TMP/game/game-engine.md"
render_dir "$TMP/game" \
    "AGENT_NAME=$AGENT_NAME" \
    "GODOGEN_COMMAND=$GODOGEN_COMMAND"
cp "$TMP/game/game-engine.md" "$TARGET/$MANIFEST"
echo "Created $MANIFEST"

mkdir -p "$TARGET/$HOOK_CONFIG_DIR/hooks"
rsync -a "$REPO_ROOT/shared/hooks/stop_post_task_gate.py" \
    "$TARGET/$HOOK_CONFIG_DIR/hooks/"
rsync -a "$REPO_ROOT/$ENGINE/hooks/" "$TARGET/$HOOK_CONFIG_DIR/hooks/"
render_dir "$TARGET/$HOOK_CONFIG_DIR/hooks" \
    "AGENT_ID=$AGENT" \
    "AGENT_NAME=$AGENT_NAME" \
    "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
    "ENGINE_NAME=${ENGINE^}"
chmod +x "$TARGET/$HOOK_CONFIG_DIR/hooks/stop_post_task_gate.py" "$TARGET/$HOOK_CONFIG_DIR/hooks/capture_result.sh"

if [ "$AGENT" = "codex" ]; then
    cp "$REPO_ROOT/shared/hooks/hooks.json" "$TARGET/$HOOK_CONFIG_DIR/hooks.json"
    render_dir "$TARGET/$HOOK_CONFIG_DIR" \
        "AGENT_ID=$AGENT" \
        "AGENT_NAME=$AGENT_NAME" \
        "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
        "ENGINE_NAME=${ENGINE^}"
    ensure_codex_hooks_feature "$TARGET/$HOOK_CONFIG_DIR/config.toml"
    echo "Installed Codex stop hook"
else
    merge_claude_stop_hook "$TARGET/$HOOK_CONFIG_DIR/settings.json"
    echo "Installed Claude Code stop hook"
fi

if [ ! -f "$TARGET/.gitignore" ]; then
    {
        if [ "$AGENT" = "claude" ]; then
            printf '.claude\nCLAUDE.md\n'
        else
            printf '.agents\nAGENTS.md\n.codex\n'
        fi
        if [ "$ENGINE" = "godot" ]; then
            printf 'assets\nscreenshots\n.godot\n*.import\nbin/\nobj/\n'
        else
            printf '/target\n/screenshots\n.bevy-help.log\n'
        fi
    } > "$TARGET/.gitignore"
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(find "$TARGET/$SKILLS_DIR_REL" -mindepth 1 -maxdepth 1 -type d | wc -l)"
