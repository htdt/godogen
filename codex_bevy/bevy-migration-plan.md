# Bevy Migration Plan

Updated on 2026-04-18.

## Operating Principle

- Bevy work lives in `codex_bevy/`. Keep the existing Godot Codex tree in `codex/` intact while the Bevy path is being established.
- Try first, then write it down. Each Bevy stage starts as a working experiment or demo project, then gets distilled into reusable skill guidance.
- Decouple late. Do not rush to split behavior into `scaffold.md`, `scene-generation.md`, `task-execution.md`, `capture.md`, or `quirks.md` until the approach has been proven in practice.
- Reuse the current Godot docs only for contract shape and workflow discipline. Keep what is useful about the process; do not port Godot commands, file formats, or assumptions.
- Track one Bevy version at a time. `bevy-api`, validation projects, examples, and docs should all move together when the repo updates Bevy; do not preserve legacy compatibility guidance in the default skill flow.
- Keep the first milestone narrow. Prove the core loop before worrying about Android, advanced physics, or broad feature parity.

## Scope

- Keep the core orchestration ideas from `codex/skills/godogen/`: staged execution, file-based resume state, risk-first thinking, asset planning, and visual verification.
- Build Bevy counterparts under `codex_bevy/` instead of replacing the Godot material in `codex/`.
- Add Bevy equivalents for the Godot-locked pieces first: `godot-api`, `scaffold`, `scene-generation`, `task-execution`, `capture`, and `quirks`.
- Bring over the mostly engine-agnostic stages later: `visual-target`, `decomposer`, `asset-planner`, `asset-gen`, `rembg`, and `visual-qa`.
- Defer Android build/export, deep 3D parity, and speculative abstractions until the Bevy loop is stable.

## Ordered Plan

### 1. Prepare `bevy-api`

Goal:
Create the Bevy API lookup skill first so every later phase can use current Bevy guidance instead of guessing.

Work:
- Replace the `godot-api` role with a new `bevy-api` skill.
- Resolve the current Bevy version from the target project and keep examples/docs aligned to it.
- Keep the skill focused on the current API surface; do not add legacy-version branches unless a task explicitly needs migration guidance.
- Store local lookup sources under `codex_bevy/skills/bevy-api/docs/`: rustdoc, `bevy`, and `bevy-website`, with that directory gitignored.
- Use the local Bevy repo, official Learn content, examples, and local rustdoc as the lookup stack.
- Record only high-value repeated patterns locally; do not pre-convert the entire Bevy API into static markdown.

Done when:
- The skill can reliably answer targeted questions about app setup, ECS, resources, systems, assets, cameras, UI, and scenes for the current Bevy version.
- The answers are good enough to be used during scaffold and scene-generation work without falling back to guesswork.

Outputs:
- New `codex_bevy/skills/bevy-api/` skill source.
- Matching `codex_bevy/skills/bevy-api/agents/openai.yaml`.
- A current-version lookup workflow that later phases can depend on.

### 2. Establish `scaffold`

Goal:
Figure out the Bevy scaffold by doing it from scratch, then write down the exact instructions only after they are proven.

Work:
- Review the current `codex/skills/godogen/scaffold.md` to preserve the useful contract shape: toolchain check, project-state assessment, output files, verification, and commit point.
- Create a Bevy scaffold path in a scratch project from an empty directory.
- Decide the baseline project contract: `Cargo.toml`, `src/main.rs`, `src/lib.rs` if needed, plugin/module layout, `assets/`, `STRUCTURE.md`, and `.gitignore`.
- Validate by recreating the project from scratch until the instructions have no hidden steps.

Done when:
- A fresh Bevy project can be created from zero by following the draft instructions exactly.
- The result builds and runs cleanly with the expected commands.
- The scaffold instructions feel deterministic rather than "mostly right".

Outputs:
- Bevy version of `codex_bevy/skills/godogen/scaffold.md`.
- Clear project skeleton contract for generated Bevy repos.

### 3. Establish `scene-generation`

Goal:
Prove the default scene-generation approach in Bevy before documenting it.

Work:
- Review the current `codex/skills/godogen/scene-generation.md` only to keep the useful discipline around structure and output expectations.
- Decide the default Bevy path for generated scenes. The starting assumption is code-first world construction and ECS spawning, not serialized scene files.
- Build at least one non-trivial scene in the scratch Bevy project using the chosen approach.
- Recreate that scene from a clean starting point so the instructions are validated, not just described.

Done when:
- There is a repeatable Bevy pattern for constructing game worlds that can serve as the default skill guidance.
- The instructions can reproduce the scene from scratch without undocumented cleanup or manual editor work.

