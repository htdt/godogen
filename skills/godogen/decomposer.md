# Game Decomposer

Decompose a game into a development plan — a small number of large tasks, each independently verifiable. The output is `PLAN.md`, the implementation strategy.

## Workflow

1. **Read `reference.png`** — understand what the game looks like: camera angle, scene complexity, number of visible entities, environment scope. Use this to judge which systems are needed and how to split tasks.
2. **Read the game description** — understand what the game is and its core technical requirements.
3. **Identify algorithmic risks** — filter for features requiring complex math, procedural generation, custom shaders, or novel physics. These are the only candidates for isolation.
4. **Bundle everything else** — group all standard game logic into large, consolidated tasks.
5. **Write `PLAN.md`** — the task DAG with verification criteria.

The task executor is a highly capable LLM agent that thrives on broad context. It can implement an entire standard game in one pass. Orchestrating many small tasks creates real costs: merge friction between tasks, loss of holistic context, overfocus on minor features, and compounding integration failures. Each additional task boundary is a place where things break.

**Minimize the total number of tasks.** A standard 2D arcade or puzzle game should rarely exceed 3 tasks. A complex game with genuinely hard algorithms might need 7.

**The exception:** Isolate a feature into its own early task ONLY when it involves genuine algorithmic risk — the kind of problem that fails unpredictably and needs multiple iteration cycles with clean signal. When such a task fails, you regenerate it alone without touching the rest of the game.

### What Counts as "Hard" (Isolate)

Features that fail unpredictably, require multiple iteration cycles, and produce ambiguous errors when mixed with other systems. This includes both algorithmic complexity and engine patterns that are notoriously brittle:

- **Procedural generation** — terrain, levels, meshes, dungeon layouts
- **Procedural animation** — runtime bone manipulation, inverse kinematics, ragdoll blending with animated states
- **Complex vehicle physics** — wheel colliders, suspension, drifting, motorcycle balance
- **Custom shaders** — water surfaces, portals, screen-space effects, dissolve/distortion
- **Runtime geometry** — destructible environments, CSG operations, mesh deformation
- **Dynamic navigation** — pathfinding that adapts to runtime obstacles, crowd simulation, flocking
- **Complex camera systems** — third-person with collision avoidance, cinematic rail transitions, split-screen

### What Counts as "Routine" (Bundle)

Patterns that Godot handles well out of the box and that a strong LLM implements reliably. Never isolate these:

