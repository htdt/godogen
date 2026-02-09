# Godot Skills

## TODO

1. ~~godot-task writes test~~ ✓
1. decomposer / orchestrator for resume
1. git worktrees

## Record screenshots

xvfb-run godot --rendering-driver opengl3 \
    --write-movie screenshots/frame.png \
    --fixed-fps 1 --quit-after 7

## How to create doc_api

```bash
mkdir -p doc_source && cd doc_source
git clone --depth 1 --filter=blob:none --sparse https://github.com/godotengine/godot.git
cd godot && git sparse-checkout set doc/classes

python -m tools.godot_api_converter \
  -i doc_source/godot/doc/classes \
  --split-dir doc_api \
  --class-desc first
```
