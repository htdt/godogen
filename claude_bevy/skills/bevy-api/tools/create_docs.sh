#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$SKILL_DIR/docs"
RUSTDOC_DIR="$DOCS_DIR/rustdoc"
BEVY_DIR="$DOCS_DIR/bevy"
BEVY_WEBSITE_DIR="$DOCS_DIR/bevy-website"
PROJECT_PATH="${1:-}"

require_docs_layout() {
    local path
    for path in "$RUSTDOC_DIR" "$BEVY_DIR" "$BEVY_WEBSITE_DIR"; do
        if [ ! -e "$path" ]; then
            echo "error: $path is missing. Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> in the source repo and republish." >&2
            exit 1
        fi
    done
}

ensure_clean_repo() {
    local repo_dir="$1"
    if [ ! -d "$repo_dir/.git" ]; then
        return 0
    fi

    if [ -n "$(git -C "$repo_dir" status --short)" ]; then
        echo "error: $repo_dir has local changes; refusing to update it" >&2
        exit 1
    fi
}

clone_or_update_repo() {
    local url="$1"
    local dest="$2"

    if [ ! -d "$dest/.git" ]; then
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

resolve_bevy_version() {
    local project_root="$1"
    local json

    json="$(python3 "$SCRIPT_DIR/resolve_bevy_context.py" --json "$project_root")"
    python3 -c 'import json,sys; data=json.load(sys.stdin); print(data.get("bevy_version") or "")' <<<"$json"
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

sync_rustdoc() {
    local source_dir="$1"
    local source_doc_root="$source_dir/target/doc"

    if [ ! -d "$source_doc_root" ]; then
        echo "error: rustdoc output not found at $source_doc_root" >&2
        exit 1
    fi

    mkdir -p "$RUSTDOC_DIR"
    rsync -a --delete "$source_doc_root/" "$RUSTDOC_DIR/"
}

build_from_project() {
    local project_root="$1"
    cargo doc --manifest-path "$project_root/Cargo.toml"
    sync_rustdoc "$project_root"
}

build_from_bevy_repo() {
    cargo doc \
        --manifest-path "$BEVY_DIR/Cargo.toml" \
        -p bevy \
        -p bevy_app \
        -p bevy_ecs \
        -p bevy_asset \
        -p bevy_ui \
        --no-deps
    sync_rustdoc "$BEVY_DIR"
}

require_docs_layout
clone_or_update_repo "https://github.com/bevyengine/bevy.git" "$BEVY_DIR"
clone_or_update_repo "https://github.com/bevyengine/bevy-website.git" "$BEVY_WEBSITE_DIR"

if [ -n "$PROJECT_PATH" ]; then
    PROJECT_ROOT="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$PROJECT_PATH")"
    BEVY_VERSION="$(resolve_bevy_version "$PROJECT_ROOT")"
    if [ -z "$BEVY_VERSION" ]; then
        echo "error: unable to resolve Bevy version from $PROJECT_ROOT" >&2
        exit 1
    fi

    maybe_checkout_tag "$BEVY_DIR" "v$BEVY_VERSION" required
    maybe_checkout_tag "$BEVY_WEBSITE_DIR" "v$BEVY_VERSION" optional
    build_from_project "$PROJECT_ROOT"
else
    STABLE_TAG="$(latest_stable_tag "$BEVY_DIR")"
    if [ -z "$STABLE_TAG" ]; then
        echo "error: unable to determine latest stable Bevy tag" >&2
        exit 1
    fi

    maybe_checkout_tag "$BEVY_DIR" "$STABLE_TAG" required
    build_from_bevy_repo
fi

printf 'docs_root=%s\n' "$DOCS_DIR"
printf 'rustdoc_root=%s\n' "$RUSTDOC_DIR"
printf 'bevy_repo=%s\n' "$BEVY_DIR"
printf 'bevy_website=%s\n' "$BEVY_WEBSITE_DIR"
