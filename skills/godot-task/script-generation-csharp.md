# C# Script Generation

Runtime scripts in C# define node behavior. They attach to nodes in scenes and run when the game plays.

## Script Output Requirements

Generate a `.cs` file that:
1. `public partial class ClassName : NodeType` matching the node it attaches to
2. Uses proper Godot lifecycle methods (`_Ready`, `_Process`, `_PhysicsProcess`)
3. References sibling/child nodes via `GetNode<T>()` in `_Ready()`
4. Defines signals with `[Signal]` delegate pattern

## Script Template

```csharp
using Godot;

public partial class PlayerController : CharacterBody3D
{
    // Signals
    [Signal] public delegate void HealthChangedEventHandler(int newValue);
    [Signal] public delegate void DiedEventHandler();

    // Exports
    [Export] public float Speed { get; set; } = 7.0f;
    [Export(PropertyHint.Range, "0,100")] public int Health { get; set; } = 100;

    // Node references (resolved in _Ready)
    private MeshInstance3D _mesh;
    private CollisionShape3D _collision;

    // State
    private int _currentHealth;

    public override void _Ready()
    {
        _mesh = GetNode<MeshInstance3D>("MeshInstance3D");
        _collision = GetNode<CollisionShape3D>("CollisionShape3D");
        _currentHealth = Health;
    }

    public override void _PhysicsProcess(double delta)
    {
    }
}
```

**Script section ordering:** Signals → Exports → Node references → State → Lifecycle methods → Public methods → Private methods → Signal handlers

## CharacterBody3D Movement

```csharp
public partial class PlayerController : CharacterBody3D
{
    [Export] public float Speed { get; set; } = 5.0f;
    [Export] public float JumpVelocity { get; set; } = -4.5f;

    public override void _PhysicsProcess(double delta)
    {
        Vector3 velocity = Velocity;

        if (!IsOnFloor())
            velocity.Y -= (float)(9.8 * delta);

        if (Input.IsActionJustPressed("jump") && IsOnFloor())
            velocity.Y = JumpVelocity;

        Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
        Vector3 direction = (Transform.Basis * new Vector3(inputDir.X, 0, inputDir.Y)).Normalized();

        if (direction != Vector3.Zero)
        {
            velocity.X = direction.X * Speed;
            velocity.Z = direction.Z * Speed;
        }
        else
        {
            velocity.X = Mathf.MoveToward(velocity.X, 0, Speed);
            velocity.Z = Mathf.MoveToward(velocity.Z, 0, Speed);
        }

        Velocity = velocity;
        MoveAndSlide();
    }
}
```

## Script Constraints

- `partial class` is MANDATORY for all Godot C# classes
- `extends` equivalent is `: BaseType` — must match the node type
- Use `GetNode<T>()` in `_Ready()`, NOT field initializers or constructors
- Connect signals in `_Ready()`, not in scene builders
- Use `GD.Print()` for Godot console output, NOT `Console.WriteLine()`
- All Godot API methods and properties use PascalCase
- `delta` is `double`, not `float` — cast when needed: `(float)delta`
- Validate via `dotnet build` — MSBuild errors are more structured than Godot GDScript errors
- ONLY use input actions from plan's inputs, never invent action names
- Connect signals in `_Ready()`, NOT in scene builders
