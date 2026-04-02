# Game Decomposer

Analyze a game for implementation risks and define verification criteria. Output is `PLAN.md`.

## Workflow

1. **Read `reference.png`** — camera angle, scene complexity, entity count, environment scope.
2. **Read the game description** — core technical requirements.
3. **Scan for risks** — identify features needing isolation (see taxonomy below).
4. **Define verification criteria** — risk-specific, general, and final.
5. **Write `PLAN.md`.**

## Risk Taxonomy

### Isolate

Features that fail unpredictably and produce ambiguous errors when mixed with other systems:

- **Procedural generation** — terrain, levels, meshes, dungeon layouts
- **Procedural animation** — runtime bone manipulation, IK, ragdoll blending. Motions jerk, blend weights fight, limbs overshoot.
- **Sprite/character animations** — multi-direction movement, state transitions. Almost always fail first pass: wrong frames for direction, transitions stutter or pop.
- **Complex vehicle physics** — wheel colliders, suspension, drifting, motorcycle balance
- **Custom shaders** — water surfaces, portals, screen-space effects, dissolve/distortion
- **Runtime geometry** — destructible environments, CSG operations, mesh deformation
- **Dynamic navigation** — pathfinding adapting to runtime obstacles, crowd simulation, flocking
- **Complex camera systems** — third-person with collision avoidance, cinematic rail transitions, split-screen

### Never isolate

Patterns Godot handles well: CharacterBody movement, collision/triggers, TileMap/GridMap, NavigationAgent on static navmesh, UI with Control nodes, spawning/timers/waves, camera follow, state machines, input handling.

## Verification Criteria

Each task gets a **Verify** field inline — what to check after implementation.

**Risk tasks** — target the exact failure mode (e.g., for animations: "every direction plays correct frames, transitions smooth, no pose snapping").

**Main build** — combine cross-cutting checks with game-specific ones:
- Movement direction matches player input
- Animation direction matches movement direction
- Player input -> character response feels correct
- Physics objects respond to gravity/collision
- UI readable, no overflow or overlap
- No missing textures (magenta/checkerboard)
- Game-specific checks (e.g., "enemies path around towers," "score increments on pickup")
- reference.png consistency
- Presentation video as final deliverable

## Output Format

Produce `PLAN.md`:

````markdown
# Game Plan: {Name}

## Game Description

{Original description, verbatim.}

## Risk Tasks

{Omit entirely if no risks identified.}

### 1. {Risk Feature}
- **Why isolated:** {what makes this algorithmically hard}
- **Verify:** {specific criteria targeting the failure mode}

## Main Build

{What to build — all routine systems. High-level, not implementation recipes.}

- **Assets needed:** {visual assets the game needs — type, approximate size, visual role. Omit if none.}
- **Verify:**
  - {General checks: movement/input/animation alignment, physics, UI, textures}
  - {Game-specific checks}
  - Gameplay flow matches game description
  - No visual glitches, clipping, or placeholder assets
  - reference.png consistency: color palette, scale, camera angle, visual density
  - **Presentation video:** ~30s cinematic MP4 showcasing gameplay
    - Write test/presentation.gd (SceneTree script), ~900 frames at 30 FPS
    - **3D:** smooth camera work, good lighting, post-processing
    - **2D:** camera pans, zoom transitions, tight viewport framing
    - Output: screenshots/presentation/gameplay.mp4
````

Include only the relevant 3D/2D presentation requirements.

## What NOT to Include

- GDScript code or implementation details
- Detailed technical specs
- Micro-tasks for routine features
- Untestable requirements
- Artificial boundaries between routine systems
