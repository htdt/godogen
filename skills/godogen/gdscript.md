# GDScript Syntax Reference

## Language Notes

- Indentation-based; a script file defines a class.
- GDScript is its own language (not Python).

## Identifiers

- Letters/digits/_; cannot start with a digit; case-sensitive.
- Unicode letters per UAX#31 are allowed; no emoji or confusable characters.

## Types

**Basic:** `null`, `bool`, `int`, `float`, `String`, `StringName`, `NodePath`

**Vector:** `Vector2`, `Vector2i`, `Vector3`, `Vector3i`, `Vector4`, `Vector4i`

**Transform:** `Transform2D`, `Transform3D`, `Basis`, `Quaternion`

**Geometry:** `Rect2`, `Rect2i`, `AABB`, `Plane`

**Other:** `Color`, `RID`, `Object`, `Callable`, `Signal`

**Containers:** `Array`, `Array[Type]`, `Dictionary`, `Dictionary[K, V]`

**Packed:** `PackedByteArray`, `PackedInt32Array`, `PackedInt64Array`, `PackedFloat32Array`,
`PackedFloat64Array`, `PackedStringArray`, `PackedVector2Array`, `PackedVector3Array`,
`PackedVector4Array`, `PackedColorArray`

**Variant:** Means untyped; not a real type for inference by default.

**Value vs reference:** Built-in types (`bool`, `int`, `float`, `Vector2/3`, `AABB`, `Transform2D/3D`, `Color`, `Rect2`, etc.) are value types — passing them to a function creates a copy, assignments inside the function do NOT update the caller. `Object`, `Array`, `Dictionary`, and packed arrays are reference types (use `duplicate()` to copy).

## Keywords

```
if elif else match when for while break continue pass return
class class_name extends is in as not and or
func signal var const enum static
self super await preload yield breakpoint assert
true false null void
PI TAU INF NAN
```

## Operators (by precedence)

```
()                           # Grouping
x.attr  x["key"]  x()        # Attribute, subscript, call
await x                      # Await
**                           # Power
~ + -                        # Unary (bitwise NOT, positive, negative)
* / %                        # Multiply, divide, modulo
+ -                          # Add, subtract
<< >>                        # Bit shift
&                            # Bitwise AND
^                            # Bitwise XOR
|                            # Bitwise OR
< > <= >= == !=              # Comparison
in  not in  is  is not       # Containment, type check
not  !                       # Boolean NOT (alias)
and  &&                      # Boolean AND (alias)
or   ||                      # Boolean OR (alias)
x if cond else y             # Ternary
as                           # Type cast
= += -= *= /= **= etc.       # Assignment
```

Operator notes:
- `**` is left-associative; ternary is right-associative.
- `/` does integer division when both operands are `int`.
- `%` only works on `int`; use `fmod()` for floats. Use `posmod()`/`fposmod()` for math-style remainders.
- Assignment is not allowed inside expressions.
- `==`/`!=` can compare different types but may cause runtime errors. Use `is_same()` for strict comparison, `is_equal_approx()` for floats.

## Literals

```
null, true, false
45, 0x8f51, 0b101010, 3.14, 1_000_000, 3.14_159
"Hello", 'Hi', """Multi""", r"Raw", r'''Raw'''
&"name"       # StringName
^"Node/Path"  # NodePath
$NodePath     # get_node("NodePath")
%UniqueNode   # get_node("%UniqueNode")
```

Common escapes: `\n \t \r \a \b \f \v \\ \" \' \uXXXX \UXXXXXX`.
Raw strings do not process escapes and cannot end with an odd number of `\`.

## Variables & Constants

```gdscript
var x = 5                    # Variant (no type)
var y: int = 5               # Explicit type
var z := 5                   # Inferred with := (literal has clear type)
const MAX := 100             # Constant
static var count := 0        # Class-level static

