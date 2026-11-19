# Custom Character Animation

Humanoid moves come from godogen_assets: `gen-moves` generates a move set from a spec of text prompts (NVIDIA Kimodo through [kimodo-practical](https://github.com/htdt/kimodo-practical)), and `add-moves` puts it onto a `mia-rig` rig as ordinary glTF clips plus `rootmotion.json`; `grip-prop` and `add-moves --hold` put a prop in a hand. Running them, the spec keys and the generation gates: `$GODOGEN_ASSETS/motion/README.md`. This page is the game side: the poses a prompt can't pin, playing the clips, and holding things and meeting other characters.

## Authored key poses

Beyond prompts, a spec's `constraints` pin full-body key poses, hand/foot targets and root paths. `$GODOGEN_ASSETS/motion/kimodo-practical/ANIMATION_AGENT.md` says which control fits when (text vs full-body pose vs end-effector target vs root waypoints/path); `BAKE.md` §3 has the format. Videogame combat and locomotion are in-distribution.

Text controls intent, not anything measurable: "feet 0.54 m apart over the trucks", "the support hand stays on the fore-grip through the reload". Author those as key poses in the game, export them, and pin them as `fullbody` constraints at each move's bookends and middle. Kimodo's fullbody keys are conditioned *and* corrected, so an authored pose survives generation verbatim. The export is a **global rotation delta from bind** per mapped joint, which *is* a SOMA global rotation because Kimodo's T-pose is its zero pose — so the game side needs no source rest skeleton, only `local[j] = global[parent]⁻¹ · global[j]` composed down the hierarchy. Verify that zero-pose property before assuming it for another generator. Author the pose table in physical units (metres above the deck), not a normalised 0..1 crouch.

- **Keys fix only the keyed frames.** The generator's prior still shapes the in-betweens (here: both arms raised overhead between keys every 13 frames), and denser keys don't remove it. An **in-engine authority layer** does: the clip owns the body, and the game pulls one chain back toward the authored pose at a partial weight (~0.8), switched off where the shape *is* the move.
- **The prompt must agree with the keys it pins.** A prompt still describing the old move pulls the in-betweens back toward it.
- **Some moves can't be baked.** If the runtime places a clip-driven body by pinning a contact to a prop (feet to the deck, hands to the bars), a move whose point is breaking that contact (a bail, a disarm) can't come from a clip: make the placement rule a per-pose property and author those moves. A held silhouette carried by entity motion (a flip, a dash) needs no generated motion at all.

## Engine bridge

The project carries only `add-moves` output — the GLB with its clips and `rootmotion.json` — and zero motion tooling; `$GODOGEN_ASSETS/motion/README.md` gives the file format and the playback basics. Integrate root motion at the entity layer from `pelvisXZ`, and derive gameplay timing windows (airborne span, low span) from `hipY` instead of hand constants — the lib's Stage 3 architecture (`INTEGRATE.md`), and it maps onto any engine. Speed-coupled contacts (a skate push, paddling — anything whose timing depends on entity velocity) split the same way: the clip owns body and balance; the entity layer owns the contact — plant point, world-pin while moving, reach-based release.

- **Babylon's mirrored import.** Babylon's glTF loader parents the import under a negative-scale root (world scale `(1,−1,1)`). Clip playback is unaffected, but any world-space rotation math against the imported skeleton — aim IK, limb pinning, orientation surgery — silently mirrors when composed from `decompose()`d quaternions. Do that math in matrices, or set `scene.useRightHandedSystem`; `$GODOGEN_ASSETS/motion/kimodo-practical/INTEGRATE.md` §9 documents the trap.
- **Impact timing.** Generated attacks have real wind-up, and `frameData` in `rootmotion.json` (a move with `strike` in its spec) is measured on the move alone, with no opponent: `active` is the fast phase of the striking limb — of the held prop's tip when the move went on with `--hold` — and `contact` an estimate inside it (with a prop, the frame its tip reaches furthest forward, `reach` metres ahead). Damage or sfx synced to `active[0]` reads as a phantom early hit. Register hits only in `[max(active[0], contact−2), active[1]]`, on a real intersection wherever one can be tested (a held prop's path is in `held`), and fire one-shot impact effects (damage, hitstop, sound) at the frame the hit registers. Express every window in clip frames checked against the playback cursor, never wall-clock time — playback-speed multipliers rescale frames-to-seconds per move.
- **Play clips at ~1×: slice, don't stretch.** Motion generated to look natural at 1× isn't at 3×. Map each beat to a named slice of a clip, not a whole clip onto a shorter beat.
- **Two writers of one skeleton crossfade, not cut.** Snapshot the pose before anything writes it and blend out of the snapshot over ~0.2 s. If the snapshot refreshes every frame, blend progress is not the per-frame slerp factor — feeding it in directly accelerates the blend into a snap at the end. Use `k = (S(u) − S(u_prev)) / (1 − S(u_prev))`.
- **Godot: seeking freezes a crossfade.** Godot drains a crossfade off the mixer delta, which a seeked clip freezes — seek through a crossfading wrapper and the previous move plays for the clip's whole length. `Play(...)` and `Seek(...)` are different code paths.

## Held props and contact

A weapon, a tool, anything carried: `grip-prop` finds the prop's handle, and `add-moves --hold right=PROP` leaves a `grip_r` node in the measured palm, the fingers closed on the handle, and the prop's path per clip (`held`) in `rootmotion.json`. Commands and spec keys (`held`, `strike_gate.min_reach`, `stance_end`): `$GODOGEN_ASSETS/motion/README.md`, Held props. `$GODOGEN_ASSETS/motion/HELD_PROPS.md` has the rules from a sword fight built end to end, for any engine; the ones the game side breaks first:

- **Parent the prop to `grip_r`, identity transform** — never to the hand bone, never with a tuned offset, rotation or scale.
- **The generator animates empty hands.** A move is generated for its prop (`held` in the spec), and what a given pair of characters can do with it is measured on their own `rootmotion.json` — an attack that lands on one opponent passes over the head of a shorter one, and a move's name is no evidence of what it does.
- **Two clips meet on events and distances read from data**: the attack's contact frame against the frame the reaction starts to move, at the distance where the prop's outer third enters the body. Steps of exact stride (`stance_end`) carry the pair from one working distance to the next.
- **Clips made apart never touch on their own.** The clip supplies the body; bounded IK on the holding arm supplies the contact; a blocked attack stops at the contact frame and rebounds the way it came.

## Contact IK

- **The mesh makes the contact, not the bone.** The chain ends at the wrist; the visible fist is 66–91 mm further on. Same for a muzzle, a grip, a blade tip. Take the vertices whose dominant skin weight is that bone and read the centroid, the thinnest axis (a palm normal), and the finger direction; solve position and orientation together, since turning the hand moves the fist. For a hand on a handle, `grip_r` is this measurement.
- **Reach.** A target farther than the limb's length from the shoulder is unreachable by any arm angle. Aim at ~93% of full extension: a two-bone solver clamps short of exactly full reach, leaving the hand off the surface and the elbow locked.
- **Release what can't be reached**, fading over the last third of reach (a narrow band makes the contact a switch and the hand teleports), and drive particles and audio from the weight the solver *achieved*, not the one it was asked for.
- **Rig-forward and stance placement are two constants.** One yaw doing both means "correcting the rig" silently re-poses the character, and every authored angle rides on the error.

## Where things live

Keep the move specs, and the pose constraints exported into them, in the project: they regenerate the set. `gen-moves` outputs are work files; the runtime asset folder gets only the `add-moves` GLB and `rootmotion.json`. Generation is ~1 min of GPU per move, and `gen-moves` redoes only the moves whose spec changed, so export → spec → `gen-moves` → `add-moves` → reimport reruns unattended whenever the poses change.
