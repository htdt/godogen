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

The character comes from `tripo make <ref.png> --then rig-check,rig:model=v1.0-20240301` (SKILL.md) — Tripo-rigged bipeds certify against the lib's Stage 1 battery (verified). Certify before animating; a rig that fails gets regenerated, not patched. After baking, run the lib's `qa_endeffectors.mjs <char.glb> <movesDir> --gate` for every character × move-set pair — skewed fists/feet from a wrong rest anchor read fine in stills and are ~free to catch mechanically.

## The move set is half authored

A generated move set and a hand-authored pose set are not alternatives — they are two halves of one thing, and the seam is: **the game owns the character's relationship to its prop; the generator owns the motion.** Text is the right control for *intent* and the wrong control for anything measurable. A prompt cannot say "feet 0.54 m apart over the trucks with the shoulders along the deck", "the support hand stays on the fore-grip through the whole reload", "the guard stays up while stepping" — and a move set authored from prompts alone gets those wrong in a *different* way every time you regenerate.

So author the key poses in the game, gate them there (below), export them, and pin them as `fullbody` constraints at each move's bookends and middle. Kimodo's fullbody keys are conditioned *and* corrected, so an authored pose survives generation verbatim (0.0000 m / 0.00° adherence, measured). The export is a **global rotation delta from bind** per mapped joint, which *is* a SOMA global rotation because Kimodo's T-pose is its zero pose — so no source rest skeleton is needed on the game side, only `local[j] = global[parent]⁻¹ · global[j]` composed down the hierarchy. Verify that zero-pose property before assuming it for another generator.


## Engine bridge

For non-three.js engines run the lib's `prebake.mjs` — the game repo then carries only ordinary assets (a GLB whose animations are the baked clips, plus `rootmotion.json`) and zero motion tooling. Play clips by driving animation time directly with weight crossfades — Babylon: paused `AnimationGroup` + `goToFrame` + `setWeightForAllAnimatables`; Godot/Bevy: the glTF animations import natively. Integrate root motion at the entity layer from `rootmotion.json`, and derive gameplay timing windows (airborne span, low span) from the baked hip-height data instead of hand constants — that is the lib's Stage 3 architecture and it maps onto any engine. The same clip/entity split handles speed-coupled contacts (a skate push, paddling — any interaction whose length and timing depend on entity velocity, which no fixed clip can know): the generated clip owns body and balance; the entity layer owns the contact — plant point, world-pin while moving, reach-based release.

**Babylon's mirrored import.** Babylon's glTF loader parents the import under a negative-scale root (world scale `(1,−1,1)`). Clip playback is unaffected, but any world-space rotation math against the imported skeleton — aim IK, limb pinning, orientation surgery — silently mirrors when composed from `decompose()`d quaternions. Do that math in matrices, or set `scene.useRightHandedSystem`; INTEGRATE.md §9 documents the trap.

**Impact timing.** Generated attacks have real wind-up: the strike visually lands at `frame_data.contact` (the measured max-extension frame), typically 5–9 clip frames *after* the speed-derived `active` window opens — damage or sfx synced to `active[0]` reads as a phantom early hit. Register hits only in `[max(active[0], contact−2), active[1]]` and fire one-shot impact effects (damage, hitstop, sound) at the frame the hit registers. Express every window in clip frames checked against the playback cursor, never wall-clock time — playback-speed multipliers rescale frames-to-seconds per move — and re-watch one hit per attack at game speed after any speed retune; timing regressions are invisible to pose-space QA.

## Gate the character against its prop, numerically

Whatever the character holds, stands on, or aims at — board, rifle, bat, opponent — write the gate before the poses. Every one of these was earned on a shipped move set; ANIMATION_AGENT.md and INTEGRATE.md §8 carry the long form.

1. **Intrinsic checks catch a broken limb; only relational checks catch a broken pose.** Knee-below-hip, elbow range, bone stretch and left-shoulder-on-the-left can all pass while the character stands on the board like a skier, holds the rifle across their chest, or faces away from the opponent. Measure in **the prop's frame** and check the relationship first: body axis vs prop axis, each contact on its named point, the prop's own attitude. A pose is a body in a relationship, and if nothing measures the relationship the most fundamental defect possible is the one that gates clean.
2. **Separate rig-forward from stance placement.** One yaw field doing both jobs is the highest-cost bug in this class: "correcting the rig" silently re-poses the character and every authored angle then rides on the error. Two named constants. If a rig fix ever changes how a pose *looks*, they are conflated.
3. **Measure a contact off the mesh, not off the bone.** The chain ends at the wrist; the contact is made by the visible fist — 66 mm away on one hand and 91 mm on the other of the same character. Same for a muzzle, a grip, a blade tip. Take the vertices whose dominant skin weight is that bone, and read the centroid, the thinnest axis (a palm normal), and the finger direction. Then solve position and orientation *together*, iterating: turning the hand moves the fist, and re-aiming the arm re-rotates the hand.
4. **Check reach before tuning a pose.** `|shoulder → target|` against the limb's own length. If it exceeds it, no arm angle anywhere in the pose will fix it. And aim at ~93% of full extension: a target at exactly full reach is one a two-bone solver clamps short of, leaving the hand off the surface *and* the elbow locked straight.
5. **If the cheapest reachable shape still reads broken, change the contact, not the pose.** Reach arithmetic says what touching costs; it never says the pose can afford it. Five versions of one pose were tuned against a contact that could not be made without capsizing the character — the fix was to delete the contact. When you delete one, replace its assertion with the **inverse** (`hand_off_road` → `hand_on_road`) or the pose drifts straight back.
6. **A contact the limb cannot reach must be released, not stretched at**, and the weight the solver *achieved* — not the one it was asked for — is what particles, audio and the audit must read. Fade over the last third of reach; a narrow band makes the contact a switch, and the frame it flips the hand teleports.
7. **Evaluate a pose under the body transform the move happens in** — lean, bank, slope, recoil. A gate that judges everything upright will demand shapes that only being upright requires, then certify them.
8. **An exemption is a debt.** A pose that legitimately breaks a whole battery — feet off the board, weapon holstered, body prone — must bring its own checks for what that battery was carrying, or it becomes the least examined pose in the set.
9. **Gate poses, then transitions, then the live frame.** Each catches a class the previous cannot see: the run spends most of its time mid-crossfade, and two clean poses can pass through a broken shape between them.
10. **Author the pose table in physical units** (metres above the deck), not a normalised 0..1 crouch. A pose that has to be reverse-engineered through a lerp gets tuned by trial and error forever.
11. **Failure messages name the cause, not just the number.** `"37° between shin and foot, want 44..148 (too small = the knee is driven over the toes with the hips stacked on the ankles)"` is what identified a missing authored dimension — hip setback — that the pose system did not have.