# Type inference only works when the RHS has a concrete type.
# Variant-returning functions or data access break := inference.
var bad := abs(speed)                   # ERROR: Cannot infer type from Variant
var bad2 := clamp(val, 0.0, 1.0)        # ERROR: Same problem
var bad3 := min(a, b)                   # ERROR: Same problem
var good: float = abs(speed)            # OK: explicit type annotation
var also_ok = abs(speed)                # OK: untyped (Variant)

enum State { IDLE, RUN, JUMP }
enum { ONE = 1, TWO, THREE }

# Named enums are dictionaries with extra methods
State.IDLE               # 0
State.keys()             # ["IDLE", "RUN", "JUMP"]
State.values()           # [0, 1, 2]
```

Initialization order (members):
- Default value by type (or `null` for untyped/Objects).
- Declaration order initializers.
- `_init()`.
- Exported values (scenes/resources).
- `@onready` values.
- `_ready()`.

## Functions

```gdscript
func add(a: int, b: int) -> int:
    return a + b

func greet(name := "World") -> void:  # Default parameter
    print("Hello, ", name)

func process(items: Array[String]) -> void:  # Typed array
    for item in items:
        print(item)

# Lambda (explicit return required)
var double := func(x): return x * 2

# Lambda capture behavior:
# - Primitives captured by value at creation time (won't see later changes)
# - Arrays/dicts/objects captured by reference (content changes shared)
# - Cannot reassign outer variables (CONFUSABLE_CAPTURE_REASSIGNMENT warning)
var x = 42
var arr = []
var fn = func():
    print(x)       # Always 42, even if x changed after lambda creation
    arr.append(1)  # Shared with outer scope
    x = 99         # Warning: only affects lambda's copy

# Static function
static func create() -> MyClass:
    return MyClass.new()

# Function reference (Callable)
var callback = my_function  # Gets Callable without calling
callback.call(arg1, arg2)   # Must use .call() to invoke

# Static constructor (called on load)
static func _static_init() -> void:
    pass

# Variadic (rest parameter; must be last, no default)
func sum(...values: Array) -> int:
    var total := 0
    for n in values:
        total += n
    return total
```

Variadic notes:
- Only one rest parameter, and it must be last.
- Rest parameter cannot be `Array[Type]` (use `Array`).
- You cannot unpack/rest-spread arguments on call sites (use `callv`).

## Control Flow

```gdscript
# Conditionals
if condition:
    pass
elif other:
    pass
else:
    pass

# Ternary
var result = "yes" if condition else "no"

# Match (pattern matching)
match value:
    1:
        print("one")
    2, 3, 4:
        print("two to four")
    [var a, var b]:
        print(a, b)
    {"key": var v}:
        print(v)
    var x when x > 10:       # Guard clause
        print("big: ", x)
    _:
        print("default")

# Loops
for i in range(10):          # 0 to 9
    if i == 5:
        continue             # Skip iteration
    if i == 8:
        break                # Exit loop
for item in array:
    pass
for name: String in names:   # Typed loop variable
    print(name.to_upper())
for key in dict:
    var val = dict[key]
while condition:
    pass
```

## Classes

```gdscript
class_name MyClass
extends Node2D

# Abstract class/method (cannot be instantiated or attached to nodes)
@abstract class Shape:
    @abstract func draw() -> void  # No body; subclasses must implement

# Unnamed abstract class
@abstract
extends Node

signal health_changed(new_value: int)
signal died

@export var speed: float = 100.0
@export_range(0, 100) var health: int = 100
@onready var sprite: Sprite2D = $Sprite2D

var _private := 0

# Property with getter/setter
var score: int:
    get:
        return score       # Direct access inside own getter (no recursion)
    set(value):
        score = clamp(value, 0, 100)  # Direct access inside own setter
        score_changed.emit(score)

# Alternative property syntax (reusing functions)
var my_prop: get = _get_prop, set = _set_prop

# Setter/getter NOT called: during initialization and inside own accessor
var x: int = 5  # Setter not called here

func _init() -> void:
    pass

