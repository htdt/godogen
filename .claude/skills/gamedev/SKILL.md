---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, and task skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Game Generator — Orchestrator

You generate complete Godot games from natural language descriptions. You coordinate specialized skills to plan, build, verify, and iterate until the game works.

## Project Root

All skills operate on `project_root=build`. Every file reference below uses `build/` as the project root.

## Assets

Read `build/assets.json` at the start to get the list of available assets. Pass the assets list to **godot-scaffold** and **game-decomposer** so they can plan around available models and textures.
If `build/assets.json` doesn't exist, proceed with no assets (placeholder geometry only).

## Skills

| Skill | Input | Output | When | How |
|-------|-------|--------|------|-----|
| **godot-scaffold** | game description, assets | `build/project.godot`, `build/STRUCTURE.md`, `build/scripts/*.gd` stubs, `build/scenes/*.tscn` stubs | Once at start | Inline |
| **game-decomposer** | game description, STRUCTURE.md, assets | `build/PLAN.md` — task DAG with verification criteria | Once at start | Inline |
| **godot-task** | task from PLAN.md, STRUCTURE.md | `.tscn` scenes + `.gd` scripts + `test/test_task.gd` + screenshots | Per task | **Sub-agent** |

## Running Sub-agents

Use the **Task tool** to run `godot-task` as a sub-agent. Each task gets ONE sub-agent that handles scene generation, script writing, test harness creation, screenshot capture, and visual verification — iterating internally until screenshots match the task's **Verify** description.

**For each task:**
```
Task(subagent_type="general-purpose", prompt="""
Use the godot-task skill. project_root=build

{paste the task block from PLAN.md — including the Verify field}

{paste relevant STRUCTURE.md sections}
""")
```

Pass only the information the sub-agent needs:
- The specific task block from PLAN.md (**including the Verify field** — this drives the test harness)
- Relevant STRUCTURE.md sections (scenes/scripts the task touches)
- Any error context if this is a retry

## Pipeline

```
User request
    |
    +- Read build/assets.json (if exists)
    +- scaffold (inline) -> STRUCTURE.md + project.godot + stubs
    +- decomposer (inline) -> PLAN.md (uses STRUCTURE.md)
    |
    +- For each task (topological order):
    |   +- Launch godot-task sub-agent
    |   |   (builds scenes + scripts, generates test harness,
    |   |    captures screenshots, iterates until Verify matches)
    |   +- Cross-project compile check: cd build && timeout 30 godot --headless --quit 2>&1
    |   +- If compile FAIL -> retry with error context
    |   +- Review sub-agent's screenshots (build/test/screenshots/)
    |   +- Update STRUCTURE.md if architecture changed
    |
    +- Final compile check + screenshot review of complete game
```

## When to Use godot-task

**Always prefer launching a godot-task sub-agent over editing files directly** — even for simple merges, tweaks, or one-line fixes. The sub-agent runs the test harness and captures screenshots, which catches issues that look trivial but break visually. If you edit a file inline, you skip verification and won't know if it worked until later (when it's harder to fix).

## Executing a Task

Before generating for task N:

1. **Read `build/PLAN.md`** — task requirements, placeholder, targets, dependencies, **Verify** description
2. **Read `build/STRUCTURE.md`** — relevant scenes, scripts, signal connections
3. **Check dependencies** — all dependency tasks must be complete and files must exist
4. **Launch sub-agent** — one godot-task agent with the task block (including Verify) + relevant STRUCTURE.md sections, with `project_root=build`. The sub-agent builds, tests, captures screenshots, and iterates internally.
5. **Cross-project compile check** — `cd build && timeout 30 godot --headless --quit 2>&1` to catch integration issues
6. **Review screenshots** — read PNGs from `build/test/screenshots/` to confirm the sub-agent's visual verification
7. **Update documents** — any architectural changes to STRUCTURE.md

## Updating Documents at Runtime

### STRUCTURE.md

Update when generators **change the inter-file graph**: new scene/script, new signal connection, changed node type, new input action.

Don't update for internals (child nodes within a scene, helper functions). STRUCTURE.md tracks files and connections, not implementation.

### PLAN.md

Update when discoveries change future tasks:
- Adjust future tasks if discoveries change the approach
- Mark tasks cut if scope must shrink (with explanation)

### MEMORY.md

Sub-agents write discoveries to `build/MEMORY.md` as they work. Check it when a task fails — previous agents may have logged relevant workarounds or known issues.
