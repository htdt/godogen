Use `$godogen` to generate or update this game from a natural language description.

The working directory is the project root. NEVER `cd` — use relative paths for all commands.

If `tg-push` is on PATH with `TG_BOT_TOKEN` and `TG_CHAT_ID` set, share key visuals via `tg-push --text "caption" --file path/to/image_or_video`: the reference image, the screenshot confirming each task is done, and the final video.

# Project Structure

Game projects follow this layout once `$godogen` runs:

```
project.godot          # Godot config: viewport, input maps, autoloads, [dotnet]
{ProjectName}.csproj   # .NET project file
reference.png          # Visual target — art direction reference image
STRUCTURE.md           # Architecture reference: scenes, scripts, signals
PLAN.md                # Game plan — risk tasks, main build, verification criteria
ASSETS.md              # Asset manifest with art direction and paths
MEMORY.md              # Accumulated discoveries from task execution
scenes/
  Build*.cs            # Headless scene builders (produce .tscn)
  *.tscn               # Compiled scenes
scripts/*.cs           # Runtime C# scripts
test/
  TestTask.cs          # Per-task visual test harness (overwritten each task)
  Presentation.cs      # Final cinematic video script
assets/                # gitignored — img/*.png, glb/*.glb
screenshots/           # gitignored — per-task frames
.vqa.log               # Visual QA debug log (gitignored)
.agents/skills/        # Published Godogen skills
```

## Limitations

- No audio support