Outputs:
- Bevy version of `codex_bevy/skills/godogen/scene-generation.md`.
- A clear default for how generated projects create their world content.

### 4. Collect early `quirks.md`

Goal:
Capture only the real, general Bevy/Rust quirks found during phases 1-3.

Work:
- Seed `codex_bevy/skills/godogen/quirks.md` with non-obvious issues discovered while establishing `bevy-api`, `scaffold`, and `scene-generation`.
- Keep the bar high: include recurring engine/tooling gotchas, not speculative notes or generic Rust advice.

Done when:
- The file contains a small, high-signal set of quirks that would have prevented real confusion in phases 1-3.

Outputs:
- Initial Bevy `quirks.md`.

### 5. Create a demo project

Goal:
Build one real Bevy demo as the first end-to-end proving ground.

Work:
- Wait for the user-provided demo brief.
- Use the demo to test whether the scaffold and scene-generation guidance actually hold up under real game work.
- Keep the scope intentionally narrow; the demo is for learning the workflow, not showing full feature coverage.

Done when:
- There is one working Bevy demo that exercises the current migration assumptions.

Outputs:
- Demo project and concrete migration feedback.

### 6. Expand `quirks.md` and establish `task-execution.md`

Goal:
Use the demo project to discover the real implementation loop, then document it.

Work:
- Watch how the demo is actually built: planning, coding, `cargo` commands, debugging, verification, retries, and stop conditions.
- Promote durable demo findings into `quirks.md`.
- Write `codex_bevy/skills/godogen/task-execution.md` only after the loop is proven in real use.

Done when:
- A second task could follow `task-execution.md` without relying on hidden tribal knowledge from the first demo.
- `quirks.md` reflects the real friction found in actual task execution, not just early setup work.

Outputs:
- Bevy version of `codex_bevy/skills/godogen/task-execution.md`.
- Expanded Bevy `quirks.md`.

### 7. Establish `capture`

Goal:
Standardize screenshot and video capture after the runtime loop is known.

Work:
- Choose the default Bevy capture path only after the demo reveals the real constraints.
- Prove one reliable screenshot path first.
- Add video capture only if it is stable enough to deserve first-class instructions.
- Validate the final instructions against the demo project from a clean setup when possible.

Done when:
- Capture instructions produce repeatable screenshots for verification and later `visual-qa` use.
- If video is included, it is reliable enough to keep in the default workflow rather than as an experimental note.

Outputs:
- Bevy version of `codex_bevy/skills/godogen/capture.md`.

### 8. Add the remaining features

Goal:
Port the rest of the stack only after the Bevy runtime loop is stable.

Work:
- Adapt `visual-target`, `decomposer`, `asset-planner`, `asset-gen`, `rembg`, and `visual-qa`.
- Re-check wording, file references, output expectations, and screenshot assumptions against the Bevy contracts established in phases 2-7.
- Keep these edits pragmatic; most of these stages should need adaptation, not reinvention.

Done when:
- The remaining skills fit the Bevy workflow cleanly and do not assume Godot file formats, commands, or capture outputs.

Outputs:
- Updated engine-agnostic skill docs and metadata where needed.

## Why This Order

- `bevy-api` comes first because every later phase depends on accurate, current API lookup.
- `scaffold` comes before `scene-generation` because there must be a known project shell to generate into.
- `quirks.md` starts early, but only as a small curated record of proven issues.
- `task-execution.md` is intentionally late because the real loop should be distilled from an actual demo, not invented upfront.
- `capture` comes after task execution because it depends on the runtime/test loop and feeds later visual verification.
- The mostly engine-agnostic stages come last because they benefit from stable Bevy contracts and should not drive those contracts.

## Deferred For Now

- Android build/export flow.
- Full parity with all Godot-era workflows.
- Heavy 3D, advanced physics, or large-scale asset pipelines before the core Bevy loop is stable.
- Large up-front abstractions that have not been earned by real project usage.

## First Stable Milestone

The migration reaches its first stable milestone when all of the following are true:

- `bevy-api` exists and is good enough to support later implementation work.
- `scaffold.md` can produce a fresh Bevy project from zero without hidden steps.
- `scene-generation.md` can reproduce a non-trivial scene from scratch using the chosen default approach.
- One demo project has been built with those instructions.
- `task-execution.md`, `capture.md`, and `quirks.md` have been written from actual use rather than speculation.
- The remaining reusable stages have been adapted on top of those stable contracts.

## Immediate Next Step

Start with phase 1 in `codex_bevy/` and make `bevy-api` real before touching the rest of the migration.
