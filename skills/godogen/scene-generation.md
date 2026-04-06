# Scene Generation

Scene builders are C# files that run headless in Godot 4 (.NET 9+) to produce `.tscn` files programmatically. They are NOT runtime scripts — they run once at build-time and exit.

## Scene Output Requirements

Generate a single C# file that:
1. `public partial class BuildXxx : SceneTree` (must be `partial`)
2. Implements `public override void _Initialize()` as entry point
3. Builds complete node hierarchy with all properties set
4. Sets `Owner` on ALL descendants for serialization
5. Attaches scripts from STRUCTURE.md via `SetScript()`
6. Saves scene using `PackedScene.Pack()` + `ResourceSaver.Save()`
7. Calls `Quit()` when done

## Owner Chain (CRITICAL)

**MUST call `SetOwnerOnNewNodes(root, root)` ONCE at the end**, after all nodes are added.

```csharp
// At end of _Initialize(), AFTER all AddChild() calls:
SetOwnerOnNewNodes(root, root);

private void SetOwnerOnNewNodes(Node node, Node sceneOwner)
{
    foreach (var child in node.GetChildren())
    {
        child.Owner = sceneOwner;
        if (string.IsNullOrEmpty(child.SceneFilePath))
        {
            // Node created with new() — recurse into children
            SetOwnerOnNewNodes(child, sceneOwner);
        }
        // else: instantiated scene (GLB/TSCN) — don't recurse, keeps as reference
    }
}
```

### Post-Pack Validation

Call after `packed.Pack(root)` to verify no nodes were silently dropped:

```csharp
private bool ValidatePackedScene(PackedScene packed, int expectedCount, string scenePath)
{
    var testInstance = packed.Instantiate();
    int actual = CountNodes(testInstance);
    testInstance.Free();
    if (actual < expectedCount)
    {
        GD.PushError($"Pack validation failed for {scenePath}: expected {expectedCount} nodes, got {actual} — nodes were dropped during serialization");
        return false;
    }
    return true;
}
```

Use in the scene template between `packed.Pack(root)` and `ResourceSaver.Save()`. **Gate the save on the validation result:**
```csharp
    int count = CountNodes(root);
    var err = packed.Pack(root);
    if (err != Error.Ok)
    {
        GD.PushError($"Pack failed: {err}");
        Quit(1);
        return;
    }
    if (!ValidatePackedScene(packed, count, "res://{output_path}.tscn"))
    {
        Quit(1);
        return;
    }
```

**WRONG patterns** (cause missing nodes in saved .tscn):
```csharp
// WRONG: Setting owner only on direct children, forgetting grandchildren
terrain.Owner = root;  // Terrain's children (Mesh, Collision) have NO owner!

// WRONG: Calling helper on containers instead of root
SetOwnerOnNewNodes(trackContainer, root);  // trackContainer itself has NO owner!
```

**GLB OWNERSHIP BUG** — Never use unconditional recursion. If you recurse into instantiated GLB models, ALL internal mesh/material nodes get serialized inline as text, causing 100MB+ .tscn files.

## Common Node Compositions

**3D Physics Object:**
```csharp
var body = new RigidBody3D();
var collision = new CollisionShape3D();
var mesh = new MeshInstance3D();
var shape = new BoxShape3D();
shape.Size = new Vector3(1, 1, 1);
collision.Shape = shape;
body.AddChild(collision);
body.AddChild(mesh);
```

**Camera Rig:**
```csharp
var pivot = new Node3D();
var camera = new Camera3D();
camera.Position = new Vector3(0, 0, 5);
pivot.AddChild(camera);
```

## Script Attachment (in Scenes)

**`SetScript()` disposes the C# wrapper** — after calling `SetScript()`, the local variable is dead. Build the full hierarchy first, set scripts last. For the root node, use a temp parent to re-obtain the reference.

```csharp
// Set scripts AFTER building the full hierarchy — SetScript() invalidates the C# wrapper.
// For non-root nodes, just call it last (no further use of the variable needed):
playerNode.SetScript(GD.Load("res://scripts/PlayerController.cs"));

// For the root node, use a temp parent pattern (see Scene Template below).
```

## Asset Loading

