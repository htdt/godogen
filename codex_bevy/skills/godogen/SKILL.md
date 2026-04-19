---
name: godogen
description: |
  Create or refresh the proven core stages of a Bevy game project from a natural-language brief. Use when the user needs the scaffold, code-first scene setup, the current Bevy implementation loop, or validated capture workflow for a concrete task.
---

# Bevy Game Generator

This Bevy migration skill currently covers the proven core loop: scaffold, default scene generation, the real task-execution workflow, headless capture, and a small curated set of quirks.

## Available Stage Docs

| File | Purpose | When to read |
|------|---------|--------------|
| `scaffold.md` | Cargo package, app entrypoints, module shell, repo contract, and verification flow | Before creating or restructuring the Bevy project shell |
| `scene-generation.md` | Code-first world construction, state-scoped setup/teardown, and scene ownership rules | Before generating or replacing the default playable scene |
| `task-execution.md` | Proven `cargo`/runtime/debug loop for real Bevy feature work | Before implementing gameplay, imported assets, or runtime fixes beyond initial scaffold/scene generation |
| `capture.md` | Proven headless screenshot and video capture workflow | Before adding automated screenshots, PNG sequences, or video output |
| `quirks.md` | Non-obvious Bevy and tooling gotchas proven during the migration work | Before scene-generation work and whenever runtime behavior is surprising |
| *(bevy-api skill)* | Current Bevy `0.18.1` API and examples | When exact Bevy symbols or patterns matter |

## Current Scope

- Fresh Bevy project creation from an empty directory
- Scaffold-level refactors of an existing Bevy repo
- Default scene generation through code-first ECS spawning
- Runtime feature implementation with the proven Bevy `cargo`/debug/verification loop
- Headless screenshot and PNG-sequence capture with the validated offscreen image-target path
- `ffmpeg` video assembly on top of the validated Bevy frame-sequence output
- Imported asset integration and manifest-feature troubleshooting within the current Bevy version
- State-scoped teardown rules for world roots, cameras, lights, and overlay UI
- Small curated record of proven Bevy quirks from scaffold through capture

Do not invent the later pipeline stages yet. `visual-target`, `decomposer`, `asset-planner`, `asset-gen`, `rembg`, and `visual-qa` should still be added only after they are proven in this workspace.

## Execution

1. Read `scaffold.md`.
2. If the task includes initial world construction, read `scene-generation.md`.
3. If the task goes beyond scaffold or initial scene setup, read `task-execution.md`.
4. If the task includes screenshots, PNG sequences, or verification video, read `capture.md`.
5. Read `quirks.md` before implementing scene hierarchies, imported assets, headless capture, or when runtime behavior is non-obvious.
6. Use `bevy-api` for exact Bevy names when needed.
7. Stop once the relevant build checks pass, runtime validation has been run, and `STRUCTURE.md` matches the shipped code.
