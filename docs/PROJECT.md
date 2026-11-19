# Godogen — Building Blocks for Coding Agents

Godogen is two agent skills that let Claude Code, Codex or Antigravity build games, and anything else a game engine renders well: a video presentation, a trailer, an interactive 3D page. It covers Godot, Bevy, Babylon.js, three.js and plain HTML.

It is not a game engine, a code generator, an asset marketplace or a pipeline. The agent is already a capable developer: it plans the work, writes the code, checks the result and decides what to hand back. Godogen supplies what it can't work out fast on its own, and nothing else.

## The skills

- **engine-guide**: how to choose an engine, how to install its toolchain at current versions, and one guide per engine with the stack, a project sketch, build commands, a headless capture recipe, and the traps that pass a build but fail at runtime.
- **asset-gen**: where each kind of asset comes from and how to make it, from GPT-Image-2.6 images to local 3D, rigged humanoids, sound and voice, Blender scripts and paid APIs, plus setting up its own tools.

The agent sets up the machine itself. All the user provides is API keys for paid generation and, for free local generation, an NVIDIA GPU.

Both are plain [Agent Skills](https://agentskills.io): a `SKILL.md` with a name and a description, plus the files it points to. The agent sees only the descriptions up front and reads the rest when a task needs it, so the guides for engines a project doesn't use cost nothing.

## The engine is chosen per project

The engine is chosen with the agent, per project. `engine-guide/SKILL.md` gives it the trade-offs to weigh with the user: what they hold at the end, how they watch while it's built, 2D, language, what's installed. A switch later is a rewrite.

- **Godot**: Godot 4 in C#/.NET or statically typed GDScript. Scenes are generated at build time by headless `SceneTree` scripts; the guide carries the serialization rules (owner chain, GLB-recursion trap, post-pack validation) and the `--write-movie` + ffmpeg capture recipe. GDScript, with no compiler, gates on `--check-only` per script and on `SCRIPT ERROR` in the log.
- **Bevy**: Rust, current stable Bevy resolved and pinned at build time, ECS scenes spawned `OnEnter`. The guide points the agent at the installed source for current APIs and gives the offscreen `RenderTarget::Image` capture recipe.
- **Babylon.js**: TypeScript/Vite, served at a live URL. The guide covers the side-effect-import trap, Havok physics and headless Chrome capture.
- **three.js**: TypeScript/Vite, served at a live URL; the agent picks physics (Rapier) and UI itself. The guide covers color space, physical lights, rigged clones, the WebGPU fallback and step-driven headless Chrome capture.
- **HTML**: text-first 2D in the DOM with CSS and TypeScript/Vite, canvas and three.js for motion, served at a live URL. The guide covers saves that survive the dev server's reloads, re-render and glyph-fallback traps, background-tab timing and the audio gesture rule.

## Beyond games

Godot's movie writer, Bevy's offscreen binary and three.js's stepped capture save one frame per fixed timestep, so render cost never shows in the result and every frame lands where it was scheduled. With voice-over and music from `asset-gen` placed on the same timeline, an engine becomes a studio for presentations, explainers, trailers and product showcases. The same guides build interactive pages: configurators, explainers, data visualizations.

## Each asset from its best source

Images come from GPT-Image-2.6, batched at half price. 3D, rigging, motion, sound effects and voice come from [godogen_assets](https://github.com/htdt/godogen_assets), free on the machine's GPU, and from Blender scripts. Paid APIs (Grok video, Tripo3D, Gemini TTS, Lyria) fill the gaps. The user's brief sets the spend: free or local holds, and otherwise the cost is confirmed with the user first. An asset manifest in the project's `README.md` tracks paths, sizes in the scene, and costs.

## Limitations

The skills don't cover mobile or native packaging.