func _ready() -> void:
    super._ready()  # Call parent
    # self.prop is runtime-checked (works for dynamic/child properties)
    # prop alone is compile-time checked (must exist in current class)
    print(self.dynamic_prop)  # OK at compile, checked at runtime

func something(p1, p2) -> void:
    super(p1, p2)   # Call overridden method by name

func other_something(p1, p2) -> void:
    super.something(p1, p2)

func _process(delta: float) -> void:
    pass

# Inner class
class InnerEnemy:
    var hp := 100
    func take_damage(amount: int) -> void:
        hp -= amount
```

## Node References

```gdscript
$NodeName                    # Get child node
$Path/To/Node                # Nested path
%UniqueNode                  # Scene-unique node (set in editor)
get_node("Path")             # Equivalent to $
get_parent()                 # Parent node
get_tree()                   # SceneTree
get_node_or_null("Path")     # Returns null if not found
has_node("Path")             # Check existence
```

## Signals

```gdscript
# Define
signal my_signal
signal value_changed(new_val: int)

# Emit
my_signal.emit()
value_changed.emit(42)

# Connect
other_node.my_signal.connect(_on_signal)
other_node.my_signal.connect(func(): print("lambda"))

# Connect with bound arguments
# _on_signal receives (signal_arg, bound_arg)
other_node.my_signal.connect(_on_signal.bind("extra_data"))

# Disconnect
other_node.my_signal.disconnect(_on_signal)

# Await
await my_signal
await get_tree().create_timer(1.0).timeout
var result = await some_async_func()
```

## Annotations

```gdscript
@export var visible_in_editor: int
@export_range(0, 100, 1) var clamped: int
@export_enum("Low", "Medium", "High") var quality: int
@export_file("*.png") var texture_path: String
@export_node_path("Sprite2D") var sprite_path: NodePath
@export_group("Movement")    # Group following exports
@export_subgroup("Speed")    # Subgroup

@onready var node := $Child  # Resolved when _ready() runs

@tool  # Script runs in editor (be careful with queue_free!)
@static_unload # Unload script when no references (for static vars)
@warning_ignore("unused_parameter")

@icon("res://icon.png")  # Custom class icon
```

Annotations:
- Multiple annotations can be stacked; they apply to the next non-annotation line.
- `@onready` with `@export` is not recommended; `@onready` overwrites exported values
  and triggers the `ONREADY_WITH_EXPORT` warning.

## Comments & Regions

```gdscript
# Line comment
## Documentation comment (for script docs/inspector tooltips)

#region Terrain
func generate_lakes():
    pass
#endregion
```

Editor highlights markers (case-sensitive):
- Critical (red): `ALERT`, `ATTENTION`, `CAUTION`, `CRITICAL`, `DANGER`, `SECURITY`
- Warning (yellow): `BUG`, `DEPRECATED`, `FIXME`, `HACK`, `TASK`, `TODO`, `WARNING`
- Notice (green): `INFO`, `NOTE`, `NOTICE`, `TEST`
No space after `#` for `#region`/`#endregion`. Regions can be nested.

## Line Continuation

```gdscript
var a = 1 + \
2 + \
3
```

## Strings

```gdscript
# Regular strings
var s = "Hello\nWorld"       # With escape sequences
var raw = r"C:\path\file"    # Raw string (no escapes)
var multi = """
Line 1
Line 2
"""                          # Triple-quoted multiline

# Special literals
var sname: StringName = &"my_action"  # StringName (interned)
var npath: NodePath = ^"Path/To/Node" # NodePath literal

# Format strings
"Hello %s" % name            # Single value
"x=%d y=%d" % [x, y]         # Multiple values
"%.2f" % 3.14159             # Float precision

# Common methods
s.length()                   # String length
s.to_upper()                 # HELLO
s.to_lower()                 # hello
s.strip_edges()              # Trim whitespace
s.split(",")                 # Split to array
",".join(["a", "b"])         # Join array
s.begins_with("He")          # Prefix check
s.ends_with("ld")            # Suffix check
s.find("ll")                 # Find substring index
s.replace("l", "L")          # Replace
str(42)                      # Convert to string
int("42")                    # Parse int
float("3.14")                # Parse float
```

