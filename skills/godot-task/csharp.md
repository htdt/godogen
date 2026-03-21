# C# + Godot .NET Reference

## GDScript → C# Mapping

| GDScript | C# |
|---|---|
| `extends Node` | `public partial class MyClass : Node` |
| `@export var speed: float = 5.0` | `[Export] public float Speed { get; set; } = 5.0f;` |
| `@onready var x = $Node` | field + `_x = GetNode<Type>("Node");` in `_Ready()` |
| `signal my_signal` | `[Signal] public delegate void MySignalEventHandler();` |
| `my_signal.emit()` | `EmitSignal(SignalName.MySignal);` |
| `func _process(delta)` | `public override void _Process(double delta)` |
| `func _physics_process(delta)` | `public override void _PhysicsProcess(double delta)` |
| `func _ready()` | `public override void _Ready()` |
| `func _input(event)` | `public override void _Input(InputEvent @event)` |
| `GD.print("x")` | `GD.Print("x");` |
| `position` | `Position` |
| `move_and_slide()` | `MoveAndSlide()` |

`partial class` is **mandatory** — Godot's source generator requires it to wire up signals, exports, and RPCs.

## Lifecycle Methods

```csharp
public override void _EnterTree() { }     // Node added to scene tree
public override void _Ready() { }         // Node and all children ready
public override void _Process(double delta) { }          // Every frame
public override void _PhysicsProcess(double delta) { }   // Physics tick
public override void _Input(InputEvent @event) { }       // All input events
public override void _UnhandledInput(InputEvent @event) { } // UI-unconsumed input
public override void _ExitTree() { }      // Node removed from scene tree
```

`delta` is `double`, not `float`. Cast explicitly: `(float)delta` when needed.

## Node References

```csharp
// Typed get — throws if not found or wrong type
GetNode<Sprite2D>("Sprite2D");
GetNode<Node>("Path/To/Node");

// Safe get — returns null instead of throwing
GetNodeOrNull<Sprite2D>("Sprite2D");

// Parent / tree
GetParent<CharacterBody2D>();
GetTree();                         // SceneTree
GetViewport();

// @onready equivalent — declare field, assign in _Ready()
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite2D");
}
```

## Signals

```csharp
// Define
[Signal] public delegate void HealthChangedEventHandler(int newValue);
[Signal] public delegate void DiedEventHandler();

// Emit
EmitSignal(SignalName.HealthChanged, 50);
EmitSignal(SignalName.Died);

// Connect (lambda)
button.Pressed += OnButtonPressed;

// Connect (string-based, useful for deferred)
button.Connect("pressed", new Callable(this, nameof(OnButtonPressed)));

// Connect with flags
button.Connect(Button.SignalName.Pressed, new Callable(this, nameof(OnButtonPressed)),
    (uint)ConnectFlags.OneShot);

// Disconnect
button.Pressed -= OnButtonPressed;

// Await signal
await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout);
await ToSignal(animationPlayer, AnimationPlayer.SignalName.AnimationFinished);
```

## Input

```csharp
// Actions (prefer these over raw keys)
Input.IsActionPressed("move_forward");
Input.IsActionJustPressed("jump");
Input.IsActionJustReleased("fire");
Input.GetActionStrength("accelerate");          // 0.0–1.0
Input.GetAxis("move_left", "move_right");       // -1.0–1.0
Input.GetVector("left", "right", "up", "down"); // Vector2

// Raw
Input.IsKeyPressed(Key.W);
Input.IsMouseButtonPressed(MouseButton.Left);
Input.GetMousePosition();

// Event handling
public override void _Input(InputEvent @event)
{
    if (@event.IsActionPressed("jump"))
        Jump();

    if (@event is InputEventMouseButton mb && mb.Pressed && mb.ButtonIndex == MouseButton.Left)
        Shoot();
}
```

## Common Patterns

### Timer

```csharp
// One-shot delay
await ToSignal(GetTree().CreateTimer(1.0f), SceneTreeTimer.SignalName.Timeout);

// Timer node
var timer = GetNode<Timer>("Timer");
timer.WaitTime = 2.0f;
timer.OneShot = true;
timer.Timeout += OnTimerTimeout;
timer.Start();
```

### Tween

