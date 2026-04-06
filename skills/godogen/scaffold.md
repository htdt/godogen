# Godot Scaffold Generator

Design game architecture and produce a compilable Godot C# project skeleton: `project.godot`, `.csproj`, `STRUCTURE.md`, script stubs, and scene builder stubs. Defines *what exists and how it connects* — not behavior.

Works for both fresh projects and incremental changes (adding scenes/scripts, reimplementing subsystems).

## Workflow

1. **Read `reference.png`** — understand the visual target: camera angle, distance, FOV, lighting direction, environment structure, scene layout. Use this to inform architecture decisions (node hierarchy, camera setup, lighting rig).
2. **Read input** — game description (fresh) or change request (incremental).
3. **Assess project state:**
   - No project → create from scratch.
   - Existing project, fresh start requested → delete existing scenes/scripts.
   - Existing project, incremental change → read existing `STRUCTURE.md` and scripts. Identify what to add or replace. Preserve unchanged files.
4. **Design / update architecture** — scenes, scripts, signals, input actions.
5. **Write/update `project.godot`** — create or merge input mappings. Include `[dotnet]` section.
6. **Write `.csproj`** — create or verify the project file exists.
7. **Write `STRUCTURE.md`** — always the complete architecture, not a diff.
8. **Write script stubs** — for new scripts and any existing scripts the task explicitly asks to replace. C# files in `scripts/`.
9. **Write `scenes/SceneBuilderBase.cs`** — shared base class (see `scene-generation.md`). Create once per project; skip if it already exists.
10. **Build .NET project** — `timeout 60 dotnet build 2>&1`. Ensures all C# compiles before scene builders run.
11. **Import assets** — `timeout 60 godot --headless --import 2>&1`. Ensures all assets (`.glb`, `.png`, etc.) are imported before scene builders reference them.
12. **Build scene stubs** — for each new/changed scene, write a scene builder script to `scenes/BuildXxx.cs`, then run in dependency order (leaf scenes first): `timeout 60 godot --headless --script scenes/BuildXxx.cs`
13. **Verify** — `timeout 60 godot --headless --quit 2>&1`. No `ERROR` lines. RID warnings are benign.
14. **Git commit** — repo is already initialized before Claude Code starts:
    ```bash
    git add -A && git commit -m "scaffold: project skeleton"
    ```

## Output Files

### 1. `project.godot`

```ini
; Engine configuration file
; Do not edit manually

[application]

config/name="{ProjectName}"
run/main_scene="res://scenes/main.tscn"

[display]

window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"

[dotnet]

project/assembly_name="{ProjectName}"

[physics]

common/physics_ticks_per_second=120
common/physics_interpolation=true
; 3D only — omit for 2D projects:
3d/physics_engine="Jolt Physics"

[rendering]

; 3D games:
lights_and_shadows/directional_shadow/soft_shadow_filter_quality=3
anti_aliasing/quality/msaa_3d=2
; 2D pixel art (instead of above):
; textures/canvas_textures/default_texture_filter=0
; 2d/snap/snap_2d_transforms_to_pixel=true

[layer_names]

; Name collision layers used by the game:
2d_physics/layer_1="player"
2d_physics/layer_2="enemies"
; (add as needed)

[autoload]

; Singletons — C# scripts:
; GameManager="*res://scripts/GameManager.cs"

[input]

move_forward={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119)]
}
```

Key physical keycodes: W=87, A=65, S=83, D=68, Up=4194320, Down=4194322, Left=4194319, Right=4194321, Space=32, Enter=4194309, Escape=4194305, Shift=4194325, Ctrl=4194326, Alt=4194328.

Mouse buttons use InputEventMouseButton with button_index (1=left, 2=right) and matching button_mask:
```ini
fire={
"deadzone": 0.2,
"events": [Object(InputEventMouseButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"button_mask":1,"position":Vector2(0,0),"global_position":Vector2(0,0),"factor":1.0,"button_index":1,"canceled":false,"pressed":true,"double_click":false)]
}
```

