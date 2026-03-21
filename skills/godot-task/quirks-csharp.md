# C# Quirks (Godot .NET)

- **`partial class` is mandatory** — every class that extends a Godot type MUST be `partial`. Without it, signal delegates and export properties fail silently or produce cryptic build errors.
- **`GD.Print()` not `Console.WriteLine()`** — `Console.WriteLine()` writes to the system console, not Godot's output panel. Use `GD.Print()` for all game output.
- **PascalCase for all Godot API** — `Position` not `position`, `MoveAndSlide()` not `move_and_slide()`, `GlobalPosition` not `global_position`. This applies to properties, methods, signals, and enums.
- **Signal delegate naming** — must end with `EventHandler`. `[Signal] public delegate void DiedEventHandler();` creates a signal named `Died`. Emit with `EmitSignal(SignalName.Died)`.
- **`dotnet build` before Godot recognizes scripts** — C# scripts exist as compiled DLLs, not interpreted files. After writing or modifying `.cs` files, run `dotnet build` before `godot --headless --quit` or Godot won't see the new scripts.
- **Export property serialization** — `[Export]` properties must have public getters and setters. Auto-properties (`{ get; set; }`) work. Private setters cause silent serialization failures.
- **Nullable reference type warnings** — Godot's generated code triggers NRT warnings. Add `<Nullable>disable</Nullable>` to `.csproj` or use `= null!` for node references resolved in `_Ready()`.
- **`_Ready()` timing with `GetNode()`** — same as GDScript: `GetNode<T>()` fails if called before the node enters the tree. Always use in `_Ready()`, never in constructors or field initializers.
- **Enum access** — Godot enums are nested in their class: `CharacterBody3D.MotionModeEnum.Floating`, not bare `MOTION_MODE_FLOATING`.
- **`Callable` construction** — `new Callable(this, MethodName.MyMethod)` or `new Callable(this, nameof(MyMethod))`. Lambda-based callables: `Callable.From(() => MyMethod())`.
- **`double` delta** — `_Process(double delta)` and `_PhysicsProcess(double delta)` use `double`, not `float`. Cast when passing to Godot methods that expect `float`: `(float)delta`.
- **Resource loading** — `GD.Load<PackedScene>("res://scenes/enemy.tscn")` for typed loading. `ResourceLoader.Load()` for untyped. Both work, but typed is preferred.
- **Node path syntax** — use string paths with `GetNode<T>("Path/To/Node")`, not the `$` or `%` shorthand from GDScript.
