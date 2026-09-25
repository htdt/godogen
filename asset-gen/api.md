# Paid APIs

For assets the local tools can't make on this machine (SKILL.md, Paid APIs). Every call costs real money: confirm the spend with the user before generating, and record it in the asset manifest.

Keys: `GOOGLE_API_KEY` (Gemini images, Gemini TTS, Lyria), `XAI_API_KEY` (Grok images, sprite video), `TRIPO_API_KEY` (the `tripo` CLI). Images, video and audio go through `${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py`; 3D goes through the `tripo` CLI.

## Images

| Model | Flag | Cost | Notes |
|-------|------|------|-------|
| Gemini 3.1 Flash Image | `--model gemini` | 5¢ (512) · 7¢ (1K) · 10¢ (2K) · 15¢ (4K) | ~10 s per image |
| Grok Imagine Image 2.0 | `--model grok` | 6¢ (1K) · 8¢ (2K), +1¢ per reference image | 1–2 min per image |

Gemini and Grok are equally strong: both follow detailed prompts closely, and both slip on small details — a miscounted item, a mirrored left/right. Use whichever key is set; with both, `asset_gen.py` defaults to Gemini for speed. When an asset is quality-critical (a character reference that anchors 3D or animation, a hero image) and both keys are set, generate it with both and keep the better one.

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o ${RUNTIME_ASSET_DIR}/img/car.png
```

`--model` (default `gemini` when its key is set, else `grok`) · `--size` (default `1K`; Gemini also `512`/`4K`) · `--aspect-ratio` (default `1:1`; also `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`).

**Image-to-image:** pass `--image ref.png` and the model sees the reference — prompt only for what changes (angle, pose, recolor), don't re-describe appearance. Use this for style families, variants, and multi-view sets.

**Transparency:** these models can't make it. Read `${ASSET_GEN_SKILL_DIR}/rembg.md`; key rule: **never prompt for a "transparent background"** (the generator bakes a checkerboard) — prompt a solid color, then matte it out.

Review every PNG before any GLB conversion — a bad image wastes 30+ credits downstream.

## Animated sprites

Recipe: **reference → pose → video → extract frames → loop-trim → rembg.**

1. Reference (1K, neutral pose, solid BG) — anchors everything; review carefully.
2. Pose per action: image-to-image from the reference, prompt only the action.
3. Video from the pose frame: `asset_gen.py video --image pose.png --duration 2 -o walk.mp4` (Grok, needs `XAI_API_KEY`; `--duration` 1–15s; `--resolution` 720p at 14¢/s, or 480p at 8¢/s — enough for small sprites).
4. Extract: `ffmpeg -i walk.mp4 -vsync 0 frames/%04d.png`.
5. Loop-trim looping cycles (walk/idle): `tools/find_loop_frame.py frames/` returns the loop frame; delete frames past it. Skip for one-shots (attack/death).
6. Batch matte: `tools/rembg_matting.py --batch frames/ -o clean/`.

Reuse one reference for all of a character's actions. **Chaining** (feed action A's last frame as action B's start) keeps positional continuity — keep chains ≤2 deep, they drift.

- **Mixed sizes:** image frames are ~1024px, video frames smaller (960px square at 720p). Downscale everything to the smallest source before matting (`magick in.png -resize 960x960 out.png`).
- **Playback fps:** source videos are ~24fps — drive sprite playback off elapsed time at ~1/24s, and only restart a loop when the animation state actually changes.

## 3D models

The `tripo` CLI (`npm install -g tripo-cli`) owns the whole 3D path: submit, poll, download, credit pre-check, refunds on failure. Its own agent docs are the reference — `tripo docs --llm`, then `tripo docs --topic commands/process` / `examples/animation` / `common-errors` — this section only covers what is specific to game use here.

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
- Rig: `rig:model=v1.0-20240301` for bipeds, with the `preset:biped:*` clips below. The CLI's default rig (v2.5) covers quadrupeds, avians, etc. with `preset:<name>` clips (`idle walk run dive climb jump slash shoot hurt fall turn`). `rig-check` in the chain aborts before rigging if the mesh isn't riggable. `--animate-in-place` when game code drives locomotion.
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

Presets are generic stock clips. Custom humanoid moves (`gen-moves`, motion.md) go onto a `mia-rig` rig, not a Tripo one.

## Voice — Gemini TTS

For what `qwen-tts` can't do: one character voice acting every line differently, vocal bursts and barks, staged two-speaker dialogue, 130 languages with regional accents. Gemini 3.8 Flash TTS, ~0.25¢ per 10 s line; `--model gemini-3.8-flash-lite-tts` is a third cheaper with plainer acting and fewer languages, for bulk neutral lines. [Prompting guide](https://ai.google.dev/gemini-api/docs/speech-generation#prompting-guide).

The text is spoken verbatim, so direction never goes in it. Each kind of direction has its own place:
- **Who is speaking** — species, age, gender, timbre, accent — is the voice. Cast it once per character (below).
- **How the whole line is delivered** goes in `--style`, kept short: `"whispered, nervous"`, `"shouting over battle"`. Most lines need none; reuse one string for a character's baseline.
- **What happens at a moment** goes inline as angle-bracket tags: `<laugh>`, `<sigh>`, `<gasp>`, `<groan>`, `<short pause>`, etc. ([full list](https://ai.google.dev/gemini-api/docs/speech-generation#vocal-bursts)). CAPS stresses a word.

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py speech --voice Algenib --style "proud, a little amused" \
  -o ${RUNTIME_ASSET_DIR}/audio/dwarf_01.ogg --text "<chuckle> Aye, that blade'll hold. <short pause> Forged it meself, three nights without sleep."
```

