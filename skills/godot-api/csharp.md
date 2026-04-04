# C# Godot Syntax Reference

## Language Notes

- All Godot C# classes must be `public partial class` — the `partial` keyword enables Godot's source generators for signals, exports, and node bindings.
- Godot API uses PascalCase everywhere: `_Ready()`, `GetNode()`, `Position`, `EmitSignal()`.
- C# uses .NET 8+. Standard C# features (LINQ, async/await, generics, pattern matching) are available.

## Types

**Godot built-in (value types):** `Vector2`, `Vector2I`, `Vector3`, `Vector3I`, `Vector4`, `Vector4I`, `Rect2`, `Rect2I`, `Aabb`, `Basis`, `Transform2D`, `Transform3D`, `Quaternion`, `Plane`, `Projection`, `Color`, `Rid`, `NodePath`, `StringName`

**C# primitives:** `bool`, `int`, `long`, `float`, `double`, `string`

**Godot collections:** `Godot.Collections.Array`, `Godot.Collections.Array<T>`, `Godot.Collections.Dictionary`, `Godot.Collections.Dictionary<TKey, TValue>`

**Variant:** `Godot.Variant` — wraps any Godot-compatible type. Explicit conversion required:
```csharp
Variant v = 42;
int n = (int)v;
var s = (string)v;
```

**Value vs reference:** `Vector2/3`, `Color`, `Transform3D`, `Aabb`, etc. are structs (value types) — passing to a function copies them. `GodotObject` subclasses (nodes, resources) are reference types.

## Class Structure

```csharp
using Godot;

public partial class PlayerController : CharacterBody3D
{
    [Signal] public delegate void DiedEventHandler();
    [Signal] public delegate void ScoredEventHandler(int points);

    [Export] public float Speed = 7.0f;
    [Export(PropertyHint.Range, "0,100,1")] public int Health = 100;

    private Sprite2D _sprite;

    public override void _Ready()
    {
        _sprite = GetNode<Sprite2D>("Sprite2D");
    }

    public override void _PhysicsProcess(double delta)
    {
    }

    private void OnHurtEntered(Area3D area)
    {
    }
}
```

## Signals

```csharp
// Define (must end in EventHandler, must be delegate void)
[Signal] public delegate void HealthChangedEventHandler(int newValue);
[Signal] public delegate void DiedEventHandler();

// Emit
EmitSignal(SignalName.Died);
EmitSignal(SignalName.HealthChanged, 42);

// Connect (C# event syntax)
otherNode.Died += OnDied;
otherNode.HealthChanged += OnHealthChanged;

// Connect with Callable (for Godot APIs that need it)
otherNode.Connect(OtherNode.SignalName.Died, Callable.From(OnDied));

// Disconnect
otherNode.Died -= OnDied;

// Await
await ToSignal(otherNode, OtherNode.SignalName.Died);
await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout);
```

## Exports

```csharp
[Export] public float Speed = 100.0f;
[Export(PropertyHint.Range, "0,100,1")] public int Health = 100;
[Export(PropertyHint.Enum, "Low,Medium,High")] public int Quality;
[Export(PropertyHint.File, "*.png")] public string TexturePath;
[Export(PropertyHint.NodePathValidTypes, "Sprite2D")] public NodePath SpritePath;
[ExportGroup("Movement")]
[ExportSubgroup("Speed")]
[Export] public float WalkSpeed = 5.0f;

// Resource/scene exports
[Export] public PackedScene BulletScene;
[Export] public Texture2D Icon;
```

## Node References

```csharp
GetNode<Sprite2D>("Sprite2D")            // Get child (throws if missing)
GetNodeOrNull<Sprite2D>("Sprite2D")      // Returns null if missing
GetNode<Node3D>("Path/To/Node")          // Nested path
GetParent<Node3D>()                      // Parent node
GetTree()                                // SceneTree
HasNode("Path")                          // Check existence

// No @onready equivalent — resolve in _Ready()
private Camera3D _camera;
public override void _Ready()
{
    _camera = GetNode<Camera3D>("Camera3D");
}
```

