---
name: godot-scene
description: Generate Godot scenes programmatically — creates GDScript that builds node hierarchies, compiles via headless Godot to produce .tscn files
argument-hint: <scene description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Godot Scene Generator

You generate GDScript that programmatically creates Godot scenes. The script is executed headless by Godot to produce `.tscn` files.

## Project Root

The caller specifies `{project_root}` (e.g. `project_root=build`). Scene builder scripts and output `.tscn` files live under `{project_root}/`. The Godot project file lives at `{project_root}/project.godot`.

## Workflow

1. **Read references** — ALWAYS read `gdscript.md` before writing code. For node/resource API lookup, follow the steps below.
2. **Write GDScript** — Generate a `.gd` file that builds the scene (see requirements below).
3. **Compile** — Run `godot --headless --script <path_to_gd>` from `{project_root}/` to produce the `.tscn`.
4. **Fix errors** — If Godot reports errors, read the output, fix the `.gd` file, and re-run. Repeat until clean.
5. **Deliver both files** — Keep the `.gd` script (for future updates) and the `.tscn` output.

### Compilation Command

```bash
cd {project_root} && godot --headless --script <path_to_gd_file>
```

The script saves the `.tscn` to the path specified in `ResourceSaver.save()`.

**Error handling:** Parse Godot's stderr/stdout for error lines. Common issues:
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class in `doc_api/`
- `Cannot infer type` — `:=` used with `instantiate()` or untyped `load()`, see type inference rules below
- Script hangs — missing `quit()` call; kill the process and add `quit()`

## Output Requirements

Generate a single GDScript file that:
1. `extends SceneTree` (required for headless execution)
2. Implements `_initialize()` as entry point
3. Builds complete node hierarchy with all properties set
4. Sets `owner` on ALL descendants for serialization
5. Saves scene using `PackedScene.pack()` + `ResourceSaver.save()`
6. Calls `quit()` when done

## API Lookup

Per-class API docs are in `doc_api/`. Follow this order:

1. **Read `doc_api/_common.md`** — index of ~128 commonly used classes (nodes, shapes, meshes, materials, math types). Find the classes you need here first.
2. **If not found, read `doc_api/_other.md`** — index of ~730 remaining classes (networking, IO, niche resources, etc.).
3. **Read `doc_api/{ClassName}.md`** — full API reference for a specific class (props, methods, signals, enums with descriptions).

Example: to look up DirectionalLight3D, read `doc_api/DirectionalLight3D.md`.

## Critical Patterns

### Node Creation & Hierarchy
```gdscript
var root := Node3D.new()
root.name = "Level"

var child := MeshInstance3D.new()
child.name = "Floor"
root.add_child(child)
child.owner = root  # CRITICAL: Required for serialization
```

### Owner Chain (CRITICAL)

**MUST call `set_owner_on_new_nodes(root, root)` ONCE at the end**, after all nodes are added. This sets owner on ALL descendants in one pass.

```gdscript
# At end of _initialize(), AFTER all add_child() calls:
set_owner_on_new_nodes(root, root)

func set_owner_on_new_nodes(node: Node, scene_owner: Node) -> void:
    for child in node.get_children():
        child.owner = scene_owner
        if child.scene_file_path.is_empty():
            # Node created with .new() - recurse into children
            set_owner_on_new_nodes(child, scene_owner)
        # else: instantiated scene (GLB/TSCN) - don't recurse, keeps as reference
```

**WRONG patterns** (cause missing nodes in saved .tscn):
```gdscript
# WRONG: Setting owner only on direct children, forgetting grandchildren
terrain.owner = root  # Terrain's children (Mesh, Collision) have NO owner!

# WRONG: Calling helper on containers instead of root
set_owner_on_new_nodes(track_container, root)  # track_container itself has NO owner!
```

**GLB OWNERSHIP BUG** — Never use unconditional recursion. If you recurse into instantiated GLB models, ALL internal mesh/material nodes get serialized inline as text, causing 100MB+ .tscn files.

### Common Node Compositions

**3D Physics Object:**
```gdscript
var body := RigidBody3D.new()
var collision := CollisionShape3D.new()
var mesh := MeshInstance3D.new()
var shape := BoxShape3D.new()
shape.size = Vector3(1, 1, 1)
collision.shape = shape
body.add_child(collision)
body.add_child(mesh)
```

