# Known Quirks

Engine-level and tooling-level gotchas discovered through real Bevy migration work. Keep this file small and high-signal.

- **Hierarchy anchors with visible children need `Visibility`** — a parent entity used only as a transform anchor can still trigger `warning[B0004]` if its children rely on propagated visibility and the parent lacks `Visibility`. Fix: if a parent owns visible children, spawn it with both `Transform` and `Visibility::default()`:
  ```rust
  commands.spawn((
      Name::new("WorldRoot"),
      Transform::default(),
      Visibility::default(),
  ));
  ```
  If the entity does not need shared local transforms, do not parent children under it just for organization.

- **Rounded Bevy UI corners belong on `Node`, not as a separate spawned component** — adding `BorderRadius::all(px(10))` as its own tuple item can fail because it is not a standalone bundle field in this shape. The working Bevy `0.18.1` pattern is to place it inside the `Node` itself:
  ```rust
  Node {
      border_radius: BorderRadius::all(px(10)),
      ..default()
  }
  ```
  Treat `border_radius`, layout, and other UI box properties as part of the `Node` component unless the current Bevy API says otherwise.

- **Imported GLTF scenes only load texture formats enabled in the Bevy manifest** — if a glTF scene references `.jpg` textures, the model can load white or fail to appear until the manifest enables Bevy's `jpeg` feature:
  ```toml
  bevy = { version = "0.18.1", features = ["jpeg"] }
  ```
  If runtime logs say `feature "jpeg" is not enabled` or show texture-loader failures, fix `Cargo.toml` before rewriting scene spawning or material code.

- **Do not default to primary-window capture for Linux headless Bevy runs** — the normal windowed app path can panic under virtual X with no usable present mode even when the same project runs fine on a real desktop display. If an interactive smoke test must run without a display, `xvfb-run` is an acceptable workaround. The stable media path is still to render to `RenderTarget::Image`, disable `WinitPlugin`, and run a dedicated offscreen capture entrypoint. If the goal is automated screenshots or video, build the capture flow around an image target first instead of trying to record the interactive window binary.

- **Capture logs get noisy fast unless you suppress engine chatter** — `cargo run --bin capture -- frames ...` can flood the terminal with renderer and asset logs, which hides the lines you actually care about. Prefer `RUST_LOG=warn`, redirect the full run to a temp log, and grep only a unique marker prefix such as `[capture]` that your capture binary emits for progress milestones.

## Feedback Loop

Quirks are curated manually in this source repo. Add only repeated, non-obvious issues that would have prevented real confusion in `bevy-api`, `scaffold`, `scene-generation`, `task-execution`, or `capture`.
