---
name: godogen
description: |
  This skill should be used when the user asks to "make a game", "build a game", "generate a game", or wants to generate or update a complete Godot game from a natural language description. Orchestrates scaffold, decomposer, and task agents.
---

# Game Generator — Orchestrator

Generate and update Godot games from natural language. Coordinate specialized agents and keep project documents current.

## Agents

| Agent | When | How |
|-------|------|-----|
| **godot-scaffold** | New project OR update | Sub-agent via Task tool (parallel with decomposer) |
| **game-decomposer** | New project OR update | Sub-agent via Task tool (parallel with scaffold) |
| **asset-planner** | After scaffold + decomposer, budget provided | Sub-agent via Task tool (reads STRUCTURE.md + PLAN.md) |
| **godot-task** | Per task from PLAN.md | Sub-agent via Task tool (sequential) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the agent it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.


## Pipeline

```
User request
    |
    +- Check if PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md -> skip to task execution
    |   +- If no: continue with fresh pipeline below
    |
    +- Visual target (Skill "visual-target") -> reference.png + ASSETS.md (style only)
    |
    +- In parallel (two Task calls in one message):
    |   +- Task(subagent_type="godot-scaffold") -> STRUCTURE.md + project.godot + stubs
    |   +- Task(subagent_type="game-decomposer") -> PLAN.md
    |
    +- If budget provided (and no asset tables in ASSETS.md):
    |   +- Task(subagent_type="asset-planner")
    |       prompt: budget_cents
    |       -> ASSETS.md + updated PLAN.md with asset assignments
    |
    +- Plan normalization (required):
    |   +- Read PLAN.md and STRUCTURE.md together
    |   +- For every task in PLAN.md:
    |   |   +- Add `**Status:** pending` if Status is missing
    |   |   +- Add `**Targets:**` if missing
    |   |   +- Fill Targets with concrete project-relative files expected to change
    |   |     (e.g. scenes/main.tscn, scripts/player_controller.gd, project.godot)
    |   |     inferred from task text + scene/script mappings in STRUCTURE.md
    |   +- Save the normalized plan
    |
    +- Show user a concise plan summary (game name, numbered task list)
    +- Proceed immediately to task execution
    |
    +- Find next ready task (pending, deps all done)
    +- While a ready task exists:
    |   +- Update PLAN.md: mark task status -> in_progress
    |   +- Launch godot-task sub-agent (see Running Tasks), then read the outcome
    |   +- Mark task completed in PLAN.md OR replan based on the outcome
    |   +- git add PLAN.md && git commit -m "plan: task N done"
    |   +- Summarize results to user
    |   +- Find next ready task
    |
    +- Presentation video (see below)
    |
    +- Summary of completed game
```

## Generating Visual Target

Before scaffold and decomposer. Load `Skill(skill="visual-target")` and follow its instructions.

## Launching Scaffold + Decomposer in Parallel

```
Task(
  subagent_type="godot-scaffold",
  description="scaffold: {game_name}",
  prompt="""
{game description}
"""
)

Task(
  subagent_type="game-decomposer",
  description="decompose: {game_name}",
  prompt="""
{game description}
"""
)
```

## Launching Asset Planner

After scaffold and decomposer complete. It reads STRUCTURE.md, PLAN.md, and reference.png itself.

```
Task(
  subagent_type="asset-planner",
  description="assets: {game_name}",
  prompt="""
Budget: {budget_cents} cents
"""
)
```

The asset planner writes ASSETS.md and updates PLAN.md with asset assignments per task. It does NOT modify source code or scenes — godot-task handles integration.

### Mid-Pipeline Re-invocation

Scaffold, decomposer, and asset-planner can be re-dispatched at any point during task execution — not just at the start.

**Scaffold** — reset or add scripts/scenes when a task has corrupted or outgrown them. Describe exactly which files to regenerate and why; scaffold reads existing STRUCTURE.md and preserves everything else.

**Decomposer** — replan when something large-scale changes: a task reveals the approach is wrong, a major feature needs rethinking, or new requirements emerge. Don't use for basic tweaks — just edit PLAN.md directly for those.