**Camera Rig:**
```gdscript
var pivot := Node3D.new()
var camera := Camera3D.new()
camera.position.z = 5
pivot.add_child(camera)
```

### Script Attachment
```gdscript
# Attach scripts listed in "Scripts to Attach" section
var script := load("res://scripts/player_controller.gd")
player_node.set_script(script)
```

## Commenting Guidelines

Code will be read by someone with general programming knowledge but no Godot API docs. Comment to bridge this gap.

### ALWAYS Comment

- **Godot-specific patterns:** Why owner assignment matters, why nodes are structured a certain way
- **Non-obvious node/resource choices:** Why `AnimatableBody3D` instead of `RigidBody3D`
- **Magic numbers with domain meaning:** Physics layers, collision masks, timing values
- **Signal connection rationale:** What triggers what and why
- **Workarounds or constraints:** Godot quirks, order-of-operations requirements
- **Implementation decisions:** Why this approach over alternatives

### NEVER Comment

- Self-explanatory assignments: `position = Vector3(0, 5, 0)`
- Standard programming constructs: loops, conditionals, basic math
- Property names that describe themselves: `sprite.visible = false`

### Examples
```gdscript
# GOOD: Godot-specific requirement
child.owner = root  # Required for PackedScene serialization—unowned nodes are excluded

# GOOD: Design decision
var body := CharacterBody3D.new()  # Kinematic for direct velocity control (vs RigidBody3D physics)

# GOOD: Non-obvious value
collision.collision_layer = 2  # Layer 2 = player, separates from environment (layer 1)

# BAD: Obvious
var speed := 5.0  # Set speed to 5
```

## Output Template
```gdscript
extends SceneTree

# Object placement - revision can adjust positions/rotations
@export var ball_position: Vector3 = Vector3(0, 2, 0)  ## Ball spawn point
@export var ball_rotation: Vector3 = Vector3(0, 0, 0)  ## Ball initial rotation
@export var camera_position: Vector3 = Vector3(0, 10, 8)  ## Camera placement
@export var camera_rotation: Vector3 = Vector3(-PI/4, 0, 0)  ## Camera angle

# Layout parameters
@export var floor_size: Vector3 = Vector3(20, 0.5, 20)  ## Floor dimensions
@export var wall_count: int = 4  ## Number of maze walls

func _initialize() -> void:
    print("Generating: {scene_name}")

    var root := {RootNodeType}.new()
    root.name = "{SceneName}"

    # Create ball at exported position/rotation
    var ball := create_ball()
    ball.position = ball_position
    ball.rotation = ball_rotation
    root.add_child(ball)
    ball.owner = root

    # Create camera at exported position/rotation
    var camera := Camera3D.new()
    camera.position = camera_position
    camera.rotation = camera_rotation
    root.add_child(camera)
    camera.owner = root

    # Set ownership chain (skips instantiated scene internals)
    set_owner_on_new_nodes(root, root)

    # Save
    var packed := PackedScene.new()
    var err := packed.pack(root)
    if err != OK:
        push_error("Pack failed: " + str(err))
        quit(1)
        return

    err = ResourceSaver.save(packed, "res://{output_path}.tscn")
    if err != OK:
        push_error("Save failed: " + str(err))
        quit(1)
        return

    print("Saved: res://{output_path}.tscn")
    quit(0)

func set_owner_on_new_nodes(node: Node, scene_owner: Node) -> void:
    for child in node.get_children():
        child.owner = scene_owner
        if child.scene_file_path.is_empty():
            set_owner_on_new_nodes(child, scene_owner)
```

## Asset Loading

When asset assignments are provided, load them into the specified nodes.

**For 3D models (GLB):**

GLB models vary in size. Measure and scale to fit your scene:

```gdscript
# Load GLB - MUST type as PackedScene (load() returns Resource)
var model_scene: PackedScene = load("res://glb/car.glb")
var model = model_scene.instantiate()  # instantiate() returns Node - use = not :=
model.name = "CarModel"

# Find MeshInstance3D to get bounds (GLB structure varies - may be nested)
var mesh_inst: MeshInstance3D = find_mesh_instance(model)
var aabb: AABB = mesh_inst.get_aabb() if mesh_inst else AABB(Vector3.ZERO, Vector3.ONE)
var current_size := aabb.size

# Helper to find first MeshInstance3D in tree
func find_mesh_instance(node: Node) -> MeshInstance3D:
    if node is MeshInstance3D:
        return node
    for child in node.get_children():
        var found = find_mesh_instance(child)  # Recursive call - use = not :=
        if found:
            return found
    return null

# Scale to desired size (e.g., car should be ~2 units long)
var target_length := 2.0
var scale_factor: float = target_length / current_size.x
model.scale = Vector3.ONE * scale_factor

# Fix vertical alignment - place bottom of model at y=0
# aabb.position.y is bottom of model in local space (often negative if origin is centered)
model.position.y = -aabb.position.y * scale_factor

parent_node.add_child(model)
```