```csharp
var tween = CreateTween();
tween.TweenProperty(this, "position", targetPos, 0.5f);
tween.TweenProperty(this, "modulate", Colors.Red, 0.3f);

// Parallel
tween.Parallel().TweenProperty(this, "scale", Vector2.One * 1.5f, 0.3f);

// Callback
tween.TweenCallback(Callable.From(() => GD.Print("done")));
```

### Scene Instantiation

```csharp
private PackedScene _enemyScene = GD.Load<PackedScene>("res://enemy.tscn");
// or at class level:
[Export] public PackedScene EnemyScene { get; set; }

var enemy = EnemyScene.Instantiate<Enemy>();
enemy.Position = spawnPoint;
AddChild(enemy);
```

### Groups

```csharp
AddToGroup("enemies");
IsInGroup("enemies");
GetTree().GetNodesInGroup("enemies");
GetTree().CallGroup("enemies", "TakeDamage", 10);
```

### Scene Management

```csharp
GetTree().ChangeSceneToFile("res://level2.tscn");
GetTree().ReloadCurrentScene();
GetTree().Quit();
```

### Deferred Calls

```csharp
CallDeferred(nameof(MyMethod));
SetDeferred("property_name", value);
```

### Pause

```csharp
GetTree().Paused = true;
ProcessMode = ProcessModeEnum.Always;    // Exempt from pause (e.g., pause menu)
ProcessMode = ProcessModeEnum.Pausable;  // Pauses with tree (default)
```

## Export Variants

```csharp
[Export] public float Speed { get; set; } = 200.0f;
[Export(PropertyHint.Range, "0,100,1")] public int Health { get; set; } = 100;
[Export(PropertyHint.Enum, "Low,Medium,High")] public int Quality { get; set; }
[Export(PropertyHint.File, "*.png")] public string TexturePath { get; set; }

[ExportGroup("Movement")]
[Export] public float MaxSpeed { get; set; }
[ExportSubgroup("Acceleration")]
[Export] public float Accel { get; set; }
```

## Key Differences from GDScript

- `partial class` is mandatory — omitting it silently breaks exports and signals.
- `GD.Print()` for Godot's output panel; `Console.WriteLine()` goes to stdout only.
- All Godot API identifiers are PascalCase: `Position`, `Rotation`, `MoveAndSlide()`, `LookAt()`.
- `delta` is `double` in `_Process` and `_PhysicsProcess` — cast to `float` when passing to Godot math helpers.
- Enums are accessed via their class: `CharacterBody2D.MotionModeEnum.Floating`, `Node.ProcessModeEnum.Always`.
- C# arrays and `List<T>` don't interop with Godot's `Array` — use `Godot.Collections.Array<T>` for Godot-facing APIs.
- `[Signal]` delegates must end with `EventHandler` — Godot strips the suffix when generating `SignalName`.
- No `@onready` annotation; assign node refs manually in `_Ready()`.
- `StringName` interop: use `new StringName("name")` or the implicit cast from `string` where needed.
- Resource loading: `GD.Load<T>("res://...")` at runtime; `ResourceLoader.Load<T>()` for async.
- `queue_free()` → `QueueFree()`.

## Physics & Movement

```csharp
// CharacterBody2D / CharacterBody3D
public override void _PhysicsProcess(double delta)
{
    var velocity = Velocity;

    if (!IsOnFloor())
        velocity.Y -= gravity * (float)delta;

    if (Input.IsActionJustPressed("jump") && IsOnFloor())
        velocity.Y = JumpVelocity;

    var dir = Input.GetAxis("move_left", "move_right");
    velocity.X = dir * Speed;

    Velocity = velocity;
    MoveAndSlide();
}

// 3D camera-relative input
var camBasis = camera.GlobalBasis;
var input = Input.GetVector("left", "right", "up", "down");
var direction = (camBasis * new Vector3(input.X, 0, input.Y)).Normalized();
```

## Utility

```csharp
GD.Print("message");
GD.PrintErr("error");
GD.Randomize();
GD.Randf();                          // 0.0–1.0
GD.RandRange(0.0, 1.0);             // double range
GD.RandRange(0, 10);                 // int range

// Math helpers (Mathf = float, same API as GDScript builtins)
Mathf.Lerp(a, b, t);
Mathf.Clamp(val, min, max);
Mathf.MoveToward(from, to, delta);
Mathf.Pi; Mathf.Tau;
```
