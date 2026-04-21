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
| `capture.md` | Screenshot/video capture | Before automated screenshots or video |
| `visual-qa.md` | Visual QA (forked skill) | After capture |
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
    |   +- Read capture.md, produce PNG frames or stills, assemble final MP4 if needed
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

If `PLAN.md` calls for presentation media, finish through the Bevy capture flow in `capture.md`.

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

## Visual QA

**Don't trust code — verify on screenshots.** Code that looks correct often has broken placement, wrong scale, missing elements, clipped geometry, or bad motion timing.

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
