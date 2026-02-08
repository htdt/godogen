---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, scene, script, and verifier skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Game Generator — Orchestrator

You generate complete Godot games from natural language descriptions. You coordinate specialized skills to plan, build, verify, and iterate until the game works.

## Project Root

All skills operate on `project_root=build`. Every file reference below uses `build/` as the project root.

## Assets

Read `build/assets.json` at the start to get the list of available assets. Pass the assets list to **godot-scaffold** and **godot-decomposer** so they can plan around available models and textures.
If `build/assets.json` doesn't exist, proceed with no assets (placeholder geometry only).

## Skills

| Skill | Input | Output | When | How |
|-------|-------|--------|------|-----|
| **godot-scaffold** | game description, assets | `build/project.godot`, `build/STRUCTURE.md`, `build/scripts/*.gd` stubs | Once at start | Inline |
| **godot-decomposer** | game description, STRUCTURE.md, assets | `build/PLAN.md` — task DAG with verification criteria | Once at start | Inline |
| **godot-scene** | task from PLAN.md, STRUCTURE.md | `.tscn` scene files via GDScript builders | Per task | **Sub-agent** |
| **godot-script** | task from PLAN.md, STRUCTURE.md | `.gd` script implementations | Per task | **Sub-agent** |
| **godot-verifier** | task from PLAN.md, built project | compilation check — pass/fail verdict | After each task | Inline |

## Running Sub-agents

Use the **Task tool** to run `godot-scene` and `godot-script` as sub-agents. This keeps their large context (API docs, gdscript reference) out of the orchestrator's context window.

**For each task that needs scene generation:**
```
Task(subagent_type="general-purpose", prompt="""
Use the godot-scene skill. project_root=build

{paste the task block from PLAN.md}

{paste relevant STRUCTURE.md sections}
""")
```

**For each task that needs script generation:**
```
Task(subagent_type="general-purpose", prompt="""
Use the godot-script skill. project_root=build

{paste the task block from PLAN.md}

{paste relevant STRUCTURE.md sections}
""")
```

Pass only the information the sub-agent needs:
- The specific task block from PLAN.md (not the entire plan)
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
    |   +- Set status: in_progress in PLAN.md
    |   +- Launch scene/script sub-agents (parallel when independent)
    |   +- Run verifier (inline): cd build && timeout 30 godot --headless --quit 2>&1
    |   +- If PASS -> status: done
    |   +- If FAIL -> retry up to 3x with error context, then mark failed
    |   +- Update PLAN.md and STRUCTURE.md if architecture changed
    |
    +- Final verification of complete game
```

## Executing a Task

Before generating for task N:

1. **Read `build/PLAN.md`** — task requirements, placeholder, targets, dependencies
2. **Read `build/STRUCTURE.md`** — relevant scenes, scripts, signal connections
3. **Check dependencies** — all must be `done` and files must exist
4. **Launch sub-agents** — pass the task block + relevant STRUCTURE.md sections, with `project_root=build`
5. **Run verifier** — `cd build && timeout 30 godot --headless --quit 2>&1`
6. **Update documents** — status, notes, any architectural changes

## Updating Documents at Runtime

### STRUCTURE.md

Update when generators **change the inter-file graph**: new scene/script, new signal connection, changed node type, new input action.

Don't update for internals (child nodes within a scene, helper functions). STRUCTURE.md tracks files and connections, not implementation.

### PLAN.md

Update after **every** task attempt:
- Set status (`done` / `failed`)
- Add notes (especially on failure — what went wrong, what to try differently)
- Adjust future tasks if discoveries change the approach
- Mark tasks `cut` if scope must shrink (with explanation)
