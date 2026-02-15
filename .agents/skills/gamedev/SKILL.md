---
name: gamedev
description: |
  Generate complete Godot games from natural language by orchestrating project skills.
  Use for end-to-end generation or iterative updates of an existing game project.
---

# Game Generator Orchestrator

Generate and update Godot games from natural language. Coordinate specialized skills and keep project documents current.

## Project Layout

```
game/           # Godot project (git repo)
assets/         # shared binary assets — glb/, img/, assets.md
worktrees/      # parallel branch checkouts (temporary)
screenshots/    # test output, per-task subfolders
```

First anchor the project root before any shell work:

```bash
PROJECT_ROOT=$(pwd)
```

Use `$PROJECT_ROOT` in all paths. Never use `$(pwd)` inline.

## Godot Runtime Environment

In sandboxed environments, run Godot with writable user paths:

```bash
mkdir -p $PROJECT_ROOT/.tmp_godot/.local/share $PROJECT_ROOT/.tmp_godot/.config
HOME=$PROJECT_ROOT/.tmp_godot \
XDG_DATA_HOME=$PROJECT_ROOT/.tmp_godot/.local/share \
XDG_CONFIG_HOME=$PROJECT_ROOT/.tmp_godot/.config \
godot --headless --quit 2>&1
```

Apply the same env prefix to `--import`, scene builder runs, and test scripts.

## Skills Used By This Orchestrator

| Skill | When |
|-------|------|
| `asset-planner` | New project with asset budget and no `assets/assets.md` |
| `godot-scaffold` | New project creation or structural update |
| `game-decomposer` | Build/update `game/PLAN.md` task DAG |
| `godot-task` | Execute one concrete PLAN.md task |

## Pipeline

1. **Resume check**
- If `game/PLAN.md` exists, read `game/PLAN.md`, `game/STRUCTURE.md`, and `game/MEMORY.md` and resume from pending work.
- If not, start fresh.

2. **Asset planning (optional)**
- If `assets/assets.md` is missing and budget is provided, apply `asset-planner` first.

3. **Scaffold + decomposition**
- Apply `godot-scaffold` to create/update structure.
- Apply `game-decomposer` to create/update `game/PLAN.md`.
- Run these two in parallel when practical.

4. **Plan review**
- Read `game/PLAN.md`.
- Present a concise summary: game name, risk profile, and numbered tasks.
- Incorporate requested plan edits before execution.

5. **Task waves**
- Parse task dependency graph from `game/PLAN.md`.
- Identify ready tasks: status `pending` and all dependencies done.
- For each wave:
  - Mark selected tasks `in_progress` in `game/PLAN.md`.
  - Execute each selected task with `godot-task` guidance.
  - Use `worktree=true` and unique branches for independent parallel tasks.
  - After results, update status to `done`, `done (partial)`, or `skipped`.
  - Commit plan status update: `cd $PROJECT_ROOT/game && git add PLAN.md && git commit -m "plan: wave N done"`.

6. **Completion**
- Continue until no ready tasks remain.
- Summarize completed work, caveats, and remaining blocked items.

## Running Tasks

### Single ready task

Run on main checkout with no worktree.

### Multiple independent ready tasks

Use one worktree branch per task:
- `task-{id}-{short-name}`
- Each branch executes full `godot-task` lifecycle: worktree setup, implementation, validation, commit, rebase/merge, cleanup.

## Handling Results

After each task:
- If success: mark `done` and continue.
- If partial: choose one path:
  1. Accept as `done (partial)` when core goal is met.
  2. Adjust task requirements in `PLAN.md` and rerun.
  3. Re-run scaffold/decomposer if architecture is the root blocker.

Do not rerun unchanged failing specs repeatedly.

## Debugging

If task output is suspicious:
- Read `game/MEMORY.md`.
- Inspect task screenshots in `screenshots/<task-folder>/`.
- Run a full parse check:

```bash
cd $PROJECT_ROOT/game && \
HOME=$PROJECT_ROOT/.tmp_godot \
XDG_DATA_HOME=$PROJECT_ROOT/.tmp_godot/.local/share \
XDG_CONFIG_HOME=$PROJECT_ROOT/.tmp_godot/.config \
timeout 30 godot --headless --quit 2>&1
```

## PLAN.md Status Contract

Each task must contain `**Status:**` with one of:
- `pending`
- `in_progress`
- `done`
- `done (partial)`
- `skipped`

Update status immediately before and after execution.

## Document Maintenance

- `game/STRUCTURE.md` is maintained by scaffold runs and manual graph-level updates.
- `game/PLAN.md` is maintained by decomposition runs plus execution status edits.
- `game/MEMORY.md` stores discoveries from task execution and debugging.