## Arrays & Dictionaries

```gdscript
# Arrays
var arr := [1, 2, 3]
var typed: Array[int] = [1, 2, 3]

# Cannot assign Array[SubType] to Array[BaseType] directly
var nodes2d: Array[Node2D] = [Node2D.new()]
var nodes: Array[Node] = []
# nodes = nodes2d  # ERROR: incompatible types
nodes.assign(nodes2d)  # OK: copies contents
arr.append(4)                # Add to end
arr.push_front(0)            # Add to start
arr.insert(2, 99)            # Insert at index
arr.pop_back()               # Remove and return last
arr.pop_front()              # Remove and return first
arr.remove_at(1)             # Remove at index
arr.erase(2)                 # Remove first occurrence of value
arr.size()                   # Length
arr.is_empty()               # Check empty
arr.has(2)                   # Check contains
arr.find(2)                  # Find index (-1 if not found)
arr.sort()                   # Sort in place
arr.reverse()                # Reverse in place
arr.duplicate()              # Shallow copy
arr.shuffle()                # Randomize order
arr.slice(1, 3)              # Subarray [1:3)
arr.map(func(x): return x*2) # Transform
arr.filter(func(x): return x > 0)  # Filter
arr.reduce(func(a, b): return a + b, 0)  # Reduce

# Dictionaries
var dict := {"key": "value", "num": 42}
var typed: Dictionary[String, int] = {"a": 1}
dict["new_key"] = 100        # Add/update
dict.get("key", "default")   # Get with default
dict.has("key")              # Check key exists
dict.erase("key")            # Remove key
dict.keys()                  # Array of keys
dict.values()                # Array of values
dict.size()                  # Number of entries
dict.is_empty()              # Check empty
dict.merge(other_dict)       # Merge in place
```

Array/dict notes:
- `Array` == `Array[Variant]`. `Dictionary` == `Dictionary[Variant, Variant]`.
- Dictionary/array access returns `Variant`, so `:=` inference can fail.

## Memory Management

- **RefCounted**: (Array, Dictionary, Resource) Automatically freed when no references exist.
- **Object/Node**: Manually managed.
  - `free()`: Immediate deletion.
  - `queue_free()`: Safely delete at end of frame (recommended for Nodes).
- **WeakRef**: `weakref(obj)` creates reference that doesn't prevent freeing.
- **is_instance_valid(obj)**: Check if object hasn't been freed (for non-RefCounted).

## Type Checking & Casting

```gdscript
# Type checking
if node is Sprite2D:
    print("It's a sprite")

if not enemy is null:
    enemy.damage(10)

# Safe casting
var sprite := node as Sprite2D
if sprite:  # null if cast failed
    sprite.modulate = Color.RED

# Type of
var t = typeof(value)        # Returns TYPE_* constant
if typeof(x) == TYPE_STRING:
    pass
```

## Common Patterns

```gdscript
# Assert (stripped in release builds; expression not evaluated)
assert(x > 0, "x must be positive")
assert(do_check(), "msg")  # do_check() NOT called in release!

# Groups
add_to_group("enemies")
get_tree().get_nodes_in_group("enemies")
is_in_group("enemies")
get_tree().call_group("enemies", "take_damage", 10)

# Scene management
get_tree().change_scene_to_file("res://level2.tscn")
get_tree().reload_current_scene()
get_tree().quit()

# Instantiate scene
var scene := preload("res://enemy.tscn")  # Compile-time load
var scene2 := load("res://enemy.tscn")    # Runtime load
var instance := scene.instantiate()
add_child(instance)

# Timer
await get_tree().create_timer(1.0).timeout

# Deferred calls (run after current frame)
call_deferred("my_method")
set_deferred("property", value)

# Pause
get_tree().paused = true                   # Pause everything
process_mode = Node.PROCESS_MODE_ALWAYS    # Exempt node from pause (for pause menu UI)
process_mode = Node.PROCESS_MODE_PAUSABLE  # Pause with tree (default)
```