> **TYPE INFERENCE ERRORS** — Two common issues with `load()` and `instantiate()`:
> ```gdscript
> # WRONG - load() returns Resource, which has no instantiate():
> var scene := load("res://glb/car.glb")
> var model := scene.instantiate()  # Error: Resource has no instantiate()
>
> # WRONG - instantiate() returns Node, := causes Variant inference error:
> var scene: PackedScene = load("res://glb/car.glb")
> var model := scene.instantiate()  # Error: Cannot infer type from Variant
>
> # CORRECT - type load() AND use = (not :=) for instantiate():
> var scene: PackedScene = load("res://glb/car.glb")
> var model = scene.instantiate()  # Works: no type inference attempted
> ```

**Collision shapes for 3D models:**

Always use simple primitive shapes (BoxShape3D, SphereShape3D, CapsuleShape3D). Never use `create_convex_shape()` or `create_trimesh_shape()` on imported GLB meshes — these cause <1 FPS on high-poly models (100k+ triangles).

```gdscript
# Box from AABB - use this for all imported models
var box := BoxShape3D.new()
box.size = aabb.size * model.scale
collision_shape.shape = box

# For characters/vehicles, capsule or box works fine
var capsule := CapsuleShape3D.new()
capsule.radius = 0.5
capsule.height = 1.8
```

Only use `mesh.create_convex_shape()` if the user explicitly requests mesh-accurate collision.

**For textures (PNG):**

Textures are generated as seamless tileable images. Apply directly as material:

```gdscript
var mat := StandardMaterial3D.new()
mat.albedo_texture = load("res://img/grass.png")
mesh_instance.set_surface_override_material(0, mat)
```

### Child Scene Instancing

When "Child Scenes to Instance" is provided, load and instance those scenes. Child scenes are pre-generated `.tscn` files.

> **TYPE INFERENCE ERRORS** — Two common issues:
> ```gdscript
> # WRONG - load() returns Resource:
> var car_scene := load("res://scenes/car.tscn")
> var car := car_scene.instantiate()  # Error: Resource has no instantiate()
>
> # WRONG - instantiate() returns Node, := causes Variant error:
> var car_scene: PackedScene = load("res://scenes/car.tscn")
> var car := car_scene.instantiate()  # Error: Cannot infer type from Variant
>
> # CORRECT - type load() AND use = for instantiate():
> var car_scene: PackedScene = load("res://scenes/car.tscn")
> var car = car_scene.instantiate()  # Works
> ```

```gdscript
# Load and instance a child scene - MUST type as PackedScene, use = for instantiate
var car_scene: PackedScene = load("res://scenes/car.tscn")
var car = car_scene.instantiate()
car.name = "PlayerCar"
car.position = Vector3(0, 0, 5)
root.add_child(car)
# Child nodes already have owner set — just set owner on the instance root
car.owner = root
```

**Important:**
- Use `instantiate()` not `new()` — scenes are PackedScenes
- Set `.owner = root` on the instanced node (child internals already have owner)
- Position/rotate each instance as needed
- The instanced scene's scripts will run at runtime, not build-time

## Scale Reference

**Godot uses 1 unit = 1 meter.** All values below assume this convention.

### 3D Scale Guidelines

| Object Type | Typical Size | Example |
|-------------|--------------|---------|
| Human/character | 1.8m tall, 0.5m wide | `BoxShape3D.size = Vector3(0.5, 1.8, 0.5)` |
| Car | 4m long, 1.8m wide, 1.5m tall | `BoxShape3D.size = Vector3(4, 1.5, 1.8)` |
| Platform/floor | 3-10m per side, 0.2-0.5m thick | `BoxShape3D.size = Vector3(5, 0.3, 5)` |
| Ball/projectile | 0.2-0.5m diameter | `SphereShape3D.radius = 0.25` |
| Door/opening | 2m tall, 1m wide | `BoxShape3D.size = Vector3(1, 2, 0.1)` |
| Large environment | 50-200m | Ground plane, sky boundary |

