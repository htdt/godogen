# Game Reader

Read the task well enough to propose an approach, then write a thin plan in the shape of the approach the user picks. Planning is emergent: the plan starts small and grows as the user reacts on the live URL — it is not a frozen up-front contract.

This runs in two passes around the approach checkpoint (`interactive.md`).

## Runtime limitations

Babylon output runs in the browser. The pipeline does not ship native or mobile packaging, and browser audio cannot play before a user gesture. If the brief assumes a native build or background audio with no interaction, drop those parts and tell the user what was dropped.

## Pass 1 — light read

Before proposing an approach, produce a short read (a handful of lines, not a task list):

- **What the game is** — genre, core loop, camera, dimensionality.
- **Hard / uncertain parts** — use the risk taxonomy below as a *detector*. These are the things to tackle first and watch closely, and what shapes the approach proposal. Naming them is not a commitment to isolate them.
- **Asset sense** — rough kind and count (models, sprites, textures, backgrounds), and how much of the task *is* assets versus logic. *When* to generate is a build decision shaped by that weight — placeholders first when the substance is logic, real assets first when it is the art (`interactive.md`).
- **Smallest showable first** — the earliest slice worth putting on the live URL.

Use this read to recommend a build approach in `interactive.md`.

### Risk taxonomy (detector)

Features that tend to fail first-pass and benefit from early, focused attention:

- **Procedural generation** — terrain, levels, meshes, dungeon layouts
- **Procedural animation** — runtime bone manipulation, IK, ragdoll blending
- **Sprite/character animations** — multi-direction movement, state transitions; wrong frames per direction, stutter or pop on transitions
- **Complex vehicle physics** — wheel colliders, suspension, drifting; Havok/Cannon/Ammo differ enough that the wrong choice derails the work
- **Custom shaders** — `ShaderMaterial`, `NodeMaterial`, post-process, water, portals, dissolve/distortion
- **Runtime geometry** — destructible meshes, CSG, deformation, baked-on-demand vertex data
- **Dynamic navigation** — pathfinding around runtime obstacles, crowds, flocking (`recastjs` real-time rebuild needs care)
- **Complex cameras** — third-person with collision avoidance, cinematic rails, pointer-lock first-person, split-screen
- **Pointer lock / first-person** — needs a user gesture; silently no-ops in some embed contexts
- **Imported GLB pipelines** — animation retargeting, morph targets, skeleton mismatches, draco/meshopt; resolve loader extensions before relying on imported rigs

Everything else is routine — build it directly.

## Pass 2 — thin PLAN.md

After the user picks an approach (the menu and when each fits live in `interactive.md`), write `PLAN.md` in that approach's shape. Keep it thin; it is a living doc you revise at every checkpoint.

- **one-shot-then-polish** — a "first cut" goal for `main`, plus a polish backlog that fills in from the user's live reactions.
- **hard-parts-first** — an ordered list of the hard parts (each a slice landed in `main` and confirmed live), then assembly, then routine fill.
- **linear** — a feature sequence, each verified live before the next.

Record the chosen approach and the reference-usage mode at the top so they survive compaction.

### Verification

Verification is mostly the user watching the live URL. For each slice, note **what to look at** — the specific behavior or transition to confirm — and self-check it with a `capture.mjs still` (see `capture.md`) before showing the user, so you never present an obviously broken state. You do not need exhaustive motion probes: the user sees motion directly.

How strict reference-matching is follows the usage mode recorded in `PLAN.md` (defined in `interactive.md`).

General things worth a glance on most slices: input → response feels right, animation matches movement direction, physics responds to gravity/collision, UI readable, no missing textures or placeholder materials, no browser console errors.

## PLAN.md shape

````markdown
# Game Plan: {Name}

**Approach:** {one-shot-then-polish | hard-parts-first | linear}
**Reference mode:** {precise | art-direction | rough guide | none}

## Now
{the current slice}

## Next
{the few upcoming slices, in the approach's shape — kept short, grown as you go}

## Reviewed live
{slices the user has seen and accepted}

## Open questions
{anything waiting on the user}
````

Keep it short. Add detail to a slice when you start it, not before.
