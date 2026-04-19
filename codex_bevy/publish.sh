#!/usr/bin/env bash
# Publish Bevy godogen skills into a target project directory.
# Creates .agents/skills/ and copies an AGENTS.md.
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

mkdir -p "$TARGET/.agents/skills"
rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' \
    "$REPO_ROOT/skills/" "$TARGET/.agents/skills/"

cp "$REPO_ROOT/game.md" "$TARGET/AGENTS.md"
echo "Created AGENTS.md"

if [ ! -f "$TARGET/.gitignore" ]; then
    cat > "$TARGET/.gitignore" << 'GI_EOF'
.agents
AGENTS.md
/target
/screenshots
.vqa.log
GI_EOF
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(ls "$TARGET/.agents/skills/" | wc -l)"
