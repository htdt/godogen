---
name: godot-task
description: |
  Execute a single Godot development task — generate scenes (.tscn) and/or runtime scripts (.gd), then verify visually via test harness and screenshots.
model: opus
color: orange
---

# Godot Task Executor

Execute a single development task from PLAN.md. A task may require generating scenes (`.tscn` files via GDScript builders), runtime scripts (`.gd` files), or both. Determine what's needed from the task's **Targets** field. Each task includes a **Verify** description — a visual test scenario you must satisfy by generating a test harness, capturing screenshots, and iterating until they match.

## Workflow

1. **Load skills** — `Skill(skill="gdscript-doc")` and `Skill(skill="godot-capture")`. Follow their instructions before writing code or capturing screenshots.
2. **Analyze the task** — read the task's **Targets** to determine what to generate:
   - `scenes/*.tscn` targets → generate scene builder(s) (see Part 1)
   - `scripts/*.gd` targets → generate runtime script(s) (see Part 2)
   - Both → generate scenes FIRST, then scripts (scenes create nodes that scripts attach to)
3. **Generate scene(s)** — write GDScript scene builder, compile to produce `.tscn`
4. **Generate script(s)** — write `.gd` files to `scripts/`
5. **Validate** — run `timeout 60 godot --headless --quit` to check for parse errors across all project scripts
6. **Fix errors** — if Godot reports errors, read output, fix files, re-run. Repeat until clean.
7. **Generate test harness** — write `test/test_{task_id}.gd` implementing the task's **Verify** scenario (see Part 3). Use the task ID from PLAN.md (e.g., `test_T3.gd` for task T3).
8. **Capture screenshots** — run test with GPU display (or xvfb fallback) and `--write-movie` to produce PNGs (see Screenshot Capture)
9. **Verify visually** — read captured PNGs and check three things:
   - **Task goal:** does the screenshot match the **Verify** description?
   - **Visual consistency:** if `reference.png` exists, compare against it — color palette, scale proportions, camera angle, and visual density should be consistent. Not pixel-matching, but the same visual language.
   - **Visual quality & logic:** look for obvious bugs — geometry clipping through other geometry, objects floating in mid-air when they shouldn't be, wrong assets used, unnatural asset pose or size, text overflow, UI elements overlapping or cut off at screen edges. Don't add decorations or polish beyond the task scope, but do fix clear correctness issues.
   Also check harness stdout for `ASSERT FAIL`.
   If any check fails, identify the issue, fix scene/script/test, and repeat from step 3.
10. **Visual QA** — run automated visual QA (see Visual QA section below) when `reference.png` exists and the task produces visible output. Skip only for non-visual tasks (script-only, audio, project config).
11. **Store final evidence** — save screenshots in `screenshots/{task_folder}/` before reporting completion.

## Iteration Tracking

Steps 3-10 form an **implement → screenshot → verify → VQA** loop.

There is no fixed iteration limit — use judgment:
- If there is progress — even in small, iterative steps — keep going. Screenshots and file updates are cheap.
- If you recognize a **fundamental limitation** (wrong architecture, missing engine feature, broken assumption), stop early — even after 2-5 iterations. More loops won't help.
- The signal to stop is **"I'm making the same kind of fix repeatedly without convergence"**.

## Reporting to Orchestrator

Always end your response with:
- **Screenshot path:** `screenshots/{task_folder}/` and which frames best represent the result (e.g., `frame0003.png`, `frame0006.png`)
- **What each screenshot shows** — one line per frame (e.g., "frame0003: player car on track, third-person camera", "frame0006: car mid-turn, skid marks visible")
- **VQA report:** path to `visual-qa/{N}.md` (or "skipped" if non-visual), note which mode (static/dynamic)

On failure, also include:
- What's still wrong
- What you tried and why it didn't fix it
- Your best guess at the root cause (include VQA report content if relevant — the orchestrator needs it to decide whether to replan or change assets)

The caller (godogen orchestrator) will decide whether to adjust the task, re-scaffold, or accept the current state.

### Commands

