# Godogen: Autonomous game development for Godot and Bevy with Claude Code and Codex

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](docs/demo_prompts.md)

Describe a game. Godogen plans it, writes the code, generates assets, runs the engine, checks screenshots, and fixes what looks wrong.

This repo is not a game. It is the source for a generator that produces games: **godogen -> game repo -> game**. You publish the skills into a fresh game repo, choosing the engine and host-agent flavor, then the agent runs inside that repo to build the actual game.

## Source layout

The source is organized along the engine axis:

- `shared/` — engine-agnostic `godogen` stages, asset-generation tooling, shared stop hook, and common game-repo instructions
- `godot/` — Godot-specific `godogen` stages, Godot capture helpers, and the `godot-api` skill
- `bevy/` — Bevy-specific `godogen` stages, Bevy capture helpers, and the `bevy-help` skill

Claude Code vs Codex is a publish-time render choice, not a separate source tree. The root [publish.sh](publish.sh) renders the right runtime layout:

```bash
./publish.sh --engine godot --agent claude --out ~/my-godot-game  # CLAUDE.md + .claude/skills/
./publish.sh --engine godot --agent codex  --out ~/my-godot-game  # AGENTS.md + .agents/skills/
./publish.sh --engine bevy  --agent claude --out ~/my-bevy-game
./publish.sh --engine bevy  --agent codex  --out ~/my-bevy-game
```

Pass `--force` to wipe existing contents at the target before publishing — use this when re-publishing over a previous run.

## What skills do

- **Godot 4 output** — real C#/.NET projects with proper scene trees, scene builders, scripts, and asset organization.
- **Godot Android export** — debug APK export remains available when the user requests an Android app.
- **Bevy output** — Rust/Bevy projects with code-first scenes, local Bevy docs lookup, deterministic capture guidance, and final proof bundles.
- **Asset generation** — Gemini creates precise references and characters; xAI Grok handles textures and simple objects; Tripo3D converts images to 3D models. Animated sprites use Grok video generation with loop detection.
- **C# / .NET 9 for Godot** — Godot output uses C#. See [why C# over GDScript](docs/gdscript-vs-csharp.md).
- **Frame-grounded self-repair** — the agent is carefully prompted to judge progress from captured screenshots, not from code that compiles, so visible defects (clipping, wrong scale, frozen motion, missing assets) drive the next iteration instead of being rationalized away.
- **Telegram proof push** — published repos install a stop hook that pushes the latest `screenshots/result/{N}/video.mp4` to Telegram when `tg-push` and the TG_* env vars are configured. No-op otherwise.
- **Runs on commodity hardware** — any machine with the relevant engine toolchain, Python, and the required API keys can run the pipeline.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (.NET build) on `PATH` for Godot projects
- Rust/Cargo plus local Bevy docs for Bevy projects
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
./publish.sh --engine godot --agent claude --out ~/my-game
./publish.sh --engine godot --agent codex  --out ~/my-game
./publish.sh --engine bevy  --agent claude --out ~/my-game
./publish.sh --engine bevy  --agent codex  --out ~/my-game
```

### Bevy docs setup

If you're working on Bevy generation, configure and populate a shared Bevy docs folder once after clone:

```bash
./setup_bevy_docs.sh /absolute/or/user/path/to/bevy-docs
```

The setup script links `bevy/skills/bevy-help/docs/` to that folder, clones the Bevy docs sources, and builds local rustdoc for the current stable release. No default path is assumed. See [setup.md](setup.md) for the full workstation setup.

## Running on a server

A full generation run can take hours, so it's convenient to offload it to a server, ideally a GPU instance, since engine rendering and video capture are much faster with hardware acceleration.

- Keep the session alive across SSH drops with `tmux` or `screen`.
- Install [tg-push](https://github.com/htdt/tg-push): the stop hook auto-sends the final proof video to Telegram on completion.
- Enable remote control so you can check in and steer the run from any device — both Claude Code and Codex have official remote-control interfaces.

## Improving the skills

After a full generation session, ask the agent you used to review how the pipeline performed:

> Analyze this session. Were the instructions optimal? Flag anything that was too obvious, missing, or misleading. Did any tools pollute context with noise? Did the capture loop catch the real problems? Any tool failures or workarounds?

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

Follow progress: [@alex_erm](https://x.com/alex_erm)
