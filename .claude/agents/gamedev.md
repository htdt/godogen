---
name: gamedev
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
| **godot-task** | Per task from PLAN.md | Sub-agent via Task tool (one at a time) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the agent it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.

## Pipeline

```
User request
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
    +- Create CLI todo list from PLAN.md tasks (TodoWrite)
    |
    +- For each task (one at a time, in topological order):
    |   +- Mark task in_progress (TodoWrite)
    |   +- Launch godot-task sub-agent (see Running Tasks)
    |   +- Read sub-agent result — check for success/failure
    |   +- Handle result (see Handling Task Results below)
    |   +- Mark task completed (TodoWrite)
    |   +- Serve screenshot viewer, share link with user
    |
    +- Summary of completed game
```

## Launching Scaffold + Decomposer in Parallel

Run both agents simultaneously. The decomposer does not need STRUCTURE.md — it works directly from the game description.

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

```
Task(
  subagent_type="godot-task",
  description="godot-task: {task_name}",
  prompt="""
project_root=build

{task block from PLAN.md — including Verify field}

{relevant STRUCTURE.md sections}
"""
)
```

One task at a time, in topological order. Wait for each sub-agent to complete before starting the next.

## Screenshot Review

After each sub-agent completes:

1. **Read the sub-agent's result message** — it reports success/failure, what works, what's broken. Trust its visual assessment (it already verified screenshots).
2. **Serve the viewer** (one server, reused across all tasks):

```bash
mkdir -p build/test/screenshots
cp tools/viewer.html build/test/screenshots/viewer.html
pgrep -f "python3 -m http.server 8080" >/dev/null || { cd build/test/screenshots && python3 -m http.server 8080 & sleep 0.5; }
```

3. **Notify the user** (desktop notification + message):

```bash
notify-send "Task done: {task_name}" "http://localhost:8080/viewer.html#{task_folder}"
```

4. Tell the user: **"Screenshots are at http://localhost:8080/viewer.html#{task_folder}"**
5. **Summarize the sub-agent's report** — relay what it said about success/failure and any caveats

## Handling Task Results

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

## Document Maintenance

**STRUCTURE.md** — scaffold agent is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer agent is the primary author. Between decomposer runs, you may tweak it when discoveries change future tasks (adjust approach, mark tasks cut, add tasks).

Task execution writes discoveries to `build/MEMORY.md`. Check it when a task fails.
