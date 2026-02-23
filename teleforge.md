Use `/godogen` to generate or update this game from a natural language description.

# Session Instructions

Non-interactive background process spawned by Teleforge. No terminal, no stdin, no interactive UI. User is on Telegram — reach them **only** via MCP tools.

**Only the main agent (godogen orchestrator) sends and checks messages.** Sub-agents must not call MCP tools.
Exception: godot-task should `send_message` a one-sentence status when hitting a blocker that requires a different approach.

Call `check_messages` before starting each new task and before ending the session.

After generating the visual target, `send_image` `reference.png` to the user so they can see the art direction.

After scaffold + decomposer, `send_message` a concise summary (game name, task count, numbered list). No approval gate — proceed immediately. User corrections arrive via `check_messages`.

godot-task reports results (screenshots, status) back to godogen. godogen sends the user a summary + best screenshots via `send_image`. After all tasks, godogen sends a final video via `send_video`. Video must be compressed to <50MB (Telegram upload limit).

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