## Variables & Constants

```csharp
// C# standard typing — no Variant inference issues
var x = 5;                               // int (inferred)
float speed = 7.0f;                      // explicit
const int Max = 100;                     // compile-time constant
static int Count = 0;                    // class-level static

// Enums
public enum State { Idle, Run, Jump }
```

## Control Flow

```csharp
// Conditionals
if (condition) { }
else if (other) { }
else { }

// Ternary
var result = condition ? "yes" : "no";

// Switch (pattern matching)
switch (value)
{
    case 1:
        GD.Print("one");
        break;
    case 2 or 3 or 4:
        GD.Print("two to four");
        break;
    case > 10:
        GD.Print("big");
        break;
    default:
        GD.Print("default");
        break;
}

// switch expression
var label = state switch
{
    State.Idle => "Standing",
    State.Run => "Running",
    _ => "Unknown"
};

// Loops
for (int i = 0; i < 10; i++) { }
foreach (var item in array) { }
while (condition) { }
```

## Functions / Methods

```csharp
public int Add(int a, int b) => a + b;

public void Greet(string name = "World")
{
    GD.Print($"Hello, {name}");
}

// Lambda / delegate
Func<int, int> doubleIt = x => x * 2;
Action<string> log = msg => GD.Print(msg);

// Callable from method (for Godot APIs)
var callable = Callable.From(MyMethod);
var callableLambda = Callable.From(() => GD.Print("hi"));
```

## Strings

```csharp
var s = "Hello\nWorld";
var raw = @"C:\path\file";               // verbatim string
var multi = """
    Line 1
    Line 2
    """;                                  // raw string literal (C# 11)

// Interpolation
var msg = $"x={x} y={y}";
var formatted = $"{value:F2}";            // 2 decimal places

// Common methods
s.Length                                  // int (property, not method)
s.ToUpper()
s.ToLower()
s.Trim()
s.Split(',')                             // string[]
string.Join(",", new[] { "a", "b" })
s.StartsWith("He")
s.EndsWith("ld")
s.Contains("ll")
s.Replace("l", "L")
42.ToString()
int.Parse("42")
float.Parse("3.14")
```

## Arrays & Collections

```csharp
// C# arrays / lists (use for internal logic)
var arr = new int[] { 1, 2, 3 };
var list = new List<int> { 1, 2, 3 };
list.Add(4);
list.Insert(2, 99);
list.RemoveAt(1);
list.Contains(2);
list.IndexOf(2);
list.Sort();
list.Reverse();
list.Count                                // property

// Godot collections (use when interop with Godot API required)
var gArr = new Godot.Collections.Array<int> { 1, 2, 3 };
var gDict = new Godot.Collections.Dictionary<string, int>
{
    ["a"] = 1, ["b"] = 2
};

// LINQ (works on any IEnumerable)
var doubled = list.Select(x => x * 2).ToList();
var filtered = list.Where(x => x > 0).ToList();
var sum = list.Aggregate(0, (a, b) => a + b);

// Dictionary
var dict = new Dictionary<string, int>
{
    { "key", 42 }, { "other", 100 }
};
dict["new_key"] = 200;
dict.TryGetValue("key", out int val);
dict.ContainsKey("key");
dict.Remove("key");
dict.Keys                                 // ICollection
dict.Values                               // ICollection
```

## Memory Management

- **RefCounted subclasses** (Resource, etc.): automatically freed when no references exist.
- **GodotObject/Node subclasses**: manually managed.
  - `node.Free()` — immediate deletion.
  - `node.QueueFree()` — safely delete at end of frame (recommended for Nodes).
- **GodotObject prevent-GC**: if you store a GodotObject in a C# field that Godot doesn't know about (e.g., a static list), the GC might collect the C# wrapper while Godot still references the native object. Use `GodotObject.IsInstanceValid(obj)` to check.
- **WeakRef**: `GodotObject.WeakRef(obj)` creates reference that doesn't prevent freeing.

