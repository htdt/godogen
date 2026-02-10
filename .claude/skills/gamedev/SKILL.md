---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, and task skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
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
Use the godot-task skill. project_root=build

{task block from PLAN.md — including Verify field}

{relevant STRUCTURE.md sections}
""")
```

Pass only what the sub-agent needs: task block (with Verify), relevant STRUCTURE.md sections, error context if retrying.

## Pipeline

```
User request
    |
    +- Read build/assets.json (if exists)
    +- scaffold (inline) -> STRUCTURE.md + project.godot + stubs
    +- decomposer (inline) -> PLAN.md
    |
    +- For each task (topological order):
    |   +- Launch godot-task sub-agent
    |   +- Read sub-agent result for status / issues
    |   +- Update STRUCTURE.md and PLAN.md as needed
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