**3D models (GLB):**
```csharp
var modelScene = GD.Load<PackedScene>("res://assets/glb/car.glb");
var model = modelScene.Instantiate();
model.Name = "CarModel";

// Measure for scaling — find MeshInstance3D (GLB structure varies, may be nested)
var meshInst = FindMeshInstance(model);
var aabb = meshInst != null ? meshInst.GetAabb() : new Aabb(Vector3.Zero, Vector3.One);

// Scale to target size (e.g., car should be ~2 units long)
float targetLength = 2.0f;
float scaleFactor = targetLength / aabb.Size.X;
model.Set("scale", Vector3.One * scaleFactor);
((Node3D)model).Position = new Vector3(0, -aabb.Position.Y * scaleFactor, 0);

parentNode.AddChild(model);

private MeshInstance3D FindMeshInstance(Node node)
{
    if (node is MeshInstance3D mi)
        return mi;
    foreach (var child in node.GetChildren())
    {
        var found = FindMeshInstance(child);
        if (found != null)
            return found;
    }
    return null;
}
```

**GLB orientation:** Imported models often face the wrong axis. After instantiating, check the AABB: the longest dimension tells you which local axis the model faces. If a car's AABB is longest on Z but your game expects forward=negative Z, no rotation needed; if longest on X, rotate 90 degrees. For animals/characters, the forward-facing axis must align with the direction of movement — an animal moving sideways is a clear bug. Verify this in screenshots: if the bounding box or silhouette doesn't match the movement direction, fix the rotation.

**Collision shapes for 3D models:** Always use simple primitives (BoxShape3D, SphereShape3D, CapsuleShape3D). Never use `CreateConvexShape()` or `CreateTrimeshShape()` on imported GLB meshes — causes <1 FPS on high-poly models (100k+ triangles).

```csharp
// Box from AABB — use this for all imported models
var box = new BoxShape3D();
box.Size = aabb.Size * ((Node3D)model).Scale;
collisionShape.Shape = box;
```

**Textures (PNG):**
```csharp
var mat = new StandardMaterial3D();
mat.AlbedoTexture = GD.Load<Texture2D>("res://assets/img/grass.png");
meshInstance.SetSurfaceOverrideMaterial(0, mat);
```

**Texture UV tiling:** For large surfaces, scale UVs to avoid stretched textures:
```csharp
mat.Uv1Scale = new Vector3(10, 10, 1);  // Tile every 2m on a 20m floor
```

## Child Scene Instancing

```csharp
var carScene = GD.Load<PackedScene>("res://scenes/car.tscn");
var car = carScene.Instantiate<Node3D>();
car.Name = "PlayerCar";
car.Position = new Vector3(0, 0, 5);
root.AddChild(car);
car.Owner = root;  // Child internals already have owner — just set on instance root
```

## Shared Base Class

All scene builders inherit from `SceneBuilderBase` instead of `SceneTree`. This eliminates 30+ lines of repeated boilerplate per builder. Create this file once during scaffold:

**`scenes/SceneBuilderBase.cs`:**
```csharp
using Godot;

public partial class SceneBuilderBase : SceneTree
{
    protected void SetOwnerOnNewNodes(Node node, Node sceneOwner)
    {
        foreach (var child in node.GetChildren())
        {
            child.Owner = sceneOwner;
            if (string.IsNullOrEmpty(child.SceneFilePath))
                SetOwnerOnNewNodes(child, sceneOwner);
        }
    }

    protected int CountNodes(Node node)
    {
        int total = 1;
        foreach (var child in node.GetChildren())
            total += CountNodes(child);
        return total;
    }

    protected bool ValidatePackedScene(PackedScene packed, int expectedCount, string scenePath)
    {
        var testInstance = packed.Instantiate();
        int actual = CountNodes(testInstance);
        testInstance.Free();
        if (actual < expectedCount)
        {
            GD.PushError($"Pack validation failed for {scenePath}: expected {expectedCount} nodes, got {actual}");
            return false;
        }
        return true;
    }

    protected void PackAndSave(Node rootNode, string outputPath)
    {
        SetOwnerOnNewNodes(rootNode, rootNode);
        int count = CountNodes(rootNode);

        var packed = new PackedScene();
        var err = packed.Pack(rootNode);
        if (err != Error.Ok)
        {
            GD.PushError($"Pack failed: {err}");
            Quit(1);
            return;
        }
        if (!ValidatePackedScene(packed, count, outputPath))
        {
            Quit(1);
            return;
        }
        err = ResourceSaver.Save(packed, outputPath);
        if (err != Error.Ok)
        {
            GD.PushError($"Save failed: {err}");
            Quit(1);
            return;
        }
        GD.Print($"BUILT: {count} nodes → {outputPath}");
        Quit(0);
    }
}
```

## Scene Template

