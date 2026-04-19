# Bevy Scaffold Generator

Design the Bevy project shell and produce a compilable baseline: `Cargo.toml`, `src/main.rs`, `src/lib.rs`, the root plugin/module stubs, `assets/`, `STRUCTURE.md`, and `.gitignore`. This defines what exists and how it connects, not gameplay behavior.

Use this for both fresh projects and scaffold-level refactors.

## Workflow

1. **Check the local Rust toolchain first** — run `cargo --version` and `rustc --version` before touching `Cargo.toml`. Record the versions in `MEMORY.md` if the project is long-running.
2. **Match one Bevy version across the whole scaffold** — the current baseline is `bevy = "0.18.1"`. On an existing project, preserve the current Bevy version and feature selection unless the user explicitly asked for a Bevy migration.
3. **Read the input brief and `reference.png` if present** — use them to decide the initial runtime shape (`2D`, `3D`, or UI-first), window defaults, and module boundaries. Do not write gameplay or world-construction systems yet.
4. **Assess project state:**
   - No Cargo package -> create the project from scratch.
   - Existing Cargo package, fresh start requested -> replace scaffold-owned files (`Cargo.toml`, `src/main.rs`, `src/lib.rs`, root plugin modules, `STRUCTURE.md`, `.gitignore`) while preserving assets unless the user asked to remove them.
   - Existing Cargo package, incremental change -> read the current `Cargo.toml`, `STRUCTURE.md`, and relevant `src/` modules first. Preserve package name, edition, lockfile, Bevy version, and crate layout unless the task is explicitly restructuring them.
   - Existing workspace or multi-crate setup -> preserve it. Do not collapse it into the default single-package scaffold.
5. **Keep the baseline contract simple** — default to one Cargo package, a thin binary entrypoint, `src/lib.rs` owning `App` construction, one root plugin module under `src/game/`, an `assets/` directory, and `STRUCTURE.md` as the architecture source of truth.
6. **Create the package shell without creating a nested git repo** — for a fresh project in an empty target directory, run `cargo new --bin --vcs none {package_name}` from the parent directory. If the repo root itself is already the target game directory, write the files manually instead of letting Cargo create another folder.
7. **Write or update `Cargo.toml` directly** — do not assume `cargo add` is installed. Pin Bevy to `0.18.1` on fresh projects and include Bevy's recommended dev-profile optimization settings.
8. **Write or update `src/main.rs`** — keep it to a single call into the library entrypoint. If the package name contains `-`, convert it to `_` in the crate path.
9. **Write or update `src/lib.rs`** — construct the Bevy `App`, configure the primary window, add `DefaultPlugins`, and register the root game plugin.
10. **Write or update `src/game/mod.rs`** — define the root `GamePlugin`. This file wires future game modules together; scene generation owns entity spawning and world setup later.
11. **Create `assets/` if missing** — only runtime-loaded assets belong there. Keep reference images, notes, captures, and debug-only files outside `assets/`.
12. **Write `STRUCTURE.md` in full** — never as a diff. It is the contract the later stages work from.
13. **Write `.gitignore`** — keep build artifacts and generated screenshots out of git. Keep `Cargo.lock` tracked for applications.
14. **Format and verify the scaffold:**
    - `cargo fmt`
    - `cargo check`
    - `cargo build`
    - Launch smoke test:
      - local desktop -> `cargo run`
      - headless workstation or CI -> `timeout 10 xvfb-run ./target/debug/{package-name}`
      - screenshot/video automation -> add a dedicated offscreen capture binary later; do not reuse the interactive window path as the media pipeline
    The headless smoke test only needs to prove that the app launches without immediate runtime errors. A timeout after the window loop starts is acceptable.
15. **Git commit** — repo is already initialized before Claude starts:
    ```bash
    git add -A && git commit -m "scaffold: bevy project skeleton"
    ```

## Baseline Contract

