# Capture

Headless screenshot and video capture for Bevy projects after the runtime loop is already proven.

## Default Capture Shape

- Use a dedicated capture entrypoint. Do not default to the interactive game binary for automated media output.
- In a normal Cargo layout, that capture entrypoint is another Rust binary target such as `src/bin/capture.rs`, not a shell script or a separate project.
- Keep it in the same package and reuse the shared game/library code so capture runs the real scene with different app wiring.
- Prefer invoking that entrypoint with `cargo run --bin {capture_bin}` from the crate root unless the binary sets its asset root explicitly. Bevy resolves asset paths relative to the process CWD, so a bare `./target/debug/{capture_bin}` can break `AssetServer` lookups when launched from the wrong directory.
- Render the scene to an offscreen `RenderTarget::Image`, not the primary window.
- Run capture headless with `WindowPlugin { primary_window: None, exit_condition: DontExit }`, `WinitPlugin` disabled, and `ScheduleRunnerPlugin` as the app runner.
- Use `Screenshot::image(...)` plus `save_to_disk(...)` for the proven screenshot path.
- Gate capture until imported assets are loaded, then wait a short settle period before writing frames.
- Keep the workflow scene-agnostic. The same capture contract should work for 2D, 3D, UI-heavy, or mixed projects.

Do not make virtual-window capture the default just because it looks simpler. On Linux, the normal primary-window path can fail under headless X/Wayland setups even when the same app works on a real desktop display. The safer default for automated screenshots and video is a dedicated offscreen image target.

Headless Linux capture may fall back to a software Vulkan adapter such as `llvmpipe`. That is acceptable for short validation screenshots and clips if the media output is correct; it just makes the run slower.

Practical fallback order:

1. Prove the scene locally with `cargo run` when a real desktop display exists.
2. If an interactive smoke test must run without a display, try `xvfb-run` as a workstation workaround.
3. If the goal is screenshots or video, switch to the dedicated offscreen capture binary instead of trying to keep the interactive window path alive under virtual display plumbing.

## Minimum Wiring

Headless app skeleton for `src/bin/{capture_bin}.rs`. For the full patterns see `bevy/examples/window/screenshot.rs` (still image path) and `bevy/examples/app/headless_renderer.rs` (headless app runner and GPU readback).

```rust
use bevy::{
    app::ScheduleRunnerPlugin,
    camera::RenderTarget,
    image::TextureFormat,
    prelude::*,
    render::view::screenshot::{save_to_disk, Screenshot},
    time::TimeUpdateStrategy,
    window::ExitCondition,
    winit::WinitPlugin,
};
use std::time::Duration;

#[derive(Resource, Clone)]
struct CaptureTarget(Handle<Image>);

fn main() {
    let mut app = App::new();

    // Pre-allocate the render target before any system that reads its handle.
    // `new_target_texture` already sets TEXTURE_BINDING | COPY_DST | RENDER_ATTACHMENT.
    let image = Image::new_target_texture(1280, 720, TextureFormat::bevy_default(), None);
    let handle = app.world_mut().resource_mut::<Assets<Image>>().add(image);
    app.insert_resource(CaptureTarget(handle));

    app.add_plugins(
        DefaultPlugins
            .set(WindowPlugin {
                primary_window: None,
                exit_condition: ExitCondition::DontExit,
                ..default()
            })
            .disable::<WinitPlugin>(),
    )
    .add_plugins(ScheduleRunnerPlugin::run_loop(Duration::ZERO))
    .insert_resource(TimeUpdateStrategy::ManualDuration(Duration::from_secs_f32(
        1.0 / 30.0,
    )))
    .run();
}

// Scene camera renders into the target:
// commands.spawn((
//     Camera3d::default(),
//     Camera { target: RenderTarget::Image(target.0.clone().into()), ..default() },
// ));

// Single still, triggered once the scene has settled:
// commands.spawn(Screenshot::image(target.0.clone()))
//     .observe(save_to_disk("screenshots/still.png"));
```

`Screenshot::image(handle).observe(save_to_disk(path))` is the proven still path. For an N-frame sequence, trigger one `Screenshot::image` per tick against the same handle, numbering the output filenames; the observer writes each PNG when its readback lands.

## Screenshot First

Prove one still image before adding video:

1. Create the offscreen render target and publish its handle resource before the scene camera is spawned.
2. Point the main scene camera at that image target.
3. Run the normal scene graph in a non-interactive capture mode from the dedicated capture binary target.
4. Spawn `Screenshot::image(render_target_handle)` and save the result to `.png`.
5. Exit only after the screenshot callback confirms the frame was captured.

