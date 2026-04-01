# Script Generation

Runtime scripts define node behavior — movement, combat, AI, signals, and game logic. They attach to nodes in scenes and run when the game plays.

## Script Output Requirements

Generate a `.gd` file that:
1. `extends {NodeType}` matching the node it attaches to
2. Uses proper Godot lifecycle methods
3. References sibling/child nodes via correct paths
4. Defines and connects signals as needed

## Script Template

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

## VehicleBody3D

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

## Script Constraints

- **Sibling signal timing:** `_ready()` fires on children in order. If sibling A emits in its `_ready()`, sibling B hasn't connected yet. Fix: after connecting, check if the emitter already has data and call the handler manually.
- Do NOT use `preload()` for scenes/resources that may not exist yet — use `load()`.
- **NEVER use `:=` with polymorphic math functions** — `abs`, `sign`, `clamp`, `min`, `max`, `floor`, `ceil`, `round`, `lerp`, `smoothstep`, `move_toward`, `wrap`, `snappedf`, `randf_range`, `randi_range` return Variant. Use explicit types: `var x: float = abs(y)` not `var x := abs(y)`
