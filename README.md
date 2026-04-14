# Godogen: Claude Code and Codex skills that build complete Godot projects

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

You describe what you want. An AI pipeline designs the architecture, generates the art, writes every line of code, captures screenshots from the running engine, and fixes what does not look right. The output is a real Godot 4 project with organized scenes, readable scripts, and proper game architecture.

This repo is not a Godot game. It is the source for a generator that produces Godot games: **godogen → game repo → game**. You publish the skills into a fresh game repo (Claude Code or Codex flavored), then the agent runs inside that repo to build the actual game.

Two parallel source trees live here, one per host agent:

- `claude/` — the Claude Code version
- `codex/` — the Codex version

## What skills do

- **Godot 4 output** — real projects with proper scene trees, scripts, and asset organization.
- **Asset generation** — Gemini creates precise references and characters; xAI Grok handles textures and simple objects; Tripo3D converts images to 3D models. Animated sprites use Grok video generation with loop detection.
- **C# / .NET 9** — all generated code uses C#. See [why C# over GDScript](gdscript-vs-csharp.md).
- **Visual QA closes the loop** — captures actual screenshots from the running game and uses multimodal review to catch z-fighting, missing textures, broken physics, and other visual regressions.
- **Runs on commodity hardware** — any machine with Godot, Python, and the required API keys can run the pipeline.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (.NET build) on `PATH`
- Python 3 with pip
- API keys as environment variables:
  - `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/)
  - `XAI_API_KEY` — [xAI Grok](https://console.x.ai/home)
  - `TRIPO3D_API_KEY` — [Tripo3D](https://platform.tripo3d.ai/) for 3D generation
- System packages from [setup.md](setup.md): `vulkan-tools`, `xvfb`, `ffmpeg`, `imagemagick`, plus platform-specific extras
- Tested on Ubuntu, Debian, and macOS
- Claude Code or Codex

### Publish a game repo

Pick the variant that matches your host agent:

```bash
./claude/publish.sh ~/my-game   # writes CLAUDE.md and .claude/skills/
./codex/publish.sh  ~/my-game   # writes AGENTS.md and .agents/skills/
```

Pass `--force` to wipe existing contents at the target before publishing — use this when re-publishing over a previous run.

## Running on a server

A full generation run can take hours, so it's convenient to offload it to a server, ideally a GPU instance, since Godot renders screenshots and videos much faster with hardware acceleration.

- Keep the session alive across SSH drops with `tmux` or `screen`.
- Install [tg-push](https://github.com/htdt/tg-push) so the agent can push progress updates, screenshots, and the final video to Telegram while you're away.
- Enable remote control so you can check in and steer the run from any device — both Claude Code and Codex have official remote-control interfaces.

## Improving the skills

After a full generation session, ask the agent you used to review how the pipeline performed:

> Analyze this session. Were the instructions optimal? Flag anything that was too obvious, missing, or misleading. Did any tools pollute context with noise? Did the screenshot verification loop catch the real problems? Any tool failures or workarounds?

## Roadmap

- Publish a full game end-to-end as a public demo
- Explore Bevy Engine as Godot alternative

## Changelog

**2026-04-14 — Codex support**
- Added a parallel Codex source tree alongside the existing Claude Code one
- Each variant publishes to its own runtime layout (`.claude/skills/` vs `.agents/skills/`)

**2026-04-06 — C# migration**
- All skills and generated code migrated from GDScript to C# / .NET 9 ([comparison](gdscript-vs-csharp.md))
- `dotnet build` replaces per-file validation loops

**2026-04-03 — Single-context architecture**
- Orchestrator and task execution merged into one main pipeline
- Added Godot API lookup and visual QA support flows

**2026-03-25 — xAI Grok video**
- Added Grok video generation for animated sprite workflows
- Background removal rewritten with BiRefNet multi-signal matting

**2026-03-09 — Initial release**
- Initial Godogen release with image generation, 3D conversion, screenshot QA, and video capture

Follow progress: [@alex_erm](https://x.com/alex_erm)
