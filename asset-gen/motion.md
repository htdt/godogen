# Custom Character Animation

Generate custom humanoid move sets with [motionbricks-practical](https://github.com/htdt/motionbricks-practical) and bake them into ordinary glTF animations.

## When to reach for it

Custom move sets driving gameplay: state machines, root-motion locomotion, moves that don't exist as stock clips (`retarget` presets are generic). For a character that just idles or waves, a retarget preset is enough — skip this pipeline.

## Fetch and follow

If `MOTIONBRICKS_HOME` is set, the deps already live under it — `motionbricks-practical`, the GR00T-WholeBodyControl LFS checkout, usually a ready venv — reuse them instead of fetching. Otherwise:

```bash
git clone https://github.com/htdt/motionbricks-practical
```

Follow the README's "For agents" reading order: MOTIONBRICKS.md → ALIGN.md → BAKE.md → INTEGRATE.md. The lib documents the pipeline itself; this page adds only environment facts and the bridges to this skill and the engine.

## Environment

- NVIDIA GPU required — generation is MuJoCo + torch. Generation is free and local: it consumes GPU time, not the asset budget.
- The GR00T-WholeBodyControl checkout is multi-GB Git LFS — needs `git-lfs`, disk, and bandwidth to match.
- On headless boxes run generation under `xvfb-run -a`.
- If `pip install -e` is unavailable (sandboxed agents), installing the deps by name into a venv and exporting `PYTHONPATH=<checkout>/motionbricks` works — verified.

## Character bridge (this skill)

The character comes from `asset_gen.py rig` — Tripo-rigged bipeds certify against the lib's Stage 1 battery (verified). Certify before animating; a rig that fails gets regenerated, not patched.

## Engine bridge

For non-three.js engines run the lib's `prebake.mjs` — the game repo then carries only ordinary assets (a GLB whose animations are the baked clips, plus `rootmotion.json`) and zero motion tooling. Play clips by driving animation time directly with weight crossfades — Babylon: paused `AnimationGroup` + `goToFrame` + `setWeightForAllAnimatables`; Godot/Bevy: the glTF animations import natively. Integrate root motion at the entity layer from `rootmotion.json`, and derive gameplay timing windows (airborne span, low span) from the baked hip-height data instead of hand constants — that is the lib's Stage 3 architecture and it maps onto any engine.

## Where things live

The motion workspace (checkout, pose library, move spec, baked clips) stays outside the game repo; record its path in the game's `README.md`. The game repo gets only the prebaked artifacts, under `${RUNTIME_ASSET_DIR}/`.

## Budgeting

A polished move set is hours, not minutes. The loop is generate → filmstrip/QA review → adjust poses or spec → rebake → re-certify, and authored ground-contact moves (slides, knockdowns) typically take several iterations. Surface this when estimating.
