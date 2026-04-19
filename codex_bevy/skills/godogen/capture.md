# Capture

Headless screenshot and video capture for Bevy projects after the runtime loop is already proven.

## Default Capture Shape

- Use a dedicated capture entrypoint. Do not default to the interactive game binary for automated media output.
- Render the scene to an offscreen `RenderTarget::Image`, not the primary window.
- Run capture headless with `WindowPlugin { primary_window: None, exit_condition: DontExit }`, `WinitPlugin` disabled, and `ScheduleRunnerPlugin` as the app runner.
- Use `Screenshot::image(...)` plus `save_to_disk(...)` for the proven screenshot path.
- Gate capture until imported assets are loaded, then wait a short settle period before writing frames.
- Keep the workflow scene-agnostic. The same capture contract should work for 2D, 3D, UI-heavy, or mixed projects.

Do not make virtual-window capture the default just because it looks simpler. On Linux, the normal primary-window path can fail under headless X/Wayland setups even when the same app works on a real desktop display. The safer default for automated screenshots and video is a dedicated offscreen image target.

Headless Linux capture may fall back to a software Vulkan adapter such as `llvmpipe`. That is acceptable for short validation screenshots and clips if the media output is correct; it just makes the run slower.

## Screenshot First

Prove one still image before adding video:

1. Create the offscreen render target as a resource before the scene camera is spawned.
2. Point the main scene camera at that image target.
3. Run the normal scene graph in a non-interactive capture mode.
4. Spawn `Screenshot::image(render_target_handle)` and save the result to `.png`.
5. Exit only after the screenshot callback confirms the frame was captured.

Example command shape:

```bash
cargo run --bin {capture_bin} -- screenshot screenshots/{task}/still.png
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

`120` frames at `30` fps gives a 4 second clip. Increase frame count only after the short path is working.

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
