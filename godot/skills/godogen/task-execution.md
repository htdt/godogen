# Task Execution

Implementation workflow and debugging reference for real Godot feature work after scaffold and scene generation are already in place.

## Planning Each Task

- Read `STRUCTURE.md`, `project.godot`, the `.csproj`, relevant scripts/scenes, `scene-generation.md`, `test-harness.md`, and `quirks.md` before touching code.
- Use the `godot-api` skill for Godot API and C# binding questions before inventing method names, enum names, or signal patterns from memory.
- Decide the concrete scope up front: scene ownership, scripts/files, runtime assets, verification commands, and stop conditions.
- Preserve the current Godot and .NET versions unless the task explicitly includes a toolchain migration.
- Keep the first pass narrow. Prove scene ownership, control flow, camera framing, and runtime state before adding imported assets or polish.

## Visual Verification

- Do not trust code alone. Look at screenshots, captured frames, and video after every visible change.
- When code and media disagree, trust the media.
- Bias toward failure. If the required behavior is not clearly visible, treat it as unfinished.
- Hidden or inferred behavior does not count. The visible result has to prove the requirement.

## Phases

### Risk Slice

If the task has one risky or unclear part, isolate it first:

1. Build the smallest scene or script path that exercises the risk.
2. Run the execution loop until the risky behavior is proven or disproven.
3. Carry only the validated pattern into the main build.

### Main Build

1. Lock scene ownership first: scene builders, script attachment, input actions, and runtime state.
2. Implement the next playable or visible vertical slice in code.
3. Add imported assets after the primitive pass is accepted or clearly required by the brief.
4. Keep iterating until build, runtime, and media verification pass.

## Default Implementation Loop

1. Read `STRUCTURE.md`, current project files, and the modules you are about to change.
2. Import changed assets with `timeout 60 godot --headless --import 2>&1`.
3. Generate or update scene builder C# files, then run them in the build order from `STRUCTURE.md`.
4. Write runtime `.cs` scripts.
5. Run `timeout 60 dotnet build 2>&1`.
6. Fix compiler and Godot API errors before running longer captures.
7. Validate the project with `timeout 60 godot --headless --quit 2>&1`.
8. Run a runtime smoke test:
   - local desktop: `godot --path .`
   - headless workstation or CI: use the capture wrapper from `capture.md`
   - screenshots or video needed: switch to the deterministic capture path in `capture.md`
9. Read runtime logs, not just the exit code. Missing resources, import failures, camera warnings, and script errors are real failures.
10. Update `STRUCTURE.md` if scene ownership, state, asset contracts, or verification commands changed.
11. Repeat from step 2 until the task's stop conditions pass.

## Imported Asset Pass

- Treat imported assets as a second pass unless the brief requires them immediately.
- Keep code-owned wrapper nodes and placement logic even when the visible child comes from a GLB or `.tscn`.
- When a GLB or texture appears missing, default grey, wrongly scaled, or invisible, inspect import logs before rewriting spawn code.
- Check three things first:
  1. the file lives under `assets/`
  2. the runtime path uses `res://assets/...`
  3. `godot --headless --import` has run after the file was added or changed
- Preserve existing `project.godot` and `.csproj` settings on incremental tasks. Dropping an engine setting can break runtime behavior without compile errors.

## Final Proof Bundle

After the whole task is complete, create a fresh `screenshots/result/{N}/` directory, incrementing `N` for each new final-attempt bundle.

It must contain:

- `video.mp4` - encoded at 30 fps and between 15s and 30s long. Prefer 15s / 450 frames; use up to 30s / 900 frames only when the task needs the extra time to prove behavior.
- the raw `frameXXX.png` sequence used to encode that video

The clip must demonstrate the task across its full chosen duration, not in one good moment. A scene that loops the same animation, holds a single static frame, or sits idle is not proof. A bundle where the opening seconds look correct and the rest degenerates into stuck or broken state is treated as a clear failure, not a partial pass. See `capture.md` for the full capture contract.

Encode `video.mp4` from the stored raw frames at the same fps they were captured. If the frame cadence and MP4 timing disagree, the bundle no longer proves the motion correctly.

## Stop Conditions

- `dotnet build` passes
- `godot --headless --quit` passes without actionable errors
- Changed assets have been imported
- A runtime launch validation has been completed on a real display path or through the capture wrapper
- A fresh `screenshots/result/{N}/` proof bundle exists for the current final attempt
- If Android was requested, `android-build.md` has been followed and `build/game.apk` exists
- `STRUCTURE.md` matches the code that shipped

If headless launch is blocked by host display or Vulkan problems but build and desktop runtime are clean, accept the desktop run as decisive and record the headless blocker instead of distorting the app around workstation-specific failures.

## Debugging Priorities

1. Red compiler errors and Godot API mismatches.
2. Runtime import and resource-load errors.
3. Scene ownership mistakes: dropped packed nodes, wrong script attachment, missing camera/current viewport, wrong input action names.
4. Gameplay tuning and feel.

This ordering keeps the fastest objective blockers first. Compile issues and asset-loader failures should be resolved before spending time on tuning, presentation, or subjective feel.

## Do Not Do This

- Do not skip `dotnet build` and jump straight to repeated Godot runs.
- Do not debug a complex scene when a minimal `test/Debug*.cs` scene can isolate the failure.
- Do not treat a workstation-specific Vulkan, `xvfb`, or compositor failure as proof that the Godot code is wrong.
- Do not leave `STRUCTURE.md` stale after the runtime shape changes.
