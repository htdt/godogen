---
name: godot-scaffold
description: Design the architecture of a Godot game and create a compilable project skeleton — project.godot, STRUCTURE.md, script stubs, and scene stubs
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Godot Scaffold Generator

You design the architecture of a Godot game and create a compilable project skeleton: `project.godot`, a structure document, script stubs, and scene stubs. The result is a valid (but blank) Godot project that compiles without errors. You define *what exists and how it connects* — not what it does or how it behaves.

## Project Root

All output goes to `{project_root}/`. The caller specifies this path (e.g. `project_root=build`). All file references below are relative to `{project_root}/`.

## Workflow

1. **Read the game description** — understand what the user wants to build.
2. **Check project directory** — handle existing content (see Build Directory rules below).
3. **Design architecture** — decide on scenes, scripts, signals, and input actions.
4. **Write `{project_root}/project.godot`** — minimal project file with input mappings.
5. **Write `{project_root}/STRUCTURE.md`** — architecture document listing all scenes, scripts, and connections.
6. **Write script stubs** — `{project_root}/scripts/*.gd` with correct extends, signals, and empty handlers.
7. **Build scene stubs** — for each scene, copy the template from `.claude/skills/godot-scaffold/stubs/build_scene.gd` to `{project_root}/scenes/build_{name}.gd` and fill in the 5 vars at the top (`_root_type`, `_root_name`, `_script_path`, `_output_path`, `_children`). Then run each builder in dependency order (leaf scenes first): `cd {project_root} && godot --headless --script scenes/build_{name}.gd`
8. **Verify compilation** — run `cd {project_root} && godot --headless --quit 2>&1` and confirm no `ERROR` or `Parser Error` lines. Fix any issues before finishing. RID leak warnings are benign.

## Build Directory

Output all files to `{project_root}/`. Before starting:

1. Check if `{project_root}/` exists and contains files
2. If it contains an unrelated project or the user asked to start fresh, **delete everything** in `{project_root}/`
3. If it contains a related project (same game, prior iteration), preserve assets (`{project_root}/glb/`, `{project_root}/img/`) and delete the rest

## Output Files

### 1. `{project_root}/project.godot`

Minimal Godot project file with input mappings.

```ini
; Engine configuration file
; Do not edit manually

[application]

config/name="{ProjectName}"
run/main_scene="res://scenes/main.tscn"

[input]

move_forward={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119)]
}
```

**Supported keys and their physical keycodes:**
- W=87, A=65, S=83, D=68
- Up=4194320, Down=4194322, Left=4194319, Right=4194321
- Space=32, Enter=4194309, Escape=4194305
- Shift=4194325, Ctrl=4194326, Alt=4194328

**Mouse buttons** use InputEventMouseButton:
```ini
fire={
"deadzone": 0.2,
"events": [Object(InputEventMouseButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"button_mask":1,"position":Vector2(0,0),"global_position":Vector2(0,0),"factor":1.0,"button_index":1,"canceled":false,"pressed":true,"double_click":false)]
}
```
- Mouse1: button_index=1, button_mask=1
- Mouse2: button_index=2, button_mask=2

Only include input actions the game actually needs.

### 2. `{project_root}/STRUCTURE.md`

Architecture document listing all scenes, scripts, and their connections. This is the reference for the decomposer and all generators.

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

### Bullet
- **File:** res://scenes/bullet.tscn
- **Root type:** RigidBody3D

## Scripts

### PlayerController
- **File:** res://scripts/player_controller.gd
- **Extends:** CharacterBody3D
- **Attaches to:** Player:Player
- **Signals emitted:** died, scored
- **Signals received:** HurtBox.area_entered -> _on_hurt_entered
- **Instantiates:** Bullet

### EnemyAI
- **File:** res://scripts/enemy_ai.gd
- **Extends:** CharacterBody3D
- **Attaches to:** Main:Enemy

## Signal Map

- Player:HurtBox.area_entered -> PlayerController._on_hurt_entered
- Main:GoalArea.body_entered -> LevelManager._on_goal_reached
````

Keep it lean — no descriptions, no requirements, no asset assignments. Just the graph of files, types, and connections.

### 3. Script stubs: `{project_root}/scripts/*.gd`

For each script in the structure, create a stub with the correct `extends`, signal declarations, and empty handler methods.

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