### 2. `.csproj`

```xml
<Project Sdk="Godot.NET.Sdk/4.4.0">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <EnableDynamicLoading>true</EnableDynamicLoading>
  </PropertyGroup>
</Project>
```

The file must be named `{ProjectName}.csproj` matching the `assembly_name` in project.godot.

### 3. `STRUCTURE.md`

Complete architecture reference. Always written in full, even for incremental updates.

````markdown
# {Project Name}

## Dimension: {2D or 3D}

## Input Actions

| Action | Keys |
|--------|------|
| move_forward | W, Up |
| jump | Space |

## Scenes

### Main
- **File:** res://scenes/main.tscn
- **Root type:** Node3D
- **Children:** Player, Enemy

### Player
- **File:** res://scenes/player.tscn
- **Root type:** CharacterBody3D

## Scripts

### PlayerController
- **File:** res://scripts/PlayerController.cs
- **Extends:** CharacterBody3D
- **Attaches to:** Player:Player
- **Signals emitted:** Died, Scored
- **Signals received:** HurtBox.AreaEntered -> OnHurtEntered
- **Instantiates:** Bullet

## Signal Map

- Player:HurtBox.AreaEntered -> PlayerController.OnHurtEntered
- Main:GoalArea.BodyEntered -> LevelManager.OnGoalReached

## Asset Hints

- Player character model (~1.8m tall humanoid)
- Ground texture (tileable grass, 2m repeat)
- Sky panorama (360° daytime sky)
````

Architecture graph plus asset hints for the asset planner. No descriptions, no requirements, no task ordering.

### 4. `.gitignore`

Assets, tools, and build artifacts stay out of git:
```
.claude
CLAUDE.md
assets
screenshots
.godot
*.import
bin/
obj/
```

### 4b. `screenshots/.gdignore`

Create `screenshots/` with an empty `.gdignore` so Godot's importer skips screenshot PNGs (they're not game textures):
```bash
mkdir -p screenshots && touch screenshots/.gdignore
```

Do NOT create `.gdignore` in `assets/` or any subdirectory of it — Godot must import those files. `.gdignore` makes the importer skip the entire directory silently.

### 5. Script stubs: `scripts/*.cs`

```csharp
using Godot;

/// res://scripts/PlayerController.cs
public partial class PlayerController : CharacterBody3D
{
    [Signal] public delegate void DiedEventHandler();
    [Signal] public delegate void ScoredEventHandler();

    [Export] public float Speed = 7.0f;
    [Export] public float JumpVelocity = -4.5f;

    public override void _Ready()
    {
    }

    public override void _PhysicsProcess(double delta)
    {
    }

    private void OnHurtEntered(Area3D area)
    {
    }
}
```

Correct base class, signal delegate declarations, `[Export]` defaults, empty lifecycle and handler methods. All classes `partial`.

### 6. `scenes/SceneBuilderBase.cs`

Create once — all builders inherit from this. See `scene-generation.md` for the full base class.

### 7. Scene builder stubs: `scenes/Build*.cs`

Write each scene builder using this template — replace all UPPER_CASE placeholders with concrete values, delete optional blocks (SCRIPT, CHILDREN) that don't apply:

```csharp
using Godot;

/// Scene builder — run: dotnet build && timeout 60 godot --headless --script scenes/Build<Name>.cs
public partial class Build<Name> : SceneBuilderBase
{
    public override void _Initialize()
    {
        var temp = new Node();
        var root = new ROOT_TYPE();         // REPLACE ROOT_TYPE — e.g. CharacterBody3D
        root.Name = "ROOT_NAME";            // REPLACE ROOT_NAME — e.g. "Player"
        temp.AddChild(root);

        // CHILDREN — delete block if none, duplicate per child
        var childVar = GD.Load<PackedScene>("CHILD_PATH").Instantiate();  // REPLACE CHILD_PATH
        childVar.Name = "CHILD_NAME";       // REPLACE CHILD_NAME
        root.AddChild(childVar);

        // SCRIPTS — set LAST (SetScript disposes C# wrapper — see quirks.md)
        root.SetScript(GD.Load("SCRIPT_PATH"));  // REPLACE — e.g. "res://scripts/PlayerController.cs"

        // Re-obtain root (old wrapper is disposed)
        var rootNode = temp.GetChild(0);
        temp.RemoveChild(rootNode);
        temp.Free();

        PackAndSave(rootNode, "OUTPUT_PATH");  // REPLACE — e.g. "res://scenes/player.tscn"
    }
}
```