## Math Constants & Functions

```gdscript
PI, TAU, INF, NAN            # Constants

# Basic
abs(x), sign(x), floor(x), ceil(x), round(x)
min(a, b), max(a, b), clamp(val, min_val, max_val)
fmod(x, y), fposmod(x, y)    # Float modulo
wrap(val, min_val, max_val)  # Wrap around
snappedf(val, step)          # Snap to step

# Interpolation
lerp(a, b, t)                # Linear interpolate
lerpf(a, b, t)               # Float lerp
inverse_lerp(a, b, val)      # Get t from value
smoothstep(from, to, val)    # Smooth interpolation
move_toward(from, to, delta) # Move by delta toward target

# Trigonometry
sin(x), cos(x), tan(x)
asin(x), acos(x), atan(x), atan2(y, x)
deg_to_rad(deg), rad_to_deg(rad)

# Power/exponential
sqrt(x), pow(base, exp), exp(x), log(x)

# Random
randf()                      # 0.0 to 1.0
randi()                      # Random int
randf_range(from, to)        # Float in range
randi_range(from, to)        # Int in range
```

## Input

```gdscript
# Actions
Input.is_action_pressed("move_right")      # Held down
Input.is_action_just_pressed("jump")       # Just pressed this frame
Input.is_action_just_released("fire")      # Just released
Input.get_action_strength("accelerate")    # 0.0 to 1.0
Input.get_axis("move_left", "move_right")  # -1.0 to 1.0
Input.get_vector("left", "right", "up", "down")  # Vector2

# Direct key/mouse (use actions when possible)
Input.is_key_pressed(KEY_W)
Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
Input.get_mouse_position()

# Event handling
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        jump()
    if event is InputEventMouseButton:
        if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
            shoot()

func _unhandled_input(event: InputEvent) -> void:
    # Called for input not consumed by UI
    pass
```

## Spawning Patterns

```gdscript
# Path-based random spawning (enemies, pickups):
# Path2D/3D defines the spawn curve, PathFollow randomizes position
var spawn_loc: PathFollow2D = $SpawnPath/SpawnLocation
spawn_loc.progress_ratio = randf()  # random point on path
var mob = MobScene.instantiate()
mob.position = spawn_loc.position

# Auto-cleanup off-screen objects:
# Add VisibleOnScreenNotifier2D as child, connect screen_exited signal
$VisibleOnScreenNotifier2D.screen_exited.connect(queue_free)

# Screen bounds clamping:
position = position.clamp(Vector2.ZERO, screen_size)
```

## Animation Patterns

```gdscript
# AnimationPlayer:
$AnimationPlayer.play("run")
$AnimationPlayer.speed_scale = velocity.length() / max_speed  # tie to movement

# AnimatedSprite2D — pick random animation:
$AnimatedSprite2D.play(anim_names.pick_random())

# AnimationTree blend parameters (3D):
$AnimationTree.set("parameters/speed/blend_amount", velocity.length() / max_speed)

# animation_finished signal for state transitions:
$AnimationPlayer.animation_finished.connect(_on_animation_finished)
```

## Character Facing/Rotation

```gdscript
# 3D — face movement direction:
if direction != Vector3.ZERO:
    basis = Basis.looking_at(direction)

# Isometric 8-directional animation index:
var angle: float = rad_to_deg(direction.angle()) + 22.5
var dir_index: int = int(floor(angle / 45.0)) % 8
```

## Jump/Gravity Patterns

```gdscript
# Terminal velocity:
velocity.y = minf(TERMINAL_VELOCITY, velocity.y + gravity * delta)

# Early jump release (variable jump height):
if Input.is_action_just_released("jump") and velocity.y < 0:
    velocity.y *= 0.6

# Gravity from ProjectSettings (3D):
var gravity: float = float(ProjectSettings.get_setting("physics/3d/default_gravity"))

# Slide collision detection (e.g., stomp enemies):
for i in range(get_slide_collision_count()):
    var col = get_slide_collision(i)
    if col.get_normal().dot(Vector3.UP) > 0.7:
        col.get_collider().squash()  # landed on top
```

