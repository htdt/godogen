# Task Execution

Implementation workflow and debugging reference for real Bevy feature work after scaffold and scene generation are already in place.

## Planning Each Task

- Read `STRUCTURE.md`, the current `Cargo.toml`, the relevant game modules, `scene-generation.md`, and `quirks.md` before touching code.
- Use the `bevy-help` skill for any Bevy-related question, not just exact names when symbols are uncertain. Reach for it when designing a feature, choosing architecture, or asking "how do I add X?" such as snow particles.
- Decide the concrete scope up front: state owner, modules/files, runtime assets, verification commands, and stop conditions.
- Preserve the current Bevy version and feature set unless the task explicitly includes a manifest or engine migration.
- Keep the first pass narrow. Prove shape, scene ownership, and control flow with generated content or simple primitives before adding imported assets, new crates, or polish work.

## Bevy Help

- `bevy-help` is the main reference tool for Bevy work. Use it for feature design, architecture, ECS ownership, rendering and UI setup, particles, animation, asset-loading flows, scheduling choices, and exact symbol lookup.
- It has convenient access to the local rustdoc cache, the checked-out Bevy repo, official Bevy examples, and Learn docs for the installed release. That makes it the fastest way to find patterns that match the version the project actually uses.
- Prefer it early, before inventing an API shape from memory. The examples often show the right composition pattern even when the question starts as "how should this feature be designed?"

## Phases

### Risk Slice

If the task has one risky or unclear part, isolate it first:

1. Build the smallest implementation that exercises the risk.
2. Run the execution loop until the risky behavior is proven or disproven.
3. Carry only the validated pattern into the main build.

### Main Build

1. Lock scene ownership first: state, plugins, setup systems, and teardown.
2. Implement the next playable or visible vertical slice in code.
3. Add imported assets after the primitive pass is accepted or clearly required by the brief.
4. Keep iterating until build and runtime verification pass.

## Default Implementation Loop

1. Read `STRUCTURE.md`, the current manifest, and the modules you are about to change.
2. Keep app wiring stable. Adjust state, plugin, and module boundaries before filling in gameplay details.
3. Implement the next slice in code.
4. Run `cargo fmt`.
5. Run `cargo check`.
6. Fix compiler and Bevy API errors first. Do not pay for repeated full builds while `cargo check` is still red.
7. Run `cargo build` once the type check is clean.
8. Run a runtime smoke test:
   - local desktop: `cargo run`
   - no display or CI: retry the interactive smoke test with `timeout 10 xvfb-run ./target/debug/{package-name}`
   - screenshots or video needed: stop using the interactive binary and switch to the dedicated offscreen capture path in `capture.md`
9. Read runtime logs, not just the exit code. Missing assets, unsupported image formats, hierarchy warnings, and camera/UI ordering problems are real failures.
10. Update `STRUCTURE.md` if module ownership, state, asset contracts, or verification commands changed.
11. Repeat from step 3 until the task's stop conditions pass.

## Fresh Package Expectations

- The first `cargo check` on a new package may need network access to resolve dependencies and write `Cargo.lock`.
- The first full build is front-loaded and slow. Do not mistake initial compile cost for a broken workflow.
- After the lockfile exists and the dependency graph is built, follow-up `cargo check` iterations are usually much faster.

## Imported Asset Pass

- Treat imported assets as a second pass unless the brief requires them immediately.
- Keep the code-owned wrapper entity and placement logic even when the visible asset comes from `SceneRoot(...)`.
- When a GLTF or texture appears white, missing, or partially loaded, inspect runtime logs before rewriting spawn code.
- Check three things first:
  1. the file lives under `assets/`
  2. the load path matches Bevy's runtime-relative asset path
  3. `Cargo.toml` enables required Bevy image format features such as `jpeg` when imported assets reference `.jpg`
- Preserve existing manifest features on incremental tasks. Dropping a needed asset feature can break runtime loads without compile errors.

## Stop Conditions

- `cargo fmt` passes
- `cargo check` passes
- `cargo build` passes
- A runtime launch validation has been completed on a real display path
- `STRUCTURE.md` matches the code that shipped

If headless launch is blocked by host display or compositor problems but build and desktop runtime are clean, accept the desktop run as decisive and record the headless blocker instead of distorting the app around workstation-specific failures.

## Debugging Priorities

1. Red compiler errors and Bevy API mismatches.
2. Runtime asset-load errors and warnings.
3. Scene ownership mistakes: wrong state, missing `DespawnOnExit`, missing `Visibility` on parent anchors, wrong camera/UI setup.
4. Gameplay tuning and feel.

This ordering keeps the fastest objective blockers first. Compile issues and asset-loader failures should be resolved before spending time on tuning, presentation, or subjective feel.

## Do Not Do This

- Do not start by adding physics crates or extra dependencies when a tuned code-first pass can prove the mechanic.
- Do not skip `cargo check` and jump straight to repeated full builds.
- Do not rewrite scene structure to chase what is actually an asset-loader or manifest-feature problem.
- Do not treat a workstation-specific `xvfb` or compositor failure as proof that the Bevy code is wrong.
- Do not treat `xvfb-run` as the long-term media path. Use it to smoke-test the interactive binary only; use the dedicated offscreen capture entrypoint for screenshots and video.
- Do not leave `STRUCTURE.md` stale after the runtime shape changes.