- **Natural lines.** Write lines as people talk ("Oh, uh... hm, fine."); plain transcripts beat heavy styling.
- **Traits stay in the voice.** Age, gender or accent in `--style` fights the voice; cast another voice instead. Instructions to "keep the same voice" add drift.
- **Barks.** A tags-only line works: `--text "<grunt> <scream>" --style "hit by an arrow, falling"` is a death cry. Tags are human sounds only; do effects (radio, robot, echo) on the finished line.
- **Other languages.** Write the transcript in the language; tags stay English.

### Casting a character

**Realistic humans** come from the voice library: 2,000+ adult voices tagged with language, regional accent, gender, pitch, and an age and role in the description. Browsing is free: `asset_gen.py voice list --language ja-JP --gender male --pitch low`, `--search "60-year-old"`. The 30 studio voices (Kore, Puck, Algenib…) are in it too.

**Everything else** (creatures, villains, wizards, stylized heroes) gets a designed voice:

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py voice design --name Grukk --gender male \
  --prompt "A small, wiry cave goblin with a high, nasal, raspy voice; sneaky and quick, giggles at his own schemes." \
  -o voices/grukk_audition.wav
```

- **Result.** `"voice": "voice_..."`, used in `--voice` and `--speakers` like a name. ~1–2¢; `-o` gets a 30–60 s in-character audition to check before voicing lines.
- **Prompt.** 1–2 sentences of permanent traits: who, age, timbre, texture, accent, attitude. Long or contradictory prompts drift. Per-line emotion still comes from `--style`.
- **Persistence.** The voice lives for a year in the key's Google project (200 max), and its id is the only handle on it: record the id in the asset manifest next to the character. `voice list --mine`, `voice delete ID`.
- **Children.** Designs of child voices are refused ("blocked by safety policies"). Use `qwen-tts`, or the youthful prebuilt Leda.
- **The user's own voice.** They create it in AI Studio's [Voice replication](https://aistudio.google.com/generate-speech), which needs their spoken consent, and give you the `voice_...` id.

### Dialogue

Games usually play lines one at a time: one file per line. `--speakers` is for one clip where the timing between two characters matters (a cutscene, radio chatter, a bark exchange):

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py speech --speakers "Guard=Orus,Grukk=voice_abc123" \
  -o ${RUNTIME_ASSET_DIR}/audio/bridge_toll.ogg --text "Guard (bored): Toll is five coppers. |five?!| Five.
Grukk (outraged): FIVE? <gasp> For a BRIDGE?"
```

- **Line format.** One `Name (style): text` per line; `(style)` is optional.
- **Backchannel.** `|...|` inside a turn is the other speaker's backchannel or overlap, spoken without breaking the turn.
- **Limit.** Two speakers per call; designed voices work here too.

## Music — Lyria

Prompting: [Lyria prompt guide](https://ai.google.dev/gemini-api/docs/lyria-prompt-guide).

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py music -o music_src/shop_theme.mp3 --prompt \
  "Lo-Fi Hip Hop, cozy village shop theme, 85 BPM, in F major, warm Rhodes piano, soft vinyl crackle, brushed drums, upright bass. Instrumental only, no vocals."
```

- **Lengths.**
  - `--length clip` (the default) returns about 30 s, which is enough for a loop.
  - `--length song` returns a full piece. Ask for its length in the prompt, but expect it to overshoot: a request for 45 s came back 67 s long.
- **Vocals.** Vocals are the default, so write "Instrumental only, no vocals" unless you want singing.
- **Format.** Lyria returns MP3 only; other `-o` extensions are converted.
- **Mood from art.** `--image concept.png` takes the mood from an image.
- **Access.** Lyria has no free tier. If the key is on the free tier, the call fails; tell the user instead of retrying.

### Loops

Lyria pieces start and end like pieces; it has no loop mode. To make a loop, put a BPM in the prompt, then cut whole bars with `loop_audio.py`. It crossfades the audio past the cut into the start, so the file loops with plain engine looping:

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/loop_audio.py music_src/shop_theme.mp3 --bpm 85 --bars 8 --start-bars 1 -o ${RUNTIME_ASSET_DIR}/audio/shop_loop.ogg
```

- **Intro.** `--start-bars` skips it.
- **Tempo drift.** If Lyria played a different tempo than the prompt asked for, bar cuts drift. Cut with `--start`/`--length` in seconds instead; that also works for ambience.

## Costs

Quick reference: 1K image 6–7¢ · 2K background 8–10¢ · a quality-critical image generated on both models ~13¢ · sprite video 14¢/s at 720p · Gemini TTS ~0.25¢ per 10 s line, a designed voice 1–2¢ (both double from 2027) · Lyria 4¢ per 30 s clip, 8¢ per song. Tripo bills in credits (≈1¢): ~30 per model, ~25 to rig, ~10 per retargeted clip — `tripo balance` before a batch, and report the `credits_consumed` the CLI returns rather than an estimate.

## Output and logging

Each `asset_gen.py` command prints JSON to stdout: `{"ok": true, "path": "...", "cost_cents": 7}`; `tripo` prints its own with `--json`. Progress goes to stderr — redirect it to a temp file and read only on failure to keep context clean:

```bash
_log=$(mktemp)
result=$(python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image --prompt "..." -o p.png 2>"$_log") || tail -20 "$_log"
```

Generate independent API images in parallel (multiple Bash calls in one message).
