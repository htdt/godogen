---
name: asset-gen
display_name: Asset Generator
short_description: Generate game images, 3D models, animated characters, sound effects, voice and music
default_prompt: "Use ${ASSET_SKILL_COMMAND} to generate images, 3D models, characters, or audio for this game."
allow_implicit_invocation: true
description: |
  Generate game assets, locally and free by default with godogen_assets: images and transparent PNGs (Qwen-Image), textured GLB models (TRELLIS.2), rigged humanoids with generated moves and lip-synced speech, sound effects and voice lines. Paid APIs cover what the local tools can't make — Gemini / xAI Grok images, animated sprites from video, Tripo 3D, Gemini TTS voice acting, Lyria music. Use whenever a game needs generated art or audio.
---

# Asset Generator

Assets come from [godogen_assets](https://github.com/htdt/godogen_assets): local generators on this machine's GPU, one command per task, free. Its checkout here is `${GODOGEN_ASSETS}`, and its docs are the reference; this page is the TL;DR plus what the game needs on top. Read `${GODOGEN_ASSETS}/README.md` once (conventions, a character start to finish, checking results), and a part's README up to `How it works` before first using its tool.

| Command | Makes | README in the checkout |
|---------|-------|------------------------|
| `qwen-image` | PNG from text; `rgba`: real transparency; `edit -i ref.png`: image-to-image | `image/` |
| `gen3d` | textured GLB from an image | `mesh/` |
| `mia-rig` | Mixamo-rigged humanoid from a GLB | `rig/` |
| `add-moves`, `gen-moves` | idle/walk/run/jump onto a rig; custom moves from text prompts | `motion/` |
| `lipsync` | speaking mouth + lip-synced clip from a voice line | `lipsync/` |
| `stable-audio` | sound effects, seamless ambience loops | `sfx/` |
| `qwen-tts` | voice lines from a description, or cloned from a reference line | `voice/` |

A character: `qwen-image rgba` (T-pose) → `gen3d` → `mia-rig --fingers --anim none` → `add-moves`, with `gen-moves` for custom moves and `lipsync` for speech. Props stop after `gen3d`.

- **Always pass `-o`** into the project; without it, results land in the godogen_assets checkout.
- **One GPU job at a time, minutes per call.** Run GPU tools as one sequential batch with a long timeout or in the background, never as parallel calls.
- **Game budget.** `gen3d` defaults to ~500k triangles and 2048² textures; pass `--faces` / `--tex` (30000 / 1024 for a character).
- **Style families.** Generate one hero asset, derive the rest with `qwen-image edit -i hero.png`, prompting only what changes.
- **Small sprites.** A 1024px image downscaled to 64px looks muddy: design display sizes ≥128px, prompt bold flat forms, or generate a kit (several objects in one image) and slice it with `python3 ${ASSET_GEN_SKILL_DIR}/tools/grid_slice.py kit.png -o out/ --grid 2x2 --names "a,b,c,d"`.
- **Direction.** Generators get left/right and facing wrong; generate one direction and flip at runtime.
- **Audio format.** Every tool picks it from the `-o` extension. Bevy's default features decode only Ogg Vorbis, so write `.ogg` for Bevy.
- **Review before building on it.** Look at every PNG. You can't look at a GLB or hear a WAV: render GLBs (`${GODOGEN_ASSETS}/README.md`, Checking results) and read audio as a spectrogram (`${GODOGEN_ASSETS}/sfx/README.md`).

Moves that drive gameplay — root-motion locomotion, attacks, state machines, anything held, ridden or aimed: read `${ASSET_GEN_SKILL_DIR}/motion.md`.

## Paid APIs

`${ASSET_GEN_SKILL_DIR}/api.md` covers Gemini / xAI Grok images, animated sprites from Grok video, Tripo 3D, Gemini TTS and Lyria music. Read it only when an asset needs one:

- godogen_assets isn't on this machine (its checkout above reads `none`), or a command answers `not installed` — that part isn't set up;
- the local tools don't make it: frame-by-frame animated 2D sprites, music, voice acting with emotion tags, two-speaker dialogue, a language `qwen-tts` lacks, a rig for a non-humanoid;
- a local result stays wrong after rewording and a few seeds.

Paid calls cost real money: confirm with the user before the first one.

## Asset manifest (in README.md)

Track every generated asset in `README.md` with an **in-game Size** column — without it, coders consistently scale assets wrong. `gen3d` models come out 1.0 tall with no real scale, so this column is where their size is decided:

- 3D models: meters, e.g. `4m long`, `1.8m tall`, `0.3m`
- Textures: tile size, e.g. `2m tile`
- Backgrounds: pixel size + behavior, e.g. `1920x1080, fullscreen`
- Sprites: display pixels, e.g. `128x128 px`
- Audio: length + use, e.g. `1.2 s one-shot`, `8 bars / 22.6 s loop`

| Name | Description | Size | Path | Cost |
|------|-------------|------|------|------|
| crate | wooden supply crate | 0.8m | ${RUNTIME_ASSET_DIR}/glb/crate.glb | local |
| theme | village shop music | 8 bars / 22.6 s loop | ${RUNTIME_ASSET_DIR}/audio/shop_loop.ogg | 4¢ |
