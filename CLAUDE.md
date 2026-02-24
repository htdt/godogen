We develop agents and skills here. They are then used in another folder for Godot game development with Claude Code.

## Layout

Source code lives at the repo root:
- `agents/` — agent system prompts (`.md` files)
- `skills/` — skill definitions (`SKILL.md`) and their tool scripts
- `teleforge.md` — CLAUDE.md in game folder (with Telegram connection)
- `publish.sh` — create ready-to-develop game folder

## Agents (autonomous, run via Task tool)

- asset-planner — analyzes game, allocates budget, generates assets (images + GLBs)
- game-decomposer — decomposes a game into isolated, testable tasks (PLAN.md)
- godot-scaffold — designs architecture and creates compilable project skeleton
- godot-task — executes a single task: generates scenes/scripts, verifies via screenshots

## Skills (loaded into context)

- asset-gen — CLI tools and instructions for generating images (Gemini) and GLBs (Tripo3D)
- godogen — orchestrator that coordinates scaffold, decomposer, and task agents (invoked via `/godogen`)
- gdscript-doc — GDScript syntax reference + Godot API docs bootstrap and lookup
- visual-qa — analyzes 7 sequential screenshots for visual defects and motion anomalies
- godot-capture — screenshot and video capture with GPU detection
- visual-target — generates a visual reference

When writing agents/skills: don't give obvious guidance. The agent is a highly capable LLM — handholding only pollutes the context.
