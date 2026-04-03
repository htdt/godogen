Use `/godogen` to generate or update this game from a natural language description.

The working directory is the project root. NEVER `cd` — use relative paths for all commands.

When a channel is connected (Telegram, Slack, etc.), share progress via `reply`. Attach screenshots and videos using `files` — task completions, QA verdicts, reference image, final video are all worth sharing.

# Project Structure

Game projects follow this layout once `/godogen` runs:

```
project.godot          # Godot config: viewport, input maps, autoloads
reference.png          # Visual target — art direction reference image
STRUCTURE.md           # Architecture reference: scenes, scripts, signals
PLAN.md                # Game plan — risk tasks, main build, verification criteria
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
.vqa.log               # Visual QA debug log (gitignored)
```

## Limitations

- No audio support
- No animated GLBs — static models only
