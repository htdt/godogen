---
name: godogen
description: |
  This skill should be used when the user asks to "make a game", "build a game", "generate a game", or wants to generate or update a complete Godot game from a natural language description. Orchestrates scaffold, decomposer, and task agents.
---

# Game Generator — Orchestrator

Generate and update Godot games from natural language. Coordinate specialized agents and keep project documents current.

## Project Layout

The Godot project is the working directory (and the git repo). Binary assets live in `assets/` (gitignored), loaded via `res://assets/glb/` and `res://assets/img/`. Screenshots go to `screenshots/` (gitignored).

**First: anchor the project root** — run `PROJECT_ROOT=$(pwd)` before any bash command. Use `$PROJECT_ROOT` in all paths. Never rely on `$(pwd)` inline.

## Agents

| Agent | When | How |
|-------|------|-----|
| **asset-planner** | New project, no assets, budget provided | Sub-agent via Task tool (runs before scaffold) |
| **godot-scaffold** | New project OR update | Sub-agent via Task tool |
| **game-decomposer** | New project OR update | Sub-agent via Task tool (parallel with scaffold) |
| **godot-task** | Per task from PLAN.md | Sub-agent via Task tool (parallel when independent) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the agent it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.


## Pipeline

```
User request
    |
    +- Check if PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md -> skip to task execution
    |   +- If no: continue with fresh pipeline below
    |
    +- If no ASSETS.md AND budget provided:
    |   +- Task(subagent_type="asset-planner")
    |       prompt: budget_cents, game description
    |
    +- In parallel (two Task calls in one message):
    |   +- Task(subagent_type="godot-scaffold") -> STRUCTURE.md + project.godot + stubs
    |   +- Task(subagent_type="game-decomposer") -> PLAN.md
    |
    +- Plan normalization (required):
    |   +- Read PLAN.md and STRUCTURE.md together
    |   +- For every task in PLAN.md:
    |   |   +- Add `**Status:** pending` if Status is missing
    |   |   +- Add `**Targets:**` if missing
    |   |   +- Fill Targets with concrete project-relative files expected to change
    |   |     (e.g. scenes/main.tscn, scripts/player_controller.gd, project.godot)
    |   |     inferred from task text + scene/script mappings in STRUCTURE.md
    |   +- Save the normalized plan before review
    |
    +- Enter plan mode (EnterPlanMode)
    |   +- Read PLAN.md
    |   +- Show user a concise summary of the plan
    |   +- User reviews / requests changes
    |   +- ExitPlanMode — show full task list to user
    |
    +- Create CLI todo list from PLAN.md tasks (TaskCreate)
    |
    +- Find ready tasks (pending, deps all done)
    +- While ready tasks exist:
    |   +- If 2+ independent tasks ready:
    |   |   +- Dispatch all as parallel Task() calls in one message
    |   |   +- Each godot-task runs in an isolated worktree
    |   +- Else (1 task or merge task):
    |   |   +- Run directly on main (no worktree)
    |   +- For each task in wave:
    |   |   +- Update PLAN.md: mark task status -> in_progress
    |   |   +- Mark task in_progress (TaskUpdate)
    |   +- Launch godot-task sub-agent(s) (see Running Tasks)
    |   +- Read sub-agent results — check for success/failure
    |   +- Handle results (see Handling Task Results below)
    |   +- Update PLAN.md: mark task statuses -> done / done (partial) / skipped
    |   +- Mark tasks completed (TaskUpdate)
    |   +- git add PLAN.md && git commit -m "plan: wave N done"
    |   +- Summarize results to user
    |   +- Find next ready tasks
    |
    +- Presentation video (see below)
    |
    +- Summary of completed game
```

## Launching Scaffold + Decomposer in Parallel

