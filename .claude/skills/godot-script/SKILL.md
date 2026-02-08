---
name: godot-script
description: Generate GDScript files that define node behavior — movement, combat, AI, signals, and game logic
argument-hint: <script description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Godot Script Generator

You generate GDScript files that define node behavior. Scripts attach to nodes in Godot scenes and run at game runtime.

## Project Root

The caller specifies `{project_root}` (e.g. `project_root=build`). Scripts are written to `{project_root}/scripts/`. The Godot project file lives at `{project_root}/project.godot`.

## Workflow

1. **Read references** — ALWAYS read `gdscript.md` before writing code. For node/resource API lookup, follow the steps below.
2. **Write GDScript** — Generate a `.gd` file implementing the required behavior, saved to `{project_root}/scripts/`.
3. **Validate** — Run `godot --headless --quit` from `{project_root}/` to check for parse errors.
4. **Fix errors** — If Godot reports errors, read the output, fix the `.gd` file, and re-run. Repeat until clean.

### Validation Command

```bash
cd {project_root} && godot --headless --quit 2>&1
```

This parses all scripts in the project and reports errors.

**Error handling:** Parse Godot's stderr/stdout for error lines. Common issues:
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class in `doc_api/`
- `Cannot infer type` — `:=` used with polymorphic math functions or untyped return values, use explicit types

## API Lookup

Per-class API docs are in `doc_api/`. Follow this order:

1. **Read `doc_api/_common.md`** — index of ~128 commonly used classes (nodes, shapes, meshes, materials, math types). Find the classes you need here first.
2. **If not found, read `doc_api/_other.md`** — index of ~730 remaining classes (networking, IO, niche resources, etc.).
3. **Read `doc_api/{ClassName}.md`** — full API reference for a specific class (props, methods, signals, enums with descriptions).

Example: to look up CharacterBody3D, read `doc_api/CharacterBody3D.md`.

## Output Requirements

Generate a single `.gd` file that:
1. `extends {NodeType}` matching the node it attaches to
2. Uses proper Godot lifecycle methods
3. References sibling/child nodes via correct paths
4. Defines and connects signals as needed
5. **Expose ALL tuneable parameters via `@export`** for easy modification

## GDScript Patterns

### Script Template
```gdscript
extends {NodeType}
## {Brief description of what this script does}

# Signals
signal health_changed(new_value: int)
signal died

# Exported parameters (tuneable in editor or via code)
@export var speed: float = 200.0  ## Movement speed in pixels/second
@export var max_health: int = 100  ## Maximum health points

# Node references (resolved at _ready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

# State
var _current_health: int

func _ready() -> void:
    _current_health = max_health

func _process(delta: float) -> void:
    # Per-frame logic (rendering, non-physics)
    pass

func _physics_process(delta: float) -> void:
    # Fixed-timestep physics logic
    pass

func _input(event: InputEvent) -> void:
    # Direct input handling
    pass

func _unhandled_input(event: InputEvent) -> void:
    # Input not consumed by UI
    pass
```

### Lifecycle Methods
| Method | When Called | Use For |
|--------|-------------|---------|
| `_ready()` | Node enters tree, children ready | Initialization, cache references |
| `_process(delta)` | Every frame | Visual updates, non-physics logic |
| `_physics_process(delta)` | Fixed timestep (default 60/s) | Movement, physics, collision response |
| `_input(event)` | Any input event | Global input handling |
| `_unhandled_input(event)` | Input not consumed | Game input (after UI) |
| `_enter_tree()` | Added to tree | Early setup |
| `_exit_tree()` | Removed from tree | Cleanup |

### Exported Parameters (@export)

**ALWAYS use `@export` for values that might need tweaking.** This allows easy parameter modification without editing code.

```gdscript
# Movement and physics (runtime behavior)
@export var speed: float = 200.0  ## Movement speed
@export var acceleration: float = 1000.0  ## Ground acceleration
@export var jump_velocity: float = -400.0  ## Jump impulse (negative = up)
@export var gravity_scale: float = 1.0  ## Multiplier for gravity
@export var move_force: float = 15.0  ## Force applied for RigidBody movement

# Combat and gameplay
@export var max_health: int = 100  ## Maximum HP
@export var damage: int = 10  ## Damage dealt on hit
@export var attack_cooldown: float = 0.5  ## Seconds between attacks
@export var fire_rate: float = 0.2  ## Seconds between shots

# Timing and behavior
@export var spawn_interval: float = 2.0  ## Seconds between spawns
@export var despawn_time: float = 5.0  ## Lifetime before auto-remove
@export var detection_range: float = 10.0  ## AI detection distance
```

**What to export (runtime behavior):**
- **Speeds/forces**: movement speed, jump velocity, acceleration, move_force
- **Timings**: cooldowns, fire_rate, spawn_interval, despawn_time
- **Gameplay values**: max_health, damage, detection_range
- **Any magic number** that affects runtime behavior

**NOT for scripts** (use scene gen instead):
- Object positions, rotations, scales (baked into scene)
- Model orientation fixes (handled when placing in scene)

**Export guidelines:**
- Add `## comment` after declaration for editor tooltip
- Use sensible defaults that make the game playable
- Group related exports together
- Prefix internal vars with `_` to distinguish from exports

