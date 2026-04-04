# Known Quirks

Engine-level gotchas discovered through building games. These are Godot bugs and non-obvious behaviors — not language tutorials.

- **`SetScript()` disposes the C# wrapper** — calling `SetScript()` on a node in a scene builder invalidates the C# managed wrapper. Any subsequent use of that variable throws `ObjectDisposedException`. Build the full node hierarchy first, call `SetScript()` last. For the root node, use a temp parent to re-obtain the reference after `SetScript()`:
  ```csharp
  var temp = new Node();
  var root = new Node2D();
  root.Name = "Main";
  temp.AddChild(root);
  // ... build entire hierarchy ...
  root.SetScript(GD.Load("res://scripts/GameManager.cs"));  // wrapper dies here
  var rootNode = temp.GetChild(0);  // re-obtain via temp parent
  temp.RemoveChild(rootNode);
  // now use rootNode for packing
  ```
- **RID leak errors on exit** — headless scene builders always produce these. Harmless; ignore them.
- **`AddToGroup()` in scene builders** — groups set at build-time persist in saved .tscn files.
- **MultiMeshInstance3D + GLBs** — does NOT render after pack+save (mesh resource reference lost during serialization). Use individual GLB instances instead.
- **`_Ready()` skipped in `_Initialize()`** — when running `--script`, `_Ready()` on instantiated scene nodes does NOT fire during `_Initialize()`. Call init methods manually after `Root.AddChild(node)`.
- **`_Process()` signature in SceneTree scripts** — must be `public override bool _Process(double delta)` (returns bool), not void.
- **Autoloads in SceneTree scripts** — cannot reference autoload singletons by name. Find them via `Root.GetChildren()` and match by `.Name`.
- **`Free()` vs `QueueFree()` in test harnesses** — `QueueFree()` leaves the node in `GetChildren()` until frame end, blocking name reuse. Use `Free()` when immediately replacing scenes.
- **Camera2D has no `Current` property** — use `MakeCurrent()`, and only after the node is in the scene tree.
- **`--write-movie` frame 0** — the first movie frame renders before `_Process()` runs. Camera position set in `_Process()` won't appear until frame 1. Pre-position the camera in `_Initialize()` (via `Position`/`RotationDegrees`, NOT `LookAt()`) or accept a junk frame 0.
- **Collision layer bitmask vs UI index** — `CollisionLayer` and `CollisionMask` are bitmasks in code, NOT UI layer numbers. UI Layer 1 = bitmask 1, Layer 2 = bitmask 2, Layer 3 = bitmask 4, Layer 4 = bitmask 8 (powers of 2). `CollisionLayer = 4` means UI Layer 3, NOT Layer 4.
- **GLB `MaterialOverride` doesn't serialize** — setting `MaterialOverride` on GLB-internal MeshInstance3D nodes does NOT persist in .tscn because `SetOwnerOnNewNodes()` skips GLB children (has `SceneFilePath`). Use procedural ArrayMesh when custom material is required.
- **Camera lerp from origin** — cameras using `Lerp()` in `_PhysicsProcess()` will visibly swoop from (0,0,0) on the first frame. Use an `_initialized` flag to snap position on the first frame, then lerp on subsequent frames.
- **Chase camera `Current` re-assertion** — game cameras that set `Current = true` in `_PhysicsProcess()` override the test harness camera every frame. Test harnesses must disable the game camera EVERY frame.
- **`CharacterBody3D.MotionModeEnum.Floating`** — also needed for 3D non-platformer movement (vehicles on slopes, snowboards). GROUNDED mode's `FloorStopOnSlope` fights slope movement.
- **Default collision mask misses non-default layers** — new bodies get `CollisionMask = 1`. If terrain/walls use layer 2+, player falls through with no error. Always set mask to include all layers the body should collide with.
- **Frame-rate dependent drag** — `speed *= (1f - drag)` per tick is exponential decay tied to tick rate. At 60Hz: `(1-0.04)^60 ~ 8.5%` remaining/sec. At 120Hz: `(1-0.04)^120 ~ 0.7%`. Use `speed *= Mathf.Exp(-rate * (float)delta)` for frame-rate independent damping.