If startup or `OnEnter` systems read the capture target immediately, do not enqueue `Assets<Image>::add(...)` through `Commands` and assume the image exists right away. That write is deferred until commands are applied. Prefer creating the image directly in the world first, for example through `app.world_mut().resource_mut::<Assets<Image>>()`, then hand the stable handle to plugins and systems that consume it.

`Screenshot::image(...).observe(save_to_disk(...))` is asynchronous. Treat screenshot completion as a latched state transition, not as "the file exists on the same frame." If you need a few extra ticks before exit, record an absolute finish tick once and compare against that fixed value. Do not recompute `current_tick + delay` every update or the exit condition can slide forever.

Example command shape:

```bash
cargo run --bin {capture_bin} -- screenshot screenshots/{task}/still.png
```

If the binary prints its own progress markers, prefix them with something unique such as `[capture]` and keep the rest of the engine logs quiet:

```bash
_log=$(mktemp)
RUST_LOG=warn cargo run --bin {capture_bin} -- screenshot screenshots/{task}/still.png \
  >"$_log" 2>&1
rg '^\[capture\]' "$_log"
```

## Video Path

The proven video flow is: capture PNG frames first, then convert them with `ffmpeg`.

Reasons:

- It keeps the Bevy side simple and debuggable.
- A bad frame sequence is easy to inspect before encoding.
- `ffmpeg` handles H.264/MP4 packaging better than trying to encode in-engine.

Example command shape:

```bash
cargo run --bin {capture_bin} -- frames screenshots/{task}/frames 120
ffmpeg -y -framerate 30 -i screenshots/{task}/frames/frame_%05d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    screenshots/{task}/capture.mp4
```

For noisy capture runs, use the same temp-log pattern and only read the capture markers back into context:

```bash
_log=$(mktemp)
RUST_LOG=warn cargo run --bin {capture_bin} -- frames screenshots/{task}/frames 120 \
  >"$_log" 2>&1
rg '^\[capture\]' "$_log"
ffmpeg -y -framerate 30 -i screenshots/{task}/frames/frame_%05d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    screenshots/{task}/capture.mp4
```

`120` frames at `30` fps gives a 4 second clip. Increase frame count only after the short path is working.

## Final Result Bundle

The final deliverable is a proof bundle under `screenshots/result/{N}/`, where `{N}` is the next integer counter for this repo.

Required contents:

- `video.mp4` — encoded at exactly 30 fps and between 15s and 30s long. The verify gate hard-rejects bundles outside that window or at the wrong frame rate before it inspects frames.
- the raw `frameXXX.png` files used to encode that video, stored in the same folder
- `task_add.md` — optional; include only when the bundle proves a slice narrower than the root `task.md` (e.g. a single feature in isolation). Omit it when the bundle covers the full task.

The original task literal lives at `task.md` in the project root, written once. The verify gate reads it every run; do not duplicate it into the bundle.

The clip has to *prove the task* across its full duration:

- Show the implemented behavior progressing from start to finish, not in one fleeting moment.
- Vary what is on screen. A clip that loops the same idle pose, replays the same camera orbit, or sits on a single static frame for the whole window proves nothing and fails verification.
- No dead time. A few good seconds followed by a stuck entity, frozen camera, blank window, or broken state for the rest of the clip is a clear failure, not a partial pass. The verifier treats any sustained degenerate window as an overall fail.

Plan the capture so something task-relevant is happening across the whole clip — scripted action, varied camera, multiple entities exercised — instead of relying on one good moment.

Recommended command shape (30fps × 30s = 900 frames; for the 15s minimum use 450):

```bash
RESULT=screenshots/result/{N}
cargo run --bin {capture_bin} -- frames "$RESULT" 900
ffmpeg -y -framerate 30 -i "$RESULT/frame%05d.png" \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    "$RESULT/video.mp4"
```

The encoded MP4 must use the same fps as the captured frame sequence. If those disagree, the resulting motion proof is inaccurate.

## Time and Motion

- Do not let headless capture depend on real wall-clock frame time.
- Use `TimeUpdateStrategy::ManualDuration(...)` so gameplay motion stays deterministic while frames are being saved.
- Keep automated capture input separate from keyboard input. If the project normally expects live input, provide a deterministic capture-time control mode instead of trying to fake key presses.

## Validation Standard

- `cargo fmt`
- `cargo check`
- `cargo build`
- one headless screenshot command succeeds and writes a real `.png`
- one headless frame-sequence command succeeds and writes multiple distinct frames
- `ffmpeg` converts the validated frame sequence to `.mp4`

If the frame hashes are identical, do not assume the video path is done. That usually means the offscreen camera target or time stepping is wired incorrectly.
