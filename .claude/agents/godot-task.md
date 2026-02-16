---
name: godot-task
description: |
  Execute a single Godot development task — generate scenes (.tscn) and/or runtime scripts (.gd), then verify visually via test harness and screenshots.

  **When to use:** For implementing individual game features from PLAN.md tasks.
---

# Godot Task Executor

Execute a single development task from PLAN.md. A task may require generating scenes (`.tscn` files via GDScript builders), runtime scripts (`.gd` files), or both. Determine what's needed from the task's **Targets** field. Each task includes a **Verify** description — a visual test scenario you must satisfy by generating a test harness, capturing screenshots, and iterating until they match.

## Project Layout

```
game/           # Godot project (git repo) — project.godot, scripts/, scenes/
assets/         # shared binary assets — glb/, img/, assets.json
worktrees/      # parallel branch checkouts (temporary)
screenshots/    # test output, per-task subfolders
```

`{game_dir}` is where Godot runs — normally `game/`, or `worktrees/{branch}` when using a worktree.

## First Step: Anchor the Project Root

Run this FIRST, before any other command:
```bash
PROJECT_ROOT=$(pwd)
```
Use `$PROJECT_ROOT` in every path. Never use `$(pwd)` inline — it breaks after `cd`.

## Worktree Lifecycle

When the caller passes `worktree=true` with a `branch` name, handle the full git worktree lifecycle for isolated parallel execution. When `worktree` is not specified, `{game_dir}` = `game/` (no git operations).

**Setup (before starting work):**

1. **Branch + worktree:**
   ```bash
   git -C $PROJECT_ROOT/game worktree add $PROJECT_ROOT/worktrees/{branch} -b {branch}
   ```
2. **Symlink assets:**
   ```bash
   ln -s $PROJECT_ROOT/assets/glb $PROJECT_ROOT/worktrees/{branch}/glb
   ln -s $PROJECT_ROOT/assets/img $PROJECT_ROOT/worktrees/{branch}/img
   ```
3. **Import assets** — required once per new worktree so scene builders can load GLBs:
   ```bash
   cd $PROJECT_ROOT/worktrees/{branch} && godot --headless --import --quit 2>&1
   ```
4. **Set game_dir** — use `worktrees/{branch}` as `{game_dir}` for the rest of the workflow.

**Teardown (after work + commit):**

5. **Commit** — `cd $PROJECT_ROOT/{game_dir} && git add -A && git commit -m "task: {task_name}"`
6. **Rebase + merge:**
   ```bash
   cd $PROJECT_ROOT/{game_dir} && git rebase master
   cd $PROJECT_ROOT/game && git merge --ff-only {branch}
   ```
7. **Cleanup:**
   ```bash
   git -C $PROJECT_ROOT/game worktree remove $PROJECT_ROOT/worktrees/{branch} && git -C $PROJECT_ROOT/game branch -d {branch}
   ```

