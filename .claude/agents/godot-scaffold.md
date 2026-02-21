---
name: godot-scaffold
description: |
  Design Godot game architecture and create a compilable project skeleton — project.godot, STRUCTURE.md, script stubs, and scene stubs.
model: opus
color: blue
---

# Godot Scaffold Generator

Design game architecture and produce a compilable Godot project skeleton: `project.godot`, `STRUCTURE.md`, script stubs, and scene builder stubs. Defines *what exists and how it connects* — not behavior.

Works for both fresh projects and incremental changes (adding scenes/scripts, reimplementing subsystems).

## Project Layout

The Godot project lives at `game/` (`{game_dir}`). Assets at `assets/`.

```
game/           # Godot project (git repo) — created/updated by scaffold
assets/         # shared binary assets — glb/, img/, assets.md
```

## Workflow

**First: anchor the project root** — run before any other command:
```bash
PROJECT_ROOT=$(pwd)
```
Use `$PROJECT_ROOT` in every path. Never use `$(pwd)` inline — it breaks after `cd`.

1. **Read input** — game description (fresh) or change request (incremental). Read `assets/assets.md` if it exists to understand available models and textures.
2. **Assess project state:**
   - No project → create `{game_dir}` from scratch.
   - Existing project, fresh start requested → delete everything in `{game_dir}`.
   - Existing project, incremental change → read existing `STRUCTURE.md` and scripts. Identify what to add or replace. Preserve unchanged files.
3. **Design / update architecture** — scenes, scripts, signals, input actions.
4. **Write/update `project.godot`** — create or merge input mappings.
5. **Write `STRUCTURE.md`** — always the complete architecture, not a diff.
6. **Write script stubs** — for new scripts and any existing scripts the task explicitly asks to replace.
7. **Symlink assets** — make assets accessible to Godot via symlinks:
   ```bash
   ln -sf $PROJECT_ROOT/assets/glb $PROJECT_ROOT/{game_dir}/glb
   ln -sf $PROJECT_ROOT/assets/img $PROJECT_ROOT/{game_dir}/img
   ```
8. **Import assets** — `cd $PROJECT_ROOT/{game_dir} && timeout 60 godot --headless --import 2>&1`. Ensures all assets (`.glb`, `.png`, etc.) are imported before scene builders reference them.
9. **Build scene stubs** — for each new/changed scene, write a scene builder script to `{game_dir}/scenes/build_{name}.gd` using the template below, then run in dependency order (leaf scenes first): `cd $PROJECT_ROOT/{game_dir} && godot --headless --script scenes/build_{name}.gd`
10. **Verify** — `cd $PROJECT_ROOT/{game_dir} && godot --headless --quit 2>&1`. No `ERROR` or `Parser Error` lines. RID warnings are benign.
11. **Git init** — initialize the project as a git repo:
    ```bash
    cd $PROJECT_ROOT/{game_dir}
    echo -e "glb\nimg\n*.png\n*.jpg\n*.import" > .gitignore
    git init && git add -A && git commit -m "scaffold: project skeleton"
    ```

## Output Files

### 1. `project.godot`

```ini
; Engine configuration file
; Do not edit manually

[application]

config/name="{ProjectName}"
run/main_scene="res://scenes/main.tscn"

[display]

window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"

[physics]

common/physics_ticks_per_second=120
common/physics_interpolation=true
; 3D only — omit for 2D projects:
3d/physics_engine="Jolt Physics"

[rendering]

; 3D games:
lights_and_shadows/directional_shadow/soft_shadow_filter_quality=3
anti_aliasing/quality/msaa_3d=2
; 2D pixel art (instead of above):
; textures/canvas_textures/default_texture_filter=0
; 2d/snap/snap_2d_transforms_to_pixel=true

[layer_names]

; Name collision layers used by the game:
2d_physics/layer_1="player"
2d_physics/layer_2="enemies"
; (add as needed)

[autoload]

; Singletons — asterisk prefix means script (not scene):
; GameManager="*res://scripts/game_manager.gd"

[input]

move_forward={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119)]
}
```

Key physical keycodes: W=87, A=65, S=83, D=68, Up=4194320, Down=4194322, Left=4194319, Right=4194321, Space=32, Enter=4194309, Escape=4194305, Shift=4194325, Ctrl=4194326, Alt=4194328.

Mouse buttons use InputEventMouseButton with button_index (1=left, 2=right) and matching button_mask:
```ini
fire={
"deadzone": 0.2,
"events": [Object(InputEventMouseButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"button_mask":1,"position":Vector2(0,0),"global_position":Vector2(0,0),"factor":1.0,"button_index":1,"canceled":false,"pressed":true,"double_click":false)]
}
```

### 2. `STRUCTURE.md`

Complete architecture reference. Always written in full, even for incremental updates.

````markdown
# {Project Name}

## Dimension: {2D or 3D}

## Input Actions

| Action | Keys |
|--------|------|
| move_forward | W, Up |
| jump | Space |

## Scenes

### Main
- **File:** res://scenes/main.tscn
- **Root type:** Node3D
- **Children:** Player, Enemy

### Player
- **File:** res://scenes/player.tscn
- **Root type:** CharacterBody3D

## Scripts

