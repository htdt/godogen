# Godogen

Autonomous game development for Godot (C# or GDScript), Bevy, Babylon.js, and three.js with Claude Code and Codex.

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](docs/demo_prompts.md)

Describe a game. The agent builds it, generates assets, runs the engine, and proves the result — as a live game you watch and steer, or as a recorded video when you're not there. It reads the situation and decides which, in the run.

This repo is not a game. It is the source for a generator that produces games: **godogen -> game repo -> game**. You publish into a fresh game repo — choosing engine and host-agent flavor — then the agent runs inside that repo and builds the actual game from a short engine guide.

## Source layout

A published repo is intentionally thin: a runtime manifest, a one-page engine guide, and the asset-generation skill. The agent recreates everything else (project scaffold, capture tooling) from the guide.

- `prompts/runtime.md` — the runtime manifest
- `asset-gen/` — the cross-engine asset-generation skill
- `engines/godot.md`, `engines/godot-gdscript.md`, `engines/bevy.md`, `engines/babylon.md`, `engines/threejs.md` — per-engine guides
- [publish.sh](publish.sh) — renders the runtime layout for the chosen engine and host agent

Engine and host agent (Claude vs Codex) are publish-time render choices, not separate source trees.

## What the agent does

- **Godot 4** — C# or statically typed GDScript projects with build-time scene generation, runtime scripts, and Jolt physics.
- **Bevy** — Rust/Bevy projects with code-first ECS scenes and offscreen capture.
- **Babylon.js** and **three.js** — TypeScript/Vite browser games served at a live URL.
- **Asset generation** — local and free by default with [godogen_assets](https://github.com/htdt/godogen_assets): images with real transparency, textured 3D models, rigged humanoids with generated moves and lip-sync, sound effects and voice lines. Paid APIs fill what it can't make: Gemini or xAI Grok images, animated sprites from Grok video, Tripo3D, Gemini TTS voice acting, Lyria music.
- **Proof over claims** — the agent judges results from the running game (a live URL or a recorded clip), not from a clean compile, so visible defects drive the next iteration.
- **You choose your involvement** — watch the live game (a Babylon.js or three.js URL, or a Godot/Bevy project you run) and steer at decision points, or leave the run unattended and get a 15–20s proof recording at the end. The agent takes its cue from how you frame the task.

## Choosing an engine

Every engine gets the same loop — build, generate assets, run, prove — so pick by what you want to hold at the end and how you want to watch along the way.

| `--engine` | Language | You watch | Pick it for |
|---|---|---|---|
| `godot` | C# | the project, run or opened in the Godot editor | desktop 2D or 3D games; the fewest runtime surprises in long unattended runs |
| `godot-gdscript` | GDScript | the same | a Godot project you'll keep developing yourself in the editor |
| `bevy` | Rust | `cargo run` | a Rust codebase: ECS, no editor, many entities |
| `babylon` | TypeScript | a live URL | a browser game that leans on engine systems: physics, GUI, particles, animation |
| `threejs` | TypeScript | a live URL | a browser game that leans on its look: custom shaders, stylized rendering, a light page |

**How you'll watch.** On a remote box or steering from your phone, a browser engine wins: the dev server gives you a URL you refresh while the agent edits. Godot and Bevy run as desktop apps — from a headless server you see them in the proof video, or by pulling the repo and running it locally. On your own desktop the engines are even here.

**2D.** Godot has a dedicated 2D engine (pixel-space nodes, tilemaps, 2D physics) and is the natural pick for 2D. Bevy handles 2D well; the web engines are 3D-first and draw 2D as sprites and planes in a 3D scene.

**Godot: C# or GDScript.** Same engine, scenes, and capture; only the language differs.
- C# compiles: `dotnet build` type-checks the whole project before anything runs, so mistakes surface early ([comparison](docs/gdscript-vs-csharp.md)). It needs the .NET build of Godot and the .NET SDK.
- GDScript is Godot's native language and what most tutorials, addons, and Asset Library entries use. It runs on any Godot build with no .NET toolchain. The agent types everything, but whatever the parser can't check still fails at runtime, where it's found only by running.
- Planning a web export later? GDScript exports everywhere Godot does; check Godot's current platform support for C# before picking it.

**Browser: Babylon.js or three.js.**
- Babylon.js is a full engine — Havok physics, GUI, particles, animation groups, and an inspector come in the box, so the agent assembles less and there are fewer seams between parts. The bundle is heavier.
- three.js is a renderer. The agent chooses and wires physics (Rapier), UI (HTML over the canvas), and audio itself; in return you get the most widely used 3D library on the web — the deepest pool of examples — with the most control over the look (custom shaders, postprocessing, WebGPU and TSL node materials) and a small bundle.

**Bevy** when you want the game in Rust: code-only, ECS, strong compile-time guarantees, and headroom for many entities. It has the slowest compiles of the five, and its API moves between releases faster than model training data catches up — the guide has the agent read the installed source instead of trusting memory.

**No strong preference?** `babylon` to watch and steer from anywhere; `godot` for a desktop game you'll receive as a video or run yourself.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) on `PATH` for Godot projects — the .NET build for C#; either build for GDScript
- Rust/Cargo for Bevy projects
- Node.js 22.12+ and npm for Babylon.js and three.js projects
- Chrome or Chromium with hardware WebGL2 for browser capture (Babylon.js, three.js)
- Python 3 with pip
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
```

Pass `--force` to wipe existing contents at the target before re-publishing.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

Follow progress: [@alex_erm](https://x.com/alex_erm)