Stubs include:
- Correct `extends` matching the node type
- All declared signals
- Sensible `@export` defaults for key parameters
- Empty lifecycle methods the script will need
- Empty signal handlers for received signals
- Brief `##` doc comment with file path

### 4. Scene builder stubs: `{project_root}/scenes/build_*.gd` → `*.tscn`

For each scene, create a stub builder script that produces a minimal `.tscn`. The scene skill later updates these same `build_*.gd` files with full implementations and re-runs them to regenerate the `.tscn`.

**Process:**

1. Read the template from `.claude/skills/godot-scaffold/stubs/build_scene.gd`.
2. For each scene, write a copy to `{project_root}/scenes/build_{name}.gd` with only the 5 vars at the top changed.
3. Run each in dependency order (leaf scenes first):
```bash
cd {project_root} && godot --headless --script scenes/build_player.gd
cd {project_root} && godot --headless --script scenes/build_main.gd
```

**Example** — stub for Player scene (`scenes/build_player.gd`):
```gdscript
var _root_type := "CharacterBody3D"
var _root_name := "Player"
var _script_path := "res://scripts/player_controller.gd"
var _output_path := "res://scenes/player.tscn"
var _children: Array = []
```

**Example** — stub for Main scene with children (`scenes/build_main.gd`):
```gdscript
var _root_type := "Node3D"
var _root_name := "Main"
var _script_path := "res://scripts/main_controller.gd"
var _output_path := "res://scenes/main.tscn"
var _children: Array = [["Player", "res://scenes/player.tscn"]]
```

| Var | Source | Notes |
|-----|--------|-------|
| `_root_type` | Scene root type from STRUCTURE.md | `"CharacterBody3D"`, `"Node3D"`, etc. |
| `_root_name` | Scene name from STRUCTURE.md | Matches root node name |
| `_script_path` | Script that attaches to root, or `""` | Only scripts where `Attaches to` is `Scene:Scene` (root) |
| `_output_path` | Scene file path from STRUCTURE.md | `"res://scenes/player.tscn"` |
| `_children` | Child scene instances | `[["Name", "res://scenes/child.tscn"], ...]` |

**Ordering:** Leaf scenes (no children) must be built before scenes that instance them. Topological sort by the children graph.

## Architecture Rules

1. **Explicit 2D or 3D** — state dimension once at top, use consistently. Never mix: 2D uses Node2D, CharacterBody2D, Area2D, Camera2D; 3D uses Node3D, CharacterBody3D, Area3D, Camera3D.
2. **One root scene minimum** — game needs at least one scene set as main_scene.
3. **Scenes before scripts** — scripts attach to nodes that scenes create.
4. **Match scope to purpose** — trigger zone = Area2D/3D, player = CharacterBody2D/3D, thrown object = RigidBody2D/3D.
5. **Declare all input actions** — any input used by scripts must appear in the input table and project.godot.
6. **Signal contracts** — if script A emits signal X, any receiver must list it. The signal map shows all connections.
7. **One responsibility per script** — split behaviors into focused scripts.
8. **Reusable scripts** — if behavior repeats (coins, enemies), one script attached to multiple nodes.
9. **Keep it simple** — minimal viable feature set. Only include what's explicitly requested.

## Scene Separation Guidelines

**Separate scenes for things that change independently:**
- Player/character
- Enemies
- UI/HUD
- Levels
- Reusable prefabs — bullets, pickups, effects

**Keep together things that change as a unit:**
- A UI panel with its labels and buttons
- An enemy with its hitbox and visual
- A pickup with its collision and sprite

## Scene Children vs Runtime Instantiation

**Children** (build-time composition):
- Reusable entities placed in a level: Player in Main, Enemy in Level
- Rule: no circular dependencies

**Instantiates** (runtime spawning via script):
- Projectiles, spawned enemies, effects, dynamic content

## Common Signal Patterns

Built-in signals (for planning connections):

- Area2D/3D — body_entered, body_exited, area_entered, area_exited
- Button — pressed
- Timer — timeout
- AnimationPlayer — animation_finished
- CharacterBody2D/3D — none built-in (use custom: died, hit, etc.)
- RigidBody2D/3D — body_entered (if contact_monitor enabled)

## What NOT to Include

- Implementation details, requirements, or behavior descriptions (decomposer handles that)
- Asset assignments (decomposer assigns per-task)
- Specific node types beyond scope (generators decide Camera3D vs Path3D)
- Task ordering or build strategy (decomposer handles that)