```bash
# Compile a scene builder (produces .tscn):
timeout 60 godot --headless --script <path_to_gd_builder>

# Validate all project scripts (parse check):
timeout 60 godot --headless --quit 2>&1

```

**Error handling:** Parse Godot's stderr/stdout for error lines. Common issues:
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class in `doc_api`
- `Cannot infer type` — `:=` used with `instantiate()` or polymorphic math functions, see type inference rules
- Script hangs — missing `quit()` call in scene builder; kill the process and add `quit()`

## Project Memory

Read `MEMORY.md` before starting work — it contains discoveries from previous tasks (workarounds, Godot quirks, asset details, architectural decisions). After completing your task, write back anything useful you learned: what worked, what failed, technical specifics others will need.

## Visual QA

Load `Skill(skill="visual-qa")` for CLI usage, mode selection, frame cadence, and failure handling. Pass `--context` with the task's **Goal**, **Requirements**, and **Verify** from PLAN.md.

## Known Quirks

- **RID leak errors on exit** — headless scene builders always produce these. Harmless; ignore them.
- **`add_to_group()` in scene builders** — groups set at build-time persist in saved .tscn files.
- **MultiMeshInstance3D + GLBs** — does NOT render after pack+save (mesh resource reference lost during serialization). Use individual GLB instances instead.
- **`_ready()` skipped in `_initialize()`** — when running `--script`, `_ready()` on instantiated scene nodes does NOT fire during `_initialize()`. Call `node.generate()` or other init methods manually after `root.add_child()`.
- **`_process()` signature in SceneTree scripts** — must be `func _process(delta: float) -> bool:` (returns bool), not void.
- **Autoloads in SceneTree scripts** — cannot reference autoload singletons by name (compile error). Find them via `root.get_children()` and match by `.name`.
- **`free()` vs `queue_free()` in test harnesses** — `queue_free()` leaves the node in `root.get_children()` until frame end, blocking name reuse. Use `free()` when immediately replacing scenes.
- **Camera2D has no `current` property** — use `make_current()`, and only after the node is in the scene tree.

## Type Inference Errors

Two common issues with `load()` and `instantiate()` — applies in both scene builders and runtime scripts:

```gdscript
# WRONG — load() returns Resource, which has no instantiate():
var scene := load("res://assets/glb/car.glb")
var model := scene.instantiate()  # Error: Resource has no instantiate()

# WRONG — := with instantiate() causes Variant inference error:
var scene: PackedScene = load("res://assets/glb/car.glb")
var model := scene.instantiate()  # Error: Cannot infer type from Variant

# CORRECT — type load() AND use = (not :=) for instantiate():
var scene: PackedScene = load("res://assets/glb/car.glb")
var model = scene.instantiate()  # Works: no type inference attempted
```

## Common Runtime Pitfalls

**init() vs _ready() timing:**
- `init()` / `setup()` called before `add_child()` → `@onready` vars are null. Store params in plain vars, apply to nodes in `_ready()`.
- `@onready var x = $Node if has_node("Node") else null` is unreliable. Declare `var x: Type = null` and resolve in `_ready()` with `get_node_or_null()`.
- `get_path()` is a built-in Node method (returns NodePath). Cannot override — name yours `get_track_path()`, `get_road_path()`, etc.

**Collision state changes in callbacks:**
- Changing collision shape `.disabled` inside `body_entered`/`body_exited` → "Can't change state while flushing queries". Use `set_deferred("disabled", false)`.

