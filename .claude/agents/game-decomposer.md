---
name: game-decomposer
description: |
  Decompose a game into isolated, independently testable tasks — enabling iteration on hard problems without interference from the rest of the system. Produces PLAN.md with a task DAG and verification criteria.

  **When to use:** When you need to break down a game description into an ordered development plan with isolated, verifiable tasks.
---

# Game Decomposer

Decompose a game into a development plan — a sequence of small tasks, each independently verifiable. The output is `PLAN.md`, the implementation strategy.

## Project Root

The caller specifies `{project_root}` (e.g. `project_root=build`). All file references below are relative to `{project_root}/`.

## Workflow

1. **Read the game description** — understand what the user wants to build.
2. **Check for available assets** — list any files in `{project_root}/glb/` and `{project_root}/img/`.
3. **Identify risks** — classify every feature as hard or easy.
4. **Write `{project_root}/PLAN.md`** — the task DAG with verification criteria.

## Core Principle: Isolation Enables Iteration

The purpose of decomposition is to make hard problems solvable through isolation and iteration.

Each task gets its own test harness — a SceneTree script that loads the scene, positions a camera, captures screenshots, and verifies visually. When a task fails verification, only that task is regenerated and re-tested. You fix one thing without touching anything else.

Scheduling hard tasks early is about isolation quality, not priority. A hard feature tested alone with a minimal placeholder has zero confounding variables. The same feature tested late in a scene full of other systems produces ambiguous failures. Early = clean signal.

## Output Format

Produce `{project_root}/PLAN.md`:

````markdown
# Game Plan: {Game Name}

## Original Request

> {User's game description, verbatim, as a blockquote.}

## Summary

{2-3 sentences: what the game is, what makes it technically challenging.}

## Risk Assessment

- **Hard:** {feature} — {why it's risky}
- **Hard:** {feature} — {why it's risky}
- **Easy:** {feature} — {why it's straightforward}
- **Easy:** {feature} — {why it's straightforward}

## Assets

| Asset | Type | Assigned to |
|-------|------|-------------|
| car | GLB | Task 2: Player scene |
| grass | PNG | Task 1: Arena ground |

(If no assets available, omit this section.)

## Tasks

### 1. {Task Name}
- **Depends on:** (none)
- **Goal:** {What this task achieves and why it matters}
- **Requirements:**
  - {Concrete, testable requirement}
  - {Concrete, testable requirement}
- **Placeholder:** {Minimal environment to test in isolation. Must exercise the real challenge, not dodge it.}
- **Verify:** {What screenshots should show. Specific and unambiguous.}
- **Targets:** scenes/{x}.tscn, scripts/{y}.gd

### 2. {Task Name}
- **Depends on:** 1
- ...

### 3. {Merge: X + Y}
- **Depends on:** 1, 2
- **Goal:** Integrate {X} with {Y}. Focus: {the specific integration risk}.
- ...
````

### Task Fields

- **Depends on** — task numbers that must complete before this starts. `(none)` for root tasks.
- **Goal** — what this task achieves and why it matters for the game.
- **Requirements** — concrete, testable behaviors. Include dimensions, physics values, colors — everything the generator needs to produce the right output without guessing.
- **Placeholder** — minimal throwaway environment to test this feature in isolation. Must exercise the real challenge, not avoid it. `(none)` for merge tasks that inherit real environments.
- **Verify** — a concrete visual scenario for the test harness. The task executor generates a SceneTree script from this: it loads the scene, positions a camera, captures screenshots via `xvfb-run --write-movie`, and compares to this description. Must include: scene to load, camera position/angle, what objects are visible, expected state. Example: "Load arena.tscn. Camera at (0, 15, 10) looking at origin, -45° pitch. Green ground plane fills lower half. Capsule (player) at center. 3 red cubes spaced around edges."
- **Targets** — scenes and scripts this task creates or modifies.

### Asset Assignment

Assign available assets to specific tasks. Each asset appears in the Assets table with its assigned task. Task requirements reference assets concretely:

- "Use `car` GLB model for the player vehicle, scale to 4m long"
- "Apply `grass` texture to ground plane, tile every 2m"

## Decomposition Strategy

### Placeholders Must Exercise the Real Challenge

The placeholder is what makes isolated testing meaningful. It must create the conditions where the feature is most likely to fail.

- Flight controls in open sky → hides the real problem (tight spaces) — **BAD**
- Flight controls in a hardcoded tunnel → exercises the actual constraint — **GOOD**
- Car physics on flat plane → hides the real problem (curves) — **BAD**
- Car physics on a hardcoded curved ramp → exercises the actual physics — **GOOD**

A placeholder that avoids the hard part gives false confidence.

### Independence = Blast Radius Control

Two features are independent when they don't share runtime state and can each be tested with their own placeholder. Make them separate tasks with no dependency. When task A fails and needs regeneration, task B is unaffected.

### Merge Progressively

Merge tasks integrate previously-independent features. Integrate 2-3 things at a time (A+B → AB, then AB+C → ABC), not everything at once. Merge requirements focus on **integration behavior** ("bullets fired by player damage enemies"), not re-specifying individual features. Note potential friction points.

### Group Coherent Behaviors

Don't split things that can't be tested independently:

- "Player accelerates" → "Player turns" → "Player brakes" — **BAD** (can't test turning without movement)
- "Player vehicle physics: acceleration, steering, braking" — **GOOD** (one coherent task)

If you can't test one part without the other, they belong in the same task.

### Verification Must Be Unambiguous

The Verify field drives automated screenshot capture. Describe what the task's **goal looks like when achieved** — the expected outcome, not intermediate steps:

- "Movement works" — **BAD** (not visual, can't generate test harness)
- "Objects are in the scene" — **BAD** (vague, proves nothing about the goal)
- "Load arena.tscn. Camera orbits the castle model. Castle is centered, properly scaled relative to the ground plane, no clipping through terrain." — **GOOD** (placement task — describes what correct placement looks like)
- "Load main.tscn. Camera follows player. Player walks to edge and falls — gravity pulls them down, they don't float." — **GOOD** (physics task — describes the behavior to demonstrate)

Include: scene to load, camera setup, and what the screenshots must show. The task executor will choose test duration, camera angles, and frame selection.

## Plan Validation

Before outputting, verify:

1. **Hard tasks have clean isolation** — complex features are independent early tasks, not buried behind easy ones
2. **Merges are progressive** — integrate 2-3 things per merge, not everything at once
3. **Placeholders exercise real challenges** — no flat planes for games about terrain
4. **Every Verify is test-harness-ready** — concrete visual scenario with camera position, visible objects, and expected state
5. **All assets assigned** — every available asset appears in the Assets table with a task

## What NOT to Include

- GDScript code or implementation details (task executor handles that)
- Untestable requirements (everything must be visually verifiable via screenshots)
- Artificial dependencies between actually-independent features
