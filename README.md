# Godogen: Claude Code and Codex skills that build complete Godot 4 projects

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

You describe what you want. An AI pipeline designs the architecture, generates the art, writes every line of code, captures screenshots from the running engine, and fixes what does not look right. The output is a real Godot 4 project with organized scenes, readable scripts, and proper game architecture.

This repository now carries two implementations of that pipeline:

- `claude/` — the Claude Code version. It publishes game repos with `CLAUDE.md` and `.claude/skills/`.
- `codex/` — the Codex version. It publishes game repos with `AGENTS.md` and `.agents/skills/`.

This repo is the skill authoring source, not the runtime layout that either tool uses day to day inside a generated game project.
Shared repo-level agent instructions live at the root in `AGENTS.md`. `CLAUDE.md` is a symlink to the same file.

## What both versions do

- **Godot 4 output** — real projects with proper scene trees, scripts, and asset organization.
- **Asset generation** — Gemini creates precise references and characters; xAI Grok handles textures and simple objects; Tripo3D converts images to 3D models. Animated sprites use Grok video generation with loop detection.
- **C# / .NET 9** — all generated code uses C#. See [why C# over GDScript](gdscript-vs-csharp.md).
- **Visual QA closes the loop** — captures actual screenshots from the running game and uses multimodal review to catch z-fighting, missing textures, broken physics, and other visual regressions.
- **Runs on commodity hardware** — any machine with Godot, Python, and the required API keys can run the pipeline.

## Repo layout

- `AGENTS.md` — shared repo-level instructions for agent work in this combined source repo
- `CLAUDE.md` — symlink to `AGENTS.md`
- `claude/` — Claude Code source tree: `publish.sh`, `game.md`, and `skills/`
- `codex/` — Codex source tree: `publish.sh`, `game.md`, and `skills/`
- `demo_prompts.md` — example prompts used for demos
- `gdscript-vs-csharp.md` — rationale for C# / .NET 9

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
- Either Claude Code or Codex, depending on which variant you want to use

### Publish a game repo

Claude Code version:

```bash
./claude/publish.sh ~/my-game
./claude/publish.sh --force ~/my-game
```

This creates a target repo with `CLAUDE.md` and `.claude/skills/`.

Codex version:

```bash
./codex/publish.sh ~/my-game
./codex/publish.sh --force ~/my-game
```

This creates a target repo with `AGENTS.md` and `.agents/skills/`.

### Codex defaults

- Start with `gpt-5.4` for full generation runs.
- Use `gpt-5.4-mini` for lighter tasks or cheaper helper work.
- Invoke `$godogen` explicitly for new runs, or ask Codex to use the `godogen` skill.
- Use dedicated helper agents only when you want context isolation for `godot-api` or `visual-qa`.

Example:

```text
Use $godogen to build a 3D alpine snowboard game. Treat screenshot-based verification as mandatory. If I explicitly ask for helper agents, use them only for Godot API lookup or visual QA context isolation.
```

## Running on a VM

A full generation run can take hours. Running on a cloud VM keeps your local machine free and gives Godot a GPU for screenshot capture.

- Claude Code users can lean on channels or remote control for long-running sessions.
- Codex users will usually keep long runs alive in `tmux` or `screen`; GPU-backed screenshot capture matters more than remote chat integrations.

## Improving the skills

After a full generation session, ask the agent you used to review how the pipeline performed:

> Analyze this session. Were the instructions optimal? Flag anything that was too obvious, missing, or misleading. Did any tools pollute context with noise? Did the screenshot verification loop catch the real problems? Any tool failures or workarounds?

Then make the fix in the matching source tree:

- Claude Code changes live under `claude/`
- Codex changes live under `codex/`

## Which version to use

- Use `claude/` if you want the Claude Code workflow and published `CLAUDE.md` runtime layout.
- Use `codex/` if you want the Codex CLI / IDE workflow and published `AGENTS.md` runtime layout.

## Roadmap

- Publish a full game end-to-end as a public demo
- Explore Bevy Engine as Godot alternative

## Changelog

**2026-04-13 — Repo split**
- Source tree split into `claude/` and `codex/`
- Root docs now describe the shared project and link to variant-specific workflows

**2026-04-11 — Codex migration**
- Codex source tree moved to the repo-wide `AGENTS.md` policy plus `codex/game.md` publish template
- Codex workflow defaults now assume local CLI use, explicit `$godogen` invocation, and helper agents only for context isolation

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
