# Godogen: Claude Code skills that build complete Godot 4 projects

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

You describe what you want. An AI pipeline designs the architecture, generates the art, writes every line of code, captures screenshots from the running engine, and fixes what doesn't look right. The output is a real Godot 4 project with organized scenes, readable scripts, and proper game architecture. Handles 2D and 3D, runs on commodity hardware.

## How it works

- **Three Claude Code skills** — one orchestrator runs the full pipeline in a single 1M-token context window (planning, building, debugging), while two forked support skills handle Godot API lookup and visual QA without polluting the main context.
- **Godot 4 output** — real projects with proper scene trees, scripts, and asset organization.
- **Asset generation** — Gemini creates precise references and characters; xAI Grok handles textures and simple objects; Tripo3D converts images to 3D models. Animated sprites use Grok video generation with loop detection. Budget-aware: maximizes visual impact per cent spent.
- **GDScript expertise** — custom-built language reference and lazy-loaded API docs for all 850+ Godot classes compensate for LLMs' thin training data on GDScript.
- **Visual QA closes the loop** — captures actual screenshots from the running game and analyzes them with Gemini Flash and Claude vision. Includes question mode for free-form visual debugging. Catches z-fighting, missing textures, broken physics.
- **Runs on commodity hardware** — any PC with Godot and Claude Code works.

## Getting started

### Prerequisites

- [Godot 4](https://godotengine.org/download/) (headless or editor) on `PATH`
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- API keys as environment variables:
  - `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/), used for Gemini image generation (references, characters, precise work)
  - `XAI_API_KEY` — [xAI Grok](https://console.x.ai/home), used for image/video generation (textures, simple objects)
  - `TRIPO3D_API_KEY` — [Tripo3D](https://platform.tripo3d.ai/), used for image-to-3D model conversion (only needed for 3D games)
- Python 3.10+ with pip
- System packages: `ffmpeg` and `ImageMagick` (via `winget` on Windows). Fully supported for native execution via PowerShell or Command Prompt. The project uses cross-platform Python scripts rather than platform-specific Bash scripts, so WSL2, Git Bash, or MSYS2 are not required. See [setup.md](setup.md) for full details including Linux and macOS.
- Tested on Windows 11, macOS, Ubuntu, and Debian.

### Windows Setup

1. Install system packages via winget:
   ```powershell
   winget install ffmpeg
   winget install ImageMagick.ImageMagick
   winget install GodotEngine.Godot
   ```
2. Install Python dependencies (requires Python 3.10+):
   ```powershell
   pip install -r skills/godogen/tools/requirements.txt
   ```
3. Set your API keys as environment variables (`GOOGLE_API_KEY`, `XAI_API_KEY`, `TRIPO3D_API_KEY`).
4. You are ready to go. No WSL2, Git Bash, or MSYS2 required.

### Create a game project

This repo is the skill development source. To start making a game, run `publish.py` to set up a new project folder with all skills installed:

```bash
python publish.py ~/my-game
python publish.py --force ~/my-game  # clean existing target before publishing
```

This creates the target directory with `.claude/skills/` and a `CLAUDE.md`, then initializes a git repo. Open Claude Code in that folder and tell it what game to make — the `/godogen` skill handles everything from there.

### Running on a VM

A single generation run can take several hours. Running on a cloud VM keeps your local machine free and gives the pipeline a GPU for Godot's screenshot capture. A basic GCE instance with a T4 or L4 GPU works well.

You don't need to keep a terminal open for the entire run. Connect a [channel](https://code.claude.com/docs/en/channels#quickstart) (Telegram, Slack, etc.) to send prompts and receive progress updates from your phone, or use [remote control](https://code.claude.com/docs/en/remote-control) to manage sessions from any browser.

## Is Claude Code the only option?

The skills were tested across different setups. Claude Code with Opus 4.6 delivers the best outcome. Sonnet 4.6 works but requires more guidance from the user. [OpenCode](https://opencode.ai/) was quite nice and porting the skills is straightforward — I'd recommend it if you're looking for an alternative.

## Roadmap

- Explore C# as GDScript alternative
- Publish a full game end-to-end as a public demo
- Explore Bevy Engine as Godot alternative

## Changelog

**2026-04-03 — Single-context architecture** (current)
- Merged task executor into godogen — full pipeline runs in one 1M-token context window
- Added godot-api skill (forked, Sonnet) for Godot class API lookup
- Added visual-qa skill (forked) with Gemini Flash, Claude vision, and question mode
- Risk-first decomposition replaces task DAG
- Android debug APK export

**2026-03-25 — xAI Grok video**
- Added xAI Grok video generation for animated sprites (ref → pose → video → frames → loop trim)
- Background removal rewritten with BiRefNet multi-signal matting
- macOS support, native channel status updates

**2026-03-09 — Initial release**
- Two-skill architecture: godogen orchestrator + godot-task executor (forked)
- Gemini image generation, Tripo3D for 3D models
- Visual QA via Gemini Flash
- Screenshot and video capture, presentation video
- GDScript reference system with lazy two-tier API lookup

Follow progress: [@alex_erm](https://x.com/alex_erm)
