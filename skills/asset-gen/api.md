# Paid APIs

Images by default, plus what the local tools can't make (SKILL.md, Where assets come from). Every call costs real money; record it in the asset manifest.

Keys, which the user creates: `OPENAI_API_KEY` (images, animated GIF sprites; platform.openai.com/api-keys), `XAI_API_KEY` (sprite video; console.x.ai), `GOOGLE_API_KEY` (Gemini TTS, Lyria; aistudio.google.com), `TRIPO_API_KEY` (the `tripo` CLI; developers.tripo3d.ai). Images, video and audio go through `scripts/asset_gen.py`; 3D goes through the `tripo` CLI.

## Images — GPT-Image-2.6 Sunburst

- **Batch by default.** Put every image of a set in one JSONL and run `batch`: half price, but it takes ~30–60 min (24 h guaranteed), so start it early and keep building meanwhile. Use `image` (live, full price, ~20 s) only for what the next step waits on: the reference a set derives from, a style draft, a single redo.
- **Quality.** `medium` (the default) for sprites, props, icons and tiles. `high` costs only ~20% more: use it for the reference that a set or a 3D model is built from, dense text, and full-screen art. `low` is already clean on flat, stylized props, and works for drafts and GIF cycles. `xhigh` and `max` are untested here; keep them for large key art.
- **Real transparency.** `--transparent` (`"transparent": true` in a job) returns real alpha, 1-bit in a GIF. Leave the background out of the prompt.
- **References.** `--image ref.png`, repeatable up to 16: the first image is the one edited, the rest guide it. Prompt only what changes. Add `--complexity low` for focused edits (a recolor, a pose, a variant); the default `high` replans the whole scene and can change what should stay.
- **Size.** `WIDTHxHEIGHT` in multiples of 16, ratio 1:3–3:1, edge ≤3840, 0.66–8.3 MP, so the smallest still is 1024x640. The default is 1024x1024. A 1080p background is `1920x1088`, cropped afterwards.
- **Drafts.** `--model flare --quality low` returns in seconds at the same token price.

| 1024x1024 | low | medium | high |
|-----------|-----|--------|------|
| live | 2.5¢ | 4.4¢ | 5.3¢ |
| batch | 1.25¢ | 2.2¢ | 2.6¢ |

Cost grows with pixels, and a reference image adds ~0.4¢ (batched). `cost_cents` is computed from the token usage the API returns.

```bash
python3 scripts/asset_gen.py image --quality high --transparent \
  --prompt "the full prompt" -o assets/img/knight.png
```

`-o` picks the format: `.png`, `.webp`, `.jpg`, `.gif`.

### Batch

```bash
cat > img_jobs.jsonl <<'EOF'
{"prompt": "...", "o": "assets/img/chest.png", "transparent": true}
{"prompt": "The same knight, sword raised overhead", "o": "assets/img/knight_cheer.png", "image": "assets/img/knight.png", "complexity": "low", "transparent": true}
{"prompt": "...", "o": "assets/img/forest_bg.png", "size": "1920x1088", "quality": "high"}
EOF
python3 scripts/asset_gen.py batch img_jobs.jsonl
```

- **Jobs.** Each line takes `prompt` and `o`, plus any of `image` (a path or a list), `quality`, `model`, `size`, `transparent`, `complexity`, `frames`, `frame_ms`. `--quality` and `--model` set the default for lines that leave them out.
- **References come from earlier runs.** A job can't use another job's output from the same batch as its reference.
- **Waiting.** The command polls until every image is saved, then prints one JSON object with a result per image. Run long sets in the background. `--no-wait` submits and returns.
- **Resuming.** The batch ids are kept in `img_jobs.jsonl.batch.json`, and rerunning the same command resumes instead of resubmitting. Once a set is collected, a rerun only reports its results, so files edited since are safe. Edit the jobs file and rerun to submit a new batch once the old one has finished.
- **Failures.** A failed image reports its error; retry it from a new jobs file. OpenAI guarantees only 24 h, so a slow batch isn't a failure.

## Animated sprites

### GIF

A short cycle (idle, walk, attack, a spinning pickup) comes out as one GIF made from the character's reference:

