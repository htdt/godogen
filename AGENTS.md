# Godogen Source Repo

This repository contains two published source trees plus one Bevy migration workspace:

- `claude/` — Claude Code source tree
- `codex/` — Codex Godot source tree
- `codex_bevy/` — Codex Bevy migration workspace

This is not a published game repo. The files at the repo root describe how to work on the source trees themselves.

## Source vs Runtime

- `claude/game.md` is the template that becomes `CLAUDE.md` in a published Claude game repo.
- `codex/game.md` is the template that becomes `AGENTS.md` in a published Codex game repo.
- `claude/publish.sh` publishes runtime skills into `.claude/skills/`.
- `codex/publish.sh` publishes runtime skills into `.agents/skills/`.
- `codex_bevy/` is additive migration work. Do not treat it as a replacement for `codex/` unless the user explicitly asks for that transition.
- Root docs such as `README.md` and `setup.md` describe the combined repo and shared workstation setup.

## Skills

Both source trees carry the same three skills:

- **godogen** — orchestrator + inline task execution + all pipeline stages
- **godot-api** — Godot class API lookup
- **visual-qa** — visual quality assurance via multimodal review

## Editing Rules

- User must specify which is the target source tree or migration workspace.
- Variant-specific work stays in the matching subtree: `claude/`, `codex/`, or `codex_bevy/`.
- Shared docs and shared repo policy live at the repo root.
- Do not align the behavior across both variants unless asked.
- Do not create or maintain `.claude/skills/` or `.agents/skills/` in this source repo.
- If you change a Codex skill's user-facing purpose, also update its `agents/openai.yaml` metadata.
- When writing skills: don't give obvious guidance. The agent is a highly capable LLM — handholding only pollutes the context.
