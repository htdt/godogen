Use `/godogen` to generate or update this game from a natural language description.

Visual quality is the top priority. If a task fails visual QA, it gets rebuilt. Asset generators can produce the needed quality — the failures come from bad asset prompts and bad post-processing. Example failures:
- Generating a detailed image then shrinking it to a tile — details become tiny and clunky. Generate with shapes appropriate for the target size.
- Tiling textures where a single high-quality drawn background is needed
- Using sprite sheets for fire, smoke, or water instead of procedural particles or shaders 

# Session Instructions

Non-interactive background process spawned by Teleforge. No terminal, no stdin, no interactive UI. User is on Telegram — reach them **only** via MCP tools.

**Only the main agent (godogen orchestrator) sends and checks messages.** Sub-agents must not call MCP tools.
Exception: godot-task should `send_message` a one-sentence status when hitting a blocker that requires a different approach to prevent long runs without feedback.

Call `check_messages` before starting each new task and before ending the session.

After scaffold + decomposer, `send_image` `reference.png` with a summary of the PLAN.md. User corrections arrive via `check_messages`.

godot-task reports results (screenshots, status) back to godogen. godogen sends the user a summary + best screenshots via `send_image`. After visual-qa and triage, `send_message` a brief summary of the QA verdict and any rebuilds triggered. After all tasks, godogen sends a final video via `send_video`. Video must be compressed to <50MB (Telegram upload limit).

# Project Structure

Game projects follow this layout once `/godogen` runs:

```
project.godot          # Godot config: viewport, input maps, autoloads
reference.png          # Visual target — art direction reference image
STRUCTURE.md           # Architecture reference: scenes, scripts, signals
PLAN.md                # Task DAG — Goal/Requirements/Verify/Status per task
ASSETS.md              # Asset manifest with style string and paths
MEMORY.md              # Accumulated discoveries from task execution
scenes/
  build_*.gd           # Headless scene builders (produce .tscn)
  *.tscn               # Compiled scenes
scripts/*.gd           # Runtime scripts
test/
  test_task.gd         # Per-task visual test harness (overwritten each task)
  presentation.gd      # Final cinematic video script
assets/                # gitignored — img/*.png, glb/*.glb
screenshots/           # gitignored — per-task frames + verification.md
visual-qa/*.md         # Gemini vision QA reports
```

The working directory is the project root. NEVER `cd` — use relative paths for all commands.

## Limitations

- No audio support
- No animated GLBs — static models only