## Type Checking & Casting

```csharp
// Type checking
if (node is Sprite2D sprite)
{
    sprite.Modulate = Colors.Red;
}

// Safe cast
var s = node as Sprite2D;
if (s != null)
{
    s.Modulate = Colors.Red;
}

// Type test
if (node.GetType() == typeof(Sprite2D)) { }
```

## Common Patterns

```csharp
// Groups
AddToGroup("enemies");
GetTree().GetNodesInGroup("enemies");
IsInGroup("enemies");
GetTree().CallGroup("enemies", "TakeDamage", 10);

// Scene management
GetTree().ChangeSceneToFile("res://level2.tscn");
GetTree().ReloadCurrentScene();
GetTree().Quit();

// Instantiate scene
var scene = GD.Load<PackedScene>("res://enemy.tscn");
var instance = scene.Instantiate();
AddChild(instance);

// Instantiate with type
var enemy = scene.Instantiate<Enemy>();

// Timer
await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout);

// Deferred calls
CallDeferred(MethodName.MyMethod);
SetDeferred(PropertyName.Disabled, true);

// Pause
GetTree().Paused = true;
ProcessMode = ProcessModeEnum.Always;     // exempt from pause
ProcessMode = ProcessModeEnum.Pausable;   // default
```

## Math

```csharp
// Constants
Mathf.Pi, Mathf.Tau, Mathf.Inf, float.NaN

// Basic
Mathf.Abs(x), Mathf.Sign(x), Mathf.Floor(x), Mathf.Ceil(x), Mathf.Round(x)
Mathf.Min(a, b), Mathf.Max(a, b), Mathf.Clamp(val, min, max)
Mathf.PosMod(x, y)                       // math-style modulo
Mathf.Snapped(val, step)                  // snap to step
Mathf.Wrap(val, min, max)

// Interpolation
Mathf.Lerp(a, b, t)
Mathf.InverseLerp(a, b, val)
Mathf.SmoothStep(from, to, val)
Mathf.MoveToward(from, to, delta)

// Trigonometry
Mathf.Sin(x), Mathf.Cos(x), Mathf.Tan(x)
Mathf.Asin(x), Mathf.Acos(x), Mathf.Atan(x), Mathf.Atan2(y, x)
Mathf.DegToRad(deg), Mathf.RadToDeg(rad)

// Power/exponential
Mathf.Sqrt(x), Mathf.Pow(b, exp), Mathf.Exp(x), Mathf.Log(x)

// Random
GD.Randf()                               // 0.0 to 1.0
GD.Randi()                               // random uint
GD.RandRange(from, to)                   // float in range
GD.RandRange(from, to)                   // cast to int if needed: (int)GD.RandRange(0, 10)
```

## Input

```csharp
// Actions
Input.IsActionPressed("move_right")
Input.IsActionJustPressed("jump")
Input.IsActionJustReleased("fire")
Input.GetActionStrength("accelerate")     // 0.0 to 1.0
Input.GetAxis("move_left", "move_right")  // -1.0 to 1.0
Input.GetVector("left", "right", "up", "down")  // Vector2

// Direct key/mouse
Input.IsKeyPressed(Key.W)
Input.IsMouseButtonPressed(MouseButton.Left)
Input.GetLastMouseScreenVelocity()

// Event handling
public override void _Input(InputEvent @event)
{
    if (@event.IsActionPressed("jump"))
        Jump();
    if (@event is InputEventMouseButton mb && mb.Pressed && mb.ButtonIndex == MouseButton.Left)
        Shoot();
}

public override void _UnhandledInput(InputEvent @event)
{
    // Called for input not consumed by UI
}
```

## Spawning Patterns

```csharp
// Path-based random spawning
var spawnLoc = GetNode<PathFollow2D>("SpawnPath/SpawnLocation");
spawnLoc.ProgressRatio = GD.Randf();
var mob = MobScene.Instantiate<CharacterBody2D>();
mob.Position = spawnLoc.Position;

// Auto-cleanup off-screen
GetNode<VisibleOnScreenNotifier2D>("Notifier").ScreenExited += QueueFree;

// Screen bounds clamping
Position = Position.Clamp(Vector2.Zero, screenSize);
```

