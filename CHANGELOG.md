# Changelog

**2026-11-19 — Two skills; the engine is chosen per project**
- Godogen is two skills in the open Agent Skills format that Claude Code, Codex and Antigravity share: `engine-guide` and `asset-gen`, under `skills/`. `npx skills add htdt/godogen` installs them into a project's `.agents/skills/` (linked from `.claude/skills/` for Claude Code), `-g` for all projects, and `npx skills update` updates them; the README also shows linking a clone. There is no publish step and no per-engine repo.
- `engine-guide` carries every engine guide plus a short manual for choosing one, so the engine is settled with the agent per project: what the user holds at the end, how they watch, 2D, language, what's installed.
- Beyond games: Godot's movie writer, Bevy's offscreen binary and three.js's stepped capture save one frame per fixed timestep, so an engine renders videos (presentations, explainers, trailers, product showcases) with generated voice-over and music placed on the same timeline. The movie writer records the scene's audio in sync to `frame.wav` beside the frames. Interactive pages (configurators, explainers, data visualizations) use the same guides.
- The agent sets up the machine. `engine-guide/setup.md` installs each engine's toolchain and `asset-gen` (Setup) its Python packages, Blender and godogen_assets, all at current stable releases resolved at install time: the newest Godot from its GitHub releases, the newest .NET SDK, current Rust and Node LTS. The guides name no fixed Node or Rust edition. API keys and the GPU stay with the user.
- `asset-gen` finds the godogen_assets checkout through its commands on `PATH`, references its own files by paths relative to the skill, and keeps its Python in `scripts/`. Both skills' frontmatter is `name` and `description`.
- The README is the one overview, and short: the idea, the two skills, install, what only the user provides, how to use them, and how the repo went from detailed guidance to building blocks.

**2026-11-18 — GPT-Image-2.6 Sunburst images, batched**
- Assets come from the best source for their type, and the user's brief sets the spend. Images come from GPT-Image-2.6, and local Qwen-Image is used only for basic assets or when the user asks for free or local. 3D stays local (`gen3d`, the humanoid tools, Blender). When the brief says nothing about spending, the agent proposes paid images with an estimate for the set at its first cost confirmation.
- Paid images come from OpenAI's `gpt-image-2.6-sunburst` (`OPENAI_API_KEY`); Gemini and Grok images are retired. `asset_gen.py batch jobs.jsonl` sends a whole set through the Batch API at half price, polls until every image is saved, and resumes from `jobs.jsonl.batch.json` rather than resubmitting; `asset_gen.py image` is the live call for whatever the next step waits on. Costs are computed from the token usage the API returns.
- `--transparent` returns real alpha (1-bit in GIF); the faint haze that edits leave in the background (alpha ~10) is cleared on save. Background removal is gone: `rembg_matting.py`, `rembg.md` and the `rembg` / `pymatting` / `onnxruntime-gpu` requirements. Grok video frames keep their solid background. `--image` takes up to 16 references, and `--complexity low` keeps focused edits from replanning the scene. `--model flare` makes fast drafts.
- Animated GIF output (`-o x.gif --frames 2–16 --frame-ms`) makes short sprite cycles from a reference in one call; Grok video stays for longer or smoother motion. `api.md` carries the quality guide and measured costs.

