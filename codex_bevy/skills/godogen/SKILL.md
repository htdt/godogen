---
name: godogen
description: |
  Generate or update a complete Bevy game from a natural-language description. Use when the user wants Codex to make, rebuild, or substantially extend a Bevy project end to end.
---

# Bevy Game Generator

Generate and update Bevy games from natural language.

## Capabilities

Read each stage file from `.agents/skills/godogen/` only when you reach that stage.

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
| `visual-qa.md` | Visual QA usage | After capture |
| *(bevy-help skill)* | Current Bevy API, examples, and architecture help | For any Bevy-specific question |

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

**If a budget is provided, generating proper assets is part of the task, not optional.** Do not fall back to procedural primitives when the budget allows a real asset. Plan and generate the asset through `asset-planner.md` / `asset-gen.md`.

Procedural stand-ins are acceptable only for genuinely abstract shapes (platforms, blockers, particles) or when the asset planner has explicitly ruled an asset out on budget grounds.

Placeholder primitives in gameplay code are a signal that the asset step was skipped. Go back and generate the asset before continuing.

## Execution

Read `task-execution.md` before starting. Two phases:

1. **Risk tasks** (if any) — implement each in isolation, verify, commit
2. **Main build** — implement everything else, verify, present results, commit

If `PLAN.md` calls for presentation media, finish through the Bevy capture flow in `capture.md`.

## Bevy Help

When you need Bevy-specific help, use the `bevy-help` skill with a targeted query. It keeps large reference material out of the main pipeline while giving you version-aware access to rustdoc, the checked-out Bevy repo, official examples, and Learn docs.

Use the skill inline when you already know what class, trait, system pattern, or example to inspect and can answer by reading a small number of docs. Use a dedicated helper agent when you need to discover candidate APIs, compare several patterns, or read multiple or large docs and reduce them to a compact answer.

Be specific about what you need:

- **Targeted query** — ask for a concrete symbol or pattern: `"Camera3d: what is the Bevy 0.18 pattern for rendering to an image target?"`
- **Full API** — only when you need to survey the whole type: `"full API for AssetServer"`

## Context Hygiene

Keep important state in files so the pipeline can resume cleanly after long threads or compaction:

- **PLAN.md** — task statuses and verification criteria
- **STRUCTURE.md** — architecture reference
- **MEMORY.md** — discoveries, quirks, workarounds, what worked or failed
- **ASSETS.md** — asset manifest with paths and generation details

After completing each task: update `PLAN.md`, write discoveries to `MEMORY.md`, and commit. If the thread becomes noisy, summarize the important state into those files and continue from the artifacts instead of relying on conversational memory.

## Visual QA

**Do not trust code alone — verify on screenshots.** Code that looks correct often has broken placement, wrong scale, missing elements, clipped geometry, or bad motion timing.

Two levels of validation:

- **Quick check** — inspect the screenshot yourself for small, targeted changes where you know exactly what to look for.
- **VQA skill** — use the `visual-qa` skill for end-to-end validation, after major changes, or whenever you need a fresh assessment. Pass `--both` for Gemini plus native image analysis when higher confidence is worth the cost.

Run Gemini-only VQA inline. For `--native` or `--both`, invoke `visual-qa` in a dedicated helper agent so image review starts from a fresh context.

Read `visual-qa.md` for invocation modes and context passing. Save VQA output to `visual-qa/{N}.md`.

Handling verdicts:

- **pass/warning** — move on
- **fail** — fix the issue. After 3 fix cycles:
  - **Replan** — if the root cause is upstream (architecture, assets)
  - **Escalate** — surface to the user if you cannot determine the fix

Never silently ignore a fail verdict. If you believe it is a false positive, report that explicitly and let the user decide.