## Pitfalls at the seam

12. **Constraint adherence says the KEYS are right, and nothing about the in-betweens.** Every real defect lived between keys: a launch that met every constraint exactly and shook between them, a held grab that hit its keys perfectly and relaxed 0.26 m out of the arm's reach halfway. Never accept a clip on adherence alone — run your own battery over every frame, held to the **union** of the poses the clip was pinned to (a clip is a move, not a pose; holding a tuck-to-extension clip to "extension" fails it on 15 of 24 frames while it does exactly what was asked).
13. **A generator's bias lives where no key can see it.** This move set's prior raised both arms overhead in the in-betweens on the cruise and both carves. Keys every 20 frames did not stop it; every 13 did not stop it. Denser keys are the wrong lever — the fix is an **in-engine authority layer**: the clip owns the body, the game pulls one chain back toward the authored pose at a partial weight (0.8 here), off in the air where the arm shape *is* the move. Expect to need this for anything the prior has opinions about: hands on a weapon, a guard, a grip.
14. **Some moves cannot be baked at all, and that is structural.** If the runtime places a clip-driven body by pinning a contact to a prop (feet to the deck, hands to the bars), a move whose whole point is *breaking* that contact — a superman, a bail, a disarm — cannot come from a clip. Make the placement rule a per-pose property and author those moves. Also make the *held* shapes candidates for authoring: a held silhouette carried by entity motion (a flip, a dash) needs no generated motion at all.
15. **The prompt must agree with the keys it pins.** Change a key pose and leave the prompt describing the old move and the in-betweens get pulled back toward it. Prompt and constraints are the same statement at two resolutions.
16. **Drive the subject in the gate exactly the way the game drives it.** The most expensive bug here: the gate scrubbed clips through the raw player (`Play(clip, 0.0)`), the game seeked them through a crossfading wrapper, and Godot drains a crossfade off the mixer delta — which a seeked clip freezes. Every seeked beat of the run played the *previous* move, for its whole length, and every gate passed. `Play(...)` and `Seek(...)` are not the same code path.
17. **Shape bounds cannot detect the wrong clip playing** — human poses in one sport resemble each other. What no other move can fake is a **contact**: a hand on a specific rail of a specific board, a magazine at a specific well. Assert contacts on clip-driven frames.
18. **Gate a derivative, not only per-frame poses.** "The hands move abruptly" is not a property of any frame — every one is a legal pose. Hand speed **in the subject's own frame** (so travel and rotation don't swamp it) is one line and found three unrelated causes in a single pass: a hard writer handover at 43.8 m/s, clips played at up to 10×, and a contact gate behaving as a switch.
19. **Two writers of one skeleton means a crossfade, not a cut.** Snapshot the pose before anything writes it, blend out of the snapshot over ~0.2 s. And the trap inside the fix: if the snapshot refreshes every frame, blend *progress* is not the per-frame slerp factor — feeding it in directly compounds into an accelerating blend that dumps the difference into the last frames, which is the snap you were removing. Use `k = (S(u) − S(u_prev)) / (1 − S(u_prev))`.
20. **Play clips at ~1×: slice them, do not stretch them.** Mapping a whole clip onto a shorter beat ran one at 10× here. Motion generated to look natural at 1× is not natural at 3×; name the *slice* of the clip each beat plays, and print the ratio at startup so retuned beat times cannot rot it.
21. **Anything simulated gets its own gate** — hair, cloth, slings, holsters. Assert movement, direction *relative to its own anchor*, attachment, stability and independence; "there are six strands" is not the property worth testing, "they are not the same strand" is. Scale thresholds to the thing's own size, or a gate set for the longest strand certifies every shorter one as a rigid stick.

## Where things live

The motion workspace (the per-project lib clone with its move specs, `out/`, baked clips) stays outside the game repo; record its path in the game's `README.md`. The game repo gets only the prebaked artifacts, under `${RUNTIME_ASSET_DIR}/`.

## Budgeting

A polished move set is hours, not minutes — but the compute is not where they go. A gated 17-move set generates in ~10 minutes on a 12 GB GPU (best-of-8 with numeric QA gates per move); the time goes to the review loop: filmstrip/QA review → adjust prompts or spec → regenerate → re-certify. Treat a gate failure as a real defect and regenerate — never patch a bad clip at runtime. Surface this when estimating.

Where the hours actually go, on a project that authors its own key poses: the **pose table and its gate**, not the generation. Regenerating a 7-move set end to end (export → spec → generate → bake → prebake → reimport → gate) is ~25 minutes unattended and can be run as often as the poses change — so treat a pose change as cheap and a *convention* mistake as expensive, because the latter is what re-runs cannot find.
