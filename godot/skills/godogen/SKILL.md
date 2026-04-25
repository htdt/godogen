---
name: godogen
display_name: Godogen
short_description: Generate or update complete Godot games
default_prompt: "Use ${GODOGEN_COMMAND} to build or update this Godot game from a natural-language design brief."
description: |
  Generate or update a complete Godot game from a natural-language description. Use when the user wants ${AGENT_NAME} to make, rebuild, or substantially extend a Godot project end to end.
---

# Game Generator — Orchestrator

Generate and update Godot games from natural language.

## Capabilities

Read each stage file from `${GODOGEN_SKILL_DIR}/` only when you reach that stage.

| File | Purpose | When to read |
|------|---------|--------------|
| `visual-target.md` | Generate reference image | Pipeline start |
| `decomposer.md` | Decompose into task plan | After visual target |
| `scaffold.md` | Architecture + skeleton | After decomposition |
| `asset-planner.md` | Budget and plan assets | If budget provided |
| `asset-gen.md` | Asset generation CLI ref | When generating assets |
| `rembg.md` | Background removal | Only when an asset needs transparency removed |
| `task-execution.md` | Task workflow + commands | Before first task |
| `quirks.md` | Godot gotchas | Before writing code |
| `scene-generation.md` | Scene builders | Targets include `.tscn` |
| `test-harness.md` | SceneTree verification scripts | Before writing capture/test scripts |
| `capture.md` | Screenshot/video capture + final result bundle | Before automated screenshots or video |
| `android-build.md` | APK export | User requests Android |
| *(godot-api skill)* | C# Godot syntax ref | When unsure about Godot API details |

## Pipeline

```text
User request
    |
    +- Check if PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md, ASSETS.md if present -> skip to task execution
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
    +- If final presentation media is required:
    |   +- Read test-harness.md and capture.md, produce a fresh screenshots/result/{N}/ bundle with raw frames and video.mp4 (task.md at project root; task_add.md only for narrower slices)
    |
    +- If user requested Android app:
    |   +- Read android-build.md, add ETC2/ASTC to project.godot, create export_presets.cfg, export APK
    |
    +- Summary of completed game
```

## Assets

**If a budget is provided, generating proper assets is part of the task, not optional.** Do not fall back to procedural primitives (boxes stacked into a human, spheres for heads, coloured quads for props) when the budget allows a real asset — plan and generate the asset through `asset-planner.md` / `asset-gen.md`. Procedural stand-ins are acceptable only for genuinely abstract shapes (platforms, blocks, particles) or when the asset-planner has explicitly ruled an asset out on budget grounds.

Placeholder primitives in gameplay code are a signal that the asset step was skipped — go back and generate the asset before continuing.

## Execution

Read `task-execution.md` before starting. Two phases:

1. **Risk tasks** (if any) — implement each in isolation, verify, commit
2. **Main build** — implement everything else, verify, present results, commit

If `PLAN.md` calls for presentation media, finish through the Godot test harness and capture flow in `test-harness.md` / `capture.md` and leave a fresh `screenshots/result/{N}/` proof bundle behind.

## Godot API Lookup

When you need to look up a Godot class API or C# Godot pattern, use the `godot-api` skill with a targeted query. It keeps large API docs out of the main pipeline.

Use the skill inline when you already know what class or symbol to inspect and can answer by searching `_common.md` / `_other.md` plus reading a small number of specific docs. Use a dedicated helper agent when you need to discover candidate classes, compare several classes, or read multiple or large docs and reduce them to a compact answer.

Be specific about what you need:

- **Targeted query** — ask for specific methods, signals, or syntax: `"CharacterBody3D: what method applies velocity and slides along collisions?"`
- **Full API** — only when you need to survey the whole class: `"full API for AnimationPlayer"`

## Context Hygiene

Keep important state in files so the pipeline can resume cleanly after long threads or compaction:

- **PLAN.md** — task statuses and verification criteria
- **STRUCTURE.md** — architecture reference
- **MEMORY.md** — discoveries, quirks, workarounds, what worked or failed
- **ASSETS.md** — asset manifest with paths and generation details

After completing each task: update `PLAN.md`, write discoveries to `MEMORY.md`, and commit. If the thread becomes noisy, summarize the important state into those files and continue from the artifacts instead of relying on conversational memory.

## Visual Verification

**Do not trust code alone — verify on screenshots, captured frames, and video.** Code that looks correct often still ships broken placement, wrong scale, clipped geometry, missing elements, or bad motion timing.

When code and media disagree, trust the media. Be skeptical: the job is to find what is still broken, not to argue that it is probably fine. If a requirement is not clearly visible, treat it as not done.

Inspect captures directly while you work, then finish with a fresh `screenshots/result/{N}/` proof bundle containing `video.mp4` and the raw `frameXXX.png` sequence used to encode it. The original task literal lives in `task.md` at the project root; only add `task_add.md` inside the bundle if it proves a slice narrower than the root task.