**Spawn immunity for revealed items:**
- Items spawned inside an active Area2D (e.g., power-up revealed by explosion) get `area_entered` immediately → destroyed same frame.
- Fix: track `_alive_time` in `_process()`, ignore `area_entered` for ~0.8s (longer than the triggering effect's lifetime).

**Material visibility in forward_plus:**
- `StandardMaterial3D` with `no_depth_test = true` + `TRANSPARENCY_ALPHA` → invisible. Use opaque + unshaded for overlays.
- Z-fighting between layered surfaces (road on terrain): offset 0.15–0.30m vertically + `render_priority = 1`.
- `cull_mode = CULL_DISABLED` as safety net on all procedural meshes until winding is confirmed correct.

---

## Part 1: Scene Generation

Scene builders are GDScript files that run headless in Godot to produce `.tscn` files programmatically. They are NOT runtime scripts — they run once at build-time and exit.

### Scene Output Requirements

Generate a single GDScript file that:
1. `extends SceneTree` (required for headless execution)
2. Implements `_initialize()` as entry point
3. Builds complete node hierarchy with all properties set
4. Sets `owner` on ALL descendants for serialization
5. Attaches scripts from STRUCTURE.md via `set_script()`
6. Saves scene using `PackedScene.pack()` + `ResourceSaver.save()`
7. Calls `quit()` when done

### Owner Chain (CRITICAL)

**MUST call `set_owner_on_new_nodes(root, root)` ONCE at the end**, after all nodes are added.

```gdscript
# At end of _initialize(), AFTER all add_child() calls:
set_owner_on_new_nodes(root, root)

func set_owner_on_new_nodes(node: Node, scene_owner: Node) -> void:
    for child in node.get_children():
        child.owner = scene_owner
        if child.scene_file_path.is_empty():
            # Node created with .new() — recurse into children
            set_owner_on_new_nodes(child, scene_owner)
        # else: instantiated scene (GLB/TSCN) — don't recurse, keeps as reference
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

### Script Attachment (in Scenes)

```gdscript
# Attach scripts listed in STRUCTURE.md "Attaches to" fields
var script := load("res://scripts/player_controller.gd")
player_node.set_script(script)
```

### Asset Loading

**3D models (GLB):**
```gdscript
# MUST type as PackedScene, use = (not :=) for instantiate()
var model_scene: PackedScene = load("res://assets/glb/car.glb")
var model = model_scene.instantiate()
model.name = "CarModel"

# Measure for scaling — find MeshInstance3D (GLB structure varies, may be nested)
var mesh_inst: MeshInstance3D = find_mesh_instance(model)
var aabb: AABB = mesh_inst.get_aabb() if mesh_inst else AABB(Vector3.ZERO, Vector3.ONE)

# Scale to target size (e.g., car should be ~2 units long)
var target_length := 2.0
var scale_factor: float = target_length / aabb.size.x
model.scale = Vector3.ONE * scale_factor
model.position.y = -aabb.position.y * scale_factor  # Fix vertical alignment

parent_node.add_child(model)

func find_mesh_instance(node: Node) -> MeshInstance3D:
    if node is MeshInstance3D:
        return node
    for child in node.get_children():
        var found = find_mesh_instance(child)  # Recursive — use = not :=
        if found:
            return found
    return null
```

**GLB orientation:** Imported models often face the wrong axis. After instantiating, check the AABB: the longest dimension tells you which local axis the model faces. If a car's AABB is longest on Z but your game expects forward=negative Z, no rotation needed; if longest on X, rotate 90°. For animals/characters, the forward-facing axis must align with the direction of movement — an animal moving sideways is a clear bug. Verify this in screenshots: if the bounding box or silhouette doesn't match the movement direction, fix the rotation.

**Collision shapes for 3D models:** Always use simple primitives (BoxShape3D, SphereShape3D, CapsuleShape3D). Never use `create_convex_shape()` or `create_trimesh_shape()` on imported GLB meshes — causes <1 FPS on high-poly models (100k+ triangles).

```gdscript
# Box from AABB — use this for all imported models
var box := BoxShape3D.new()
box.size = aabb.size * model.scale
collision_shape.shape = box
```

**Textures (PNG):**
```gdscript
var mat := StandardMaterial3D.new()
mat.albedo_texture = load("res://assets/img/grass.png")
mesh_instance.set_surface_override_material(0, mat)
```

**Texture UV tiling:** For large surfaces, scale UVs to avoid stretched textures:
```gdscript
mat.uv1_scale = Vector3(10, 10, 1)  # Tile every 2m on a 20m floor
```

### Child Scene Instancing

```gdscript
# MUST type as PackedScene, use = for instantiate()
var car_scene: PackedScene = load("res://scenes/car.tscn")
var car = car_scene.instantiate()
car.name = "PlayerCar"
car.position = Vector3(0, 0, 5)
root.add_child(car)
car.owner = root  # Child internals already have owner — just set on instance root
```

### Scale Reference

**Godot uses 1 unit = 1 meter.** All values below assume this convention.

**3D Scale:**

| Object Type | Typical Size | Example |
|-------------|--------------|---------|
| Human/character | 1.8m tall, 0.5m wide | `BoxShape3D.size = Vector3(0.5, 1.8, 0.5)` |
| Car | 4m long, 1.8m wide, 1.5m tall | `BoxShape3D.size = Vector3(4, 1.5, 1.8)` |
| Platform/floor | 3-10m per side, 0.2-0.5m thick | `BoxShape3D.size = Vector3(5, 0.3, 5)` |
| Ball/projectile | 0.2-0.5m diameter | `SphereShape3D.radius = 0.25` |
| Door/opening | 2m tall, 1m wide | `BoxShape3D.size = Vector3(1, 2, 0.1)` |
| Large environment | 50-200m | Ground plane, sky boundary |

**Camera distances:** Third-person: 5-10m behind/above; Top-down: 15-30m above (orthogonal for strategy); First-person: ~1.7m height.

**2D uses pixels.** Standard viewport: 1920x1080 or 1280x720. Player sprite: 64-128px; Tiles: 16/32/64px.

### Scene Template

```gdscript
extends SceneTree

func _initialize() -> void:
    print("Generating: {scene_name}")

    var root := {RootNodeType}.new()
    root.name = "{SceneName}"

    # ... build node hierarchy, add_child(), set properties ...

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

### Scene Constraints

- Use ONLY nodes and resources available in Godot — look up unfamiliar classes in `doc_api`
- Do NOT use `@onready` or scene-time annotations (this runs at build-time)
- Do NOT use `preload()` — use `load()` (preload fails in headless)
- ATTACH all scripts listed in STRUCTURE.md using `node.set_script(load("path"))`
- Do NOT connect signals at build-time — scripts aren't instantiated yet. Signal connections belong in runtime scripts' `_ready()` method
- ALWAYS set `.name` on every node you create — script generator needs predictable names for `@onready` references
- Save to the EXACT output path specified by the task
- **MANDATORY `quit()`** — Script MUST call `quit()` at the end. Without it, Godot runs forever in headless mode.
- **2D/3D consistency** — Use ONLY 2D nodes (Node2D, CharacterBody2D, Area2D, Camera2D) OR 3D nodes. Never mix dimensions in the same scene hierarchy.
- **No spatial methods in `_initialize()`** — `look_at()`, `to_global()`, etc. fail because nodes aren't in the tree yet. Use `rotation_degrees` or compute transforms manually.

### Environment & Lighting (3D Scenes)

When building 3D scenes, set up environment and lighting programmatically:

```gdscript
# WorldEnvironment
var world_env := WorldEnvironment.new()
var env := Environment.new()
env.background_mode = Environment.BG_SKY
env.tonemap_mode = Environment.TONE_MAP_FILMIC
env.ambient_light_color = Color.WHITE
env.ambient_light_sky_contribution = 0.5
var sky := Sky.new()
sky.sky_material = ProceduralSkyMaterial.new()
env.sky = sky
world_env.environment = env
root.add_child(world_env)

# Sun (DirectionalLight3D)
var sun := DirectionalLight3D.new()
sun.shadow_enabled = true
sun.shadow_bias = 0.05
sun.shadow_blur = 2.0
sun.directional_shadow_max_distance = 30.0
sun.sky_mode = Light3D.SKY_MODE_LIGHT_AND_SKY
sun.rotation_degrees = Vector3(-45, -30, 0)
root.add_child(sun)
```

### CSG for Rapid Prototyping

CSG nodes generate collision automatically — no separate CollisionShape needed:

```gdscript
var floor := CSGBox3D.new()
floor.size = Vector3(20, 0.5, 20)
floor.use_collision = true
floor.material = ground_mat
root.add_child(floor)

# Subtraction (carve holes): child CSG on parent CSG
var hole := CSGCylinder3D.new()
hole.operation = CSGShape3D.OPERATION_SUBTRACTION
hole.radius = 1.0
hole.height = 1.0
floor.add_child(hole)
```

### Noise/Procedural Textures

```gdscript
var noise := FastNoiseLite.new()
noise.noise_type = FastNoiseLite.TYPE_CELLULAR
noise.frequency = 0.02
noise.fractal_type = FastNoiseLite.FRACTAL_FBM
noise.fractal_octaves = 5

var tex := NoiseTexture2D.new()
tex.noise = noise
tex.width = 1024
tex.height = 1024
tex.seamless = true       # tileable
tex.as_normal_map = true  # for normal maps
tex.bump_strength = 2.0
```

### StandardMaterial3D Extended Properties

Beyond basic albedo, useful properties for richer materials:
- `normal_enabled = true` + `normal_texture` + `normal_scale = 2.0`
- `rim_enabled = true` + `rim_tint = 1.0` — silhouette glow
- `emission_enabled = true` + `emission_texture` — self-illumination
- `texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC`

---

## Part 2: Script Generation

Runtime scripts define node behavior — movement, combat, AI, signals, and game logic. They attach to nodes in scenes and run when the game plays.

### Script Output Requirements

Generate a `.gd` file that:
1. `extends {NodeType}` matching the node it attaches to
2. Uses proper Godot lifecycle methods
3. References sibling/child nodes via correct paths
4. Defines and connects signals as needed

### Script Template

```gdscript
extends {NodeType}
## {script_path}: {Brief description}

# Signals
signal health_changed(new_value: int)
signal died

# Node references (resolved at _ready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

# State
var _current_health: int

func _ready() -> void:
    _current_health = max_health

func _physics_process(delta: float) -> void:
    pass
```

**Script section ordering:** signals → @onready vars → private state → lifecycle methods → public methods → private methods → signal handlers

### VehicleBody3D

```gdscript
extends VehicleBody3D

@export var max_engine_force := 150.0
@export var max_steer := 0.5
var _steer_target := 0.0

func _physics_process(delta: float) -> void:
    var fwd: float = Input.get_axis("brake", "accelerate")
    _steer_target = Input.get_axis("steer_right", "steer_left") * max_steer
    steering = move_toward(steering, _steer_target, 2.0 * delta)
    var spd: float = linear_velocity.length()
    engine_force = fwd * max_engine_force * clampf(5.0 / maxf(spd, 0.1), 0.5, 5.0)
```

### Script Constraints

- `extends` MUST match the node type this script attaches to
- Use `@onready` for node refs, NOT `get_node()` in `_process()`
- ONLY use input actions from plan's `inputs[]`, never invent action names. If none declared, use direct key checks.
- Connect signals in `_ready()`, NOT in scene builders (scripts aren't instantiated at build-time)
- **Sibling signal timing:** `_ready()` fires on children in order. If sibling A emits in its `_ready()`, sibling B hasn't connected yet. Fix: after connecting, check if the emitter already has data and call the handler manually.
- Do NOT use `preload()` for scenes/resources that may not exist yet — use `load()`. Add spawned children to `get_parent()`, not `self`.
- When "Available Nodes" section is provided, use ONLY the exact paths and types listed — do not guess or invent node names
- **CRITICAL: NEVER use `:=` with polymorphic math functions** — `abs`, `sign`, `clamp`, `min`, `max`, `floor`, `ceil`, `round`, `lerp`, `smoothstep`, `move_toward`, `wrap`, `snappedf`, `randf_range`, `randi_range` return Variant (work on multiple types). Use explicit types: `var x: float = abs(y)` not `var x := abs(y)`

---

## Coordinating Scene + Script

When a task requires both scene(s) and script(s):

1. **Generate scenes first** — scenes define the node hierarchy that scripts reference via `@onready`
2. **Name nodes predictably** — scripts use `@onready var x: Type = $NodeName`, so the scene builder MUST set `.name` on every node to match
3. **Attach scripts in scene builder** — use `node.set_script(load("res://scripts/foo.gd"))` as specified in STRUCTURE.md
4. **Connect signals in scripts, not scenes** — signal connections go in the script's `_ready()`, NOT in the scene builder (scripts aren't instantiated at build-time)
5. **Match extends to node type** — the script's `extends CharacterBody3D` must match the node it's attached to in the scene

### Example Coordination

Scene builder creates the node:
```gdscript
# In scene builder (_initialize):
var player := CharacterBody3D.new()
player.name = "Player"                          # Script uses @onready $Player
var hitbox := Area3D.new()
hitbox.name = "Hitbox"                           # Script uses @onready $Hitbox
player.add_child(hitbox)
player.set_script(load("res://scripts/player_controller.gd"))
```

Runtime script references those nodes:
```gdscript
# In player_controller.gd:
extends CharacterBody3D                          # Matches node type
@onready var hitbox: Area3D = $Hitbox            # Matches .name from scene

func _ready() -> void:
    hitbox.body_entered.connect(_on_hitbox_body_entered)  # Signal connected here, not in scene
```

---

## Part 3: Test Harness & Visual Verification

Write `test/test_{task_id}.gd` (e.g., `test/test_T3.gd`) — a SceneTree script that loads the scene under test and **thoroughly verifies the task's goal**. Do NOT call `quit()` — the movie writer handles exit.

**Verify what the task actually asks for.** Read the Verify description and think about what would convince you — a skeptic, not the author — that the task is done. A decoration task needs multiple camera angles to check placement and scale. A movement task needs the camera to follow the action over time. A UI task needs the full interface visible. Match the test to the goal.

Load `Skill(skill="godot-capture")` for capture commands (screenshots and video).

### Test Harness Patterns

**Static scene (decoration, terrain, environment) — use multiple angles:**
```gdscript
extends SceneTree

var _cam: Camera3D
var _frame: int = 0
var _target_pos: Vector3  # Center of the scene or object of interest

func _initialize() -> void:
    var scene: PackedScene = load("res://scenes/{scene_name}.tscn")
    var instance = scene.instantiate()
    root.add_child(instance)

    _target_pos = Vector3(0, 2, 0)
    _cam = Camera3D.new()
    _cam.current = true
    root.add_child(_cam)

func _process(delta: float) -> bool:
    _frame += 1
    # Orbit around the subject to see it from multiple angles
    var angle: float = float(_frame) / 60.0 * TAU * 0.5  # half orbit over 6s
    var radius := 12.0
    _cam.position = _target_pos + Vector3(sin(angle) * radius, 6, cos(angle) * radius)
    _cam.look_at(_target_pos)
    return false
```

**Dynamic scene (movement, physics, gameplay) — follow the action:**
```gdscript
extends SceneTree

var _cam: Camera3D
var _target: Node3D
var _frame: int = 0

func _initialize() -> void:
    var scene: PackedScene = load("res://scenes/{scene_name}.tscn")
    var instance = scene.instantiate()
    root.add_child(instance)

    _target = instance.get_node("Player")
    _cam = Camera3D.new()
    _cam.current = true
    root.add_child(_cam)

func _process(delta: float) -> bool:
    _frame += 1
    if _target:
        _cam.position = _target.position + Vector3(5, 4, 5)
        _cam.look_at(_target.position)
    return false
```

### Console Assertions

The test harness stdout is captured alongside screenshots. Use `print("ASSERT PASS/FAIL: ...")` to verify behavioral properties that are hard to judge visually (exact positions, velocities, state changes). After capture, check stdout for any `ASSERT FAIL` lines — these must be fixed before the task is complete.

### Simulated Input

For tests needing player input, use a Timer to trigger actions:

```gdscript
    var timer := Timer.new()
    timer.wait_time = 1.0
    timer.one_shot = true
    timer.timeout.connect(func(): Input.action_press("move_forward"))
    root.add_child(timer)
    timer.start()
```

