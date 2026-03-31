# Single-Context Architecture Migration

Remove `context: fork` from godot-task, merge into godogen as one skill running the full pipeline inline. Create a separate API doc lookup skill for Godot class reference.

## Rationale

1M context lets the model see all prior decisions, reasoning, assets, and quirks across the full pipeline. Empirically works better than forked sub-agents that start blind each task.

## Final Structure

```
skills/godogen/
  SKILL.md                    # Orchestrator + inline task execution
  visual-target.md            # (unchanged)
  decomposer.md               # (unchanged)
  scaffold.md                 # (unchanged)
  asset-planner.md            # (unchanged)
  asset-gen.md                # (unchanged)
  rembg.md                    # (unchanged)
  android-build.md            # (unchanged)
  task-execution.md           # Workflow, commands, debugging — extracted from godot-task
  quirks.md                   # moved from godot-task
  gdscript.md                 # moved from godot-task
  scene-generation.md         # moved from godot-task
  script-generation.md        # moved from godot-task
  coordination.md             # moved from godot-task
  test-harness.md             # moved from godot-task
  capture.md                  # moved from godot-task
  visual-qa.md                # moved from godot-task
  scripts/                    # VQA prompts — moved from godot-task
  tools/                      # godogen tools only (asset_gen, rembg, etc.)

skills/godot-api/
  SKILL.md                    # API doc lookup skill (context: fork, agent: Explore)
  doc_api/                    # Godot class reference docs
  tools/
    ensure_doc_api.sh         # bootstrap doc_api
    godot_api_converter.py
    class_list.py
```

## Steps

### 1. Move godot-task sub-files into godogen

Move these files from `skills/godot-task/` to `skills/godogen/`:

- `quirks.md`
- `gdscript.md`
- `scene-generation.md`
- `script-generation.md`
- `coordination.md`
- `test-harness.md`
- `capture.md`
- `visual-qa.md`
- `scripts/` directory (VQA prompts)

### 2. Create task-execution.md

Extract from godot-task SKILL.md into `skills/godogen/task-execution.md`:

- Workflow steps (analyze, import, generate scenes, generate scripts, validate, fix, test, capture, verify, VQA)
- Iteration tracking guidance
- Reporting section (adapt: no longer reporting to an external orchestrator, just updating PLAN.md)
- Commands reference (godot --headless, etc.)
- Structured error recovery
- Project memory read/write instructions
- Debugging with Gemini section

Strip the skill frontmatter and the "Reporting to Orchestrator" framing — the executor IS the orchestrator now.

### 3. Update godogen SKILL.md

**Expand capabilities table** — add task-execution files:

```markdown
| File | Purpose | When to read |
|------|---------|--------------|
| `visual-target.md` | Generate reference image | Pipeline start |
| `decomposer.md` | Decompose into task DAG | After visual target |
| `scaffold.md` | Architecture + skeleton | After decomposition |
| `asset-planner.md` | Budget and plan assets | If budget provided |
| `asset-gen.md` | Asset generation CLI ref | When generating assets |
| `rembg.md` | Background removal | Before rembg operations |
| `task-execution.md` | Task workflow + commands | Before first task |
| `quirks.md` | Godot gotchas | Before writing code |
| `gdscript.md` | GDScript syntax ref | Before writing code |
| `scene-generation.md` | Scene builders | Targets include .tscn |
| `script-generation.md` | Runtime scripts | Targets include .gd |
| `coordination.md` | Scene+script ordering | Both .tscn and .gd |
| `test-harness.md` | Verification scripts | Before test harness |
| `capture.md` | Screenshot/video | Before capture |
| `visual-qa.md` | Gemini VQA | After capture |
| `android-build.md` | APK export | User requests Android |
```

**Replace the "Running Tasks" section** — no more Skill invocation:

```markdown
## Running Tasks

Read `task-execution.md` before starting the first task. Execute each task inline:

1. Read the task block from PLAN.md
2. Mark status -> in_progress
3. Read target-specific sub-files (scene-generation, script-generation, etc.)
4. Execute the implement -> validate -> capture -> VQA loop
5. Mark completed in PLAN.md
6. git add . && git commit
7. Move to next ready task
```

**Replace API doc references** — use the godot-api skill:

```markdown
## Godot API Lookup

When you need to look up a Godot class API (methods, properties, signals), use `Skill(skill="godot-api")` with your query. This runs in a separate context to avoid loading large API docs into the main pipeline.

Examples:
- Skill(skill="godot-api") "which class handles 2D particle effects?"
- Skill(skill="godot-api") "full API for CharacterBody3D"
- Skill(skill="godot-api") "how to detect collisions between Area3D nodes?"
```

**Add context hygiene section:**

```markdown
## Context Hygiene

Keep important state in files so the pipeline can resume even after compaction or clear:

- **PLAN.md** — task statuses, always up to date before moving on
- **STRUCTURE.md** — architecture reference, update if scaffolding changes
- **MEMORY.md** — discoveries, quirks, workarounds, what worked/failed
- **ASSETS.md** — asset manifest with paths and generation details

After completing each task: update PLAN.md status, write discoveries to MEMORY.md, git commit. This ensures the pipeline can resume from any point by reading these files.

If the context becomes polluted from debugging loops, manually compact with:
`/compact "Preserve current task context, PLAN.md statuses, and discoveries from MEMORY.md. Discard failed debugging attempts."`
```

### 4. Create godot-api skill

New skill at `skills/godot-api/SKILL.md`:

```yaml
---
name: godot-api
description: |
  Look up Godot engine class APIs — methods, properties, signals, enums.
  Use when you need to find which class to use or look up specific API details.
context: fork
model: sonnet
agent: Explore
---

# Godot API Lookup

$ARGUMENTS

## How to answer

1. Read `${CLAUDE_SKILL_DIR}/doc_api/_common.md` — index of ~128 common classes
2. If the class isn't there, read `${CLAUDE_SKILL_DIR}/doc_api/_other.md`
3. Read `${CLAUDE_SKILL_DIR}/doc_api/{ClassName}.md` for full API reference
4. Return only what was asked for — relevant methods, properties, signals with their signatures

Bootstrap if doc_api is empty: `bash ${CLAUDE_SKILL_DIR}/tools/ensure_doc_api.sh`
```

Put `doc_api/` and `tools/` (ensure_doc_api.sh, godot_api_converter.py, class_list.py) inside `skills/godot-api/`.

### 5. Update game.md template

Add to the game.md CLAUDE.md template:

```markdown
## Resumability

All pipeline state lives in files. After compaction or `/clear`, read these to resume:
- `PLAN.md` — task statuses and the full task DAG
- `STRUCTURE.md` — architecture, scene/script mappings, signal map
- `MEMORY.md` — discoveries and workarounds from completed tasks
- `ASSETS.md` — asset manifest with paths and art direction

Always keep these files up to date as you work.
```

### 6. Update publish.sh

- Only copies `skills/` (already does this)
- Verify skill count output is correct with the new layout (one skill becomes two: godogen + godot-api)

### 7. Delete skills/godot-task/

Remove entirely — everything is merged into godogen or godot-api.