```bash
python3 scripts/asset_gen.py image --image knight.png --transparent --frames 8 --frame-ms 100 \
  -o walk.gif --prompt "The same knight walking to the right in a smooth walk cycle, side view, fixed camera; the eighth frame flows back into the first"
```

- **Frames.** `--frames` takes 2–16 (default 9). `--frame-ms` sets the delay per frame, 20–2000 ms (default 200); it is also the playback rate. GIF jobs batch like stills.
- **Output.** Each frame is 512x512 with `auto` size, and the GIF loops forever. 8 medium frames cost ~3.8¢ live; 6 low frames cost 1.3¢ batched.
- **Consistency.** Frames keep the reference's design, and the character moves in place.
- **Prompt.** Describe the motion and how the loop closes, and fix the camera.
- **Alpha.** It is 1-bit, so edges are hard.
- **Frames for the engine.** Only HTML plays a GIF directly. Elsewhere, split it with `magick walk.gif -coalesce frames/%02d.png` and play the frames at `--frame-ms`.

### Video

For motion longer or smoother than 16 frames: **reference → pose → video → extract frames → loop-trim.** Frames keep the video's solid background; nothing here mattes it out, so this fits a scene drawn in that color, or a color key in the engine's sprite shader.

1. Reference (1024x1024, neutral pose, without `--transparent`: video needs a solid background, in a color distinct from the subject) — anchors everything.
2. Pose per action: `--image` from the reference with `--complexity low`, prompt only the action.
3. Video from the pose frame: `asset_gen.py video --image pose.png --duration 2 -o walk.mp4` (Grok, needs `XAI_API_KEY`; `--duration` 1–15s; `--resolution` 720p at 14¢/s, or 480p at 8¢/s — enough for small sprites).
4. Extract: `ffmpeg -i walk.mp4 -vsync 0 frames/%04d.png`.
5. Loop-trim looping cycles (walk/idle): `scripts/find_loop_frame.py frames/` returns the loop frame; delete frames past it. Skip for one-shots (attack/death).

Reuse one reference for all of a character's actions. **Chaining** (feed action A's last frame as action B's start) keeps positional continuity — keep chains ≤2 deep, they drift.

- **Mixed sizes:** image frames are ~1024px, video frames smaller (960px square at 720p). Downscale everything to the smallest source (`magick in.png -resize 960x960 out.png`).
- **Playback fps:** source videos are ~24fps — drive sprite playback off elapsed time at ~1/24s, and only restart a loop when the animation state actually changes.

## 3D models

The `tripo` CLI (`npm install -g tripo-cli`) owns the whole 3D path: submit, poll, download, credit pre-check, refunds on failure. Its own agent docs are the reference — `tripo docs --llm`, then `tripo docs --topic commands/process` / `examples/animation` / `common-errors` — this section only covers what is specific to game use here.

```bash
tripo make ref.png --name car -p face_limit=30000 -p auto_size=true --json --yes -o assets/glb
tripo make ref.png --name hero --then rig-check,rig:model=v1.0-20240301 --json --yes -o assets/glb
tripo anim retarget @hero --animation preset:biped:walk preset:biped:idle --json --yes -o assets/glb
```

- `make` is blocking (default timeout 30 min) and prints one JSON line: read `model_file`, `preview.png` and `credits_consumed` from it. Never add your own shorter timeout, never resubmit because a task_id appeared in stderr. If the process does die, `tripo task watch <id> --download` finishes the same task for free.
- Output lands in `<-o dir>/<name>-<id8>/` (`model.glb`, `preview.png`, `task.json`). Move or reference the GLB from there; `task.json` keeps the seeds and task id, so there is nothing else to save.
- `--name X` makes the task addressable as `@X` for later steps (retarget, convert, decimate). Retarget reuses the rig task — never re-rig for another clip; up to 5 animations per call, billed per animation.
- Model defaults to v3.1. For `face_limit` ≤ 20000 the CLI silently switches to P1 (low-poly topology, no `geometry_quality`) — that is the right choice for mobile-style budgets, but know it happens. `--for game-pc` converts to FBX by default; skip it for GLB engines.
- `-p geometry_quality=detailed -p texture_quality=detailed` is the HD tier (≈ double credits).
- Rig: `rig:model=v1.0-20240301` for bipeds, with the `preset:biped:*` clips below. The CLI's default rig (v2.5) covers quadrupeds, avians, etc. with `preset:<name>` clips (`idle walk run dive climb jump slash shoot hurt fall turn`). `rig-check` in the chain aborts before rigging if the mesh isn't riggable. `--animate-in-place` when game code drives locomotion.
- Don't assume the preset name survives into the GLB; inspect the imported clip names before wiring playback.

