---
name: asset-gen
display_name: Asset Generator
short_description: Generate game images, GLB 3D models, rigged characters, and animated sprites
default_prompt: "Use ${ASSET_SKILL_COMMAND} to generate images, 3D models, or animated sprites for this game."
allow_implicit_invocation: true
description: |
  Generate visual assets from text prompts: PNG images (Gemini / xAI Grok), GLB 3D models (Tripo CLI), rigged characters, retargeted animations, and frame-by-frame animated sprites, plus background removal. Use whenever a game needs generated art.
---

# Asset Generator

Generate PNG images (Gemini or xAI Grok) and GLB 3D models (Tripo) from text prompts. These are paid APIs — every call costs real money. Image tools live at `${ASSET_GEN_SKILL_DIR}/tools/`; 3D goes through the `tripo` CLI. Run from the project root and keep runtime-loaded outputs under `${RUNTIME_ASSET_DIR}/`.

## Models

| Model | Flag | Cost | Best for |
|-------|------|------|----------|
| Gemini | `--model gemini` | 5¢ (512) · 7¢ (1K) · 10¢ (2K) · 15¢ (4K) | Precise prompt following — references, characters, 3D refs, exact layouts |
| Grok | `--model grok` (default) | 2¢ | High quality but imprecise — textures, simple objects, item kits, scenic backgrounds |

Grok produces great-looking output but often ignores specific instructions; reach for Gemini when the result must match what you described.

