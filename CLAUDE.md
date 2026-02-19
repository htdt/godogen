The goal is to develop Claude Code agents and skills for Godot game development.
We take a natural language game description and turn it into a real game.
We iterate via building games and updating agents/skills.

Codex targets the same pipeline via `.agents/skills/` — don't change it unless asked.

**Agents** (autonomous, run via Task tool):
- asset-planner — analyzes game, allocates budget, generates assets (images + GLBs)
- game-decomposer — decomposes a game into isolated, testable tasks (PLAN.md)
- godot-scaffold — designs architecture and creates compilable project skeleton
- godot-task — executes a single task: generates scenes/scripts, verifies via screenshots

**Skills** (loaded into context):
- asset-gen — CLI tools and instructions for generating images (Gemini) and GLBs (Tripo3D)
- godogen — orchestrator that coordinates scaffold, decomposer, and task agents (invoked via `/godogen`)
- gdscript-doc — GDScript syntax reference + Godot API docs bootstrap and lookup
- visual-qa — analyzes 4 sequential screenshots for visual defects and motion anomalies

When writing agents/skills: don't give obvious guidance. Assume the agent is a strong LLM — handholding only pollutes the context.