## Movement Feel

```gdscript
# Walk/stop force asymmetry for momentum:
if abs(input_dir) > 0.2:
    velocity.x = move_toward(velocity.x, input_dir * MAX_SPEED, WALK_FORCE * delta)
else:
    velocity.x = move_toward(velocity.x, 0, STOP_FORCE * delta)

# Velocity clamping:
velocity.x = clamp(velocity.x, -MAX_SPEED, MAX_SPEED)

# 3D smooth acceleration:
horizontal_vel = horizontal_vel.lerp(target_vel, accel * delta)

# Analog input (triggers, sticks):
var throttle: float = Input.get_action_strength("accelerate")  # 0.0–1.0
```

## State Machine Pattern

```gdscript
# Node-based hierarchical state machine:
class State extends Node:
    signal finished(next_state: StringName)
    func enter() -> void: pass
    func exit() -> void: pass
    func handle_input(_event: InputEvent) -> void: pass
    func update(_delta: float) -> void: pass

# State machine manages current + stack for push/pop (temp states like attack, stagger):
var current_state: State
var states_stack: Array[State]  # push_front for temp, pop_front to return
```

## Navigation Patterns

```gdscript
# 2D: NavigationAgent2D as child of CharacterBody2D
func set_target(pos: Vector2) -> void:
    $NavigationAgent2D.target_position = pos

func _physics_process(_delta: float) -> void:
    if $NavigationAgent2D.is_navigation_finished():
        return
    var next = $NavigationAgent2D.get_next_path_position()
    velocity = global_position.direction_to(next) * speed
    move_and_slide()

# 3D: same pattern with NavigationAgent3D, or use server directly:
var path = NavigationServer3D.map_get_path(nav_map, start, target, true)
```

## RigidBody _integrate_forces

```gdscript
# Low-level physics control (called before engine applies forces):
func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    var lv = state.get_linear_velocity()
    # Modify velocity based on input...
    state.set_linear_velocity(lv)
    # Contact info:
    for i in range(state.get_contact_count()):
        var normal = state.get_contact_local_normal(i)
        var collider = state.get_contact_collider_object(i)

# Collision exceptions (e.g., bullet ignores shooter):
bullet.add_collision_exception_with(shooter)
```

## Server API (Performance)

```gdscript
# PhysicsServer2D for 500+ objects without nodes (bullets, particles):
var shape = PhysicsServer2D.circle_shape_create()
var body = PhysicsServer2D.body_create()
PhysicsServer2D.body_add_shape(body, shape)
PhysicsServer2D.body_set_state(body, PhysicsServer2D.BODY_STATE_TRANSFORM, xform)
PhysicsServer2D.body_set_collision_mask(body, 0)  # no inter-object collision
# MUST cleanup: PhysicsServer2D.free_rid(body) in _exit_tree()

# Custom drawing for server-managed objects:
func _process(_delta: float) -> void:
    queue_redraw()
func _draw() -> void:
    for bullet in bullets:
        draw_texture(bullet_tex, bullet.position)
```

## Custom Drawing

```gdscript
# Key _draw() methods on any CanvasItem:
draw_line(from, to, color, width, antialiased)
draw_circle(pos, radius, color, filled, width, antialiased)
draw_rect(Rect2(pos, size), color, filled, width, antialiased)
draw_polygon(points, colors)
draw_texture(texture, pos, modulate)
draw_set_transform(pos, rotation, scale)  # stateful — affects subsequent draws
queue_redraw()  # call in _process() to trigger redraw
```

## Tween Advanced

