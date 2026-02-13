---
triggers:
  - "make a game"
  - "build a game"
  - "generate a game"
  - "godot game"
  - "game from description"
description: |
  Generate complete Godot games from natural language — orchestrates scaffold, decomposer, and task agents.

  **When to use:** When you need to generate or update a complete Godot game from a natural language description.
---

# Game Generator — Orchestrator

Generate and update Godot games from natural language. Coordinate specialized agents and keep project documents current.

## Project Root

All agents operate on `project_root=build`.

## Assets

Read `build/assets.json` at the start. Pass the assets list to **godot-scaffold** and **game-decomposer**. If it doesn't exist, proceed with placeholder geometry.

## Agents

| Agent | When | How |
|-------|------|-----|
| **godot-scaffold** | New project OR update | Sub-agent via Task tool |
| **game-decomposer** | New project OR update | Sub-agent via Task tool (parallel with scaffold) |
| **godot-task** | Per task from PLAN.md | Sub-agent via Task tool (parallel when independent) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the agent it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.

## Pipeline

```
User request
    |
    +- Check if build/PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md -> skip to task execution
    |   +- If no: continue with fresh pipeline below
    |
    +- Read build/assets.json (if exists)
    |
    +- In parallel (two Task calls in one message):
    |   +- Task(subagent_type="godot-scaffold") -> STRUCTURE.md + project.godot + stubs
    |   +- Task(subagent_type="game-decomposer") -> PLAN.md
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
    |   |   +- Each godot-task handles its own worktree lifecycle
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
    |   +- cd build && git add PLAN.md && git commit -m "plan: wave N done"
    |   +- Summarize results to user
    |   +- Find next ready tasks
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
project_root=build

{game description}

{assets list from assets.json}
"""
)

Task(
  subagent_type="game-decomposer",
  description="decompose: {game_name}",
  prompt="""
project_root=build

{game description}

{assets list from assets.json}
"""
)
```

## Plan Mode

After both agents complete, enter plan mode for user review.

1. Call `EnterPlanMode`
2. Read `build/PLAN.md`
3. Show the user a **concise summary**: game name, risk assessment, and a numbered list of tasks (one line each: task name + goal)
4. Let the user review. If they request changes, update PLAN.md accordingly.
5. Call `ExitPlanMode` — in the exit message, list all tasks with their dependencies so the user sees the full scope.

## Running Tasks as Sub-Agents

Each task runs as a **sub-agent** via the Task tool. This gives each task a clean context window, preventing accumulated state from earlier tasks from polluting later ones.

**Choosing targets:** godot-task expects a `**Targets:**` field listing files to generate (e.g. `scenes/track.tscn`, `scripts/car_controller.gd`). Read STRUCTURE.md and add the appropriate targets to each task block in the prompt.

### Single task (or only 1 ready)

Run directly on main — no worktree:

```
Task(
  subagent_type="godot-task",
  description="godot-task: {task_name}",
  prompt="""
project_root=build

{task block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)
```

### Parallel wave (2+ independent tasks ready)

Send ALL ready tasks as parallel Task() calls in a single message. Each gets `worktree=true` and a unique branch name:

```
# All in ONE message — parallel dispatch:

Task(
  subagent_type="godot-task",
  description="godot-task: {task_A_name}",
  prompt="""
project_root=build
worktree=true
branch=task-{A_id}-{short_name}

{task A block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)

Task(
  subagent_type="godot-task",
  description="godot-task: {task_B_name}",
  prompt="""
project_root=build
worktree=true
branch=task-{B_id}-{short_name}

{task B block from PLAN.md}

{relevant STRUCTURE.md sections}
"""
)
```

Each godot-task handles its own worktree lifecycle (branch, work, commit, rebase, merge, cleanup). After the wave completes, commit PLAN.md status updates: `cd build && git add PLAN.md && git commit -m "plan: wave N done"`.

## Handling Task Results

After each sub-agent completes, read its result message and summarize to the user (what succeeded, what's broken, any caveats).

godot-task iterates internally and uses judgment to decide when to stop (it won't spin forever — it stops when it recognizes a fundamental blocker or lack of convergence). When the sub-agent reports back:

**Task succeeded** — mark completed, move on.

**Task stopped with partial results** — read the report (what works, what's broken, root cause guess) and decide:
1. **Good enough** — the core goal is met even if imperfect. Mark completed, note caveats.
2. **Adjust task** — simplify requirements or change approach. Update the task in PLAN.md and launch a new sub-agent with the revised spec.
3. **Replan** — the task is fundamentally blocked. Re-run scaffold (to fix architecture) and/or decomposer (to restructure tasks), then resume from the new plan.

Don't retry the same task with the same spec — that's what godot-task already tried.

## Debugging

If a task reports failure or you suspect integration issues:
- Read `build/MEMORY.md` — task execution logs discoveries and workarounds
- Read screenshots in `build/test/screenshots/{task_folder}/`
- Run `cd build && timeout 30 godot --headless --quit 2>&1` to check cross-project compilation

## PLAN.md Task Status

Keep a `**Status:**` field on each task in PLAN.md: `pending` | `in_progress` | `done` | `done (partial)` | `skipped`. Update it immediately when state changes — before launching the sub-agent and after reading its result. This is what enables resumption.

## Resuming an Interrupted Pipeline

At the start of every run, check if `build/PLAN.md` exists. If so, read it along with STRUCTURE.md and MEMORY.md, then resume from the first non-`done` task. Treat `in_progress` as needing a retry.

## Document Maintenance

**STRUCTURE.md** — scaffold agent is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer agent is the primary author. You own the `**Status:**` fields. Between decomposer runs, you may also tweak tasks when discoveries change future work (adjust approach, mark tasks skipped, add tasks).

Task execution writes discoveries to `build/MEMORY.md`. Check it when a task fails.
