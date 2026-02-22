#!/usr/bin/env bash
# Publish godogen agents + skills into a target project directory.
# Creates .claude/{agents,skills}/ and a game-oriented CLAUDE.md.
#
# Usage: ./tools/publish.sh <target_dir>
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <target_dir>"
    exit 1
fi

TARGET="$(cd "$1" 2>/dev/null && pwd || mkdir -p "$1" && cd "$1" && pwd)"

echo "Publishing to: $TARGET"

# Copy agents
mkdir -p "$TARGET/.claude/agents"
cp "$REPO_ROOT"/agents/*.md "$TARGET/.claude/agents/"

# Copy skills (exclude generated docs and pycache)
mkdir -p "$TARGET/.claude/skills"
rsync -a --exclude='doc_source/' --exclude='doc_api/' --exclude='__pycache__/' \
    "$REPO_ROOT/skills/" "$TARGET/.claude/skills/"

# Write game-oriented CLAUDE.md if none exists
if [ ! -f "$TARGET/CLAUDE.md" ]; then
    cat > "$TARGET/CLAUDE.md" << 'CLAUDE_EOF'
Use `/godogen` to generate or update this game from a natural language description.

When writing agents/skills: don't give obvious guidance. Assume the agent is a strong LLM — handholding only pollutes the context.
CLAUDE_EOF
    echo "Created CLAUDE.md"
fi

# Copy settings template (permissions for Godot workflow)
if [ ! -f "$TARGET/.claude/settings.local.json" ]; then
    cp "$REPO_ROOT/.claude/settings.local.json" "$TARGET/.claude/settings.local.json"
    echo "Created .claude/settings.local.json"
fi

echo "Done. agents: $(ls "$TARGET/.claude/agents/" | wc -l), skills: $(ls "$TARGET/.claude/skills/" | wc -l)"
