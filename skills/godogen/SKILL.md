---
name: godogen
description: |
  This skill should be used when the user asks to "make a game", "build a game", "generate a game", or wants to generate or update a complete Godot game from a natural language description.
---

# Game Generator — Orchestrator

Generate and update Godot games from natural language.

## Capabilities

Read each sub-file from `${CLAUDE_SKILL_DIR}/` when you reach its pipeline stage.

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
| *(godot-api skill)* | GDScript syntax ref | When unsure about GDScript syntax |
| `scene-generation.md` | Scene builders | Targets include .tscn |
| `test-harness.md` | Verification scripts | Before test harness |
| `capture.md` | Screenshot/video | Before capture |
| `visual-qa.md` | Visual QA (forked skill) | After capture |
| `android-build.md` | APK export | User requests Android |

## Pipeline

```
User request
    |
    +- Check if PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md -> skip to task execution
    |   +- If no: continue with fresh pipeline below
    |
    +- Generate visual target -> reference.png + ASSETS.md (art direction only)
    +- Decompose into tasks -> PLAN.md
    +- Design architecture -> STRUCTURE.md + project.godot + stubs
    |
    +- If budget provided (and no asset tables in ASSETS.md):
    |   +- Plan and generate assets -> ASSETS.md + updated PLAN.md with asset assignments
    |
    +- For every task in PLAN.md:
    |   +- Set `**Status:** pending`
    |   +- Fill `**Targets:**` with concrete project-relative files expected to change
    |     (e.g. scenes/main.tscn, scripts/player_controller.gd, project.godot)
    |     inferred from task text + scene/script mappings in STRUCTURE.md
    |
    +- Show user a concise plan summary (game name, numbered task list)
    |
    +- Execute tasks (see Running Tasks below)
    |
    +- If user requested Android app:
    |   +- Read android-build.md, add ETC2/ASTC to project.godot, create export_presets.cfg, export APK
    |
    +- Summary of completed game
```

PLAN.md task `**Status:**`: one of `pending`, `in_progress`, `done`, `done (partial)`, `skipped`.

## Running Tasks

Read `task-execution.md` before starting the first task. Execute each task:

1. Read the task block from PLAN.md
2. Mark status -> in_progress
3. Read target-specific sub-files (scene-generation, script-generation, etc.)
4. Execute the implement -> validate -> capture -> VQA loop
5. Mark completed in PLAN.md
6. git add . && git commit
7. Move to next ready task

## Godot API Lookup

When you need to look up a Godot class API (methods, properties, signals), use `Skill(skill="godot-api")` with your query. This runs in a separate context to avoid loading large API docs into the main pipeline.

Be specific about what you need — the docs are comprehensive and full returns are large:
- **Targeted query** — ask for specific methods/signals to get a concise answer: `"CharacterBody3D: what method applies velocity and slides along collisions?"`
- **Full API** — only request when you need to survey the entire class: `"full API for AnimationPlayer"`

Examples:
- Skill(skill="godot-api") "TileMapLayer: methods for setting/getting cells and their alternatives"
- Skill(skill="godot-api") "full API for CharacterBody3D"
- Skill(skill="godot-api") "which class handles 2D particle effects?"
- Skill(skill="godot-api") "GDScript: tween parallel syntax and callbacks"

## Visual QA

After capturing screenshots, verify with `Skill(skill="visual-qa")`. Runs in a forked context with Claude's native vision.

- **Static:** `Skill(skill="visual-qa") "Check reference.png against screenshots/{task}/frame0003.png — Goal: ..., Verify: ..."`
- **Dynamic:** `Skill(skill="visual-qa") "Check reference.png against frame1.png frame2.png ... — Goal: ..., Verify: ..."`
- **Question:** `Skill(skill="visual-qa") "Are surfaces showing magenta? screenshots/{task}/frame*.png"`

Save output to `visual-qa/{N}.md`. See `visual-qa.md` for full usage.

## Context Hygiene

Keep important state in files so the pipeline can resume even after compaction or clear:

- **PLAN.md** — task statuses, always up to date before moving on
- **STRUCTURE.md** — architecture reference, update if scaffolding changes
- **MEMORY.md** — discoveries, quirks, workarounds, what worked/failed
- **ASSETS.md** — asset manifest with paths and generation details

After completing each task: update PLAN.md status, write discoveries to MEMORY.md, git commit. This ensures the pipeline can resume from any point by reading these files.

If the context becomes polluted from debugging loops, manually compact with:
`/compact "Discard failed debugging attempts."`

## Visual QA

Visual QA runs inline with each task. **Never ignore a fail verdict** — always act on it before marking a task done.

**VQA reports are clear signal.** If a significant issue is reported, fix it. If you genuinely believe it's a false positive — report it to the user and let them decide. Never silently ignore a fail verdict.

- **pass/warning** — move on.
- **fail** — fix the issue. If you've already attempted up to 3 fix cycles, decide:
  - **Replan** — reset architecture, rewrite plan, and/or regenerate assets if the root cause is upstream.
  - **Escalate** — surface the issue to the user if you can't determine the right fix.

The final task in PLAN.md is a presentation video — a script that showcases gameplay in a ~30-second cinematic MP4.
