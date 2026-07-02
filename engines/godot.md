# Godot engine guide

Stack: **Godot 4 (.NET / Mono build)**, **C#**. All Godot C# classes must be `partial`.

## Project shape

- `project.godot` — config, input actions, display, physics. **Match version-sensitive fields to the installed toolchain** (`config_version`, and in `.csproj` the `Godot.NET.Sdk/...` version + `TargetFramework`) — run `godot --version` / `dotnet --version` and don't hardcode values from memory; on an existing project preserve them. For 3D, set `3d/physics_engine="Jolt Physics"` and a fixed `physics_ticks_per_second`.
- `{ProjectName}.csproj` — name must match `assembly_name`; `<EnableDynamicLoading>true</EnableDynamicLoading>`.
- `scripts/*.cs` runtime behavior · `scenes/*.tscn` scenes · `assets/` **only** files the running game loads (keep generation inputs/refs outside it).
- Build gate: `dotnet build`, then `godot --headless --import` after asset changes, then `godot --headless --quit` (RID-leak warnings on headless exit are benign).

The user watches by running the project themselves (`godot --path .` or the editor) — keep it building and importing cleanly so each run reflects current state.

## Scenes are generated at build time, not by hand

Write scenes as **C# `SceneTree` scripts** that run once headless and emit a `.tscn`: `godot --headless --script scenes/BuildX.cs`. A builder builds the node hierarchy, sets properties, attaches scripts, packs, and `Quit()`s — it contains **no** runtime logic (no `_Ready`/`_Process`, signals, or game state). Build **leaf scenes first**, parents after.

The serialization rules below are silent-failure — they pass compilation and drop nodes or bloat files only in the saved `.tscn`:

- **Owner chain:** every node must have `Owner` set to the scene root or it won't serialize. After building, walk the tree and set `child.Owner = root` on all descendants — but **do not recurse into instantiated GLB/`.tscn` nodes** (those have a non-empty `SceneFilePath`). Recursing into a GLB inlines all its meshes as text → 100MB+ `.tscn`.
- **Validate the pack:** count nodes before packing, `Instantiate()` the `PackedScene` after, and compare counts; gate `ResourceSaver.Save()` on the match. A silent drop otherwise looks like success.
- **`SetScript()` disposes the C# wrapper** — set scripts *last*, after the hierarchy is built. For the root, add it under a temp `Node`, set the script, then re-fetch it via `temp.GetChild(0)` before packing.

Sketch of the shared save path:

```csharp
void PackAndSave(Node root, string path) {
    SetOwnerRecursive(root, root);               // skip nodes with SceneFilePath set
    int expected = CountNodes(root);
    var packed = new PackedScene();
    if (packed.Pack(root) != Error.Ok) { Quit(1); return; }
    var test = packed.Instantiate(); int got = CountNodes(test); test.Free();
    if (got < expected) { GD.PushError("nodes dropped"); Quit(1); return; }   // serialization failed silently
    ResourceSaver.Save(packed, path);
    Quit(0);
}
```

GLB models: instantiate the `PackedScene`, measure the `MeshInstance3D` AABB to scale, and use a **primitive** collision shape (Box/Sphere/Capsule) from the AABB — never `CreateTrimeshShape()`/`CreateConvexShape()` on imported meshes (drops to <1 FPS).

## Quirks worth knowing (silent-failure)

Most Godot behavior the model already knows; these few fail with no error:

- **`ArrayMesh.GenerateNormals()`** is required for a procedural mesh to *receive* shadows. Without it (or with `CullMode.Disabled` as a "safety net"), shadows silently vanish — fix winding instead.
- **MultiMeshInstance3D + GLB** loses the mesh on pack/save; use individual instances. `MaterialOverride` on GLB-internal nodes also won't serialize (owner is skipped) — use a procedural `ArrayMesh` when a custom material is needed.
- **Raycasts don't reliably hit `ConcavePolygonShape3D`** (trimesh) — use a shape query or sample terrain height analytically.
- **`.gdignore`** in a directory makes the importer skip it silently — only `screenshots/` should have one, never `assets/`.
- **C# enum names:** training data is GDScript-biased, so guessed C# enum names are often wrong (`BGMode.Sky`, not `BGModeEnum.Sky`). Verify against the installed Godot — read the C# API in the Godot docs/assemblies rather than guessing.
- Frame-rate-independent damping: `speed *= Mathf.Exp(-rate * delta)`, not `speed *= (1 - drag)` per tick.

## Capture (proof video)

Hardware **Vulkan** gives correct rendering and is required for video; software Vulkan (`llvmpipe`/`lavapipe`) can still do stills but skip video and report it.

Capture deterministically with Godot's movie writer from a dedicated capture `SceneTree` script under `test/`:

```bash
# under xvfb-run -a -s '-screen 0 1920x1080x24' on a headless Linux box; prefer the hardware Vulkan ICD
godot --headless --import
godot --write-movie screenshots/result/frame.png --fixed-fps 30 --quit-after 450 --script test/Presentation.cs
ffmpeg -y -framerate 30 -pattern_type glob -i 'screenshots/result/frame*.png' \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart screenshots/result/video.mp4
```

`--fixed-fps` makes motion deterministic (450 frames @30fps = 15s). **Pre-position the camera** in the builder/`_Initialize` (the first movie frame renders before `_Process`). Drive capture-time input from the script, not live keys. The clip must show the behavior progressing across the whole window — no dead time, no single looped frame.
