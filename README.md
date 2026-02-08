# Godot Skills

## TODO

1. Merge godot-scene + godot-script skill invocations into a single "godot-task" skill
2. Add a lightweight runtime test skill (launch game for N seconds, take screenshot, check for crashes)
3. The scaffold skill could auto-generate the main_controller.gd stub with signal wiring boilerplate since that pattern is always needed
4. Consider having the decomposer produce the scene builder scripts as stubs (just node hierarchy, no logic) so sub-agents only fill in
runtime scripts

## Setup

### 1. Fetch Godot XML docs

```bash
mkdir -p doc_source && cd doc_source
git clone --depth 1 --filter=blob:none --sparse https://github.com/godotengine/godot.git
cd godot && git sparse-checkout set doc/classes
```

### 2. Generate per-class API reference

```bash
python -m tools.godot_api_converter \
  -i doc_source/godot/doc/classes \
  --split-dir doc_api \
  --class-desc first
```

This creates `doc_api/` with:
- `_common.md` — index of ~128 commonly used classes
- `_other.md` — index of ~730 remaining classes
- `{ClassName}.md` — full API reference per class (props, methods, signals, enums)

### Token counts (single-file mode)

```
scene_api.md  - 35,865 tokens
script_api.md - 66,513 tokens
uni_api.md    - 49,787 tokens
```
