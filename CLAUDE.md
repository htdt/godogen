We develop agents and skills here. They are then used in another folder for Godot game development with Claude Code.

## Layout

Source code lives at the repo root:
- `skills/` — skill definitions (`SKILL.md`) and their tool scripts
- `game.md` — CLAUDE.md template for game folders
- `publish.sh` — create ready-to-develop game folder

## Skills

- godogen — orchestrator + scaffold + decomposer + asset planning + asset generation + visual target (main thread)
- godot-task — task execution + GDScript docs + screenshot capture + visual QA (context: fork)

When writing skills: don't give obvious guidance. The agent is a highly capable LLM — handholding only pollutes the context.
