# Godogen: Claude Code skills that build complete Godot 4 projects

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

You describe what you want. An AI pipeline designs the architecture, generates the art, writes every line of code, captures screenshots from the running engine, and fixes what doesn't look right. The output is a real Godot 4 project with organized scenes, readable scripts, and proper game architecture. Handles 2D and 3D, runs on commodity hardware.

## How it works

- **Two Claude Code skills** orchestrate the entire pipeline — one plans, one executes. Each task runs in a fresh context to stay focused.
- **Godot 4 output** — real projects with proper scene trees, scripts, and asset organization.
- **Asset generation** — Gemini creates 2D art and textures; Tripo3D converts selected images to 3D models. Budget-aware: maximizes visual impact per cent spent.
- **GDScript expertise** — custom-built language reference and lazy-loaded API docs for all 850+ Godot classes compensate for LLMs' thin training data on GDScript.
- **Visual QA closes the loop** — captures actual screenshots from the running game and analyzes them with Gemini Flash vision. Catches z-fighting, missing textures, broken physics.
- **Runs on commodity hardware** — any PC with Godot and Claude Code works.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (headless or editor) on `PATH`
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- API keys as environment variables:
  - `GOOGLE_API_KEY` — Gemini, used for image generation and visual QA
  - `TRIPO3D_API_KEY` — [Tripo3D](https://platform.tripo3d.ai/), used for image-to-3D model conversion (only needed for 3D games)
- Python 3 with pip (asset tools install their own deps)
- Tested on Ubuntu and Debian. macOS is untested — screenshot capture depends on X11/xvfb/Vulkan and will need a native capture path to work.

### Create a game project

This repo is the skill development source. To start making a game, run `publish.sh` to set up a new project folder with all skills installed:

```bash
./publish.sh ~/my-game          # uses teleforge.md as CLAUDE.md
./publish.sh ~/my-game local.md # uses a custom CLAUDE.md instead
```

This creates the target directory with `.claude/skills/` and a `CLAUDE.md`, then initializes a git repo. Open Claude Code in that folder and tell it what game to make — the `/godogen` skill handles everything from there.

### Running on a VM

A single generation run can take several hours. Running on a cloud VM keeps your local machine free and gives the pipeline a GPU for Godot's screenshot capture. A basic GCE instance with a T4 or L4 GPU works well.

The default `CLAUDE.md` (`teleforge.md`) is set up for [Teleforge](https://github.com/htdt/teleforge) — a lightweight Telegram bridge that lets you monitor progress and send messages to the running session from your phone. If you don't use Teleforge, pass your own `CLAUDE.md` to `publish.sh` or edit the generated one after publishing.

## Is Claude Code the only option?

The skills were tested across different setups. Claude Code with Opus 4.6 delivers the best outcome. Sonnet 4.6 works but requires more guidance from the user. [OpenCode](https://opencode.ai/) was quite nice and porting the skills is straightforward — I'd recommend it if you're looking for an alternative.

## Roadmap

- Migrate image generation to `grok-imagine-image` (cheaper per image)
- Migrate spritesheets to `grok-imagine-video` (animated sprites from video)
- Add recipes for game builds (Android export)
- Explore C# as GDScript alternative
- Publish a full game end-to-end as a public demo
- Explore Bevy Engine as Godot alternative

Follow progress: [@alex_erm](https://x.com/alex_erm)
