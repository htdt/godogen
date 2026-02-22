#!/usr/bin/env bash
# Publish godogen agents + skills into a target project directory.
# Creates .claude/{agents,skills}/ and a game-oriented CLAUDE.md.
#
# Usage: ./tools/publish.sh [--teleforge] <target_dir>
#   --teleforge  Use teleforge.md as CLAUDE.md (for Telegram bot server)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

TELEFORGE=false
while [[ "${1:-}" == --* ]]; do
    case "$1" in
        --teleforge) TELEFORGE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ $# -lt 1 ]; then
    echo "Usage: $0 [--teleforge] <target_dir>"
    exit 1
fi

TARGET="$(cd "$1" 2>/dev/null && pwd || mkdir -p "$1" && cd "$1" && pwd)"

echo "Publishing to: $TARGET"

mkdir -p "$TARGET/.claude/agents"
cp "$REPO_ROOT"/agents/*.md "$TARGET/.claude/agents/"

mkdir -p "$TARGET/.claude/skills"
rsync -a --exclude='doc_source/' --exclude='__pycache__/' \
    "$REPO_ROOT/skills/" "$TARGET/.claude/skills/"

if [ "$TELEFORGE" = true ]; then
    cp "$REPO_ROOT/teleforge.md" "$TARGET/CLAUDE.md"
    echo "Created CLAUDE.md (from teleforge.md)"
elif [ ! -f "$TARGET/CLAUDE.md" ]; then
    cat > "$TARGET/CLAUDE.md" << 'CLAUDE_EOF'
Use `/godogen` to generate or update this game from a natural language description.
CLAUDE_EOF
    echo "Created CLAUDE.md"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. agents: $(ls "$TARGET/.claude/agents/" | wc -l), skills: $(ls "$TARGET/.claude/skills/" | wc -l)"
