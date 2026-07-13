# Custom Character Animation

Generate custom humanoid move sets with [kimodo-practical](https://github.com/htdt/kimodo-practical) and bake them into ordinary glTF animations.

## When to reach for it

Custom move sets driving gameplay: state machines, root-motion locomotion, moves that don't exist as stock clips (`retarget` presets are generic). For a character that just idles or waves, a retarget preset is enough — skip this pipeline.

## Fetch and follow

If `KIMODO_HOME` is set, the deps already live under it — `kimodo-practical`, the `kimodo` checkout, usually a ready venv — reuse them instead of fetching. Otherwise:

```bash
git clone https://github.com/htdt/kimodo-practical
```

Follow the README's "For agents" reading order: KIMODO.md → ALIGN.md → BAKE.md → INTEGRATE.md. Moves are authored as text prompts on a human skeleton; videogame combat and locomotion are in-distribution. The lib documents the pipeline itself; this page adds only environment facts and the bridges to this skill and the engine.

## Environment

- Generation is free and local: it consumes GPU time, not the asset budget.
- A CUDA GPU is needed but a small one suffices: keep the Llama-3-8B text encoder on CPU (`TEXT_ENCODER_DEVICE=cpu`, needs ≥20 GB free RAM) and diffusion peaks ~2.5 GB VRAM; ~35 GB disk. Start `kimodo_textencoder` once as a service before batch generation — reloading the 16 GB encoder per CLI call is otherwise the dominant cost.
- The encoder base model is HF-gated (`meta-llama`). If the account has no Llama access, the lib's `kimodo/setup_text_encoder.py` builds a local `TEXT_ENCODERS_DIR` from the public byte-identical mirror — don't fight the gate.

## Character bridge (this skill)

The character comes from `asset_gen.py rig` — Tripo-rigged bipeds certify against the lib's Stage 1 battery (verified). Certify before animating; a rig that fails gets regenerated, not patched. After baking, run the lib's `qa_endeffectors.mjs <char.glb> <movesDir> --gate` for every character × move-set pair — skewed fists/feet from a wrong rest anchor read fine in stills and are ~free to catch mechanically.

## Engine bridge

For non-three.js engines run the lib's `prebake.mjs` — the game repo then carries only ordinary assets (a GLB whose animations are the baked clips, plus `rootmotion.json`) and zero motion tooling. Play clips by driving animation time directly with weight crossfades — Babylon: paused `AnimationGroup` + `goToFrame` + `setWeightForAllAnimatables`; Godot/Bevy: the glTF animations import natively. Integrate root motion at the entity layer from `rootmotion.json`, and derive gameplay timing windows (airborne span, low span) from the baked hip-height data instead of hand constants — that is the lib's Stage 3 architecture and it maps onto any engine.

**Impact timing.** Generated attacks have real wind-up: the strike visually lands at `frame_data.contact` (the measured max-extension frame), typically 5–9 clip frames *after* the speed-derived `active` window opens — damage or sfx synced to `active[0]` reads as a phantom early hit. Register hits only in `[max(active[0], contact−2), active[1]]` and fire one-shot impact effects (damage, hitstop, sound) at the frame the hit registers. Express every window in clip frames checked against the playback cursor, never wall-clock time — playback-speed multipliers rescale frames-to-seconds per move — and re-watch one hit per attack at game speed after any speed retune; timing regressions are invisible to pose-space QA.

## Where things live

The motion workspace (checkout, move spec, baked clips) stays outside the game repo; record its path in the game's `README.md`. The game repo gets only the prebaked artifacts, under `${RUNTIME_ASSET_DIR}/`.

## Budgeting

A polished move set is hours, not minutes — but the compute is not where they go. A gated 17-move set generates in ~10 minutes on a 12 GB GPU (best-of-8 with numeric QA gates per move); the time goes to the review loop: filmstrip/QA review → adjust prompts or spec → regenerate → re-certify. Treat a gate failure as a real defect and regenerate — never patch a bad clip at runtime. Surface this when estimating.
