The goal is to develop Claude Code agents and skills for Godot game development.
We take a natural language game description and turn it into a real game.
We iterate via building games and updating agents/skills.

## Layout

Source code lives at the repo root:
- `agents/` — agent system prompts (`.md` files)
- `skills/` — skill definitions (`SKILL.md`) and their tool scripts
- `tools/` — dev scripts (publish, token counting, etc.)

**Publishing:** `./tools/publish.sh <target_dir>` copies agents + skills into `<target_dir>/.claude/` as a ready-to-use runtime.

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

When writing agents/skills: don't give obvious guidance. Assume the agent is a strong LLM — handholding only pollutes the context.
