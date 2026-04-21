#!/usr/bin/env bash
# Publish Bevy godogen skills into a target project directory.
# Creates .claude/skills/, the Claude Code Stop hook, and copies a CLAUDE.md.
#
# Usage: ./publish.sh [--force] <target_dir>
#   --force    Delete existing target contents before publishing
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

resolve_path() {
    local raw_path="$1"
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$raw_path"
}

merge_stop_hook() {
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
    "timeout": 600,
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

mkdir -p "$TARGET/.claude/skills"
rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' --exclude='bevy-help/docs/' \
    "$REPO_ROOT/skills/" "$TARGET/.claude/skills/"

link_bevy_docs "$TARGET/.claude/skills/bevy-help/docs"
echo "Linked bevy-help docs from source repo"

cp "$REPO_ROOT/game.md" "$TARGET/CLAUDE.md"
echo "Created CLAUDE.md"

mkdir -p "$TARGET/.claude/hooks"
cp "$REPO_ROOT/claude_hooks/stop_post_task_gate.py" "$TARGET/.claude/hooks/stop_post_task_gate.py"
cp "$REPO_ROOT/claude_hooks/verify_result.py" "$TARGET/.claude/hooks/verify_result.py"
cp "$REPO_ROOT/claude_hooks/verify_result_prompt.md" "$TARGET/.claude/hooks/verify_result_prompt.md"
merge_stop_hook "$TARGET/.claude/settings.json"
echo "Installed Claude Code stop hook"

if [ ! -f "$TARGET/.gitignore" ]; then
    cat > "$TARGET/.gitignore" << 'GI_EOF'
.claude
CLAUDE.md
/target
/screenshots
.bevy-help.log
GI_EOF
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(ls "$TARGET/.claude/skills/" | wc -l)"
