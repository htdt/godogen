---
name: godot-decomposer
description: Decompose a game into a development plan — a sequence of small, independently verifiable tasks with dependencies
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Game Decomposer

You decompose a game into a development plan — a sequence of small tasks, each independently verifiable. The output is a markdown file that serves as the implementation strategy.

## Project Root

The caller specifies `{project_root}` (e.g. `project_root=build`). All file references below are relative to `{project_root}/`.

## Workflow

1. **Read the game description** — understand what the user wants to build.
2. **Read `{project_root}/STRUCTURE.md`** — understand the architecture (scenes, scripts, signals).
3. **Check for available assets** — list any files in `{project_root}/glb/` and `{project_root}/img/`.
4. **Identify risks** — classify every feature as hard or easy.
5. **Write `{project_root}/PLAN.md`** — the task DAG with verification criteria.
6. **Initialize `{project_root}/MEMORY.md`** — create with a heading and empty sections for agents to fill in.

## Why Decompose

Complex games fail when generated in one shot — too many interacting systems, too many things that can go wrong, and no way to tell what broke. Decomposition solves this by:

1. **Isolating risk** — each task is small enough to iterate to correctness on its own
2. **Verifying early** — every task has visual verification before it's integrated with others
3. **Focusing iteration** — when something fails, you regenerate one small task, not the whole game
4. **Surfacing the hard parts** — the decomposition forces you to identify what's actually difficult for *this specific game* and tackle it first

## Output Format

Produce a markdown file (`{project_root}/PLAN.md`) with the structure below. Implementation agents read this file, execute tasks in order, and update it as they go.

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
- **Placeholder:** {Minimal scaffolding to test in isolation. Must exercise the real challenge, not dodge it.}
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

- **Depends on** — task numbers that must be complete before this starts. `(none)` for root tasks.
- **Goal** — what this task achieves and why it matters for the game
- **Requirements** — concrete, testable behaviors. Include descriptions, dimensions, physics values — everything the generator needs. Each should be verifiable from a screenshot or gameplay test.
- **Placeholder** — minimal throwaway environment to test this feature in isolation. Must exercise the real challenge. `(none)` for merge tasks that inherit real environments from dependencies.
- **Verify** — a concrete, scripted visual scenario that will be turned into a test harness. Describe: what scene to load, where the camera should look, what objects/state should be visible, and what behavior should be occurring. Must be specific enough to generate a test script and judge pass/fail from screenshots. Example: "Load main.tscn. Camera at (0, 15, 10) looking down at -45°. A green ground plane fills the lower half. A capsule (player) stands at center. 3 red cubes (enemies) are spaced around the edges."
- **Targets** — scenes and scripts this task creates or modifies

### Asset Assignment

The decomposer assigns available assets to specific tasks. Each asset appears in the Assets table with its assigned task. Task requirements should mention which assets to use:

- "Use `car` GLB model for the player vehicle, scale to 4m long"
- "Apply `grass` texture to ground plane, tile every 2m"

### Project Memory

All agents working on this project share `{project_root}/MEMORY.md` as a living knowledge base. When an agent discovers something useful — what worked, what failed, a Godot quirk, a workaround, an architectural decision — it writes it there. Before starting work, agents should read this file for context from previous tasks.

Write entries that are useful to any agent on the project: both high-level decisions ("switched from RigidBody3D to CharacterBody3D for the player because...") and technical specifics ("car.glb faces +Z, needs PI rotation on Y"). Keep it organized by topic, not chronologically.

## Decomposition Strategy

### 1. Identify What's Actually Hard

Before writing any tasks, ask: **what is the core technical risk for this specific game?**

This is game-specific. "Player movement" is almost never the hard part — it's a well-understood pattern. The hard part is whatever makes *this* game different from a tutorial project.

**Classify every feature:**
- **Hard** — algorithmically complex, likely to need multiple iteration cycles (procedural generation, complex physics interactions, AI behavior, novel mechanics)
- **Easy** — well-understood patterns that rarely fail (basic movement, simple UI, score tracking, timers)

