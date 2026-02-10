---
name: godot-scaffold
description: Design the architecture of a Godot game and create a compilable project skeleton — project.godot, STRUCTURE.md, script stubs, and scene stubs
argument-hint: <game description or change request>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Godot Scaffold Generator

Design game architecture and produce a compilable Godot project skeleton: `project.godot`, `STRUCTURE.md`, script stubs, and scene builder stubs. Defines *what exists and how it connects* — not behavior.

Works for both fresh projects and incremental changes (adding scenes/scripts, reimplementing subsystems).

## Project Root

All output goes to `{project_root}/` (e.g. `build/`).

## Workflow

1. **Read input** — game description (fresh) or change request (incremental).
2. **Assess project state:**
   - No project → create from scratch.
   - Existing project, fresh start requested → delete everything except `glb/` and `img/`.
   - Existing project, incremental change → read existing `STRUCTURE.md` and scripts. Identify what to add or replace. Preserve unchanged files.
3. **Design / update architecture** — scenes, scripts, signals, input actions.
4. **Write/update `project.godot`** — create or merge input mappings.
5. **Write `STRUCTURE.md`** — always the complete architecture, not a diff.
6. **Write script stubs** — for new scripts and any existing scripts the task explicitly asks to replace.
7. **Build scene stubs** — for each new/changed scene, copy `.claude/skills/godot-scaffold/stubs/build_scene.gd` to `{project_root}/scenes/build_{name}.gd`, replace all placeholders with concrete values, then run in dependency order (leaf scenes first): `cd {project_root} && godot --headless --script scenes/build_{name}.gd`
8. **Verify** — `cd {project_root} && godot --headless --quit 2>&1`. No `ERROR` or `Parser Error` lines. RID warnings are benign.

## Output Files

### 1. `project.godot`

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

### 3. Script stubs: `scripts/*.gd`

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

### 4. Scene builder stubs: `scenes/build_*.gd`

Copy `.claude/skills/godot-scaffold/stubs/build_scene.gd`, replace all UPPER_CASE placeholders with concrete values. Delete optional blocks (SCRIPT, CHILDREN) that don't apply.

Run in dependency order (leaf scenes first):
```bash
cd {project_root} && godot --headless --script scenes/build_player.gd
cd {project_root} && godot --headless --script scenes/build_main.gd
```

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

## What NOT to Include

- Implementation details or behavior descriptions
- Asset assignments
- Task ordering
