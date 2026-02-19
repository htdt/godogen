This repository builds Godot game-development skills for Codex.
Take a natural-language game description and turn it into a real, runnable Godot game.
Iterate by building games and updating skills based on what is learned.

Claude Code targets the same pipeline via `.claude/agents/` + `.claude/skills/` — don't change it unless asked.

## Available Skills

Skills live under `.agents/skills/`.

- `godogen` — orchestrates full game generation/update workflow.
- `asset-planner` — plans and generates assets within a budget.
- `godot-scaffold` — creates/updates project architecture and stubs.
- `game-decomposer` — produces `game/PLAN.md` with isolated, testable tasks.
- `godot-task` — executes one task with visual verification; loads capture workflow.
- `godot-capture` — handles screenshot/video capture with GPU-first fallback logic.
- `visual-qa` — analyzes 4 sequential screenshots for visual defects and motion anomalies.
- `asset-gen` — CLI instructions for PNG, spritesheet, and GLB generation.
- `gdscript-doc` — GDScript and Godot API local reference workflow.

When writing skills: don't give obvious guidance. Assume the agent is a strong LLM — handholding only pollutes the context.

