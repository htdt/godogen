#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
DOCS_ROOT=""
RUSTDOC_DIR=""
BEVY_DIR=""
BEVY_WEBSITE_DIR=""

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

ensure_clean_repo() {
    local repo_dir="$1"
    if [ ! -d "$repo_dir/.git" ]; then
        return 0
    fi

    if [ -n "$(git -C "$repo_dir" status --short --untracked-files=no)" ]; then
        echo "error: $repo_dir has tracked local changes; refusing to update it" >&2
        exit 1
    fi
}

clone_or_update_repo() {
    local url="$1"
    local dest="$2"

    if [ ! -d "$dest/.git" ]; then
        if [ -e "$dest" ] && dir_has_entries "$dest"; then
            echo "error: $dest exists but is not a git checkout; move it aside or use an empty docs folder." >&2
            exit 1
        fi
        rmdir "$dest" 2>/dev/null || true
        git clone "$url" "$dest"
        return
    fi

    ensure_clean_repo "$dest"
    git -C "$dest" fetch --tags origin
}

latest_stable_tag() {
    local repo_dir="$1"
    git -C "$repo_dir" tag --list 'v*' --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1
}

maybe_checkout_tag() {
    local repo_dir="$1"
    local ref="$2"
    local required="$3"

    [ -n "$ref" ] || return 0

    if git -C "$repo_dir" rev-parse -q --verify "refs/tags/$ref" >/dev/null; then
        git -C "$repo_dir" checkout "$ref"
        return 0
    fi

    if [ "$required" = "required" ]; then
        echo "error: could not find required ref $ref in $repo_dir" >&2
        exit 1
    fi

    echo "warning: ref $ref not found in $repo_dir; keeping current checkout" >&2
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

sync_rustdoc() {
    local source_doc_root="$BEVY_DIR/target/doc"

    if [ ! -d "$source_doc_root" ]; then
        echo "error: rustdoc output not found at $source_doc_root" >&2
        exit 1
    fi

    mkdir -p "$RUSTDOC_DIR"
    rsync -a --delete "$source_doc_root/" "$RUSTDOC_DIR/"
}

build_rustdoc() {
    cargo doc \
        --manifest-path "$BEVY_DIR/Cargo.toml" \
        -p bevy \
        -p bevy_app \
        -p bevy_ecs \
        -p bevy_asset \
        -p bevy_ui \
        --no-deps
    sync_rustdoc
}

DOCS_ROOT="$(resolve_path "$1")"
RUSTDOC_DIR="$DOCS_ROOT/rustdoc"
BEVY_DIR="$DOCS_ROOT/bevy"
BEVY_WEBSITE_DIR="$DOCS_ROOT/bevy-website"

mkdir -p "$DOCS_ROOT"

echo "Using shared Bevy docs folder: $DOCS_ROOT"
echo "Bevy docs are heavy, about 7 GB after population."
echo "Use a separate permanent folder outside this repo."

link_skill_docs "$REPO_ROOT/bevy/skills/bevy-help"

clone_or_update_repo "https://github.com/bevyengine/bevy.git" "$BEVY_DIR"
clone_or_update_repo "https://github.com/bevyengine/bevy-website.git" "$BEVY_WEBSITE_DIR"

STABLE_TAG="$(latest_stable_tag "$BEVY_DIR")"
if [ -z "$STABLE_TAG" ]; then
    echo "error: unable to determine latest stable Bevy tag" >&2
    exit 1
fi

maybe_checkout_tag "$BEVY_DIR" "$STABLE_TAG" required
maybe_checkout_tag "$BEVY_WEBSITE_DIR" "$STABLE_TAG" optional
build_rustdoc

echo "Configured Bevy docs root: $DOCS_ROOT"
echo "Linked bevy/skills/bevy-help/docs/*"
echo "Populated Bevy repo, Bevy website, and rustdoc for ${STABLE_TAG#v}"