```gdscript
var tween = create_tween()
tween.set_loops(3)           # loop count (0 = infinite)
tween.set_speed_scale(2.0)
# Parallel tweens:
tween.parallel().tween_property(node, ^"position", target, 0.5)
tween.parallel().tween_property(node, ^"modulate", Color.RED, 0.5)
# Callbacks:
tween.tween_callback(method.bind(args))
# Method tween (non-property interpolation):
tween.tween_method(callable, start_val, end_val, duration)
# Relative motion:
tween.tween_property(node, ^"position", offset, 0.5).as_relative()
# State: tween.is_valid(), .is_running(), .pause(), .play(), .kill()
```

## File I/O

```gdscript
var f = FileAccess.open(path, FileAccess.WRITE)
f.store_string(data)
var text = FileAccess.get_file_as_string(path)
```

## Physics Gotchas

- BoxShape3D on RigidBody3D snags on trimesh collision edges (well-known Godot/Jolt bug). Use CapsuleShape3D for objects that slide across trimesh surfaces (vehicles, rolling objects).
- `reset_physics_interpolation()` — call when teleporting or switching cameras to prevent visible interpolation glitch.

## MultiMeshInstance3D Gotchas

- `Mesh.duplicate()` needed before freeing the source GLB instance — otherwise the mesh resource is garbage-collected.
- `custom_aabb` must cover the entire visible area. Without it, the MultiMesh gets frustum-culled when the camera moves to edges.
- Has no `set_surface_override_material()`. Use `material_override` on the GeometryInstance3D, or keep materials from the source mesh.

## ProceduralSkyMaterial

- Automatically uses DirectionalLight3D direction and color for the sun disc in the sky.
- Set `sky_mode = SKY_MODE_LIGHT_AND_SKY` on the sun light, `SKY_MODE_LIGHT_ONLY` on fill lights — otherwise multiple sun discs appear.

## 2D Top-Down Patterns

- `CharacterBody2D.motion_mode = MOTION_MODE_FLOATING` — required for top-down 2D (disables gravity and floor detection). Also needed for 3D non-platformer movement (vehicles on slopes, snowboards) where `GROUNDED` mode's `floor_stop_on_slope` fights slope movement.
- Collision shape slightly smaller than tile (e.g., 48px in 64px grid) allows smooth cornering through 1-tile corridors.
- Grid alignment assist: when moving horizontally, snap Y to nearest row center (`round(pos.y / tile_size) * tile_size + tile_size / 2`), and vice versa. Prevents snagging on corridor entrances.
- For modifiable grids (breakable blocks), Sprite2D + StaticBody2D per cell is simpler than TileMapLayer — allows individual node removal without atlas manipulation.
- TileMapLayer coordinate conversion: `local_to_map(position)` → cell coords, `map_to_local(cell)` → world position.

## Camera Patterns

- **Detach child camera:** Set `top_level = true` in `_ready()` on a Camera3D that's a child of a moving node. It operates in world space while remaining a scene child.
- **Smooth follow (3D):** `camera.position = camera.position.lerp(target.position + offset, smooth * delta)`, then `camera.look_at(target.position)`.
- **Camera-relative input:** Remove pitch from camera basis, multiply input by it for world-space direction:
  ```gdscript
  var cam_basis = camera.global_basis
  cam_basis = cam_basis.rotated(cam_basis.x, -cam_basis.get_euler().x)
  var world_dir = cam_basis * Vector3(input.x, 0, input.y)
  ```
- **Smooth yaw tracking:** Wrap angle difference to [-PI, PI] before lerping to avoid 360-degree spin-arounds:
  ```gdscript
  var diff: float = fmod(target_yaw - current_yaw + 3.0 * PI, TAU) - PI
  current_yaw += diff * rotation_speed * delta
  ```
- **Snap on first frame:** Use an `_initialized` flag to skip lerp on the first `_physics_process()` call — prevents camera starting at origin and visibly swooping to the target.
- **Dynamic FOV:** `camera.fov = clamp(base_fov + (speed - threshold) * factor, base_fov, max_fov)` — speed-based for vehicles.