## Images

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o ${RUNTIME_ASSET_DIR}/img/car.png
```

`--model` (default `grok`) · `--size` (default `1K`; Gemini also `512`/`4K`) · `--aspect-ratio` (default `1:1`; also `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`).

**Image-to-image:** pass `--image ref.png` and the model sees the reference — prompt only for what changes (angle, pose, recolor), don't re-describe appearance. Use this for style families (one hero asset → the rest), variants, and multi-view sets.

**Small sprites:** minimum generation is 1K, so a 1024px image downscaled to 64px looks muddy. Design display sizes ≥128px, or generate a kit (multiple objects in one 1K image) and slice it with `tools/grid_slice.py ... --grid 2x2 --names "a,b,c,d"`, or prompt for bold flat forms that survive downscaling.

Review every PNG before any GLB conversion — a bad image wastes 30+ credits downstream.

### Background removal

Read `${ASSET_GEN_SKILL_DIR}/rembg.md`. Key rule: **never prompt for a "transparent background"** (the generator bakes a checkerboard) — prompt a solid color, then matte it out.

## Animated sprites

Recipe: **reference → pose → video → extract frames → loop-trim → rembg.**

1. Reference (Gemini 1K, neutral pose, solid BG) — anchors everything; review carefully.
2. Pose per action: image-to-image from the reference, prompt only the action.
3. Video from the pose frame: `asset_gen.py video --image pose.png --duration 2 -o walk.mp4` (`--duration` 1–15s, `--resolution` 720p; cost 5¢/s).
4. Extract: `ffmpeg -i walk.mp4 -vsync 0 frames/%04d.png`.
5. Loop-trim looping cycles (walk/idle): `tools/find_loop_frame.py frames/` returns the loop frame; delete frames past it. Skip for one-shots (attack/death).
6. Batch matte: `tools/rembg_matting.py --batch frames/ -o clean/`.

Reuse one reference for all of a character's actions. **Chaining** (feed action A's last frame as action B's start) keeps positional continuity — keep chains ≤2 deep, they drift.

## 3D models

The `tripo` CLI (`npm install -g tripo-cli`, key in `TRIPO_API_KEY`) owns the whole 3D path: submit, poll, download, credit pre-check, refunds on failure. Its own agent docs are the reference — `tripo docs --llm`, then `tripo docs --topic commands/process` / `examples/animation` / `common-errors` — this section only covers what is specific to game use here.

```bash
tripo make ref.png --name car -p face_limit=30000 -p auto_size=true --json --yes -o ${RUNTIME_ASSET_DIR}/glb
tripo make ref.png --name hero --then rig-check,rig:model=v1.0-20240301 --json --yes -o ${RUNTIME_ASSET_DIR}/glb
tripo anim retarget @hero --animation preset:biped:walk preset:biped:idle --json --yes -o ${RUNTIME_ASSET_DIR}/glb
```

- `make` is blocking (default timeout 30 min) and prints one JSON line: read `model_file`, `preview.png` and `credits_consumed` from it. Never add your own shorter timeout, never resubmit because a task_id appeared in stderr. If the process does die, `tripo task watch <id> --download` finishes the same task for free.
- Output lands in `<-o dir>/<name>-<id8>/` (`model.glb`, `preview.png`, `task.json`). Move or reference the GLB from there; `task.json` keeps the seeds and task id, so there is nothing else to save.
- `--name X` makes the task addressable as `@X` for later steps (retarget, convert, decimate). Retarget reuses the rig task — never re-rig for another clip; up to 5 animations per call, billed per animation.
- Model defaults to v3.1. For `face_limit` ≤ 20000 the CLI silently switches to P1 (low-poly topology, no `geometry_quality`) — that is the right choice for mobile-style budgets, but know it happens. `--for game-pc` converts to FBX by default; skip it for GLB engines.
- `-p geometry_quality=detailed -p texture_quality=detailed` is the HD tier (≈ double credits).
- Rig: keep `rig:model=v1.0-20240301` for bipeds — that is the rig motion.md's pipeline is certified against, and it uses the `preset:biped:*` clips below. The CLI's default rig (v2.5) covers quadrupeds, avians, etc. with `preset:<name>` clips (`idle walk run dive climb jump slash shoot hurt fall turn`); unverified with motion.md. `rig-check` in the chain aborts before rigging if the mesh isn't riggable. `--animate-in-place` when game code drives locomotion.
- Don't assume the preset name survives into the GLB; inspect the imported clip names before wiring playback.

Source image for `make`: 3/4 elevated angle, solid white/gray background, matte finish, opaque glass, single centered subject — and **do not** rembg it (Tripo needs the solid bg). For characters, generate the reference in a T-pose.

v1.0 biped retarget presets (pass as `preset:biped:<name>`):

```
afraid agree angry_01/02/03 basketball_shot bow box_01/02/03 cast_a_spell cheer chop
clap climb complain_01/02 cross_body_crunch crossover_dribble cry dance_01..06
defeat_02/03 depressed dig dive dribble fall fire flee_01/02 flip fold_arms
football_catch/save/pass freaky frightened front_kick_01/02 frustrated_01/02 golf
greet_01..04 heart_pose hit_to_body_01/02 hit_to_head/side/stomach hug hurt idle
jump jump_down jump_rope_01/02 laugh_01/02 lift_heavy look_around make_a_call_01/02
pitch_baseball play_mobile_game play_video_game press-up run run_upstairs scared_01/02
scratch shoot shovel sing_01..04 sit slash sob standing_relax surf swagger swim turn
victory_celebration volleyball wait walk warm_up wave_goodbye_01/02
```

Presets are generic stock clips. **Important:** when gameplay needs a custom humanoid move set (state machines, root-motion locomotion, moves not in this list), read `${ASSET_GEN_SKILL_DIR}/motion.md`.

## Costs

Each generation costs real money, so confirm with the user before generating. Quick reference: texture/simple sprite (Grok) 2¢ · character/ref (Gemini 1K) 7¢ · background 2¢ (Grok) or 10¢ (Gemini 2K). Tripo bills in credits (≈1¢): ~30 per model, ~25 to rig, ~10 per retargeted clip — `tripo balance` before a batch, and report the `credits_consumed` the CLI returns rather than an estimate.

## Output and logging

Each `asset_gen.py` command prints JSON to stdout: `{"ok": true, "path": "...", "cost_cents": 7}`; `tripo` does the same with `--json`. Progress goes to stderr — redirect it to a temp file and read only on failure to keep context clean:

```bash
_log=$(mktemp)
result=$(python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image --prompt "..." -o p.png 2>"$_log") || tail -20 "$_log"
```

Generate independent images in parallel (multiple Bash calls in one message).

## Visual pitfalls

Generators and vision checks have weak spatial sense — verify from screenshots when it matters.

- **Direction/orientation** is unreliable ("facing left" vs "right" often comes out identical). Generate one direction and flip horizontally at runtime rather than paying for the mirror.
- **Mixed sizes:** image frames are ~1024px, video frames ~720px. Downscale everything to the smallest source before matting (`magick in.png -resize 720x720 out.png`).
- **Playback fps:** source videos are ~24fps — drive sprite playback off elapsed time at ~1/24s, and only restart a loop when the animation state actually changes.

## Asset manifest (in README.md)

Track every generated asset in `README.md` with an **in-game Size** column — without it, coders consistently scale assets wrong:

- 3D models: meters, e.g. `4m long`, `1.8m tall`, `0.3m`
- Textures: tile size, e.g. `2m tile`
- Backgrounds: pixel size + behavior, e.g. `1920x1080, fullscreen`
- Sprites: display pixels, e.g. `128x128 px`

| Name | Description | Size | Path | Cost |
|------|-------------|------|------|------|
| car | sedan with spoiler | 4m long | ${RUNTIME_ASSET_DIR}/glb/car.glb | 7¢ + 30 cr |
