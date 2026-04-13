#!/usr/bin/env bash
# Publish godogen skills into a target project directory.
# Creates .claude/skills/ and copies a CLAUDE.md.
#
# Usage: ./publish.sh [--force] <target_dir>
#   --force    Delete existing target contents before publishing
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

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
rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' \
    "$REPO_ROOT/skills/" "$TARGET/.claude/skills/"

cp "$REPO_ROOT/game.md" "$TARGET/CLAUDE.md"
echo "Created CLAUDE.md"

if [ ! -f "$TARGET/.gitignore" ]; then
    cat > "$TARGET/.gitignore" << 'GI_EOF'
.claude
CLAUDE.md
assets
screenshots
.vqa.log
.godot
*.import
GI_EOF
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(ls "$TARGET/.claude/skills/" | wc -l)"