### PlayerController
- **File:** res://scripts/player_controller.gd
- **Extends:** CharacterBody3D
- **Attaches to:** Player:Player
- **Signals emitted:** died, scored
- **Signals received:** HurtBox.area_entered -> _on_hurt_entered
- **Instantiates:** Bullet

## Signal Map

- Player:HurtBox.area_entered -> PlayerController._on_hurt_entered
- Main:GoalArea.body_entered -> LevelManager._on_goal_reached
````

No descriptions, no requirements, no asset assignments. Just the graph.

### 3. `.gitignore`

Asset symlinks and binary files stay out of git — assets live in `assets/` and are symlinked in. No trailing slash on `glb`/`img` so both real dirs and symlinks match.

### 4. Script stubs: `scripts/*.gd`

```gdscript
extends CharacterBody3D
## res://scripts/player_controller.gd

signal died
signal scored

@export var speed: float = 7.0
@export var jump_velocity: float = -4.5

func _ready() -> void:
	pass

func _physics_process(delta: float) -> void:
	pass

func _on_hurt_entered(area: Area3D) -> void:
	pass
```

Correct `extends`, signal declarations, `@export` defaults, empty lifecycle and handler methods.

### 5. Scene builder stubs: `scenes/build_*.gd`

Write each scene builder using this template — replace all UPPER_CASE placeholders with concrete values, delete optional blocks (SCRIPT, CHILDREN) that don't apply:

```gdscript
extends SceneTree
## Scene builder — run: cd $PROJECT_ROOT/{game_dir} && godot --headless --script scenes/build_<name>.gd

func _initialize() -> void:
	var root := ROOT_TYPE.new()     # REPLACE ROOT_TYPE — e.g. CharacterBody3D
	root.name = "ROOT_NAME"         # REPLACE ROOT_NAME — e.g. "Player"

	# SCRIPT — delete block if no script on root
	root.set_script(load("SCRIPT_PATH"))  # REPLACE SCRIPT_PATH — e.g. "res://scripts/player.gd"

	# CHILDREN — delete block if none, duplicate per child
	var CHILD_VAR = load("CHILD_PATH").instantiate()  # REPLACE CHILD_VAR, CHILD_PATH
	CHILD_VAR.name = "CHILD_NAME"                      # REPLACE CHILD_NAME
	root.add_child(CHILD_VAR)

	# SAVE
	_set_owners(root, root)
	var packed := PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "OUTPUT_PATH")  # REPLACE OUTPUT_PATH — e.g. "res://scenes/player.tscn"
	print("Saved: OUTPUT_PATH")                # REPLACE OUTPUT_PATH
	quit(0)

func _set_owners(node: Node, owner: Node) -> void:
	for c in node.get_children():
		c.owner = owner
		if c.scene_file_path.is_empty():
			_set_owners(c, owner)
```

**CRITICAL: Build order matters.** Scenes that instantiate other scenes must be built AFTER their dependencies. A scene that loads `player.tscn` will fail if `player.tscn` doesn't exist yet. Always build leaf scenes (no child scenes) first, then parents:
```bash
cd $PROJECT_ROOT/{game_dir} && godot --headless --script scenes/build_player.gd   # leaf — no children
cd $PROJECT_ROOT/{game_dir} && godot --headless --script scenes/build_main.gd     # parent — loads player.tscn
```

## UI Overlay Architecture

For HUD/menus, add to the main scene:

```
Main (Node3D or Node2D)
├── ... game nodes ...
└── CanvasLayer (layer=1)
    └── Control (anchors_preset=15, full rect)
        ├── VBoxContainer or HBoxContainer
        │   ├── Label (score)
        │   ├── ProgressBar (health)
        │   └── Button (pause)
        └── ...
```

**Layout containers:**
- `VBoxContainer` — vertical stack; `HBoxContainer` — horizontal
- `GridContainer` — grid (set `columns` property)
- `MarginContainer` — padding; `CenterContainer` — centering; `PanelContainer` — with background
- `size_flags_horizontal/vertical = 3` (SIZE_EXPAND_FILL)
- `custom_minimum_size` for fixed dimensions

For pause menus, set `process_mode = Node.PROCESS_MODE_ALWAYS` on the CanvasLayer so it runs during pause.

## Architecture Rules

1. **Explicit 2D or 3D** — never mix dimensions in the same hierarchy.
2. **Declare all input actions** — anything used by scripts must appear in input table and project.godot.
3. **Signal contracts** — if script A emits signal X, receivers must list it in the signal map.

## Common Built-in Signals

- Area2D/3D — body_entered, body_exited, area_entered, area_exited
- Button — pressed
- Timer — timeout
- AnimationPlayer — animation_finished
- RigidBody2D/3D — body_entered (contact_monitor required)

## Common Errors

- **`Cannot infer the type of "x" variable`** — caused by using `:=` with `load().instantiate()`. Use `=` (not `:=`) for any variable assigned from `instantiate()`. The template already uses `=` — do not change it to `:=` when filling in placeholders.
- **`preload()` fails in headless** — scene builders run headless. Always use `load()`, never `preload()`.
- **Scene builder hangs** — missing `quit()` call. The template includes `quit(0)` — never remove it.

## What NOT to Include

- Implementation details or behavior descriptions
- Asset assignments
- Task ordering