## Animation Patterns

```csharp
// AnimationPlayer
GetNode<AnimationPlayer>("AnimationPlayer").Play("run");
GetNode<AnimationPlayer>("AnimationPlayer").SpeedScale =
    Velocity.Length() / maxSpeed;

// AnimatedSprite2D — pick random
var names = GetNode<AnimatedSprite2D>("Sprite").SpriteFrames.GetAnimationNames();
GetNode<AnimatedSprite2D>("Sprite").Play(names[GD.Randi() % names.Length]);

// AnimationTree blend parameters
GetNode<AnimationTree>("AnimationTree")
    .Set("parameters/speed/blend_amount", Velocity.Length() / maxSpeed);

// animation_finished signal
GetNode<AnimationPlayer>("AnimationPlayer").AnimationFinished += OnAnimationFinished;
```

## Character Facing/Rotation

```csharp
// 3D — face movement direction
if (direction != Vector3.Zero)
    Basis = Basis.LookingAt(direction);

// Isometric 8-directional animation index
float angle = Mathf.RadToDeg(direction.Angle()) + 22.5f;
int dirIndex = ((int)Mathf.Floor(angle / 45.0f)) % 8;
```

## Jump/Gravity Patterns

```csharp
// Terminal velocity
Velocity = Velocity with { Y = Mathf.Min(TerminalVelocity, Velocity.Y + gravity * (float)delta) };

// Early jump release (variable jump height)
if (Input.IsActionJustReleased("jump") && Velocity.Y < 0)
    Velocity = Velocity with { Y = Velocity.Y * 0.6f };

// Gravity from ProjectSettings (3D)
float gravity = (float)ProjectSettings.GetSetting("physics/3d/default_gravity");

// Slide collision detection (stomp enemies)
for (int i = 0; i < GetSlideCollisionCount(); i++)
{
    var col = GetSlideCollision(i);
    if (col.GetNormal().Dot(Vector3.Up) > 0.7f)
        ((Enemy)col.GetCollider()).Squash();
}
```

## Movement Feel

```csharp
// Walk/stop force asymmetry
if (Mathf.Abs(inputDir) > 0.2f)
    vel.X = Mathf.MoveToward(vel.X, inputDir * MaxSpeed, WalkForce * (float)delta);
else
    vel.X = Mathf.MoveToward(vel.X, 0, StopForce * (float)delta);

// Velocity clamping
vel.X = Mathf.Clamp(vel.X, -MaxSpeed, MaxSpeed);

// 3D smooth acceleration
horizontalVel = horizontalVel.Lerp(targetVel, accel * (float)delta);

// Analog input
float throttle = Input.GetActionStrength("accelerate");
```

## State Machine Pattern

```csharp
// Node-based state machine
public abstract partial class State : Node
{
    [Signal] public delegate void FinishedEventHandler(StringName nextState);
    public virtual void Enter() { }
    public virtual void Exit() { }
    public virtual void HandleInput(InputEvent @event) { }
    public virtual void Update(double delta) { }
}

// State machine manages current + stack
private State _currentState;
private Stack<State> _stateStack = new();
```

## Navigation Patterns

```csharp
// 2D: NavigationAgent2D as child of CharacterBody2D
public void SetTarget(Vector2 pos)
{
    GetNode<NavigationAgent2D>("NavigationAgent2D").TargetPosition = pos;
}

public override void _PhysicsProcess(double delta)
{
    var agent = GetNode<NavigationAgent2D>("NavigationAgent2D");
    if (agent.IsNavigationFinished())
        return;
    var next = agent.GetNextPathPosition();
    Velocity = GlobalPosition.DirectionTo(next) * Speed;
    MoveAndSlide();
}

// 3D: NavigationAgent3D, or server API
var path = NavigationServer3D.MapGetPath(navMap, start, target, true);
```