- **CharacterBody movement** — walking, jumping, gravity, slopes (Godot's `move_and_slide` handles this)
- **Collision and triggers** — Area signals, damage on contact, pickups, zones
- **AnimationPlayer / AnimationTree** — playing premade animations, blend trees, state transitions
- **TileMap / GridMap levels** — tile-based or grid-based world building
- **NavigationAgent** — basic pathfinding on static navmesh (dynamic obstacles make it hard — see above)
- **UI with Control nodes** — HUD, menus, health bars, score display, pause screens
- **Spawning, timers, waves** — enemy spawners, cooldowns, wave progression
- **Camera follow** — smooth follow, lerp-based tracking, fixed offsets
- **State machines, input handling** — player states, input mapping, action buffering

## Output Format

Produce `PLAN.md`:


````markdown
# Game Plan: {Game Name}

## Game Description

{Original game description from the user, preserved verbatim.}

## 1. {Task Name}
- **Depends on:** (none)
- **Goal:** {What this task achieves and why it matters}
- **Requirements:**
  - {High-level, testable behavior}
  - {High-level, testable behavior}
- **Assets needed:** {What visual assets this task needs — type, approximate size, visual role. Omit if task needs no assets.}
- **Audio needed:** {What sounds this task needs — SFX triggers, music, ambient. Omit if task needs no audio.}
- **Verify:** {What screenshots should show to prove the task works. Specific and unambiguous.}

## 2. {Task Name}
- **Depends on:** 1
- ...

````

### Task Fields

- **Depends on** — task numbers that must complete before this starts. `(none)` for root tasks.
- **Goal** — what this task achieves and why it matters for the game.
- **Requirements** — high-level behaviors the task must achieve. Focus on *what* the player experiences, not *how* to implement it. The task executor is a highly capable LLM — it doesn't need implementation recipes. Specify concrete values only when they matter for game feel (e.g., "car should feel heavy, not twitchy") or correctness (e.g., "arena is 50m wide to fit 4 players").
- **Assets needed** — visual assets this task requires, described by type, approximate size, and visual role. Omit for tasks that don't need assets. The asset planner reads these and generates the actual files, then replaces this field with concrete **Assets:** assignments.
- **Audio needed** — sound effects and music this task requires, described by trigger event and character. Omit for tasks that don't involve audio. The asset planner reads these and generates the actual files.
- **Verify** — what the task's goal looks like when achieved. Describe the expected visual outcome: what objects are visible, what state they're in, what behavior is demonstrated. Must be concrete enough that a verifier seeing only screenshots can judge pass/fail. The task executor will choose camera angles, test actions, and frame timing.

## Decomposition Strategy

### The Two-Phase Approach

**Phase 1 — De-risk:** Scan for hard algorithmic features. If any exist, create isolated early tasks for them only. Each gets a minimal test environment that exercises the real challenge (not a simplified version that avoids it). These tasks run first so failures are caught with clean signal, before the rest of the game adds noise.

**Phase 2 — Bundle:** Once algorithmic risks are handled (or if the game has none), bundle ALL remaining standard logic into as few tasks as possible. A single task can encompass player mechanics, enemies, UI, scoring, and level design if they're all routine work.

### Examples of Correct Task Counts

**Bomberman** (no algorithmic risk): 2 tasks total.
1. Visual architecture — arena grid, walls, destructible blocks, player and enemy sprites, all correctly animated and scaled.
2. Core game loop — movement, bomb placement and detonation, chain reactions, enemy AI, health, HUD, win/lose conditions.

**3D flight game through procedural canyons** (algorithmic risk: procedural canyon geometry): 3 tasks.
1. Procedural canyon generation — narrow passages with working collision geometry, verified navigable.
2. Flight mechanics in canyon — plane controls tuned for tight spaces within the generated canyon.
3. Game completion — rings, scoring, HUD, game over conditions.

**Tower defense with custom pathfinding** (algorithmic risk: pathfinding + dynamic tower placement interaction): 3 tasks.
1. Pathfinding system — enemies follow paths, reroute when towers block, maintain spacing.
2. Tower placement and targeting — grid snapping, path validation, range detection, projectiles, damage.
3. Game loop — waves, economy, upgrade UI, win/lose.

### Independence = Blast Radius Control

Two hard features that don't share runtime state should be separate tasks with no dependency between them. When one fails and needs regeneration, the other is unaffected. But don't apply this principle to routine features — the merge cost of splitting them outweighs the isolation benefit.

### Verification Must Be Visual and Concrete

The Verify field describes what the task's goal looks like when achieved — the expected visual outcome, not intermediate steps. It must be specific enough that a verifier seeing only screenshots can judge pass/fail. The task executor chooses camera angles, test actions, and frame timing.

## Common Game Structures

Reference these by name in task goals — the task executor knows how to implement them:
spawn system, state machine, navigation/AI, HUD overlay, pause, turn-based combat, grid movement.

## Mandatory Final Task: Presentation Video

The last task in every plan is always a presentation video, just add it after everything else. It creates a ~30-second cinematic gameplay video as the final deliverable.

```markdown
## N. Presentation Video
- **Depends on:** {all other tasks}
- **Goal:** Create a ~30-second cinematic video showcasing the completed game.
- **Requirements:**
  - Write test/presentation.gd — a SceneTree script (extends SceneTree)
  - Showcase representative gameplay via simulated input or scripted animations
  - ~900 frames at 30 FPS (30 seconds)
  - Use Video Capture from godot-capture (AVI via --write-movie, convert to MP4 with ffmpeg)
  - Output: screenshots/presentation/gameplay.mp4
  - **3D games:** smooth camera work (orbits, tracking shots, dolly moves), good lighting (DirectionalLight3D key + fill/rim), post-processing (glow/bloom, SSAO, SSR, ACES tonemapping, volumetric fog)
  - **2D games:** camera pans and smooth scrolling, zoom transitions between overview and close-up, trigger representative gameplay sequences, tight viewport framing
- **Verify:** A smooth MP4 video showing polished gameplay with no visual glitches.
```

Adapt the 3D/2D requirements based on the game's dimension — include only the relevant set.

## What NOT to Include

- GDScript code or implementation details (task executor handles that)
- Detailed technical specs — the task executor is a strong LLM, it makes good implementation decisions on its own
- Micro-tasks for routine features (UI, simple collisions, input handling)
- Untestable requirements (everything must be visually verifiable)
- Artificial dependencies between independent systems
