#!/usr/bin/env bash
# Publish Bevy godogen skills into a target project directory.
# Creates .claude/skills/ and copies a CLAUDE.md.
#
# Usage: ./publish.sh [--force] <target_dir>
#   --force    Delete existing target contents before publishing
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

resolve_path() {
    local raw_path="$1"
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$raw_path"
}

link_bevy_docs() {
    local target_docs_dir="$1"
    local source_docs_dir="$REPO_ROOT/skills/bevy-api/docs"
    local name

    mkdir -p "$target_docs_dir"
    if [ -f "$source_docs_dir/.gitignore" ]; then
        cp "$source_docs_dir/.gitignore" "$target_docs_dir/.gitignore"
    fi

    for name in rustdoc bevy bevy-website; do
        local source_link="$source_docs_dir/$name"
        local target_link="$target_docs_dir/$name"

        if [ ! -L "$source_link" ]; then
            echo "error: $source_link is not configured." >&2
            echo "Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> in this source repo before publishing." >&2
            exit 1
        fi

        rm -rf "$target_link"
        ln -s "$(resolve_path "$source_link")" "$target_link"
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
rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' --exclude='bevy-api/docs/' \
    "$REPO_ROOT/skills/" "$TARGET/.claude/skills/"

link_bevy_docs "$TARGET/.claude/skills/bevy-api/docs"
echo "Linked bevy-api docs from source repo"

cp "$REPO_ROOT/game.md" "$TARGET/CLAUDE.md"
echo "Created CLAUDE.md"

if [ ! -f "$TARGET/.gitignore" ]; then
    cat > "$TARGET/.gitignore" << 'GI_EOF'
.claude
CLAUDE.md
/target
/screenshots
.vqa.log
GI_EOF
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(ls "$TARGET/.claude/skills/" | wc -l)"
