# Godogen

Autonomous game development for Godot (C# or GDScript), Bevy, Babylon.js, three.js, and plain HTML with Claude Code and Codex.

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](docs/demo_prompts.md)

Describe a game. The agent builds it, generates assets, and runs the engine — headless capture included, so it can see the game and record it.

This repo is not a game. It is the source for a generator that produces games: **godogen -> game repo -> game**. You publish into a fresh game repo — choosing engine and host-agent flavor — then the agent runs inside that repo and builds the actual game from a short engine guide.

## Source layout

A published repo is intentionally thin: a runtime manifest, a one-page engine guide, and the asset-generation skill. The agent recreates everything else (project scaffold, capture tooling) from the guide.

- `prompts/runtime.md` — the runtime manifest
- `asset-gen/` — the cross-engine asset-generation skill
- `engines/godot.md`, `engines/godot-gdscript.md`, `engines/bevy.md`, `engines/babylon.md`, `engines/threejs.md`, `engines/html.md` — per-engine guides
- [publish.sh](publish.sh) — renders the runtime layout for the chosen engine and host agent

Engine and host agent (Claude vs Codex) are publish-time render choices, not separate source trees.

## What the agent does

- **Godot 4** — C# or statically typed GDScript projects with build-time scene generation, runtime scripts, and Jolt physics.
- **Bevy** — Rust/Bevy projects with code-first ECS scenes and offscreen capture.
- **Babylon.js** and **three.js** — TypeScript/Vite browser games served at a live URL.
- **HTML** — text-first 2D games in the DOM: type and CSS for the look, TypeScript/Vite, served at a live URL.
- **Asset generation** — local and free by default with [godogen_assets](https://github.com/htdt/godogen_assets): images with real transparency, textured 3D models, rigged humanoids with generated moves and lip-sync, sound effects and voice lines. Paid APIs fill what it can't make: Gemini or xAI Grok images, animated sprites from Grok video, Tripo3D, Gemini TTS voice acting, Lyria music.
- **Building blocks, not process** — the guides carry the stack, project sketch, capture recipe and silent-failure traps. How to check the game and what to hand back are the model's call.

## Choosing an engine

Every engine gets the same loop — build, generate assets, run — so pick by what you want to hold at the end and how you want to watch along the way.

| `--engine` | Language | You watch | Pick it for |
|---|---|---|---|
| `godot` | C# | the project, run or opened in the Godot editor | desktop 2D or 3D games; the fewest runtime surprises in long unattended runs |
| `godot-gdscript` | GDScript | the same | a Godot project you'll keep developing yourself in the editor |
| `bevy` | Rust | `cargo run` | a Rust codebase: ECS, no editor, many entities |
| `babylon` | TypeScript | a live URL | a browser game that leans on engine systems: physics, GUI, particles, animation |
| `threejs` | TypeScript | a live URL | a browser game that leans on its look: custom shaders, stylized rendering, a light page |
| `html` | TypeScript | a live URL | a 2D game that is mostly text and UI: interactive fiction, cards, grid roguelikes, puzzles, management |

**How you'll watch.** On a remote box or steering from your phone, a browser engine wins: the dev server gives you a URL you refresh while the agent edits. Godot and Bevy run as desktop apps — from a headless server you see them in a recorded video, or by pulling the repo and running it locally. On your own desktop the engines are even here.

**2D.** Godot has a dedicated 2D engine (pixel-space nodes, tilemaps, 2D physics) and is the natural pick for 2D. Bevy handles 2D well; Babylon.js and three.js are 3D-first and draw 2D as sprites and planes in a 3D scene. For 2D that is mostly text, panels and buttons, `html` skips the scene entirely: the DOM is the renderer, type and CSS are the art, it needs no GPU, and it plays on a phone.

**Godot: C# or GDScript.** Same engine, scenes, and capture; only the language differs.
- C# compiles: `dotnet build` type-checks the whole project before anything runs, so mistakes surface early ([comparison](docs/gdscript-vs-csharp.md)). It needs the .NET build of Godot and the .NET SDK.
- GDScript is Godot's native language and what most tutorials, addons, and Asset Library entries use. It runs on any Godot build with no .NET toolchain. The agent types everything, but whatever the parser can't check still fails at runtime, where it's found only by running.
- Planning a web export later? GDScript exports everywhere Godot does; check Godot's current platform support for C# before picking it.

**Browser: Babylon.js or three.js.**
- Babylon.js is a full engine — Havok physics, GUI, particles, animation groups, and an inspector come in the box, so the agent assembles less and there are fewer seams between parts. The bundle is heavier.
- three.js is a renderer. The agent chooses and wires physics (Rapier), UI (HTML over the canvas), and audio itself; in return you get the most widely used 3D library on the web — the deepest pool of examples — with the most control over the look (custom shaders, postprocessing, WebGPU and TSL node materials) and a small bundle.

**Bevy** when you want the game in Rust: code-only, ECS, strong compile-time guarantees, and headroom for many entities. It has the slowest compiles of the six, and its API moves between releases faster than model training data catches up — the guide has the agent read the installed source instead of trusting memory.

**No strong preference?** `babylon` to watch and steer from anywhere; `godot` for a desktop game you'll receive as a video or run yourself.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) on `PATH` for Godot projects — the .NET build for C#; either build for GDScript
- Rust/Cargo for Bevy projects
- Node.js 22.12+ and npm for Babylon.js, three.js and HTML projects
- Chrome or Chromium for headless browser runs — with hardware WebGL2 for Babylon.js and three.js capture; HTML needs no GPU
- Python 3 with pip
- [Blender](https://www.blender.org/download/) on `PATH` (recommended) — the agent scripts it for 3D models and animation the generators don't make well
- [godogen_assets](https://github.com/htdt/godogen_assets) for local asset generation (NVIDIA GPU), set up per its README and recorded in `.godogen_assets` ([setup.md](setup.md))
- Optional API keys as environment variables, for assets the local tools can't make (or all of them, without godogen_assets):
  - `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/) for Gemini images, Gemini TTS and Lyria music
  - `XAI_API_KEY` — [xAI Grok](https://console.x.ai/home) for images and animated-sprite video
  - `TRIPO_API_KEY` — [Tripo](https://developers.tripo3d.ai/) for 3D generation (used by the `tripo` CLI: `npm install -g tripo-cli`, Node.js 20+)
- System packages from [setup.md](setup.md): `vulkan-tools`, `xvfb`, `ffmpeg`, `imagemagick`, plus platform-specific extras
- Tested on Ubuntu, Debian, and macOS
- Claude Code or Codex

### Publish a game repo

Pick the engine and host agent:

```bash
./publish.sh --engine godot          --agent claude --out ~/my-game   # CLAUDE.md + .claude/skills/
./publish.sh --engine godot-gdscript --agent claude --out ~/my-game
./publish.sh --engine bevy           --agent claude --out ~/my-game
./publish.sh --engine babylon        --agent codex  --out ~/my-game   # AGENTS.md + .agents/skills/
./publish.sh --engine threejs        --agent codex  --out ~/my-game
./publish.sh --engine html           --agent claude --out ~/my-game
```

Pass `--force` to wipe existing contents at the target before re-publishing.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

Follow progress: [@alex_erm](https://x.com/alex_erm)
