#!/usr/bin/env bash
# Bootstrap doc_api for gdscript-doc skill.
# Clones Godot docs (sparse checkout) and generates per-class markdown API reference.
# Safe to re-run — skips if doc_api/ already exists.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS_DIR="$SKILL_DIR/tools"
DOC_SOURCE="$SKILL_DIR/doc_source"
DOC_API="$SKILL_DIR/doc_api"

if [ -d "$DOC_API" ] && [ -f "$DOC_API/_common.md" ]; then
    exit 0
fi

echo "Bootstrapping doc_api..."

if [ ! -d "$DOC_SOURCE/godot/doc/classes" ]; then
    mkdir -p "$DOC_SOURCE"
    git clone --depth 1 --filter=blob:none --sparse \
        https://github.com/godotengine/godot.git "$DOC_SOURCE/godot"
    git -C "$DOC_SOURCE/godot" sparse-checkout set doc/classes
fi

PYTHONPATH="$TOOLS_DIR" python3 "$TOOLS_DIR/godot_api_converter.py" \
    -i "$DOC_SOURCE/godot/doc/classes" \
    --split-dir "$DOC_API" \
    --class-desc full \
    --method-desc full \
    --property-desc full \
    --signal-desc full \
    --constant-desc full \
    --include-virtual \
    --full-signals

echo "doc_api ready at $DOC_API"