**Camera distances:**
- Third-person: 5-10m behind/above subject
- Top-down: 15-30m above (use orthogonal projection for strategy games)
- First-person: camera at ~1.7m height (eye level)

**Texture UV tiling:** For large surfaces, scale UVs to avoid stretched textures:
```gdscript
var mat := StandardMaterial3D.new()
mat.albedo_texture = load("res://img/grass.png")
# Tile texture every 2 meters on a 20m floor
mat.uv1_scale = Vector3(10, 10, 1)  # 20m / 2m = 10 tiles
mesh_instance.set_surface_override_material(0, mat)
```

### 2D Scale Guidelines

2D uses pixels. Standard viewport: 1920x1080 or 1280x720.

| Object Type | Typical Size | Example |
|-------------|--------------|---------|
| Player sprite | 64-128px | `Sprite2D` with 64x64 texture |
| Tile | 16, 32, or 64px | TileMap with 32x32 tiles |
| UI button | 150-300px wide | `Button` with min size |
| Projectile | 8-32px | Small sprite or particle |

**Camera2D zoom:**
- `zoom = Vector2(1, 1)` — default, pixel-perfect
- `zoom = Vector2(2, 2)` — zoomed in 2x
- `zoom = Vector2(0.5, 0.5)` — zoomed out, shows 2x area

### Common Mistakes

- **`load()` without type** causes `instantiate()` method not found — always type as `PackedScene`
- **`:=` with `instantiate()`** causes Variant type inference error — use `=` instead

## @export Parameters

Use `@export` for ALL tunable build-time values. This allows adjustment without regenerating code.

```gdscript
extends SceneTree

# Object placement and orientation
@export var player_position: Vector3 = Vector3(0, 1, 0)  ## Player spawn point
@export var player_rotation: Vector3 = Vector3(0, 0, 0)  ## Player facing direction (radians)
@export var model_rotation: Vector3 = Vector3(0, PI, 0)  ## Fix GLB orientation (often needs 180 Y)
@export var model_scale: float = 1.0  ## Scale factor for imported models

# Layout and structure
@export var platform_count: int = 5  ## Number of platforms
@export var platform_spacing: float = 3.0  ## Meters between platforms
@export var floor_size: Vector3 = Vector3(20, 0.5, 20)  ## Floor dimensions
@export var wall_height: float = 3.0  ## Wall height

# Camera setup
@export var camera_position: Vector3 = Vector3(0, 15, 10)  ## Camera world position
@export var camera_rotation: Vector3 = Vector3(-PI/4, 0, 0)  ## Camera angle (radians)
```

**What to export (scene placement):**
- **Positions**: `player_position`, `spawn_point`, `camera_position`
- **Rotations**: `model_rotation`, `player_rotation` (fix GLB orientation with `Vector3(0, PI, 0)`)
- **Scales**: `model_scale`, `object_scale`
- **Layout**: `platform_count`, `spacing`, `grid_size`
- **Dimensions**: `floor_size`, `wall_height`, `room_size`

**NOT for scenes** (use runtime scripts instead):
- Movement speeds, forces, gravity
- Health, damage, cooldowns
- Anything that changes during gameplay

**Format:** `@export var name: Type = default  ## Brief description`

## Constraints

- Use ONLY nodes and resources available in Godot — look up unfamiliar classes in `doc_api/`
- Do NOT use `@onready` or scene-time annotations (this runs at build-time)
- Do NOT use `preload()` — use `load()` (preload fails in headless)
- ATTACH all scripts listed in "Scripts to Attach" using `node.set_script(load("path"))`
- Do NOT connect signals at build-time — scripts aren't instantiated yet, so `signal.connect(node.method)` will fail. Signal connections belong in runtime scripts' `_ready()` method
- ALWAYS set `.name` on every node you create — script generator needs predictable names for `@onready` references
- Save to the EXACT output path specified by the user (e.g., `res://scenes/main.tscn`)
- **MANDATORY `quit()`** — Script MUST call `quit()` at the end. Without it, Godot runs forever in headless mode.
- **2D/3D consistency** — Use ONLY 2D nodes (Node2D, CharacterBody2D, Area2D, Camera2D) OR 3D nodes (Node3D, CharacterBody3D, Area3D, Camera3D). Never mix dimensions in the same scene hierarchy.