```
# Send BOTH Task calls in a single message:

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

## Plan Mode

After both agents complete, enter plan mode for user review.

1. Call `EnterPlanMode`
2. Read `PLAN.md`
3. Show the user a **concise summary**: game name, risk assessment, and a numbered list of tasks (one line each: task name + goal)
4. Let the user review. If they request changes, update PLAN.md accordingly.
5. Call `ExitPlanMode` — in the exit message, list all tasks with their dependencies so the user sees the full scope.

## Running Tasks as Sub-Agents

Each task runs as a **sub-agent** via the Task tool. This gives each task a clean context window, preventing accumulated state from earlier tasks from polluting later ones.

### Single task (or only 1 ready)

Run directly on main — no worktree:

```
Task(
  subagent_type="godot-task",
  description="godot-task: {task_name}",
  prompt="""
{task block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)
```

### Parallel wave (2+ independent tasks ready)

Send ALL ready tasks as parallel Task() calls in a single message. Each gets `isolation: "worktree"` for native git worktree isolation:

```
# All in ONE message — parallel dispatch:

Task(
  subagent_type="godot-task",
  isolation="worktree",
  description="godot-task: {task_A_name}",
  prompt="""
{task A block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)

Task(
  subagent_type="godot-task",
  isolation="worktree",
  description="godot-task: {task_B_name}",
  prompt="""
{task B block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)
```

Each agent runs in an isolated worktree copy. After the wave completes, merge results and clean up (see Post-Task Merge below). Then commit PLAN.md status updates: `git add PLAN.md && git commit -m "plan: wave N done"`.

### Post-Task Merge (worktree agents only)

After each worktree sub-agent completes, the Task result includes the worktree path and branch name (if changes were committed). For each:

1. **Copy screenshots** from the worktree before they're lost:
   ```bash
   cp -r <worktree_path>/screenshots/* $PROJECT_ROOT/screenshots/ 2>/dev/null
   ```
2. **Merge the branch:**
   ```bash
   git merge <branch>
   ```
   If conflicts arise, the task's files are authoritative — accept theirs for conflicting paths.
3. **Clean up:**
   ```bash
   git worktree remove <worktree_path> && git branch -d <branch>
   ```

If the agent made no changes, the worktree is auto-deleted — no merge needed.

## Handling Task Results

After each sub-agent completes, read its result message and summarize to the user (what succeeded, what's broken, any caveats).

godot-task iterates internally and uses judgment to decide when to stop (it won't spin forever — it stops when it recognizes a fundamental blocker or lack of convergence). When the sub-agent reports back:

**Task succeeded** — mark completed, move on.

**Task stopped with partial results** — read the report (what works, what's broken, root cause guess) and decide:
1. **Good enough** — the core goal is met even if imperfect. Mark completed, note caveats.
2. **Adjust task** — simplify requirements or change approach. Update the task in PLAN.md and launch a new sub-agent with the revised spec.
3. **Replan** — the task is fundamentally blocked. Re-run scaffold (to fix architecture) and/or decomposer (to restructure tasks), then resume from the new plan.

Don't retry the same task with the same spec — that's what godot-task already tried.

## Visual QA

After a task completes, run visual QA on its screenshots if the game has progressed past early grey-box stage (real textures, lighting, gameplay visible). Skip it on early tasks that are still mostly placeholders.

Pick 7 frames: 4 consecutive (for motion analysis) + 3 from different parts of the game (for diversity). Save the report to `visual-qa/{N}.md` where N is the next sequential number:
```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 .claude/skills/visual-qa/scripts/visual_qa.py consec1.png consec2.png consec3.png consec4.png diverse1.png diverse2.png diverse3.png > visual-qa/${N}.md
```

After capture, read the report and act on the verdict:
- **pass** — move on. The report serves as proof the feature was externally tested.
- **warning** — read the issues. Fix anything that's a real correctness problem; ignore stylistic nitpicks.
- **fail** — read the issues. Decide whether to fix in the current task (adjust + re-run godot-task) or defer to a follow-up task in PLAN.md.

Commit reports alongside task work: `git add visual-qa/ && git commit -m "visual-qa: report N"`.

Budget ~20 calls across the entire generation — don't run on every task. The QA tends to be overly picky; use judgment on which issues actually warrant action vs. noise.

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
- Run `cd $PROJECT_ROOT && timeout 30 godot --headless --quit 2>&1` to check cross-project compilation

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
