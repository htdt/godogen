The goal is to develop Claude Code agents and skills for Godot game development:

**Agents** (autonomous, run via Task tool):
- game-decomposer — decomposes a game into isolated, testable tasks (PLAN.md)
- godot-scaffold — designs architecture and creates compilable project skeleton
- godot-task — executes a single task: generates scenes/scripts, verifies via screenshots

**Skills** (loaded into context):
- gamedev — orchestrator that coordinates scaffold, decomposer, and task agents (invoked via `/gamedev`)
- gdscript-doc — GDScript syntax reference + Godot API docs bootstrap and lookup

We take a natural language game description and turn it into a real game.
We iterate via building games and updating agents/skills.

When writing agents/skills: don't give obvious guidance. Assume the agent is a strong LLM — handholding only pollutes the context.

Where to record learnings:
- Generally useful Godot knowledge → add to the relevant agent or skill file
- Dev process details (workflow, conventions) → add to CLAUDE.md
- Don't use local auto memory — this repo is shared, local memory creates invisible leaks