Hard features must become early tasks. They need iteration budget. Easy features can come later.

### 2. Test Features in Realistic Conditions

Each task needs a placeholder environment to be testable — but **the placeholder must exercise the real challenge.** A placeholder that avoids the hard part is useless.

- Testing flight controls in open sky (hides the real problem: tight spaces) — BAD
- Testing flight controls in a hardcoded tunnel (exercises the actual constraint) — GOOD
- Testing car physics on a flat plane (hides the real problem: curves and banking) — BAD
- Testing car physics on a hardcoded curved ramp (exercises the actual physics) — GOOD

**Rule:** The placeholder should create the conditions where the feature is most likely to fail.

### 3. Isolate Independent Features

Two features are independent when:
- They don't share runtime state
- They can each be tested with their own placeholder
- Changing one doesn't require changing the other

Independent features become separate tasks with no dependency between them. This isn't about speed — it's about **limiting blast radius**. When task A fails and needs regeneration, task B is unaffected.

### 4. Merge Progressively

Merge tasks integrate previously-independent features. This is where things break — systems that worked in isolation may conflict.

- Integrate 2-3 things at a time, not everything at once: A+B -> AB, then AB+C -> ABC
- Merge requirements focus on **integration behavior** ("bullets fired by player damage enemies"), not re-specifying individual features
- Note potential friction points ("player velocity may affect bullet trajectory")

### 5. Group Coherent Behaviors

A single "feature" should be ONE task. Don't over-split things that can't be tested independently:

- "Player accelerates" -> "Player turns" -> "Player brakes" (can't test turning without movement) — BAD
- "Player vehicle physics: acceleration, steering, braking" (one coherent task) — GOOD

**Rule of thumb:** If you can't test one part without the other, they belong in the same task.

### 6. Visual Verification Must Be Unambiguous

The Verify field drives a test harness that captures screenshots. Describe what the camera sees, not what the code does:

- "Movement works" — BAD (not visual, can't generate test)
- "Load main.tscn. Camera at (0, 10, 8) facing -45° down. Capsule visible on flat green plane. After 2s, capsule has moved forward ~3 units." — GOOD
- "Integration successful" — BAD
- "Load main.tscn. Player capsule at center. 3 red cubes spaced at edges. A small sphere (bullet) visible between player and nearest cube." — GOOD

Include: scene to load, camera position/angle, what objects are visible, colors/shapes, expected positions or state changes over time.

### 7. Decorations and Polish Come Last

Props, particles, visual effects — always the final tasks. If the game doesn't work, decoration is wasted effort.

## Common Anti-Patterns

- **Testing in easy conditions** — Flight in open sky, car on flat road. The placeholder must exercise the real challenge.
- **Artificial sequential chains** — Don't make B depend on A just because A sounds like it should "come first." If they can be tested independently, they're independent tasks.
- **One giant merge at the end** — Integrate progressively (A+B, then AB+C), not everything at once.
- **Splitting inseparable behaviors** — Movement + jump + gravity are one task, not three.
- **Burying the hard part late** — If the hardest challenge is integration, it should happen early with simplified dependencies.

## Plan Validation

Before outputting, verify:

1. **No cycles** — if A depends on B, B cannot depend on A
2. **All dependencies exist** — every referenced task number is defined
3. **Hard tasks are early** — complex features are not blocked behind easy ones
4. **Merge tasks integrate 2-3 things** — not everything at once
5. **Placeholders exercise real challenges** — no "flat plane" for a game about terrain
6. **Every task is verifiable** — Verify describes a concrete visual scenario with camera position, visible objects, and expected state
7. **All assets assigned** — every available asset appears in the Assets table with a task

## What NOT to Include

- Specific GDScript code (generators write that)
- Features without visual feedback
- Untestable requirements
- Artificial dependencies between actually-independent features
