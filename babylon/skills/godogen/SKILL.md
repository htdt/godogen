---
name: godogen
display_name: Godogen
short_description: Build or update Babylon.js browser games interactively, delivered as a live URL
default_prompt: "Use ${GODOGEN_COMMAND} to build or update this Babylon.js browser game from a natural-language design brief."
description: |
  Generate or update a complete Babylon.js browser game from a natural-language description, working interactively with the user. Use when the user wants ${AGENT_NAME} to make, rebuild, or substantially extend a Babylon.js project. The game is delivered as a live URL the user watches and steers.
---

# Babylon Game Generator

Build and update Babylon.js browser games interactively. The deliverable is a **live URL**: the user keeps `http://127.0.0.1:5173` open and watches the game update as you work. Checkpoint at the decisions that depend on their taste or intent; otherwise keep building.

## Capabilities

Read each stage file from `${GODOGEN_SKILL_DIR}/` only when you reach that stage.

| File | Purpose | When to read |
|------|---------|--------------|
| `interactive.md` | Checkpoint protocol + live-URL delivery | Pipeline start |
| `decomposer.md` | Light read of the task + thin, revisable plan | After the opening conversation |
| `visual-target.md` | Generate a reference image (CLI) | Only if a reference earns its cost |
| `scaffold.md` | Vite/Babylon project shell + scene router | When creating/refreshing the shell |
| `architecture.md` | Babylon gameplay architecture stance | Before designing game code |
| `asset-planner.md` | Budget and plan assets | When you generate assets during the build (budget provided) |
| `asset-gen.md` | Asset generation CLI ref | When generating assets |
| `rembg.md` | Background removal | Only when an asset needs transparency removed |
| `task-execution.md` | Task workflow + commands | Before first task |
| `quirks.md` | Babylon/browser gotchas | Before writing code |
| `scene-generation.md` | Scene/router implementation patterns | When creating or replacing a scene |
| `capture.md` | Browser screenshots for self-verification | Before taking screenshots |
| *(babylon-help skill)* | Babylon/Vite/browser API lookup | For Babylon-specific questions |

## Pipeline

This is a set of moves, not a rigid sequence. The fixed parts are: read before you propose, scaffold before you can show a URL, and the live URL is the deliverable. Everything else — reference, assets, isolation, polish — happens when it earns its place, interleaved with the build. Scale the ceremony to the task: a small change to an existing game drops straight into the build loop, while a fresh, ambitious brief earns the full opening conversation.

```text
User request
    |
    +- Resume check: PLAN.md exists? -> read state, confirm with the user what to continue
    |
    +- Opening conversation (interactive.md + decomposer.md Pass 1):
    |   +- Light read: what the game is, the hard/uncertain parts, rough asset
    |   |  sense, the smallest thing worth showing live first
    |   +- Reference decision: simple/low-benefit -> skip and say why; else propose a
    |   |  specific scene, generate, serve at /reference.png, ask usage mode
    |   +- Propose a build approach (shaped by the read), let the user choose
    |
    +- Scaffold/refresh the Vite project; start `npm run dev`; SURFACE the URL
    +- Write a thin PLAN.md in the chosen approach's shape (decomposer.md Pass 2)
    |
    +- Build live in ?scene=main, the user watching. Make these moves when the
    |  moment calls for them, not on a fixed schedule:
    |   +- Assets: time them to where the work is — placeholders first when the
    |   |  substance is logic, real assets first when it is the art (confirm cost first)
    |   +- Isolation: spin up a ?scene=X route only when main is too noisy or asked
    |   +- Checkpoint at slice boundaries; revise PLAN.md; let the user steer anytime
    |
    +- Deliverable is the live URL(s)
```

## Execution

Read `task-execution.md` before starting. Keep `npm run dev` alive so the user can watch. The inner loop:

1. Edit `src/game/**` or `src/assets/**`.
2. Refresh the browser to see the change (your `capture.mjs` check navigates a fresh page).
3. Self-verify with a screenshot when the change is visual; let the user judge motion live.
4. Run `npm run check` before larger edits and `npm run build` as a compile gate.

Build in `?scene=main` by default. Isolation into a separate `?scene=` route is on demand — only when the main scene is too noisy to judge a feature, or the user asks. See `interactive.md` for the checkpoint protocol and `scene-generation.md` for the router contract.

Chrome/Chromium and WebGL2 are required for your own screenshot checks. If either is missing, report it rather than working around it. A `[capture] WARNING` about a software renderer (SwiftShader, llvmpipe, lavapipe) means the browser GPU path is misconfigured on a GPU host — fix it; on a GPU-less host it is informational.

## Babylon Help

Use `babylon-help` for Babylon API questions, examples, loader behavior, Vite integration, or exact import paths. Prefer the installed npm package sources/types for the current project version, then official docs.

## Context Hygiene

Keep state in files so the work survives long threads and compaction:

- `PLAN.md` — a living doc: current slice, what the user has reviewed live, open questions, and the chosen approach + reference-usage mode
- `STRUCTURE.md` — architecture/router reference
- `MEMORY.md` — discoveries, quirks, workarounds, what worked or failed
- `ASSETS.md` — asset manifest with paths and generation details

Revise `PLAN.md` at each checkpoint, not just at the end. Commit after verified slices when the repo policy or user asks for commits.

## Visual Verification

Do not trust code alone. Self-verify visible work with a screenshot before showing the user, and let the user confirm motion and feel on the live URL. When code and the browser disagree, trust the browser.
