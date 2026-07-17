# Custom Character Animation

Generate custom humanoid move sets with [kimodo-practical](https://github.com/htdt/kimodo-practical) and bake them into ordinary glTF animations.

## When to reach for it

Custom move sets driving gameplay: state machines, root-motion locomotion, moves that don't exist as stock clips (`retarget` presets are generic). For a character that just idles or waves, a retarget preset is enough — skip this pipeline.

## Fetch and follow

If `KIMODO_HOME` is set, the full stack is installed under it with fixed names — `kimodo-practical/` (the lib), `kimodo/` (the upstream checkout), `kimenv/` (the pipeline venv: run the lib's python tools with `$KIMODO_HOME/kimenv/bin/python`), `text_encoders/` (the encoder mirror: set `TEXT_ENCODERS_DIR="$KIMODO_HOME/text_encoders"` for every Kimodo command) — reuse it; never re-fetch or hunt the filesystem. Start the motion workspace by cloning the lib from the local reference:

```bash
git clone "$KIMODO_HOME/kimodo-practical" && cd kimodo-practical && npm install
```

(No `KIMODO_HOME` → clone https://github.com/htdt/kimodo-practical and install the stack per its KIMODO.md.) The clone is per-project on purpose: `kimogen.py` writes its outputs inside its own checkout, so the small repo is project state — move specs, `out/`, baked clips — while the heavy venv, encoder mirror, and model cache stay shared through the env.

Follow the README's "For agents" reading order: KIMODO.md → ALIGN.md → BAKE.md → INTEGRATE.md — and keep **ANIMATION_AGENT.md** open while authoring move specs: it is the which-control-when decision page (text vs full-body pose vs end-effector target vs root waypoints/path, plus the pre/post-generation checklist). Moves are authored as text prompts + constraints on a human skeleton; videogame combat and locomotion are in-distribution. The lib documents the pipeline itself; this page adds only environment facts and the bridges to this skill and the engine.

## Environment

- Generation is free and local: it consumes GPU time, not the asset budget.
- A CUDA GPU is needed but a small one suffices: keep the Llama-3-8B text encoder on CPU (`TEXT_ENCODER_DEVICE=cpu`, needs ≥20 GB free RAM) and diffusion peaks ~2.5 GB VRAM; ~35 GB disk. Start `kimodo_textencoder` once as a service before batch generation — reloading the 16 GB encoder per CLI call is otherwise the dominant cost.
- The encoder base model is HF-gated (`meta-llama`). Under `KIMODO_HOME` the local mirror already exists at `text_encoders/`. To build it fresh, the lib's `kimodo/setup_text_encoder.py` assembles one from the public byte-identical mirror — don't fight the gate.

## Character bridge (this skill)

The character comes from `asset_gen.py rig` — Tripo-rigged bipeds certify against the lib's Stage 1 battery (verified). Certify before animating; a rig that fails gets regenerated, not patched. After baking, run the lib's `qa_endeffectors.mjs <char.glb> <movesDir> --gate` for every character × move-set pair — skewed fists/feet from a wrong rest anchor read fine in stills and are ~free to catch mechanically.

## Engine bridge

For non-three.js engines run the lib's `prebake.mjs` — the game repo then carries only ordinary assets (a GLB whose animations are the baked clips, plus `rootmotion.json`) and zero motion tooling. Play clips by driving animation time directly with weight crossfades — Babylon: paused `AnimationGroup` + `goToFrame` + `setWeightForAllAnimatables`; Godot/Bevy: the glTF animations import natively. Integrate root motion at the entity layer from `rootmotion.json`, and derive gameplay timing windows (airborne span, low span) from the baked hip-height data instead of hand constants — that is the lib's Stage 3 architecture and it maps onto any engine. The same clip/entity split handles speed-coupled contacts (a skate push, paddling — any interaction whose length and timing depend on entity velocity, which no fixed clip can know): the generated clip owns body and balance; the entity layer owns the contact — plant point, world-pin while moving, reach-based release.

**Babylon's mirrored import.** Babylon's glTF loader parents the import under a negative-scale root (world scale `(1,−1,1)`). Clip playback is unaffected, but any world-space rotation math against the imported skeleton — aim IK, limb pinning, orientation surgery — silently mirrors when composed from `decompose()`d quaternions. Do that math in matrices, or set `scene.useRightHandedSystem`; INTEGRATE.md §9 documents the trap.

**Impact timing.** Generated attacks have real wind-up: the strike visually lands at `frame_data.contact` (the measured max-extension frame), typically 5–9 clip frames *after* the speed-derived `active` window opens — damage or sfx synced to `active[0]` reads as a phantom early hit. Register hits only in `[max(active[0], contact−2), active[1]]` and fire one-shot impact effects (damage, hitstop, sound) at the frame the hit registers. Express every window in clip frames checked against the playback cursor, never wall-clock time — playback-speed multipliers rescale frames-to-seconds per move — and re-watch one hit per attack at game speed after any speed retune; timing regressions are invisible to pose-space QA.

## Where things live

The motion workspace (the per-project lib clone with its move specs, `out/`, baked clips) stays outside the game repo; record its path in the game's `README.md`. The game repo gets only the prebaked artifacts, under `${RUNTIME_ASSET_DIR}/`.

## Budgeting

A polished move set is hours, not minutes — but the compute is not where they go. A gated 17-move set generates in ~10 minutes on a 12 GB GPU (best-of-8 with numeric QA gates per move); the time goes to the review loop: filmstrip/QA review → adjust prompts or spec → regenerate → re-certify. Treat a gate failure as a real defect and regenerate — never patch a bad clip at runtime. Surface this when estimating.
