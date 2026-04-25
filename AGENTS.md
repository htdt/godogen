# Godogen Source Repo

This repository is not a published game repo. It is the source for runtime skills and game-repo templates that are rendered by engine and host agent.

## Source Layout

- `shared/` — engine-agnostic `godogen` files, shared hook templates, and common game-repo instructions
- `godot/` — Godot-specific `godogen` files, `godot-api`, Godot capture hook helpers, and Godot game-repo instructions
- `bevy/` — Bevy-specific `godogen` files, `bevy-help`, Bevy capture hook helpers, and Bevy game-repo instructions
- `publish.sh` — renders a runtime repo with `--engine {godot,bevy}` and `--agent {claude,codex}`

Claude vs Codex is a publish-time render choice, not a source-tree split.

## Source vs Runtime

- `godot/game-engine.md` and `bevy/game-engine.md` render to `CLAUDE.md` or `AGENTS.md` in published game repos.
- Runtime skills render to `.claude/skills/` for Claude Code and `.agents/skills/` for Codex.
- Runtime hooks render to `.claude/hooks/` or `.codex/hooks/`.
- Codex `agents/openai.yaml` files are generated from each skill's rendered `SKILL.md` frontmatter.
- Do not create or maintain `.claude/skills/` or `.agents/skills/` in this source repo.

## Skills

Published Godot repos carry:

- **godogen**
- **godot-api**

Published Bevy repos carry:

- **godogen**
- **bevy-help**

## Editing Rules

- Engine-specific work stays in the matching subtree: `godot/` or `bevy/`.
- Shared behavior stays in `shared/` only when it is genuinely engine-agnostic.
- Do not align Godot and Bevy behavior unless asked or the file belongs under `shared/`.
- If you change a skill's user-facing purpose, update its `SKILL.md` frontmatter. Do not hand-edit generated `agents/openai.yaml`.
- When writing skills: don't give obvious guidance. The agent is a highly capable LLM; handholding only pollutes the context.
