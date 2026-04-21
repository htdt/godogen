#!/usr/bin/env bash
# Publish Bevy godogen skills into a target project directory.
# Creates .agents/skills/, Codex hook config, and copies an AGENTS.md.
#
# Usage: ./publish.sh [--force] <target_dir>
#   --force    Delete existing target contents before publishing
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

resolve_path() {
    local raw_path="$1"
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$raw_path"
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

link_bevy_docs() {
    local target_docs_dir="$1"
    local source_docs_dir="$REPO_ROOT/skills/bevy-help/docs"
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

FORCE=0
if [ "${1:-}" = "--force" ]; then
    FORCE=1
    shift
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 [--force] <target_dir>"
    exit 1
fi

TARGET="$(cd "$1" 2>/dev/null && pwd || (mkdir -p "$1" && cd "$1" && pwd))"

if [ "$FORCE" -eq 1 ] && [ -d "$TARGET" ]; then
    echo "Force: cleaning $TARGET"
    rm -rf "${TARGET:?}"
    mkdir -p "$TARGET"
fi

echo "Publishing to: $TARGET"

mkdir -p "$TARGET/.agents/skills"
rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' --exclude='bevy-help/docs/' \
    "$REPO_ROOT/skills/" "$TARGET/.agents/skills/"

link_bevy_docs "$TARGET/.agents/skills/bevy-help/docs"
echo "Linked bevy-help docs from source repo"

cp "$REPO_ROOT/game.md" "$TARGET/AGENTS.md"
echo "Created AGENTS.md"

mkdir -p "$TARGET/.codex/hooks"
cp "$REPO_ROOT/codex_hooks/hooks.json" "$TARGET/.codex/hooks.json"
cp "$REPO_ROOT/codex_hooks/stop_post_task_gate.py" "$TARGET/.codex/hooks/stop_post_task_gate.py"
cp "$REPO_ROOT/codex_hooks/verify_result.py" "$TARGET/.codex/hooks/verify_result.py"
cp "$REPO_ROOT/codex_hooks/verify_result_prompt.md" "$TARGET/.codex/hooks/verify_result_prompt.md"
ensure_codex_hooks_feature "$TARGET/.codex/config.toml"
echo "Installed Codex stop hook"

if [ ! -f "$TARGET/.gitignore" ]; then
    cat > "$TARGET/.gitignore" << 'GI_EOF'
.agents
AGENTS.md
.codex
/target
/screenshots
.bevy-help.log
GI_EOF
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(ls "$TARGET/.agents/skills/" | wc -l)"
