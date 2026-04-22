# Bevy Scene Generation

Build Bevy scenes directly in Rust with ECS spawning. The default path is code-first world construction inside ordinary plugins and systems, not serialized scene files or editor-authored scene assets.

## Default Path

- Own initial scene setup in `OnEnter(AppState::Playing)` or the equivalent state that should create the world.
- Spawn explicit roots for the world, scene camera, lights, and overlay UI.
- Mark each scene-owned root with `DespawnOnExit(state)` so teardown is deterministic.
- Extract repeated scene fragments into helper functions instead of one giant setup system.
- Use parent-child hierarchies only where local transforms matter: camera rigs, prop clusters, stacked crates, archways, imported asset groups.
- Keep `SceneRoot(...)` for imported authored assets such as GLTF scenes. Do not use it as the default way to describe generated game layout.

## Workflow

1. Read `scaffold.md` and the current `STRUCTURE.md`.
2. Decide which runtime state owns the initial world. If the project has no state yet, add one instead of putting scene setup into `src/lib.rs`.
3. Create or update `src/game/world.rs` as the scene-generation entrypoint.
4. Add `src/game/ui.rs` only if the scene needs a runtime overlay, HUD, or menu root.
5. Register the scene plugins from `src/game/mod.rs` and initialize the owning state there.
6. In `world.rs`, create the world from `OnEnter(state)`:
   - camera
   - lights
   - world root
   - repeated prop groups
   - optional scene-local animation/update systems gated by `run_if(in_state(state))`
7. Create shared mesh and material handles once during setup, then clone those handles into helper spawns.
8. Update `STRUCTURE.md` to name the scene-owning modules, state, and teardown contract.
9. Verify with formatting, build checks, and a launch smoke test.

## Required Output Shape

### `src/game/state.rs`

Use a real state type even for a single playable scene:

```rust
#[derive(Debug, Clone, Copy, Default, Eq, PartialEq, Hash, States)]
pub enum AppState {
    #[default]
    Playing,
}
```

This gives scene generation a deterministic owner and later lets menu/gameplay/capture work attach to the same contract.

### `src/game/world.rs`

Minimum shape:

```rust
pub struct WorldPlugin;

impl Plugin for WorldPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(AppState::Playing), spawn_world)
            .add_systems(Update, animate_scene.run_if(in_state(AppState::Playing)));
    }
}
```

Rules:

- `spawn_world` is the one-time constructor for the scene owned by that state.
- Put repeated prop layouts in helper functions such as `spawn_arena_wall`, `spawn_beacon`, `spawn_ui_panel`, or `spawn_enemy_group`.
- Scene-local update systems live next to setup systems in the same module unless they have clearly earned their own module.
- Use `AssetServer` for runtime-loaded assets and ordinary Bevy handles for meshes, materials, fonts, and scenes.

### `src/game/ui.rs`

Optional, but when present it should follow the same state-scoped pattern:

- spawn UI roots in `OnEnter(state)`
- use `DespawnOnExit(state)` on the UI root and UI camera
- keep gameplay scene setup and UI setup in separate plugins unless they are trivially small

For a 3D scene with Bevy UI on top, a reliable overlay camera pattern is:

```rust
commands.spawn((
    Camera2d,
    Camera {
        order: 1,
        clear_color: ClearColorConfig::None,
        ..default()
    },
    IsDefaultUiCamera,
));
```

This matches the local Bevy example `examples/camera/2d_on_ui.rs`.

## Hierarchy Rules

- Parent anchors that own visible children must include both `Transform` and `Visibility`.
- A transform-only parent will trigger `warning[B0004]` when children with propagated visibility are inserted.
- Use `(Transform::from_translation(...), Visibility::default())` for anchors like `WorldRoot`, prop groups, camera rigs, archways, crate stacks, and imported scene wrappers.
- If objects do not need shared local transforms, do not parent them just for organization. Spawn them as separate top-level entities.

If the first smoke test produces `B0004` warnings, check parent anchors first; they usually need `Visibility` in addition to `Transform`.

## Lighting

Bevy 0.18 splits ambient light into two types. `GlobalAmbientLight` is a `Resource`, auto-inserted by `LightPlugin`, and fills the whole scene. `AmbientLight` is a `Component` that lives on a camera entity and overrides the global value for that camera only (it carries `#[require(Camera)]`).

```rust
commands.insert_resource(GlobalAmbientLight {
    color: Color::WHITE,
    brightness: 200.0,
    ..default()
});
```

Raise `brightness` (candela per m²) rather than spawning filler point lights when a scene reads as too dark. Spawn a `DirectionalLight` or `PointLight` alongside it for shape and shadows. See `bevy/examples/3d/lighting.rs` for the canonical pattern.

## Imported Assets vs Generated Layout

- Generated layout stays code-first.
- Imported authored assets such as GLTF scenes can be attached as leaves inside that code-owned layout using `SceneRoot(handle)`.
- Keep ownership clear: the plugin and state own where imported assets are spawned, how they are transformed, and when they are torn down.

## 2D vs 3D

- 2D scenes use the same ownership pattern: state-scoped setup, explicit roots, helper spawns, deterministic teardown.
- The difference is the rendering primitives: `Camera2d`, sprites, `Mesh2d`, UI layout, and 2D transforms instead of `Camera3d`, `Mesh3d`, and lights.
- Do not split the workflow into separate 2D and 3D documents unless the repo proves that the differences are large enough to earn that complexity.

## Verification

- `cargo fmt`
- `cargo check`
- `cargo build`
- local desktop smoke test: `cargo run`
- headless interactive smoke test fallback: `xvfb-run timeout 10 ./target/debug/{package-name}`
- if you need screenshots or video, use the dedicated offscreen capture entrypoint from `capture.md` instead of the interactive binary

The smoke test only needs to prove that the app launches cleanly. Exit code `124` from `timeout` is acceptable once the window loop is running, but hierarchy warnings, missing asset errors, or camera/UI clear-order issues are not.

## Do Not Do This

- Do not invent serialized scene files as the default Bevy output.
- Do not hide scene construction inside `src/lib.rs`; keep app wiring and world construction separate.
- Do not attach visible children under parent anchors that lack `Visibility`.
- Do not collapse the whole scene into one unstructured setup function when repeated groups can be expressed as helpers.
