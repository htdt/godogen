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
| `rembg.md` | Background removal | Only when an asset needs transparency removed |
| `task-execution.md` | Task workflow + commands | Before first task |
| `quirks.md` | Godot gotchas | Before writing code |
| *(godot-api skill)* | C# Godot syntax ref | When unsure about C# Godot syntax |
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
    +- Analyze risks + define verification criteria -> PLAN.md
    +- Design architecture -> STRUCTURE.md + project.godot + stubs
    |
    +- If budget provided (and no asset tables in ASSETS.md):
    |   +- Plan and generate assets -> ASSETS.md + updated PLAN.md with asset assignments
    |
    +- Show user a concise plan summary (risk tasks if any, main build scope)
    |
    +- Execute (see Execution below)
    |
    +- If user requested Android app:
    |   +- Read android-build.md, add ETC2/ASTC to project.godot, create export_presets.cfg, export APK
    |
    +- Summary of completed game
```

## Execution

Read `task-execution.md` before starting. Three phases:

1. **Risk tasks** (if any) — implement each in isolation, verify, commit
2. **Main build** — implement everything else, verify, present results (video for new games), commit

The final task in PLAN.md is a presentation video — a ~30-second cinematic MP4 showcasing gameplay.

## Godot API Lookup

When you need to look up a Godot class API (methods, properties, signals), use `Skill(skill="godot-api")` with your query. This runs in a separate context to avoid loading large API docs into the main pipeline.

Be specific about what you need — the docs are comprehensive and full returns are large:
- **Targeted query** — ask for specific methods/signals to get a concise answer: `"CharacterBody3D: what method applies velocity and slides along collisions?"`
- **Full API** — only request when you need to survey the entire class: `"full API for AnimationPlayer"`

Examples:
- Skill(skill="godot-api") "TileMapLayer: methods for setting/getting cells and their alternatives"
- Skill(skill="godot-api") "full API for CharacterBody3D"
- Skill(skill="godot-api") "which class handles 2D particle effects?"
- Skill(skill="godot-api") "C#: tween parallel syntax and callbacks"

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

**Don't trust code — verify on screenshots.** Code that looks correct often has broken placement, wrong scale, missing elements, or clipped geometry.

**Two levels of validation:**

- **Quick check** — read the screenshot yourself with Read. Use for small, targeted changes where you know exactly what to look for. Be aware: you are biased toward confirming your own work, especially code you just wrote.
- **VQA skill** — `Skill(skill="visual-qa")` runs in a forked context with Gemini (unbiased, no knowledge of your code). Use for end-to-end validation, after major changes, or whenever you need a fresh assessment. Pass `--both` for Gemini + Claude when higher confidence is needed.

Read `visual-qa.md` for invocation modes (static/dynamic/question) and context passing. Save VQA output to `visual-qa/{N}.md`.

**Handling verdicts:**

- **pass/warning** — move on.
- **fail** — fix the issue. After 3 fix cycles:
  - **Replan** — if root cause is upstream (architecture, assets).
  - **Escalate** — surface to user if you can't determine the fix.

Never silently ignore a fail verdict. If you believe it's a false positive — report to user, let them decide.