**CRITICAL: Build order is specified in STRUCTURE.md.** The `## Build Order` section lists the exact sequence. Follow it mechanically — do not infer or reorder.

## UI Overlay Architecture

For HUD/menus, add to the main scene:

```
Main (Node3D or Node2D)
├── ... game nodes ...
└── CanvasLayer (layer=1)
    └── Control (anchors_preset=15, full rect)
        ├── VBoxContainer or HBoxContainer
        │   ├── Label (score)
        │   ├── ProgressBar (health)
        │   └── Button (pause)
        └── ...
```

**Layout containers:**
- `VBoxContainer` — vertical stack; `HBoxContainer` — horizontal
- `GridContainer` — grid (set `Columns` property)
- `MarginContainer` — padding; `CenterContainer` — centering; `PanelContainer` — with background
- `SizeFlagsHorizontal/Vertical = SizeFlags.ExpandFill`
- `CustomMinimumSize` for fixed dimensions

For pause menus, set `ProcessMode = ProcessModeEnum.Always` on the CanvasLayer so it runs during pause.

## Architecture Rules

1. **Explicit 2D or 3D** — never mix dimensions in the same hierarchy.
2. **Declare all input actions** — anything used by scripts must appear in input table and project.godot.
3. **Signal contracts** — if script A emits signal X, receivers must list it in the signal map.

## Common Built-in Signals

- Area2D/3D — BodyEntered, BodyExited, AreaEntered, AreaExited
- Button — Pressed
- Timer — Timeout
- AnimationPlayer — AnimationFinished
- RigidBody2D/3D — BodyEntered (ContactMonitor required)

## Common Errors

- **`CS0260: Missing partial modifier`** — all Godot C# classes MUST be declared `partial`. Add `partial` keyword.
- **`dotnet build` fails** — must run before `godot --headless --script`. Scene builders and runtime scripts compile together.
- **`GD.Load()` returns null** — asset not imported yet. Run `godot --headless --import` first.
- **Scene builder hangs** — missing `Quit()` call. The template includes `Quit(0)` — never remove it.
- **Signal delegate wrong name** — must end in `EventHandler`. `[Signal] public delegate void Died();` fails silently; use `DiedEventHandler`.

## Asset Hints in STRUCTURE.md

Assets are generated AFTER scaffold. Include an `## Asset Hints` section at the end of STRUCTURE.md listing what visual assets the architecture needs. The asset planner uses these to decide what to generate.

```markdown
## Asset Hints

- Player character model (~1.8m tall humanoid)
- Ground texture (tileable grass, 2m repeat)
- Sky panorama (360° daytime sky)
- Enemy model (~1m tall creature)
```

Be specific about type (model, texture, background, sprite), approximate size, and visual role. Don't describe style — the asset planner chooses that.

### Build Order

The scaffold emits an explicit build order in STRUCTURE.md based on scene dependency analysis. Leaf scenes (no child scene references) first, parents after:

```markdown
## Build Order
1. dotnet build
2. scenes/BuildPlayer.cs → scenes/player.tscn
3. scenes/BuildEnemy.cs → scenes/enemy.tscn
4. scenes/BuildMain.cs → scenes/main.tscn (depends: player.tscn, enemy.tscn)
```

`dotnet build` is always step 1. The task executor follows this order mechanically. Do not rely on the executor to infer dependencies.

## What NOT to Include

- Implementation details or behavior descriptions
- Task ordering
- Lighting, environment, tonemapping, post-processing
- Any logic beyond empty method stubs — real scripts are written in a later stage