**Asset planner** — generate new assets or regenerate broken ones mid-run. Pass a targeted description of what's needed.

## Running Tasks as Sub-Agents

Each task runs as a **sub-agent** via the Task tool. This gives each task a clean context window, preventing accumulated state from earlier tasks from polluting later ones. Tasks run sequentially on main.

```
Task(
  subagent_type="godot-task",
  description="godot-task: {task_name}",
  prompt="""
{task block from PLAN.md}
"""
)
```

## Visual QA

Visual QA runs inside godot-task — each task handles its own VQA cycle. The task agent reports a VQA report path alongside screenshots. **Never ignore a fail verdict** — always act on it before marking a task done.

- **pass/warning** — move on.
- **fail** — godot-task already attempted up to 3 fix cycles. Read its failure report (includes VQA issues and root cause hypothesis) and decide:
  - **Replan** — re-invoke scaffold, decomposer, and/or asset-planner if the root cause is upstream (wrong assets, wrong architecture, fundamentally mismatched approach).
  - **Escalate** — surface the issue to the user if you can't determine the right fix.

## Presentation Video

After all tasks are complete, create a ~30-second cinematic gameplay video as the final deliverable. Dispatch as a godot-task sub-agent — it's just another task, but outputs video instead of screenshots. Adapt the prompt to the game's dimension (3D or 2D):

```
Task(
  subagent_type="godot-task",
  description="godot-task: presentation video",
  prompt="""
## Presentation Video
- **Goal:** Create a ~30-second cinematic video showcasing the completed game.
- **Targets:** test/presentation.gd
- **Requirements:**
  - Write test/presentation.gd — a SceneTree script (extends SceneTree)
  - Showcase representative gameplay via simulated input or scripted animations
  - ~900 frames at 30 FPS (30 seconds)
  - Use Video Capture from godot-capture (AVI via --write-movie, convert to MP4 with ffmpeg)
  - Output: screenshots/presentation/gameplay.mp4

  **3D games:**
  - Smooth camera work: orbits, tracking shots, dolly moves — show the world from its best angles
  - Good lighting: DirectionalLight3D key (shadow-casting) + fill/rim, warm/cool contrast
  - Post-processing: Environment + WorldEnvironment with glow/bloom, SSAO, SSR, ACES tonemapping, volumetric fog

  **2D games:**
  - Camera pans and smooth scrolling across the game world — show key areas and variety
  - Zoom transitions between overview and close-up to highlight detail
  - Trigger representative gameplay sequences: player movement, enemies, pickups, scoring, level transitions
  - Keep the viewport framing tight — no large empty regions

- **Verify:** Capture and verify screenshots before capturing the final video to verify the presentation.
"""
)
```

Commit after: `git add test/presentation.gd && git commit -m "add presentation video"`.

## Debugging

If a task reports failure or you suspect integration issues:
- Read `MEMORY.md` — task execution logs discoveries and workarounds
- Read screenshots in `screenshots/{task_folder}/`
- Run `timeout 30 godot --headless --quit 2>&1` to check cross-project compilation

## PLAN.md Task Contract

Each task must contain:
- `**Status:**` with one of `pending`, `in_progress`, `done`, `done (partial)`, `skipped`.
- `**Targets:**` listing concrete project-relative files the task is expected to modify (for example `scenes/main.tscn`, `scripts/player_controller.gd`).

When missing, initialize `Status` to `pending` and fill `Targets` from STRUCTURE.md during plan normalization.
Update status immediately before and after execution.

## Resuming an Interrupted Pipeline

At the start of every run, check if `PLAN.md` exists. If so, read it along with STRUCTURE.md and MEMORY.md, then resume from the first non-`done` task. Treat `in_progress` as needing a retry.

## Document Maintenance

**STRUCTURE.md** — scaffold agent is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer agent is the primary author. You own the `**Status:**` fields. Between decomposer runs, you may also tweak tasks when discoveries change future work (adjust approach, mark tasks skipped, add tasks).

Task execution writes discoveries to `MEMORY.md`. Check it when a task fails.