### Movement Patterns

**CharacterBody2D/3D (Kinematic):**
```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var jump_velocity: float = -400.0

func _physics_process(delta: float) -> void:
    # Gravity
    if not is_on_floor():
        velocity += get_gravity() * delta

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Horizontal
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

    move_and_slide()
```

**RigidBody3D (Physics-driven):**
```gdscript
extends RigidBody3D

@export var move_force: float = 10.0

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
if Input.is_key_pressed(KEY_SPACE):
    jump()
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

**Define:**
```gdscript
signal health_changed(new_health: int)
signal item_collected(item_type: String, value: int)
signal died  # No parameters
```

**Emit:**
```gdscript
health_changed.emit(current_health)
died.emit()
```

**Connect (code):**
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

func _on_player_died() -> void:
    show_game_over()
```

**Connect (scene-defined):** Signal connections from planner are set up in scene; script just implements the handler:
```gdscript
# Scene connects Area2D.body_entered -> _on_goal_reached
func _on_goal_reached(body: Node2D) -> void:
    if body.name == "Player":
        get_tree().change_scene_to_file("res://scenes/win.tscn")
```

### Node References

**Children (via @onready):**
```gdscript
@onready var sprite: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var hitbox: Area2D = $Hitbox
```

**Nested children:**
```gdscript
@onready var muzzle: Marker3D = $Arm/Gun/Muzzle
```

**Siblings (via parent):**
```gdscript
@onready var level_manager: Node = get_parent().get_node("LevelManager")
```

**Global (autoload singletons):**
```gdscript
# Assumes GameManager is autoloaded
func _ready() -> void:
    GameManager.score += 10
```

**Find in group:**
```gdscript
func get_all_enemies() -> Array[Node]:
    return get_tree().get_nodes_in_group("enemies")
```

### Timer Patterns

**One-shot timer:**
```gdscript
func start_cooldown() -> void:
    await get_tree().create_timer(1.5).timeout
    can_fire = true
```

**Repeating (via Timer node):**
```gdscript
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

### State Machine Pattern
```gdscript
enum State { IDLE, WALKING, JUMPING, ATTACKING }
var _state: State = State.IDLE

func _physics_process(delta: float) -> void:
    match _state:
        State.IDLE:
            _process_idle(delta)
        State.WALKING:
            _process_walking(delta)
        State.JUMPING:
            _process_jumping(delta)
        State.ATTACKING:
            _process_attacking(delta)

func _change_state(new_state: State) -> void:
    _state = new_state
    match new_state:
        State.IDLE:
            anim.play("idle")
        State.WALKING:
            anim.play("walk")
        # etc.
```

### Scene Instantiation (Runtime Spawning)

When "Scenes to Instantiate" section is provided, use `load()` + `instantiate()`:

```gdscript
# Preload at top of script (use load(), NOT preload() for dynamic scenes)
var BulletScene: PackedScene = load("res://scenes/bullet.tscn")

func shoot() -> void:
    var bullet := BulletScene.instantiate()
    bullet.position = $Muzzle.global_position
    bullet.rotation = rotation
    # Add to scene tree (usually parent or root)
    get_parent().add_child(bullet)
```

**Spawner pattern:**
```gdscript
var EnemyScene: PackedScene = load("res://scenes/enemy.tscn")

func spawn_enemy(pos: Vector3) -> void:
    var enemy := EnemyScene.instantiate()
    enemy.global_position = pos
    add_child(enemy)
```

**Rules:**
- Use `load()` not `preload()` — scenes may not exist at parse time
- Add spawned nodes to appropriate parent (not always `self`)
- Set position/rotation before or after `add_child()` depending on coordinate system needed

## Commenting Guidelines

Your code will be read by a revision agent that has general programming knowledge but lacks Godot API documentation. Comment to bridge this gap.

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

# GOOD: Explains what API call does
move_and_slide()  # Integrates velocity, handles collisions, updates is_on_floor()

# BAD: Obvious
var speed := 5.0  # Set speed to 5
```

## Output Format
```gdscript
extends {NodeType}
## {script_path}: {Brief description}

{signals}

{exports}

{onready vars}

{private state vars}

{lifecycle methods}

{public methods}

{private methods}

{signal handlers}
```

## Constraints

- `extends` MUST match the node type this script attaches to
- Use `@onready` for node refs, NOT `get_node()` in `_process()`
- ONLY use input actions from plan's `inputs[]`, never invent action names
- Use typed variables and return types for clarity
- Signal handler names: `_on_{source}_{signal}` by convention
- Do NOT use `preload()` for scenes/resources that may not exist yet — use `load()`
- When "Available Nodes" section is provided, use ONLY the exact paths and types listed — do not guess or invent node names
- **CRITICAL: NEVER use `:=` with polymorphic math functions** — `abs`, `sign`, `clamp`, `min`, `max`, `floor`, `ceil`, `round`, `lerp`, `smoothstep`, `move_toward`, `wrap`, `snappedf`, `randf_range`, `randi_range` return Variant (work on multiple types). Use explicit types: `var x: float = abs(y)` not `var x := abs(y)`
