We develop agents and skills here. They are then used in another folder for Godot game development (C# / .NET 9+) with Claude Code.

## Layout

Source code lives at the repo root:
- `skills/` — skill definitions (`SKILL.md`) and their tool scripts
- `game.md` — CLAUDE.md template for game folders
- `publish.sh` — create ready-to-develop game folder

## Skills

- godogen — orchestrator + inline task execution + all pipeline stages (main thread, 1M context)
- godot-api — Godot class API lookup (context: fork, sonnet, Explore agent)
- visual-qa — visual quality assurance via Claude vision (context: fork)

When writing skills: don't give obvious guidance. The agent is a highly capable LLM — handholding only pollutes the context.
