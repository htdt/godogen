---
name: godogen
description: |
  This skill should be used when the user asks to "make a game", "build a game", "generate a game", or wants to generate or update a complete Bevy game from a natural language description.
---

# Bevy Game Generator — Orchestrator

Generate and update Bevy games from natural language.

## Capabilities

Read each sub-file from `${CLAUDE_SKILL_DIR}/` when you reach its pipeline stage.

| File | Purpose | When to read |
|------|---------|--------------|
| `visual-target.md` | Generate reference image | Pipeline start |
| `decomposer.md` | Decompose into task plan | After visual target |
| `scaffold.md` | Architecture + skeleton | After decomposition |
| `asset-planner.md` | Budget and plan assets | If budget provided |
| `asset-gen.md` | Asset generation CLI ref | When generating assets |
| `rembg.md` | Background removal | Only when an asset needs transparency removed |
| `task-execution.md` | Task workflow + commands | Before first task |
| `quirks.md` | Bevy gotchas | Before writing code |
| `scene-generation.md` | Code-first world construction | When creating or replacing the default playable scene |
| `capture.md` | Screenshot/video capture + final result bundle | Before automated screenshots or video |
| *(bevy-help skill)* | Current Bevy API, examples, and architecture help | For any Bevy-specific question |

## Pipeline

```
User request
    |
    +- Check if PLAN.md exists (resume check)
    |   +- If yes: read PLAN.md, STRUCTURE.md, MEMORY.md, ASSETS.md if present -> skip to task execution
    |   +- If no: continue with fresh pipeline below
    |
    +- Generate visual target -> reference.png + ASSETS.md (art direction only)
    +- Analyze risks + define verification criteria -> PLAN.md
    +- Design architecture -> STRUCTURE.md + Cargo.toml + src/ stubs
    |
    +- If budget provided (and no asset tables in ASSETS.md):
    |   +- Plan and generate assets -> ASSETS.md + updated PLAN.md with asset assignments
    |
    +- Show user a concise plan summary (risk tasks if any, main build scope)
    |
    +- Execute (see Execution below)
    |
    +- If final presentation media is required:
    |   +- Read capture.md, produce a fresh screenshots/result/{N}/ bundle with raw frames, video.mp4, and task.md
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

If `PLAN.md` calls for presentation media, finish through the Bevy capture flow in `capture.md` and leave a fresh `screenshots/result/{N}/` proof bundle behind.

## Bevy Help

When you need Bevy-specific help, use `Skill(skill="bevy-help")` with your query. This runs in a separate context to avoid loading large reference material into the main pipeline while giving you version-aware access to rustdoc, the checked-out Bevy repo, official examples, and Learn docs.

Be specific about what you need — the docs are comprehensive and full returns are large:
- **Targeted query** — ask for a concrete symbol or pattern: `"Camera3d: what is the Bevy 0.18 pattern for rendering to an image target?"`
- **Full API** — only request when you need to survey the whole type: `"full API for AssetServer"`

Examples:
- Skill(skill="bevy-help") "Camera3d: pattern for rendering to an image target"
- Skill(skill="bevy-help") "full API for AssetServer"
- Skill(skill="bevy-help") "which components drive 2D sprite animation?"
- Skill(skill="bevy-help") "AnimationPlayer: how to play a clip once and listen for completion"

## Context Hygiene

Keep important state in files so the pipeline can resume even after compaction or clear:

- **PLAN.md** — task statuses, always up to date before moving on
- **STRUCTURE.md** — architecture reference, update if scaffolding changes
- **MEMORY.md** — discoveries, quirks, workarounds, what worked/failed
- **ASSETS.md** — asset manifest with paths and generation details

After completing each task: update PLAN.md status, write discoveries to MEMORY.md, git commit. This ensures the pipeline can resume from any point by reading these files.

If the context becomes polluted from debugging loops, manually compact with:
`/compact "Discard failed debugging attempts."`

## Visual Verification

**Do not trust code alone — verify on screenshots, captured frames, and video.** Code that looks correct often still ships broken placement, wrong scale, clipped geometry, missing elements, or bad motion timing.

When code and media disagree, trust the media. Be skeptical: the job is to find what is still broken, not to argue that it is probably fine. If a requirement is not clearly visible, treat it as not done.

Inspect captures directly while you work, then finish with a fresh `screenshots/result/{N}/` proof bundle containing `video.mp4`, the raw `frameXXX.png` sequence used to encode it, and `task.md` with the exact task that bundle proves.
