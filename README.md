# Godogen

Autonomous game development for Godot, Bevy, and Babylon.js with Claude Code and Codex.

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](docs/demo_prompts.md)

Describe a game. The agent builds it, generates assets, runs the engine, and proves the result — as a live game you watch and steer, or as a recorded video when you're not there. It reads the situation and decides which, in the run.

This repo is not a game. It is the source for a generator that produces games: **godogen -> game repo -> game**. You publish into a fresh game repo — choosing engine and host-agent flavor — then the agent runs inside that repo and builds the actual game from a short engine guide.

## Source layout

A published repo is intentionally thin: a runtime manifest, a one-page engine guide, and the asset-generation skill. The agent recreates everything else (project scaffold, capture tooling) from the guide.

- `prompts/runtime.md` — the runtime manifest
- `asset-gen/` — the cross-engine asset-generation skill
- `engines/babylon.md`, `engines/godot.md`, `engines/bevy.md` — per-engine guides
- [publish.sh](publish.sh) — renders the runtime layout for the chosen engine and host agent

Engine and host agent (Claude vs Codex) are publish-time render choices, not separate source trees.

## What the agent does

- **Godot 4** — C#/.NET projects with build-time scene generation, runtime scripts, and Jolt physics.
- **Bevy** — Rust/Bevy projects with code-first ECS scenes and offscreen capture.
- **Babylon.js** — TypeScript/Vite browser games served at a live URL.
- **Asset generation** — Gemini for precise references and characters, xAI Grok for textures and simple objects, Tripo3D for image-to-3D and rigged biped animation; animated sprites via Grok video with loop detection and background removal.
- **Proof over claims** — the agent judges results from the running game (a live URL or a recorded clip), not from a clean compile, so visible defects drive the next iteration.
- **You choose your involvement** — watch the live game (a Babylon.js URL, or a Godot/Bevy project you run) and steer at decision points, or leave the run unattended and get a 15–20s proof recording at the end. The agent adapts to your presence.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (.NET build) on `PATH` for Godot projects
- Rust/Cargo for Bevy projects
- Node.js 22.12+ and npm for Babylon.js projects
- Chrome or Chromium with hardware WebGL2 for Babylon.js browser capture
- Python 3 with pip
- API keys as environment variables:
  - `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/) for Gemini image generation
  - `XAI_API_KEY` — [xAI Grok](https://console.x.ai/home) for image/video generation
  - `TRIPO3D_API_KEY` — [Tripo3D](https://platform.tripo3d.ai/) for 3D generation
- System packages from [setup.md](setup.md): `vulkan-tools`, `xvfb`, `ffmpeg`, `imagemagick`, plus platform-specific extras
- Tested on Ubuntu, Debian, and macOS
- Claude Code or Codex

### Publish a game repo

Pick the engine and host agent:

```bash
./publish.sh --engine godot   --agent claude --out ~/my-game       # CLAUDE.md + .claude/skills/
./publish.sh --engine babylon --agent codex  --out ~/my-game       # AGENTS.md + .agents/skills/
./publish.sh --engine bevy    --agent claude --out ~/my-game
```

Pass `--force` to wipe existing contents at the target before re-publishing.

## Running on a server

A full generation run can take hours, so it's convenient to offload it to a server — ideally a GPU instance, since engine rendering and video capture are much faster with hardware acceleration.

- Keep the session alive across SSH drops with `tmux` or `screen`.
- Enable remote control so you can check in and steer the run from any device — both Claude Code and Codex have official remote-control interfaces.

## Improving the guides

After a generation session, ask the agent you used to review how it went:

> Analyze this session. Were the instructions optimal? Flag anything that was too obvious, missing, or misleading. Did any tool pollute context with noise? Did the proof video / live URL catch the real problems? Any tool failures or workarounds?

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

Follow progress: [@alex_erm](https://x.com/alex_erm)
