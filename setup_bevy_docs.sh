#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <shared_bevy_docs_dir>" >&2
    exit 1
fi

resolve_path() {
    local raw_path="$1"
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$raw_path"
}

dir_has_entries() {
    local dir_path="$1"
    [ -n "$(find "$dir_path" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]
}

ensure_docs_gitignore() {
    local docs_dir="$1"
    mkdir -p "$docs_dir"
    if [ ! -f "$docs_dir/.gitignore" ]; then
        printf '*\n!.gitignore\n' > "$docs_dir/.gitignore"
    fi
}

link_docs_subdir() {
    local docs_dir="$1"
    local shared_root="$2"
    local name="$3"
    local link_path="$docs_dir/$name"
    local shared_path="$shared_root/$name"

    if [ -L "$link_path" ]; then
        if [ "$(resolve_path "$link_path")" = "$shared_path" ]; then
            mkdir -p "$shared_path"
            return 0
        fi
        rm "$link_path"
    elif [ -d "$link_path" ]; then
        if dir_has_entries "$link_path"; then
            if [ -e "$shared_path" ]; then
                if dir_has_entries "$shared_path"; then
                    echo "error: both $link_path and $shared_path contain data; move one side manually." >&2
                    exit 1
                fi
                rmdir "$shared_path"
            fi
            mv "$link_path" "$shared_path"
        else
            rmdir "$link_path"
            mkdir -p "$shared_path"
        fi
    elif [ -e "$link_path" ]; then
        echo "error: $link_path exists and is not a directory or symlink" >&2
        exit 1
    else
        mkdir -p "$shared_path"
    fi

    ln -s "$shared_path" "$link_path"
}

link_skill_docs() {
    local skill_dir="$1"
    local docs_dir="$skill_dir/docs"
    ensure_docs_gitignore "$docs_dir"
    link_docs_subdir "$docs_dir" "$DOCS_ROOT" rustdoc
    link_docs_subdir "$docs_dir" "$DOCS_ROOT" bevy
    link_docs_subdir "$docs_dir" "$DOCS_ROOT" bevy-website
}

DOCS_ROOT="$(resolve_path "$1")"
mkdir -p "$DOCS_ROOT"

echo "Using shared Bevy docs folder: $DOCS_ROOT"
echo "Bevy docs are heavy, about 7 GB after population."
echo "Use a separate permanent folder outside this repo."

link_skill_docs "$REPO_ROOT/codex_bevy/skills/bevy-api"
link_skill_docs "$REPO_ROOT/claude_bevy/skills/bevy-api"

echo "Configured Bevy docs root: $DOCS_ROOT"
echo "Linked codex_bevy/skills/bevy-api/docs/*"
echo "Linked claude_bevy/skills/bevy-api/docs/*"