**2026-10-16 — Local assets by default, audio, GDScript and three.js**
- Assets come from [godogen_assets](https://github.com/htdt/godogen_assets) by default: free local generators for images (Qwen-Image), textured 3D (TRELLIS.2), humanoid rigging (Make-It-Animatable), Kimodo moves (`gen-moves`, `add-moves`), lip-sync, sound effects (Stable Audio 3) and voice lines (Qwen3-TTS). `asset-gen/SKILL.md` is a TL;DR linking to its docs; its README carries the setup, and `publish.sh` writes the checkout recorded in `.godogen_assets` into the published skill.
- Blender is a recommended dependency: `asset-gen` scripts it headless for 3D better built than generated — exact or articulated models, edits to generated GLBs, mechanical and non-humanoid animation — and falls back to godogen_assets' own Blender through `asset-blender` when `blender` isn't on `PATH`.
- Paid APIs live in `asset-gen/api.md`, read only when the local tools are missing or can't make an asset: Gemini / Grok images, animated sprites from Grok video, Tripo 3D, Gemini TTS voice acting and Lyria music (`asset_gen.py music`), with `loop_audio.py` cutting seamless music loops. API keys and the Tripo CLI are optional.
- `asset_gen.py speech` runs Gemini 3.8 Flash TTS through the Interactions API (~0.25¢ per 10 s line; `--model gemini-3.8-flash-lite-tts` for bulk). The text is a verbatim transcript: whole-line delivery goes in `--style`, moments in inline `<tags>`, and `--speakers` takes `Name (style): text` lines staged in conversational mode with `|backchannels|`.
- `asset_gen.py voice design` creates a persistent `voice_...` from a one- or two-sentence description and saves its in-character audition (~1–2¢). `voice list` browses the 2,000+ voice library by language, accent, gender and pitch; `voice delete` frees a slot. `api.md` covers casting (library voices for realistic humans, designed voices for everything else), barks from tags alone, dialogue clips, the refusal of child voices, and using the user's own replicated voice.
- A character holds a prop through godogen_assets' `grip-prop` and `add-moves --hold`: the prop's handle is found, the hand gets a `grip_r` / `grip_l` node to parent the prop to with an identity transform, its fingers close on the handle, and `rootmotion.json` carries the prop's path per clip, with strike timing read from its tip.
- `motion.md` is the game side of the `add-moves` output: authored key poses pinned as spec constraints, root motion and impact timing from `rootmotion.json` (`frameData` measured on the move alone), prop-relative gates, and "Held props and contact" — the one-number attachment check, moves generated for their prop, and how two characters meet (events and distances read from data, IK on the contact, every exchange verified on the posed skeleton), with the full rules in godogen_assets' `motion/HELD_PROPS.md`.
- `--engine godot-gdscript`: Godot 4 in statically typed GDScript on any Godot build, with the same build-time scene builders and movie-writer capture as C#. With no compiler, the guide gates on `--check-only` per script and on `SCRIPT ERROR` in the log (a runtime error leaves the exit code at 0), and names the silent drop of `set()` before `set_script()`.
- `--engine threejs`: three.js + Vite + TypeScript at a live URL; the agent picks physics (Rapier) and UI itself. The guide covers color space, physical light units and shadow bounds, rigged clones, the WebGPU→WebGL2 fallback, and headless Chrome capture stepped from the capture script.
- README "Choosing an engine" compares the five options: how you watch, 2D, C# vs GDScript, Babylon.js vs three.js, Bevy.

**2026-09-22 — Local image generation, current image models**
- Added local image generation: when `qwen-image` is on PATH, `asset-gen` runs Qwen-Image-2.1 on the machine's GPU for free, so simple images (textures, props, icons, UI, backgrounds, in-image text) go there before the paid APIs; `qwen-image rgba` outputs real alpha with no matting. `setup.md` carries a brief for building the command on each machine.
- Image generation uses Gemini 3.1 Flash Image and Grok Imagine Image 2.0 (medium quality) as equals — a side-by-side on a 3D-ready character and a dense composition came out even. `asset_gen.py` uses whichever key is set, Gemini by default for speed (~10 s vs 1–2 min); quality-critical assets are generated on both and the better kept.
- Sprite video uses `grok-imagine-video-1.5` without audio (14¢/s at 720p, 8¢/s at 480p). Grok results report the cost xAI actually billed; Grok requires `xai-sdk>=1.19`.
- Background removal preloads the CUDA libraries from the `nvidia-*` wheels and checks the provider the session actually runs on, so a mismatched `onnxruntime-gpu` build warns instead of silently running on CPU; requirements pull matching CUDA/cuDNN via `onnxruntime-gpu[cuda,cudnn]`. `rembg_matting.py --preview` no longer crashes.

**2026-09-22 — Custom character animation, Tripo CLI**
- Added custom humanoid animation through `asset-gen/motion.md`: move sets generated locally with [kimodo-practical](https://github.com/htdt/kimodo-practical) (NVIDIA Kimodo), baked to ordinary glTF clips plus `rootmotion.json`, so the game repo carries no motion tooling. Reached from the asset-gen skill when stock retarget presets aren't enough.
- `motion.md` covers the environment, the Tripo-rig → Kimodo and prebake → engine bridges, the authored-pose hybrid (game-authored key poses pinned as `fullbody` constraints), impact timing, numeric prop-relative gates, and a pitfalls index from shipped move sets.
- The animation stack is machine-level under `KIMODO_HOME` with a fixed layout (`kimodo-practical/`, `kimodo/`, `kimenv/`, `text_encoders/`); each project clones its motion workspace from the local reference. Install and verify steps in `setup.md`.
- 3D generation, rigging, and retargeting go through the `tripo` CLI (`npm install -g tripo-cli`, `TRIPO_API_KEY`), which owns submit/poll/download, credit pre-checks, and resume. Removed the in-repo `tripo3d.py` client and the `glb` / `rig` / `retarget` / `resume` subcommands from `asset_gen.py`; Tripo costs are reported in credits.
- Node.js 20+ is now needed for every engine (Tripo CLI); published repos ignore `/tripo-out`.

**2026-07-02 — Docs-only runtime**
- Replaced the multi-stage skill pipeline with a thin runtime: a single engine-agnostic manifest (`prompts/runtime.md`), a one-page per-engine guide, and the cross-engine `asset-gen` skill. The model plans, scaffolds, and decomposes the work itself.
- One runtime manifest covers delivery. The agent reads how the task is framed in-run: an open-ended direction gets the live game early and checkpoints at taste/scope/cost decisions; a finished brief runs on reasonable calls and closes with a 15–20s proof recording, watched back before done. Run/show/capture mechanics live in the engine guides and serve both paths.
- Dropped the planner/decomposer/architecture/scene/scaffold/quirks/capture skill docs, the Vite scaffold, the `godot-api` / `bevy-help` / `babylon-help` lookup skills, and all hooks. The engine-specific traps and capture recipes that survive a compile but fail at runtime moved into the engine guide.
- Trimmed asset docs to generation only; `asset-gen` is now the sole published skill.
- Reorganized the source tree: engine-agnostic runtime text lives in `prompts/runtime.md`, and the asset skill lives at top-level `asset-gen/`.
- Continues the 2026-04-26 "dropped Gemini verification" trajectory — removing guidance the current model no longer needs.

**2026-05-18 — Babylon.js support**
- Added Babylon.js as a first-class engine alongside Godot and Bevy
- Disposable TypeScript/Vite scaffold with scene-level hot reload through a custom Vite plugin (`godogen:scene-change`); engine and canvas persist across edits
- Browser capture through Playwright + Chrome/Chromium; hardware WebGL2 preferred, software-renderer fallback warns prominently but still produces media
- `babylon-help` skill uses installed npm package types as the primary local reference
- `publish.sh` extended to `--engine babylon`

**2026-04-26 — Bevy support**
- Added Bevy as a first-class engine alongside Godot
- Replaced the four Claude/Codex source trees with `shared/`, `godot/`, and `bevy/`
- Added one root `publish.sh` switcher: `--engine godot|bevy` × `--agent claude|codex`
- Dropped Gemini verification — Opus 4.7 / GPT 5.5 self-verify from captured frames; external pass added no signal; the stop hook pushes the latest proof video to Telegram

**2026-04-14 — Codex support**
- Added a parallel Codex source tree alongside the existing Claude Code one
- Each variant publishes to its own runtime layout (`.claude/skills/` vs `.agents/skills/`)

**2026-04-06 — C# migration**
- All skills and generated code migrated from GDScript to C# / .NET 9
- `dotnet build` replaces per-file validation loops

**2026-04-03 — Single-context architecture**
- Orchestrator and task execution merged into one main pipeline
- Added Godot API lookup and visual QA support flows

**2026-03-25 — xAI Grok video**
- Added Grok video generation for animated sprite workflows
- Background removal rewritten with BiRefNet multi-signal matting

**2026-03-09 — Initial release**
- Initial Godogen release with image generation, 3D conversion, screenshot QA, and video capture
