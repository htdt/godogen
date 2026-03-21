Use `/godogen` to generate or update this game from a natural language description.

Visual quality is the top priority. Example failures:
- Generating a detailed image then shrinking it to a tile — details become tiny and clunky. Generate with shapes appropriate for the target size.
- Tiling textures where a single high-quality drawn background is needed
- Using sprite sheets for fire, smoke, or water instead of procedural particles or shaders 

# Session Instructions

Non-interactive background process spawned by Teleforge. No terminal, no stdin, no interactive UI. User is on Telegram — reach them **only** via MCP tools.

## godogen orchestrator

1. `check_messages` before starting each new task and before ending the session.
2. After creating PLAN.md: `send_image` `reference.png` with the plan summary.
3. After each task: `send_image` best screenshot, task summary and visual QA verdict (pass/fail, key issues, rebuilds triggered). Never skip the verdict even on pass.
4. After all tasks: `send_video` final video (<50MB).

## godot-task

Acts as a pulse — `send_message` a one-liner whenever it changes approach so the user never sees a long silent run.

# Project Structure

Game projects follow this layout once `/godogen` runs:

```
project.godot          # Godot config: viewport, input maps, autoloads
reference.png          # Visual target — art direction reference image
STRUCTURE.md           # Architecture reference: scenes, scripts, signals
PLAN.md                # Task DAG — Goal/Requirements/Verify/Status per task
ASSETS.md              # Asset manifest with art direction and paths
MEMORY.md              # Accumulated discoveries from task execution
scenes/
  build_*.gd           # Headless scene builders (produce .tscn)
  *.tscn               # Compiled scenes
scripts/*.gd           # Runtime scripts
test/
  test_task.gd         # Per-task visual test harness (overwritten each task)
  presentation.gd      # Final cinematic video script
assets/                # gitignored — img/*.png, glb/*.glb
screenshots/           # gitignored — per-task frames
visual-qa/*.md         # Gemini vision QA reports
```

The working directory is the project root. NEVER `cd` — use relative paths for all commands.

## Limitations

- No animated GLBs — static models only
