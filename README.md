# Godogen: Claude Code skills that build complete Godot 4 projects

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

You describe what you want. An AI pipeline designs the architecture, generates the art, writes every line of code, captures screenshots from the running engine, and fixes what doesn't look right. The output is a real Godot 4 project with organized scenes, readable scripts, and proper game architecture. Handles 2D and 3D, runs on commodity hardware.

## How it works

- **Two Claude Code skills** orchestrate the entire pipeline — one plans, one executes. Each task runs in a fresh context to stay focused.
- **Godot 4 output** — real projects with proper scene trees, scripts, and asset organization.
- **Asset generation** — xAI Grok creates 2D art and textures; Tripo3D converts selected images to 3D models. Budget-aware: maximizes visual impact per cent spent.
- **GDScript expertise** — custom-built language reference and lazy-loaded API docs for all 850+ Godot classes compensate for LLMs' thin training data on GDScript.
- **Visual QA closes the loop** — captures actual screenshots from the running game and analyzes them with Gemini Flash vision. Catches z-fighting, missing textures, broken physics.
- **Runs on commodity hardware** — any PC with Godot and Claude Code works.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (headless or editor) on `PATH`
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- API keys as environment variables:
  - `XAI_API_KEY` — [xAI Grok](https://console.x.ai/home), used for image and video generation
  - `GOOGLE_API_KEY` — [Gemini](https://aistudio.google.com/app/api-keys), used for visual QA
  - `TRIPO3D_API_KEY` — [Tripo3D](https://platform.tripo3d.ai/), used for image-to-3D model conversion (only needed for 3D games)
- Python 3 with pip (asset tools install their own deps)
- System packages: `mesa-utils`, `ffmpeg` (see [setup.md](setup.md) for full details)
- **macOS additional:**
  - `brew install coreutils` (provides `gtimeout`) — or the capture script uses a perl-based fallback
  - `brew install ffmpeg` — needed for AVI-to-MP4 video conversion
  - Godot 4 must be on `PATH` (symlink from `Godot.app/Contents/MacOS/Godot` or install via Homebrew)
- Tested on Ubuntu, Debian, and macOS. Linux uses X11/xvfb/Vulkan; macOS uses Metal natively.

### Create a game project

This repo is the skill development source. To start making a game, run `publish.sh` to set up a new project folder with all skills installed:

```bash
./publish.sh ~/my-game          # uses game.md as CLAUDE.md
./publish.sh ~/my-game local.md # uses a custom CLAUDE.md instead
```

This creates the target directory with `.claude/skills/` and a `CLAUDE.md`, then initializes a git repo. Open Claude Code in that folder and tell it what game to make — the `/godogen` skill handles everything from there.

### Running on a VM

A single generation run can take several hours. Running on a cloud VM keeps your local machine free and gives the pipeline a GPU for Godot's screenshot capture. A basic GCE instance with a T4 or L4 GPU works well.

You don't need to keep a terminal open for the entire run. Connect a [channel](https://code.claude.com/docs/en/channels#quickstart) (Telegram, Slack, etc.) to send prompts and receive progress updates from your phone, or use [remote control](https://code.claude.com/docs/en/remote-control) to manage sessions from any browser.

## Is Claude Code the only option?

The skills were tested across different setups. Claude Code with Opus 4.6 delivers the best outcome. Sonnet 4.6 works but requires more guidance from the user. [OpenCode](https://opencode.ai/) was quite nice and porting the skills is straightforward — I'd recommend it if you're looking for an alternative.

## Roadmap

- Add recipes for game builds (Android export)
- Explore C# as GDScript alternative
- Publish a full game end-to-end as a public demo
- Explore Bevy Engine as Godot alternative

Follow progress: [@alex_erm](https://x.com/alex_erm)
