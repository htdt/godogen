---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, and task skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList
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
| **game-decomposer** | New project OR update (plan new/changed features) | Inline |
| **godot-task** | Per task from PLAN.md | **Sub-agent** |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the skill it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.

## Running Task Sub-agents

Each task gets ONE sub-agent that builds, tests, captures screenshots, and iterates internally until verification passes.

```
Task(subagent_type="general-purpose", prompt="""
CRITICAL: Your FIRST action must be to invoke the Skill tool with skill="godot-task" to load the task executor instructions.

project_root=build

{task block from PLAN.md — including Verify field}

{relevant STRUCTURE.md sections}
""")
```

Pass only what the sub-agent needs: task block (with Verify), relevant STRUCTURE.md sections, error context if retrying.

### Screenshot Review

After a task sub-agent reports success, review its screenshots with a **separate sub-agent that has no implementation context** — just the task spec and the visual evidence. This catches confirmation bias (the implementer sees what it expects, not what's actually there).

```
Task(subagent_type="general-purpose", model="sonnet", prompt="""
You are reviewing screenshots from a Godot game development task.

## Task
{task Goal + Requirements + Verify from PLAN.md}

## Screenshots
Read these files and judge whether the task's Verify criteria are met:
- build/test/screenshots/frame00000000.png  (initial state)
- build/test/screenshots/frame{mid}.png     (action in progress)
- build/test/screenshots/frame{late}.png    (expected outcome)

Also read the test harness stdout below for any ASSERT FAIL lines:
{stdout from xvfb-run capture}

## Your job
Reply with exactly one of:
- PASS — screenshots and assertions confirm the Verify criteria are met
- FAIL: {one-line reason} — what's wrong or missing

Be strict: judge whether the Verify criteria are actually demonstrated, not just whether the scene loads. If Verify describes a behavior, the screenshots must show it happening. If Verify describes placement or appearance, the screenshots must show it clearly from the angles provided.
""")
```

If the reviewer returns FAIL, retry the task sub-agent with the reviewer's reason appended as context.

## Pipeline

```
User request
    |
    +- Read build/assets.json (if exists)
    +- scaffold (inline) -> STRUCTURE.md + project.godot + stubs
    +- decomposer (inline) -> PLAN.md
    |
    +- Create CLI todo list from PLAN.md tasks (TaskCreate)
    |
    +- For each task (one at a time, in topological order):
    |   +- Mark task in_progress (TaskUpdate)
    |   +- Launch godot-task sub-agent
    |   +- On success: launch screenshot reviewer (clean context, sonnet)
    |   +- If reviewer says FAIL: retry task with reviewer's feedback
    |   +- On final pass: mark task completed (TaskUpdate)
    |   +- Update STRUCTURE.md and PLAN.md as needed
    |   +- Wait for completion before starting next task
    |
    +- Summary of completed game
```

## Debugging

The task sub-agent owns build + verify. If a sub-agent reports failure or you suspect integration issues, you can:
- Read `build/MEMORY.md` — sub-agents log discoveries and workarounds
- Read screenshots in `build/test/screenshots/`
- Run `cd build && timeout 30 godot --headless --quit 2>&1` to check cross-project compilation

But don't do this by default — only when something goes wrong.

## Document Maintenance

**STRUCTURE.md** — scaffold skill is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer skill is the primary author. Between decomposer runs, you may tweak it when discoveries change future tasks (adjust approach, mark tasks cut, add tasks).

Sub-agents write discoveries to `build/MEMORY.md`. Check it when a task fails.

## Always Prefer Sub-agents

Launch a godot-task sub-agent rather than editing files directly — even for small fixes. The sub-agent runs the test harness, which catches issues that inline edits miss.
