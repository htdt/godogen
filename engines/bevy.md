# Bevy engine guide

Stack: **current stable Bevy**, Rust (edition 2024). Run `cargo add bevy` to resolve the latest stable release (skip any `-rc` prerelease), pin the exact version it writes, and keep every `bevy_*` crate on that same minor — mismatched minors pull two copies of bevy into the dependency tree and their types stop unifying.

> Whatever minor you land on is likely newer than this model's training data, so APIs may have changed under you. **Verify shapes against the installed version** rather than from memory: read the source under `~/.cargo/registry/src/.../bevy-*`, run `cargo doc --open`, or grep the crate. When a runtime log names a missing feature or a moved item, trust it over recollection.

## Project shape

One Cargo package: a tiny `src/main.rs` calling into `src/lib.rs` (which builds the `App`, sets the primary window, adds `DefaultPlugins`, registers a root `GamePlugin`), feature plugins under `src/game/`, and `assets/` for runtime-loaded files only (keep refs/captures out of it). Include dev-profile opt settings so iteration isn't glacial:

```toml
[dependencies]
bevy = "x.y.z"           # the exact version cargo add resolved; add features as needed, e.g. features = ["jpeg"] for jpg glTF textures
[profile.dev]
opt-level = 1
[profile.dev.package."*"]
opt-level = 3
```

Build gate: `cargo fmt` · `cargo check` · `cargo build`. Construct the world from systems run `OnEnter(state)` (spawn a world root, camera, lights, UI), mark entities for teardown on state exit, and keep `src/lib.rs` as the single `App`-wiring point.

The user watches by running the project themselves (`cargo run`) — keep it compiling and launching cleanly.

## Verify against the installed version

A few things that have bitten real builds and won't error at compile time — check them if they bite:

- glTF scenes only load texture formats enabled in the manifest — `.jpg` textures load white until `features = ["jpeg"]` is set (the log says `feature "jpeg" is not enabled`).
- UI box properties (`border_radius`, layout) live **inside** the `Node` component, not as separately spawned bundle items.
- Procedural meshes are back-face culled by default — terrain wound the wrong way renders invisible (looks like "broken generation"; it's index order). A transform anchor with visible children needs both `Transform` and `Visibility`.

## Capture (proof video)

Do **not** record the windowed binary — on headless Linux the primary-window path panics under virtual X even when it runs fine on a desktop. Use a **dedicated offscreen capture binary** (`src/bin/capture.rs`) in the same crate that reuses the real scene code but renders to a `RenderTarget::Image`:

- `DefaultPlugins` with `WindowPlugin { primary_window: None, exit_condition: DontExit }`, `WinitPlugin` disabled, and `ScheduleRunnerPlugin` as the runner.
- Allocate the target `Image` **directly in the world** (`world_mut().resource_mut::<Assets<Image>>()`) and publish its handle *before* the camera/`OnEnter` systems read it — adding it via `Commands` in `Startup` is deferred and yields black captures.
- Point the scene camera at `RenderTarget::Image(handle)`; capture with `Screenshot::image(handle).observe(save_to_disk(path))`. Saving is async — exit on a latched completion or an absolute finish tick recorded once, not `current_tick + delay`.
- Use `TimeUpdateStrategy::ManualDuration(1/30s)` so motion is deterministic across saved frames, and drive capture-time action from the script, not live input.
- Run it from the crate root (`cargo run --bin capture -- ...`) so `AssetServer` resolves `assets/` from the CWD. Quiet the logs with `RUST_LOG=warn` and a unique `[capture]` marker.

```bash
RESULT=screenshots/result/0
cargo run --bin capture -- frames "$RESULT" 450     # 450 frames @30fps = 15s
ffmpeg -y -framerate 30 -i "$RESULT/frame%05d.png" \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart "$RESULT/video.mp4"
```

Software Vulkan (`llvmpipe`) is acceptable for capture — just slower. The clip must show the behavior progressing across its full length: varied action, no dead time, no single looped frame.

Bevy's `headless_renderer` and `screenshot` examples show the exact offscreen-render and still-capture wiring — read them from the Bevy repo for the current API.