- Start with one Cargo package. Do not create a workspace until the project has earned one.
- Keep `src/main.rs` stable and tiny.
- Put app wiring in `src/lib.rs` so future modules, tests, and tools can reuse the same entrypoint.
- Keep one root plugin module under `src/game/` as the integration point for later feature plugins.
- Create `assets/` up front so later asset planning and loading have a deterministic root.
- Treat `STRUCTURE.md` as the complete architecture reference, not a task log.

## Output Files

### 1. `Cargo.toml`

```toml
[package]
name = "{package-name}"
version = "0.1.0"
edition = "2024"

[dependencies]
bevy = "0.18.1"

[profile.dev]
opt-level = 1

[profile.dev.package."*"]
opt-level = 3
```

Rules:

- Fresh project -> write the manifest directly with `bevy = "0.18.1"`.
- Existing project -> preserve package name, edition, existing features, and Bevy version unless the user asked to migrate them.
- Keep `Cargo.lock` committed. This is an application scaffold, not a published library.

### 2. `src/main.rs`

```rust
fn main() {
    {crate_name}::run();
}
```

`{crate_name}` is the package name with `-` converted to `_`.

### 3. `src/lib.rs`

```rust
use bevy::{
    prelude::*,
    window::{PresentMode, Window, WindowPlugin},
};

mod game;

pub fn run() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "{Project Name}".into(),
                resolution: (1280, 720).into(),
                present_mode: PresentMode::AutoVsync,
                ..default()
            }),
            ..default()
        }))
        .add_plugins(game::GamePlugin)
        .run();
}
```

Rules:

- `src/lib.rs` owns top-level app wiring.
- Set the primary window title to the project name.
- Use one root plugin registration point here. Do not spread top-level `App` construction across multiple files during scaffold.

### 4. `src/game/mod.rs`

```rust
use bevy::prelude::*;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, _app: &mut App) {
        // Scene generation fills this in later.
    }
}
```

Rules:

- This is the integration point for later feature plugins and module registration.
- Keep it compile-clean even before any gameplay code exists.
- Do not spawn the world here yet unless the user explicitly asked for more than scaffold work.

### 5. `STRUCTURE.md`

Write the full architecture contract every time. Start with this shape:

````markdown
# {Project Name}

## Runtime

- Bevy 0.18.1
- Package: {package-name}
- Dimension: {2D | 3D | UI-first}

## App Entry

- `src/main.rs` -> `{crate_name}::run()`
- `src/lib.rs` -> builds `App`, configures the primary window, registers `GamePlugin`

## Plugins

### GamePlugin
- **File:** `src/game/mod.rs`
- **Owns:** top-level plugin registration
- **Will register:** {world, ui, audio, gameplay, states}

## Modules

### world
- **Planned file(s):** `src/game/world.rs` or `src/game/world/mod.rs`
- **Role:** world construction and scene setup

### ui
- **Planned file(s):** `src/game/ui.rs` or `src/game/ui/mod.rs`
- **Role:** menus, HUD, overlays

## State / Resources

- `AppState` -> {Boot, Menu, Playing, Paused}
- `GameConfig` resource -> shared runtime configuration

## Assets

- Runtime root: `assets/`
- Planned asset groups: {audio, fonts, models, shaders, textures}

## Verification

- `cargo fmt`
- `cargo check`
- `cargo build`
- `cargo run`
````

Keep this file structural. No task ordering, no speculative implementation notes, no hidden TODO list.

### 6. `.gitignore`

```gitignore
/target
/screenshots
```

Rules:

- Ignore build output.
- Ignore generated screenshots and capture artifacts.
- Do not ignore `Cargo.lock`.

## Runtime vs Reference Files

`assets/` is the runtime asset root that Bevy loads from. Keep it clean:

- Runtime-loaded files stay in `assets/`.
- Reference images such as `reference.png` stay at repo root or under a sibling like `refs/`.
- Debug captures, notes, and temporary analysis outputs stay outside `assets/`.

Mixing those categories makes asset planning and loading ambiguous.