- **BoxShape3D on trimesh** — snags on collision edges (Godot/Jolt bug). Use CapsuleShape3D for objects that slide across trimesh surfaces (vehicles, rolling objects).
- **`ResetPhysicsInterpolation()`** — call when teleporting or switching cameras to prevent visible interpolation glitch.
- **MultiMeshInstance3D `Mesh.Duplicate()`** — needed before freeing the source GLB instance, otherwise the mesh resource is garbage-collected.
- **MultiMeshInstance3D `CustomAabb`** — must cover the entire visible area. Without it, the MultiMesh gets frustum-culled when the camera moves to edges.
- **MultiMeshInstance3D materials** — has no `SetSurfaceOverrideMaterial()`. Use `MaterialOverride` on the GeometryInstance3D, or keep materials from the source mesh.
- **ProceduralSkyMaterial sun disc** — automatically uses DirectionalLight3D direction/color. Set `SkyMode = DirectionalLight3D.SkyModeEnum.LightAndSky` on the sun light, `SkyModeEnum.LightOnly` on fill lights — otherwise multiple sun discs appear.
- **2D collision shape sizing** — slightly smaller than tile (e.g., 48px in 64px grid) allows smooth cornering through 1-tile corridors. Without this, characters snag on corridor entrances.
- **Smooth yaw tracking 360 spin** — `Mathf.Lerp()` on raw angles causes 360-degree spin-arounds. Wrap angle difference to [-PI, PI] before lerping: `float diff = ((targetYaw - currentYaw + 3f * Mathf.Pi) % Mathf.Tau) - Mathf.Pi`.

- **Sibling signal timing in `_Ready()`** — `_Ready()` fires on children in tree order. If sibling A emits in its `_Ready()`, sibling B hasn't connected yet. Fix: after connecting, check if the emitter already has data and call the handler manually.

- **C# enum names — don't guess, look up** — LLM training data is mostly GDScript Godot content, so the model confidently generates plausible but wrong C# enum names (e.g., `BGModeEnum.Sky` instead of `BGMode.Sky`). Always use the `godot-api` skill to verify C# enum names.
- **`.gdignore` silently blocks imports** — a `.gdignore` in any directory makes Godot's importer skip it entirely. Never create one in `assets/` — only `screenshots/` should have it. If textures aren't importing, check for stray `.gdignore` files.

## Common Runtime Pitfalls

**Collision state changes in callbacks:**
- Changing collision shape `Disabled` inside `BodyEntered`/`BodyExited` triggers "Can't change state while flushing queries". Use `SetDeferred`:
  ```csharp
  shape.SetDeferred(CollisionShape3D.PropertyName.Disabled, true);
  ```

**Spawn immunity for revealed items:**
- Items spawned inside an active Area2D (e.g., power-up revealed by explosion) get `AreaEntered` immediately — destroyed same frame.
- Fix: track `_aliveTime` in `_Process()`, ignore `AreaEntered` for ~0.8s (longer than the triggering effect's lifetime).

**Pass-by-value types in functions:**
- `bool`, `int`, `float`, `Vector3`, `Aabb`, `Transform3D` etc. are value types — assigning to a parameter inside a method does NOT update the caller's variable. Use `ref`/`out` or return the modified value:
  ```csharp
  // WRONG — result never updates caller:
  void Collect(Node node, Aabb result) { result = result.Merge(childAabb); }
  // CORRECT:
  Aabb Collect(Node node, Aabb result) { return result.Merge(childAabb); }
  ```

**UV tiling double-scaling:**
- Do NOT use world-space UV coords AND `Uv1Scale` together — causes extreme Moire. Pick one: world-space UVs with `Uv1Scale = Vector3.One`, OR normalized UVs with `Uv1Scale = new Vector3(tiles, tiles, 1)`.

**Material visibility in forward_plus:**
- `StandardMaterial3D` with `NoDepthTest = true` + transparency alpha = invisible. Use opaque + unshaded for overlays.
- Z-fighting between layered surfaces (road on terrain): offset 0.15-0.30m vertically + `RenderPriority = 1`.
- `CullMode = BaseMaterial3D.CullModeEnum.Disabled` as safety net on all procedural meshes until winding is confirmed correct.

## Feedback Loop

Quirks are curated manually in this file (skill source repo). When the task executor discovers a workaround during a game build, it writes to `MEMORY.md` (project-level). The skill maintainer periodically reviews `MEMORY.md` entries across projects and promotes recurring patterns here. This is a manual curation step — do not modify this file from within a game project.
