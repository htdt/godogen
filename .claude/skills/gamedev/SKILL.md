---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, and task skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, Task, EnterPlanMode, ExitPlanMode, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Game Generator — Orchestrator

You generate and update Godot games from natural language. You coordinate specialized skills and keep project documents current.

## Project Root

All skills operate on `project_root=build`.

## Assets

Read `build/assets.json` at the start. Pass the assets list to **godot-scaffold** and **game-decomposer**. If it doesn't exist, proceed with placeholder geometry.

## Skills

| Skill | When | How |
|-------|------|-----|
| **godot-scaffold** | New project OR update (new modules, reset subsystems) | Inline |
| **game-decomposer** | New project OR update (plan new/changed features) | Inline, inside plan mode |
| **godot-task** | Per task from PLAN.md | Sub-agent (Task tool, one at a time) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the skill it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.

## Pipeline

```
User request
    |
    +- Read build/assets.json (if exists)
    +- scaffold (inline) -> STRUCTURE.md + project.godot + stubs
    |
    +- Enter plan mode (EnterPlanMode)
    |   +- decomposer (inline) -> PLAN.md
    |   +- Show user a concise summary of the plan
    |   +- User reviews / requests changes
    |   +- ExitPlanMode — show full task list to user
    |
    +- Create CLI todo list from PLAN.md tasks (TaskCreate)
    |
    +- For each task (one at a time, in topological order):
    |   +- Mark task in_progress (TaskUpdate)
    |   +- Launch godot-task sub-agent (see Running Tasks as Sub-Agents)
    |   +- Read sub-agent result — check for success/failure
    |   +- Handle result (see Handling Task Results below)
    |   +- Mark task completed (TaskUpdate)
    |   +- Serve screenshot viewer, share link with user
    |
    +- Summary of completed game
```

## Plan Mode

After scaffolding, enter plan mode before decomposition. This gives the user a chance to review and adjust the plan before any tasks execute.

1. Call `EnterPlanMode`
2. Run game-decomposer inline — produces `build/PLAN.md`
3. Show the user a **concise summary**: game name, risk assessment, and a numbered list of tasks (one line each: task name + goal)
4. Let the user review. If they request changes, update PLAN.md accordingly.
5. Call `ExitPlanMode` — in the exit message, list all tasks with their dependencies so the user sees the full scope.

## Running Tasks as Sub-Agents

Each task runs as a **sub-agent** via the Task tool. This gives each task a clean context window, preventing accumulated state from earlier tasks from polluting later ones.

```
Task(
  subagent_type="general-purpose",
  description="godot-task: {task_name}",
  prompt="""
Run the godot-task skill:

Skill(skill="godot-task", args=\"\"\"
project_root=build

{task block from PLAN.md — including Verify field}

{relevant STRUCTURE.md sections}
\"\"\")
"""
)
```

One task at a time, in topological order. Wait for each sub-agent to complete before starting the next.

## Screenshot Review

After each sub-agent completes:

1. **Read the sub-agent's result message** — it reports success/failure, what works, what's broken. Trust its visual assessment (it already verified screenshots).
2. **Serve the viewer** so the user can see the screenshots:

```bash
cp .claude/skills/gamedev/viewer.html build/test/screenshots/{task_folder}/viewer.html
pkill -f "python3 -m http.server 8080" 2>/dev/null; sleep 0.5
cd build/test/screenshots/{task_folder} && python3 -m http.server 8080 &
```

3. Tell the user: **"Screenshots for {task_name} are at http://localhost:8080/viewer.html"**
4. **Summarize the sub-agent's report** — relay what it said about success/failure and any caveats

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

**STRUCTURE.md** — scaffold skill is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer skill is the primary author. Between decomposer runs, you may tweak it when discoveries change future tasks (adjust approach, mark tasks cut, add tasks).

Task execution writes discoveries to `build/MEMORY.md`. Check it when a task fails.
