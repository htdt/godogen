---
name: asset-gen
description: |
  Generate assets for a game, a video or any other project: images, transparent sprites and animated GIF sprites (GPT-Image-2.6, batched at half price), textured GLB models, rigged humanoids with generated moves and lip-synced speech, sound effects and voice lines (local and free with godogen_assets), 3D built in Blender, plus Grok sprite video, Tripo 3D, Gemini TTS voice acting and Lyria music. Use whenever a project needs generated art, 3D or audio.
---

# Asset Generator

`api.md`, `motion.md` and `scripts/` sit next to this file. Commands run from the project, so call the scripts by their full path. Missing tools: Setup, at the end.

## Where assets come from

Choose by asset type, then let the user's words decide: a budget, "free" or "local only", or "best quality".

- **Images.** GPT-Image-2.6 Sunburst (`api.md`) makes everything on screen: characters, sprites, animated sprites, backgrounds, key art, UI with text, and the reference images that 3D is built from. It is paid: 2.2¢ for a batched 1024x1024 at medium. Local `qwen-image` is free but only good for basic assets (flat textures, simple icons, placeholders); use it for everything only when the user asks for free or local, or when `OPENAI_API_KEY` isn't set.
- **3D.** Local first. `gen3d` turns a reference image into a textured GLB, and the humanoid tools rig and animate it. Blender builds what generation doesn't (below). Use Tripo (api.md) when godogen_assets isn't set up, or to rig a non-humanoid.
- **Audio.** Use local `stable-audio` and `qwen-tts` for sound effects and voice lines. The paid APIs cover music, a voice that acts many emotions, barks, two-speaker dialogue, and languages `qwen-tts` lacks.

When the brief says nothing about spending, propose paid images with an estimate for the whole set when you confirm the first paid call. The user can choose free local images instead. Without godogen_assets (its commands aren't on `PATH`, or answer `not installed`), 3D and audio come from the paid APIs too.

## Local: godogen_assets

[godogen_assets](https://github.com/htdt/godogen_assets) runs local generators on this machine's GPU, one command per task, for free. Its docs are the reference; this page is the TL;DR plus what a project needs on top. Its checkout is where its commands resolve, `$GODOGEN_ASSETS` below. The lookup fails when the commands aren't on `PATH`, which means godogen_assets isn't set up:

```bash
p=$(command -v gen3d) && GODOGEN_ASSETS=$(dirname "$(dirname "$(readlink -f "$p")")")
```

Read `$GODOGEN_ASSETS/README.md` once (conventions, a character start to finish, checking results). Before first using a part's tool, read its README up to `How it works`.

| Command | Makes | README in the checkout |
|---------|-------|------------------------|
| `qwen-image` | basic PNGs from text; `rgba`: real transparency; `edit -i ref.png`: image-to-image | `image/` |
| `gen3d` | textured GLB from an image | `mesh/` |
| `mia-rig` | Mixamo-rigged humanoid from a GLB | `rig/` |
| `add-moves`, `gen-moves` | idle/walk/run/jump onto a rig; custom moves from text prompts | `motion/` |
| `grip-prop` | a prop made holdable; `add-moves --hold` puts it in a character's hand | `motion/` |
| `lipsync` | speaking mouth + lip-synced clip from a voice line | `lipsync/` |
| `stable-audio` | sound effects, seamless ambience loops | `sfx/` |
| `qwen-tts` | voice lines from a description, or cloned from a reference line | `voice/` |

A character: a transparent T-pose reference (`asset_gen.py image --transparent --quality high`, or `qwen-image rgba`) → `gen3d` → `mia-rig --fingers --anim none` → `add-moves`, with `gen-moves` for custom moves and `lipsync` for speech. Props stop after `gen3d`; one a character holds goes on through `grip-prop` and `add-moves --hold`, never by an offset tuned in the engine.

- **Always pass `-o`** into the project; without it, results land in the godogen_assets checkout.
- **One GPU job at a time, minutes per call.** Run GPU tools as one sequential batch with a long timeout or in the background, never as parallel calls.
- **Real-time budget.** `gen3d` defaults to ~500k triangles and 2048² textures; pass `--faces` / `--tex` (30000 / 1024 for a game character).
- **Style families.** Generate one hero asset and derive the rest from it (`--image hero.png` in api.md, or `qwen-image edit -i hero.png`), prompting only what changes.
- **Small sprites.** A 1024px image downscaled to 64px looks muddy: design display sizes ≥128px, prompt bold flat forms, or generate a kit (several objects in one image) and slice it with `python3 scripts/grid_slice.py kit.png -o out/ --grid 2x2 --names "a,b,c,d"`.
- **Direction.** Generators get left/right and facing wrong; generate one direction and flip at runtime.
- **Audio format.** Every tool picks it from the `-o` extension. Bevy's default features decode only Ogg Vorbis, so write `.ogg` for Bevy.
- **Seeing GLBs and audio.** Render GLBs to images (`$GODOGEN_ASSETS/README.md`, Checking results); read audio as a spectrogram (`$GODOGEN_ASSETS/sfx/README.md`).

Moves that drive gameplay — root-motion locomotion, attacks, state machines, anything held, ridden or aimed, characters that touch each other: read `motion.md`.

## Blender

A `bpy` script run headless (`blender -b -P make_turret.py`, exporting with `bpy.ops.export_scene.gltf`) builds the 3D the generators don't: exact or articulated shapes (wheels that turn, a turret that aims, snap-together kit pieces), work on a generated GLB (split, new pivots, decimate, merge), and animation outside the humanoid tools (mechanical parts, a creature of a few bones, keyframed or procedural clips). Without `blender` on `PATH`, `asset-blender script.py -- args` runs the script in godogen_assets' Blender (its `print` goes to stderr).

## Paid APIs

`api.md` covers GPT-Image-2.6 Sunburst images and animated GIF sprites, sprites from Grok video, Tripo 3D, Gemini TTS and Lyria music. Paid calls cost real money: confirm with the user before the first one.

## Asset manifest (in README.md)

Track every generated asset in the project's `README.md` with a **Size** column, the size it has in the scene. `gen3d` models come out 1.0 tall with no real scale, so this column is where their size is decided:

- 3D models: meters, e.g. `4m long`, `1.8m tall`, `0.3m`
- Textures: tile size, e.g. `2m tile`
- Backgrounds: pixel size + behavior, e.g. `1920x1080, fullscreen`
- Sprites: display pixels, e.g. `128x128 px`
- Audio: length + use, e.g. `1.2 s one-shot`, `8 bars / 22.6 s loop`

| Name | Description | Size | Path | Cost |
|------|-------------|------|------|------|
| crate | wooden supply crate | 0.8m | assets/glb/crate.glb | local |
| theme | village shop music | 8 bars / 22.6 s loop | assets/audio/shop_loop.ogg | 4¢ |

## Setup

Install the current releases, resolved at install time:

- **Python packages:** `pip install -U -r scripts/requirements.txt`, into a venv when the system Python refuses.
- **Blender:** the current release (blender.org, `snap install blender --classic`, `brew install --cask blender`). Without it, `asset-blender` runs godogen_assets' own.
- **godogen_assets:** its README's Setup is written for an agent to follow on this machine. It needs an NVIDIA GPU, ~130 GB of free disk, the user's Hugging Face token, and a long download, so set it up only when the user wants local generation. `./setup.sh link` then puts its commands on `PATH`.
- **API keys** belong to the user, as environment variables (`api.md`). Name the missing one and where to get it rather than working around it.