If rebase has conflicts, resolve them (this task's files are authoritative), then continue: `git add <resolved> && GIT_EDITOR=true git rebase --continue`.

## Workflow

1. **Load GDScript docs** — `Skill(skill="gdscript-doc")`. Follow its instructions before writing any code.
2. **Analyze the task** — read the task's **Targets** to determine what to generate:
   - `scenes/*.tscn` targets → generate scene builder(s) (see Part 1)
   - `scripts/*.gd` targets → generate runtime script(s) (see Part 2)
   - Both → generate scenes FIRST, then scripts (scenes create nodes that scripts attach to)
3. **Generate scene(s)** — write GDScript scene builder, compile to produce `.tscn`
4. **Generate script(s)** — write `.gd` files to `{game_dir}/scripts/`
5. **Validate** — run `godot --headless --quit` to check for parse errors across all project scripts
6. **Fix errors** — if Godot reports errors, read output, fix files, re-run. Repeat until clean.
7. **Generate test harness** — write `{game_dir}/test/test_task.gd` implementing the task's **Verify** scenario (see Part 3)
8. **Capture screenshots** — run test with `xvfb-run` and `--write-movie` to produce PNGs (see Screenshot Capture)
9. **Verify visually** — read captured PNGs and check two things:
   - **Task goal:** does the screenshot match the **Verify** description?
   - **Visual quality & logic:** look for obvious bugs — geometry clipping through other geometry, objects floating in mid-air when they shouldn't be, wrong assets used, unnatural asset pose or size, text overflow, UI elements overlapping or cut off at screen edges. Don't add decorations or polish beyond the task scope, but do fix clear correctness issues.
   Also check harness stdout for `ASSERT FAIL`.
   If either check fails, identify the issue, fix scene/script/test, and repeat from step 3.
10. **Store final evidence** — save screenshots and `verification.md` in `screenshots/{task_folder}/` before reporting completion.

## Iteration Tracking

Steps 3-9 form an **implement → screenshot → verify** loop.

There is no fixed iteration limit — use judgment:
- If there is progress — even in small, iterative steps — keep going. Screenshots and file updates are cheap.
- If you recognize a **fundamental limitation** (wrong architecture, missing engine feature, broken assumption), stop early — even after 2-5 iterations. More loops won't help.
- The signal to stop is **"I'm making the same kind of fix repeatedly without convergence"**.

When you stop, report:
- What works (with screenshot evidence)
- What's still wrong
- What you tried and why it didn't fix it
- Your best guess at the root cause

The caller (gamedev orchestrator) will decide whether to adjust the task, re-scaffold, or accept the current state.

### Commands

```bash
# Compile a scene builder (produces .tscn):
cd $PROJECT_ROOT/{game_dir} && godot --headless --script <path_to_gd_builder>

# Validate all project scripts (parse check):
cd $PROJECT_ROOT/{game_dir} && godot --headless --quit 2>&1
```

**Error handling:** Parse Godot's stderr/stdout for error lines. Common issues:
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class in `doc_api`
- `Cannot infer type` — `:=` used with `instantiate()` or polymorphic math functions, see type inference rules
- Script hangs — missing `quit()` call in scene builder; kill the process and add `quit()`

## Project Memory

Read `{game_dir}/MEMORY.md` before starting work — it contains discoveries from previous tasks (workarounds, Godot quirks, asset details, architectural decisions). After completing your task, write back anything useful you learned: what worked, what failed, technical specifics others will need.

## Known Quirks

- **RID leak errors on exit** — headless scene builders always produce these. Harmless; ignore them.
- **`--import` for worktrees** — must run `godot --headless --import --quit` once per new worktree before scene builders can load GLB files. Already included in worktree setup above.
- **`add_to_group()` in scene builders** — groups set at build-time persist in saved .tscn files.
- **MultiMeshInstance3D + GLBs** — does NOT render after pack+save (mesh resource reference lost during serialization). Use individual GLB instances instead.
- **Software renderer perf** — llvmpipe (software vulkan) gets ~3-4 FPS with ~150 GLB instances. Keep total draw calls under 200 for reasonable capture times.

## Type Inference Errors

Two common issues with `load()` and `instantiate()` — applies in both scene builders and runtime scripts:

```gdscript
# WRONG — load() returns Resource, which has no instantiate():
var scene := load("res://glb/car.glb")
var model := scene.instantiate()  # Error: Resource has no instantiate()

# WRONG — := with instantiate() causes Variant inference error:
var scene: PackedScene = load("res://glb/car.glb")
var model := scene.instantiate()  # Error: Cannot infer type from Variant

# CORRECT — type load() AND use = (not :=) for instantiate():
var scene: PackedScene = load("res://glb/car.glb")
var model = scene.instantiate()  # Works: no type inference attempted
```

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
var model_scene: PackedScene = load("res://glb/car.glb")
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
mat.albedo_texture = load("res://img/grass.png")
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

### Movement Patterns

**CharacterBody2D/3D (Kinematic):**
```gdscript
extends CharacterBody2D

var speed: float = 200.0
var jump_velocity: float = -400.0

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity += get_gravity() * delta
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed
    move_and_slide()
```

**RigidBody3D (Physics-driven):**
```gdscript
extends RigidBody3D

var move_force: float = 10.0

func _physics_process(_delta: float) -> void:
    var input := Vector3.ZERO
    input.x = Input.get_axis("move_left", "move_right")
    input.z = Input.get_axis("move_forward", "move_back")
    if input.length() > 0:
        apply_central_force(input.normalized() * move_force)
```

### Input Handling

ONLY use input actions declared in the plan's `inputs[]` array.

**Action-based:**
```gdscript
if Input.is_action_just_pressed("jump"):
    jump()
if Input.is_action_pressed("fire"):  # Held
    fire()
var axis := Input.get_axis("move_left", "move_right")  # -1 to 1
var vec := Input.get_vector("left", "right", "up", "down")  # Vector2
```

**If no inputs declared in plan, use direct key checks:**
```gdscript
if Input.is_key_pressed(KEY_W):
    move_forward()
```

**Event-based:**
```gdscript
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("interact"):
        interact()
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_LEFT:
            shoot()
```

### Signal Patterns

**Define and emit:**
```gdscript
signal health_changed(new_health: int)
signal item_collected(item_type: String, value: int)
signal died

health_changed.emit(current_health)
died.emit()
```

**Connect in _ready():**
```gdscript
func _ready() -> void:
    # Connect child's signal to our method
    $Area2D.body_entered.connect(_on_body_entered)

    # Connect to sibling (via parent)
    var player = get_parent().get_node("Player")
    player.died.connect(_on_player_died)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("enemies"):
        take_damage(10)
```

**Sibling signal timing:** Scene tree calls `_ready()` on children in order. If sibling A emits a signal in its `_ready()`, sibling B (added later) hasn't connected yet and misses it. Fix: after connecting, check if the emitter already has data and call the handler manually.

### Node References

```gdscript
# Children (via @onready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var hitbox: Area2D = $Hitbox
@onready var muzzle: Marker3D = $Arm/Gun/Muzzle

# Siblings (via parent)
@onready var level_manager: Node = get_parent().get_node("LevelManager")

# Groups
func get_all_enemies() -> Array[Node]:
    return get_tree().get_nodes_in_group("enemies")
```

### Timer Patterns

```gdscript
# One-shot timer
await get_tree().create_timer(1.5).timeout

# Repeating (Timer node)
@onready var spawn_timer: Timer = $SpawnTimer

func _ready() -> void:
    spawn_timer.timeout.connect(_on_spawn_timer)
    spawn_timer.start()

func _on_spawn_timer() -> void:
    spawn_enemy()
```

### Tween Animations

```gdscript
func flash_damage() -> void:
    var tween := create_tween()
    tween.tween_property(sprite, "modulate", Color.RED, 0.1)
    tween.tween_property(sprite, "modulate", Color.WHITE, 0.1)

func move_to(target: Vector2) -> void:
    var tween := create_tween()
    tween.tween_property(self, "position", target, 0.5)\
        .set_ease(Tween.EASE_OUT)\
        .set_trans(Tween.TRANS_CUBIC)
```

### Scene Instantiation (Runtime Spawning)

```gdscript
# Load at top of script (use load(), NOT preload() — scenes may not exist at parse time)
var BulletScene: PackedScene = load("res://scenes/bullet.tscn")

func shoot() -> void:
    var bullet := BulletScene.instantiate()
    bullet.position = $Muzzle.global_position
    bullet.rotation = rotation
    get_parent().add_child(bullet)  # Add to parent, not self
```

### Script Constraints

- `extends` MUST match the node type this script attaches to
- Use `@onready` for node refs, NOT `get_node()` in `_process()`
- ONLY use input actions from plan's `inputs[]`, never invent action names
- Use typed variables and return types for clarity
- Signal handler names: `_on_{source}_{signal}` by convention
- Do NOT use `preload()` for scenes/resources that may not exist yet — use `load()`
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

Write `{game_dir}/test/test_task.gd` — a SceneTree script that loads the scene under test and **thoroughly verifies the task's goal**. Do NOT call `quit()` — the movie writer handles exit.

**Verify what the task actually asks for.** Read the Verify description and think about what would convince you — a skeptic, not the author — that the task is done. A decoration task needs multiple camera angles to check placement and scale. A movement task needs the camera to follow the action over time. A UI task needs the full interface visible. Match the test to the goal.

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

### Screenshot Capture

Screenshots go in `screenshots/` — outside the Godot project and worktrees, always at the same path. Each task gets a subfolder. Resolve the absolute path before `cd $PROJECT_ROOT/{game_dir}`.

```bash
MOVIE=$PROJECT_ROOT/screenshots/{task_folder}
rm -rf $MOVIE && mkdir -p $MOVIE
cd $PROJECT_ROOT/{game_dir} && mkdir -p _captures && timeout 20 xvfb-run -s '-screen 0 1280x720x24' godot --rendering-driver vulkan \
    --write-movie _captures/frame.png \
    --fixed-fps 10 --quit-after {N} \
    --script test/test_task.gd 2>&1
mv $PROJECT_ROOT/{game_dir}/_captures/* $MOVIE/ && rm -rf $PROJECT_ROOT/{game_dir}/_captures
```

**`--write-movie` path:** MUST be relative and inside the Godot project directory. Absolute paths or paths outside the project resolve incorrectly. That's why we write to `_captures/` inside `{game_dir}` then move the frames out.

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`, `task_02_car_physics`). Use lowercase with underscores.

**Timeout:** The `timeout 20` is a safety net — `--quit-after` should handle exit, but if Godot hangs for any reason, this kills it after 20 seconds. Exit code 124 means the timeout fired.

**Rendering driver:** Use `vulkan` (default) — it runs via lavapipe software rasterizer under xvfb and supports `forward_plus` rendering (shadows, lighting, post-processing). Fall back to `opengl3` only if vulkan fails (e.g. missing lavapipe/mesa-vulkan-drivers).

`--quit-after {N}` is the frame count. Choose FPS and duration based on scene type:
- **Static scenes** (decoration, terrain, UI): use `--fixed-fps 1`. Higher FPS just produces duplicate screenshots and wastes time. Adjust `--quit-after` to however many distinct views you need (e.g. 8 frames for a full orbit at 1 FPS = 8s).
- **Dynamic scenes** (physics, movement, gameplay): use `--fixed-fps 10`. Low FPS breaks physics and movement — `delta` becomes too large, causing objects to tunnel through collisions or behave erratically. Typical duration: 3-10s (30-100 frames).

**Smart frame selection:** Don't read all frames — pick 3-5 that cover the verification:
- For static/decoration: frames spread across a camera orbit (different angles)
- For movement/physics: early (initial state), mid (action in progress), late (outcome)
- For UI/HUD: frames showing different states or interactions

Think about **what would convince a skeptic** — someone who hasn't seen the code — that the task is done.

**Write verification record:** after reviewing frames, save `screenshots/{task_folder}/verification.md` with concrete evidence.
Template:
```md
# Verification
- Task: {task_id_or_name}
- Capture folder: screenshots/{task_folder}
- Reviewed frames: frame0001.png, frame0004.png, frame0008.png
- Verify criteria: {copied from PLAN.md task Verify}
- Decision: PASS | FAIL
- Notes: {visual findings, ASSERT FAIL/PASS summary, remaining caveats}
```

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