Source image for `make`: 3/4 elevated angle, solid white/gray background, matte finish, opaque glass, single centered subject — and **no** `--transparent` (Tripo needs the solid bg). For characters, generate the reference in a T-pose.

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
python3 scripts/asset_gen.py speech --voice Algenib --style "proud, a little amused" \
  -o assets/audio/dwarf_01.ogg --text "<chuckle> Aye, that blade'll hold. <short pause> Forged it meself, three nights without sleep."
```

- **Natural lines.** Write lines as people talk ("Oh, uh... hm, fine."); plain transcripts beat heavy styling.
- **Traits stay in the voice.** Age, gender or accent in `--style` fights the voice; cast another voice instead. Instructions to "keep the same voice" add drift.
- **Barks.** A tags-only line works: `--text "<grunt> <scream>" --style "hit by an arrow, falling"` is a death cry. Tags are human sounds only; do effects (radio, robot, echo) on the finished line.
- **Other languages.** Write the transcript in the language; tags stay English.

### Casting a character

**Realistic humans** come from the voice library: 2,000+ adult voices tagged with language, regional accent, gender, pitch, and an age and role in the description. Browsing is free: `asset_gen.py voice list --language ja-JP --gender male --pitch low`, `--search "60-year-old"`. The 30 studio voices (Kore, Puck, Algenib…) are in it too.

**Everything else** (creatures, villains, wizards, stylized heroes) gets a designed voice:

```bash
python3 scripts/asset_gen.py voice design --name Grukk --gender male \
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
python3 scripts/asset_gen.py speech --speakers "Guard=Orus,Grukk=voice_abc123" \
  -o assets/audio/bridge_toll.ogg --text "Guard (bored): Toll is five coppers. |five?!| Five.
Grukk (outraged): FIVE? <gasp> For a BRIDGE?"
```

- **Line format.** One `Name (style): text` per line; `(style)` is optional.
- **Backchannel.** `|...|` inside a turn is the other speaker's backchannel or overlap, spoken without breaking the turn.
- **Limit.** Two speakers per call; designed voices work here too.

## Music — Lyria

Prompting: [Lyria prompt guide](https://ai.google.dev/gemini-api/docs/lyria-prompt-guide).

```bash
python3 scripts/asset_gen.py music -o music_src/shop_theme.mp3 --prompt \
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
python3 scripts/loop_audio.py music_src/shop_theme.mp3 --bpm 85 --bars 8 --start-bars 1 -o assets/audio/shop_loop.ogg
```

- **Intro.** `--start-bars` skips it.
- **Tempo drift.** If Lyria played a different tempo than the prompt asked for, bar cuts drift. Cut with `--start`/`--length` in seconds instead; that also works for ambience.

## Costs

Quick reference: 1024x1024 image 2.2¢ batched at medium (4.4¢ live) · 8-frame medium GIF ~3.8¢ live · sprite video 14¢/s at 720p · Gemini TTS ~0.25¢ per 10 s line, a designed voice 1–2¢ (both double from 2027) · Lyria 4¢ per 30 s clip, 8¢ per song. Tripo bills in credits (≈1¢): ~30 per model, ~25 to rig, ~10 per retargeted clip — `tripo balance` before a batch, and report the `credits_consumed` the CLI returns rather than an estimate.

## Output and logging

Each `asset_gen.py` command prints JSON to stdout: `{"ok": true, "path": "...", "cost_cents": 7}`; `tripo` prints its own with `--json`. Progress goes to stderr. Unlike the local GPU tools, API calls can run in parallel.