## RigidBody _IntegrateForces

```csharp
public override void _IntegrateForces(PhysicsDirectBodyState2D state)
{
    var lv = state.LinearVelocity;
    // Modify based on input...
    state.LinearVelocity = lv;

    for (int i = 0; i < state.GetContactCount(); i++)
    {
        var normal = state.GetContactLocalNormal(i);
        var collider = state.GetContactColliderObject(i);
    }
}

// Collision exceptions
bullet.AddCollisionExceptionWith(shooter);
```

## Server API (Performance)

```csharp
// PhysicsServer2D for 500+ objects without nodes
var shape = PhysicsServer2D.CircleShapeCreate();
var body = PhysicsServer2D.BodyCreate();
PhysicsServer2D.BodyAddShape(body, shape);
PhysicsServer2D.BodySetState(body, PhysicsServer2D.BodyState.Transform, xform);
PhysicsServer2D.BodySetCollisionMask(body, 0);
// MUST cleanup in _ExitTree():
PhysicsServer2D.FreeRid(body);

// Custom drawing for server-managed objects
public override void _Process(double delta) => QueueRedraw();
public override void _Draw()
{
    foreach (var bullet in _bullets)
        DrawTexture(bulletTex, bullet.Position);
}
```

## Custom Drawing

```csharp
DrawLine(from, to, color, width, antialiased);
DrawCircle(pos, radius, color, filled, width, antialiased);
DrawRect(new Rect2(pos, size), color, filled, width, antialiased);
DrawPolygon(points, colors);
DrawTexture(texture, pos, modulate);
DrawSetTransform(pos, rotation, scale);   // stateful
QueueRedraw();                            // trigger in _Process()
```

## Tween

```csharp
var tween = CreateTween();
tween.SetLoops(3);                        // 0 = infinite
tween.SetSpeedScale(2.0f);

// Parallel tweens
tween.Parallel().TweenProperty(node, "position", target, 0.5f);
tween.Parallel().TweenProperty(node, "modulate", Colors.Red, 0.5f);

// Callbacks
tween.TweenCallback(Callable.From(() => DoSomething()));

// Method tween (non-property interpolation)
tween.TweenMethod(Callable.From<float>(SetCustomValue), 0.0f, 1.0f, 0.5f);

// Relative motion
tween.TweenProperty(node, "position", offset, 0.5f).AsRelative();

// State
tween.IsValid(); tween.IsRunning(); tween.Pause(); tween.Play(); tween.Kill();
```

## File I/O

```csharp
using var f = FileAccess.Open(path, FileAccess.ModeFlags.Write);
f.StoreString(data);
var text = FileAccess.GetFileAsString(path);
```

## 2D Top-Down Patterns

- Grid alignment assist: snap Y to nearest row center when moving horizontally (`Mathf.Round(pos.Y / tileSize) * tileSize + tileSize / 2`), and vice versa.
- For modifiable grids (breakable blocks), Sprite2D + StaticBody2D per cell is simpler than TileMapLayer.
- TileMapLayer coordinate conversion: `LocalToMap(position)` → cell coords, `MapToLocal(cell)` → world position.

## Camera Patterns

- **Detach child camera:** Set `TopLevel = true` in `_Ready()` on a Camera3D that's a child of a moving node.
- **Smooth follow (3D):** `camera.Position = camera.Position.Lerp(target.Position + offset, smooth * (float)delta); camera.LookAt(target.Position);`
- **Camera-relative input:** Remove pitch from camera basis, multiply input:
  ```csharp
  var camBasis = camera.GlobalBasis;
  camBasis = camBasis.Rotated(camBasis.X, -camBasis.GetEuler().X);
  var worldDir = camBasis * new Vector3(input.X, 0, input.Y);
  ```
- **Dynamic FOV:** `camera.Fov = Mathf.Clamp(baseFov + (speed - threshold) * factor, baseFov, maxFov);`
