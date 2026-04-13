Use `$godogen` to generate or update this game from a natural-language description.

The working directory is the project root. NEVER `cd` — use relative paths for all commands.

This repository was published from the Godogen source repo. Runtime skills live in `.agents/skills/`.

Default operating rules:

- Treat screenshot-based verification as mandatory, not optional polish.
- Keep `PLAN.md`, `STRUCTURE.md`, `MEMORY.md`, and `ASSETS.md` current so the run can resume cleanly.
- Use the `godot-api` skill for targeted Godot API or C# Godot syntax questions. If you already know the class or symbol you need, search `_common.md` / `_other.md` and read only the specific doc inline. If you need to discover candidate classes or synthesize across multiple or large docs, use a dedicated helper agent.
- Never list `.agents/skills/godot-api/doc_api/` or `.agents/skills/godot-api/doc_source/`. They contain nearly a thousand files and waste context. Use the index files and targeted class docs only.
- Use the `visual-qa` skill for screenshot validation and visual debugging. Run Gemini checks inline. For `--native` or `--both`, use a dedicated helper agent so native review starts from a fresh context.

# Project Structure

Game projects follow this layout once `$godogen` runs:

```
AGENTS.md              # Published runtime instructions for this game repo
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
.agents/skills/        # Published Godogen skills used by Codex
```

## Limitations

- No audio support
- No animated GLBs — static models only
