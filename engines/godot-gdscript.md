# Godot engine guide (GDScript)

Stack: **Godot 4**, **GDScript**, statically typed. Any Godot 4 build runs it — the standard build or the .NET one.

## Project shape

- `project.godot` — config, input actions, display, physics. **Match `config_version` to the installed toolchain** (`godot --version`) — don't hardcode it from memory; on an existing project preserve it. For 3D, set `3d/physics_engine="Jolt Physics"` and a fixed `physics_ticks_per_second`.
- `scripts/*.gd` runtime behavior · `scenes/*.tscn` scenes · `assets/` **only** files the running game loads (keep generation inputs/refs outside it).
- Build gate: `godot --headless --import` after asset changes and after adding or renaming a `class_name` (other scripts can't resolve it until then), then `godot --headless --check-only --script <file>.gd` on each changed script (exit 1 on parse and type errors), then `godot --headless --quit` (RID/ObjectDB-leak errors on headless exit are benign).

The user watches by running the project themselves (`godot --path .` or the editor) — keep it importing cleanly so each run reflects current state.

## Types are the only compile step

The parser checks what it can type; untyped code fails at runtime, and only on the path that runs. Type every declaration and signature. `:=` rejects values the parser can't type — calls on an untyped receiver (`load(...).instantiate()`), `abs`/`clamp`/`lerp`/`min`/`max`, reads from untyped arrays and dictionaries — so annotate the type (`var s: PackedScene = load(...)`) or use the typed variants (`absf`, `clampf`, `lerpf`, `maxi`, ...).

A runtime `SCRIPT ERROR` aborts only the function it's in: the game keeps running and the exit code stays 0. Gate headless runs on the log — grep it for `SCRIPT ERROR`.

## Scenes are generated at build time, not by hand

Write scenes as **`extends SceneTree` scripts** that build in `_initialize()`, run once headless, and emit a `.tscn`: `godot --headless --script scenes/build_x.gd`. A builder builds the node hierarchy, sets properties, attaches scripts, packs, and `quit()`s — it contains **no** runtime logic (no `_ready`/`_process`, signal connections, or game state). Build **leaf scenes first**, parents after, and `load()` them — a `preload()` of a scene that isn't generated yet is a parse error.

The serialization rules below are silent-failure — they pass the parser and drop nodes, values, or bloat files only in the saved `.tscn`:

- **Owner chain:** every node must have `owner` set to the scene root or it won't serialize. After building, walk the tree and set `child.owner = root` on all descendants — but **do not recurse into instantiated GLB/`.tscn` nodes** (those have a non-empty `scene_file_path`). Recursing into a GLB inlines all its meshes as text → 100MB+ `.tscn`.
- **Validate the pack:** count nodes before packing, `instantiate()` the `PackedScene` after, and compare counts; gate `ResourceSaver.save()` on the match. A silent drop otherwise looks like success.
- **Attach a script before setting its properties.** `set()` of an `@export` the node doesn't have yet is dropped without a warning — `set_script()` first, then assign.
- **Builder nodes are outside the tree.** `look_at()` and `global_*` log an error and the builder carries on — `look_at()` leaves the rotation unchanged, `global_position` lands as a local offset. Set local transforms; `Transform3D.looking_at()` composes a facing.

Sketch of the shared save path:

```gdscript
func pack_and_save(root: Node, path: String) -> void:
	set_owner_recursive(root, root)               # skip nodes with scene_file_path set
	var expected := count_nodes(root)
	var packed := PackedScene.new()
	if packed.pack(root) != OK:
		quit(1); return
	var test := packed.instantiate()
	var got := count_nodes(test)
	test.free()
	if got < expected:
		push_error("nodes dropped"); quit(1); return   # serialization failed silently
	ResourceSaver.save(packed, path)
	quit(0)
```

GLB models: instantiate the `PackedScene`, measure the `MeshInstance3D` AABB to scale, and use a **primitive** collision shape (Box/Sphere/Capsule) from the AABB — never `create_trimesh_shape()`/`create_convex_shape()` on imported meshes (drops to <1 FPS).

## Quirks worth knowing (silent-failure)

Most Godot behavior the model already knows; these few fail with no error:

- **On macOS a fatal error hangs instead of exiting.** Godot reports it in an `NSAlert` modal that `--headless` can't dismiss, so the process idles at 0% CPU forever (a missing main scene does it too). Run every `godot` call under `timeout`; exit 124 is the failure.
- **`SurfaceTool.generate_normals()`** is required for a procedural mesh to *receive* shadows. Without it (or with `CULL_DISABLED` as a "safety net"), shadows silently vanish — fix winding instead.
- **MultiMeshInstance3D + GLB** loses the mesh on pack/save; use individual instances. `material_override` on GLB-internal nodes also won't serialize (owner is skipped) — use a procedural `ArrayMesh` when a custom material is needed.
- **Raycasts don't reliably hit `ConcavePolygonShape3D`** (trimesh) — use a shape query or sample terrain height analytically.
- **`.gdignore`** in a directory makes the importer skip it silently — only `screenshots/` should have one, never `assets/`.
- Frame-rate-independent damping: `speed *= exp(-rate * delta)`, not `speed *= (1 - drag)` per tick.

## Capture (proof video)

Hardware **Vulkan** (Metal on macOS) gives correct rendering and is required for video; software Vulkan (`llvmpipe`/`lavapipe`) can still do stills but skip video and report it. macOS has no `xvfb`, so capture runs in a real window there — adding `--headless` to `--write-movie` aborts (`Parameter "t" is null`).

Capture deterministically with Godot's movie writer from a dedicated capture `SceneTree` script under `test/`:

```bash
# under xvfb-run -a -s '-screen 0 1920x1080x24' on a headless Linux box; prefer the hardware Vulkan ICD
godot --headless --import
godot --write-movie screenshots/result/frame.png --fixed-fps 30 --quit-after 450 --script test/presentation.gd
ffmpeg -y -framerate 30 -pattern_type glob -i 'screenshots/result/frame*.png' \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart screenshots/result/video.mp4
```

`--fixed-fps` makes motion deterministic (450 frames @30fps = 15s). **Pre-position the camera** in the builder/`_initialize()` (the first movie frame renders before `_process`) — but `_ready()` of nodes added there runs after `_initialize()` returns and overwrites what it set on them. Autoloads are loaded, yet a `SceneTree` script can't name them — use `root.get_node("Name")`. Drive capture-time input from the script, not live keys. The clip must show the behavior progressing across the whole window — no dead time, no single looped frame.