```csharp
using Godot;

public partial class Build{SceneName} : SceneBuilderBase
{
    public override void _Initialize()
    {
        GD.Print("Generating: {scene_name}");

        var temp = new Node();
        var root = new {RootNodeType}();
        root.Name = "{SceneName}";
        temp.AddChild(root);

        // ... build node hierarchy, AddChild(), set properties ...

        // Set scripts LAST (SetScript disposes C# wrapper — see quirks.md)
        // root.SetScript(GD.Load("res://scripts/{Script}.cs"));

        // Re-obtain root (old wrapper is disposed after SetScript)
        var rootNode = temp.GetChild(0);
        temp.RemoveChild(rootNode);
        temp.Free();

        PackAndSave(rootNode, "res://{output_path}.tscn");
    }
}
```

### CRITICAL: Build order

Scene builders run via `godot --headless --script res://builders/BuildXxx.cs`. Each builder must be self-contained. If scene A instances scene B, build B first.

### What NOT to Include

Scene builders produce `.tscn` files only. They must NOT contain:
- Runtime logic (`_Ready()`, `_Process()`, `_PhysicsProcess()`, input handling)
- Signal connections (signals are wired in runtime scripts)
- Game state, scoring, win/lose conditions
- UI behavior or button callbacks

## Scene Constraints

- Do NOT use `[Export]` or scene-time annotations (this runs at build-time)
- Do NOT use `preload()` — use `GD.Load<T>()` (no preload equivalent in C#)
- Do NOT connect signals at build-time — scripts aren't instantiated yet. Signal connections belong in runtime scripts' `_Ready()` method
- **No spatial methods in `_Initialize()`** — `LookAt()`, `ToGlobal()`, etc. fail because nodes aren't in the tree yet. Use `RotationDegrees` or compute transforms manually. In runtime scripts (`_Ready()`, `_Process()`), **always use `LookAt()` to orient cameras and objects toward targets** — it's the correct tool there. Manual rotation math is error-prone and unnecessary.
- **2D/3D consistency** — never mix dimensions in the same scene hierarchy.

## Environment & Lighting (3D Scenes)

When building 3D scenes, set up environment and lighting programmatically:

```csharp
// WorldEnvironment
var worldEnv = new WorldEnvironment();
var env = new Godot.Environment();
env.BackgroundMode = Godot.Environment.BGMode.Sky;
env.TonemapMode = Godot.Environment.ToneMapper.Filmic;
env.AmbientLightColor = Colors.White;
env.AmbientLightSkyContribution = 0.5f;
var sky = new Sky();
sky.SkyMaterial = new ProceduralSkyMaterial();
env.Sky = sky;
worldEnv.Environment = env;
root.AddChild(worldEnv);

// Sun (DirectionalLight3D)
var sun = new DirectionalLight3D();
sun.ShadowEnabled = true;
sun.ShadowBias = 0.05f;
sun.ShadowBlur = 2.0f;
sun.DirectionalShadowMaxDistance = 30.0f;
sun.SkyMode = DirectionalLight3D.SkyModeEnum.LightAndSky;
sun.RotationDegrees = new Vector3(-45, -30, 0);
root.AddChild(sun);
```

## CSG for Rapid Prototyping

CSG nodes generate collision automatically — no separate CollisionShape needed:

```csharp
var floor = new CsgBox3D();
floor.Size = new Vector3(20, 0.5f, 20);
floor.UseCollision = true;
floor.Material = groundMat;
root.AddChild(floor);

// Subtraction (carve holes): child CSG on parent CSG
var hole = new CsgCylinder3D();
hole.Operation = CsgShape3D.OperationEnum.Subtraction;
hole.Radius = 1.0f;
hole.Height = 1.0f;
floor.AddChild(hole);
```

## Noise/Procedural Textures

```csharp
var noise = new FastNoiseLite();
noise.NoiseType = FastNoiseLite.NoiseTypeEnum.Cellular;
noise.Frequency = 0.02f;
noise.FractalType = FastNoiseLite.FractalTypeEnum.Fbm;
noise.FractalOctaves = 5;

var tex = new NoiseTexture2D();
tex.Noise = noise;
tex.Width = 1024;
tex.Height = 1024;
tex.Seamless = true;       // tileable
tex.AsNormalMap = true;     // for normal maps
tex.BumpStrength = 2.0f;
```

## StandardMaterial3D Extended Properties

Beyond basic albedo, useful properties for richer materials:
- `NormalEnabled = true` + `NormalTexture` + `NormalScale = 2.0f`
- `RimEnabled = true` + `RimTint = 1.0f` — silhouette glow
- `EmissionEnabled = true` + `EmissionTexture` — self-illumination
- `TextureFilter = BaseMaterial3D.TextureFilterEnum.LinearWithMipmapsAnisotropic`
