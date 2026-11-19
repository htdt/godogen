# Godogen Source Repo

This repository holds two agent skills in the open Agent Skills format, which Claude Code, Codex and Antigravity share. Users install them with `npx skills add htdt/godogen`, which finds them in `skills/`, or link a clone (README.md, Install). Nothing is rendered: the files here are what the agent reads.

## Layout

- `skills/engine-guide/` — `SKILL.md` (choosing an engine, uses beyond games), `setup.md` (installing each toolchain), and one guide per engine: `godot.md` (C#), `godot-gdscript.md`, `bevy.md`, `babylon.md`, `threejs.md`, `html.md` (stack, project sketch, capture recipe, silent-failure traps)
- `skills/asset-gen/` — asset generation: local through [godogen_assets](https://github.com/htdt/godogen_assets) (`SKILL.md`, with its own Setup), paid APIs (`api.md`), game-side animation (`motion.md`), `scripts/`

## Editing Rules

- Skills live only in `skills/`. Do not create `.claude/skills/` or `.agents/skills/` in this repo.
- Frontmatter is `name` (equal to the directory name) and `description`, nothing host-specific: no Claude Code fields or `${CLAUDE_*}` variables, no Codex `agents/openai.yaml`.
- Setup is written for the agent, which installs what a project needs. It resolves current stable releases at install time; never pin a version from memory. Only what the user alone can provide (API keys, hardware) goes in the README.
- A skill's files reference each other by paths relative to the skill directory. The godogen_assets checkout is `$GODOGEN_ASSETS`, defined in `asset-gen/SKILL.md` from where its commands resolve.
- Local generation is documented and coded in godogen_assets. `asset-gen` links to its docs with a short TL;DR and adds only what the project side needs; never copy its instructions or tools here.
- Don't give obvious guidance. The agent is a highly capable LLM that plans, verifies and decides what to deliver on its own — so keep the guides to building blocks: what the model can't infer or discover fast.
- When you change or remove a feature, describe the new state on its own terms. Name the new thing as if it were always the design.
