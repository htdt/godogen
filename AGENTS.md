# Godogen Source Repo

This repository contains three source trees:

- `claude/` — Claude Code source tree
- `codex/` — Codex Godot source tree
- `codex_bevy/` — Codex Bevy source tree

This is not a published game repo. The files at the repo root describe how to work on the source trees themselves.

## Source vs Runtime

- `*/game.md` files are runtime instruction templates:
  `claude/game.md` becomes `CLAUDE.md`; `codex/game.md` and `codex_bevy/game.md` become `AGENTS.md` in published repos.
- `*/publish.sh` publishes runtime skills:
  `claude/` publishes to `.claude/skills/`; `codex/` and `codex_bevy/` publish to `.agents/skills/`.
- `codex/` and `codex_bevy/` are both active Codex source trees for different engines.
- Root docs such as `README.md` and `setup.md` describe the combined repo and shared workstation setup.

## Skills

The current source trees carry these runtime skills:

- `claude/` and `codex/`: **godogen**, **godot-api**, **visual-qa**
- `codex_bevy/`: **godogen**, **bevy-api**, **visual-qa**

## Editing Rules

- User must specify the target source tree.
- Variant-specific work stays in the matching subtree: `claude/`, `codex/`, or `codex_bevy/`.
- Shared docs and shared repo policy live at the repo root.
- Do not align the behavior across both variants unless asked.
- Do not create or maintain `.claude/skills/` or `.agents/skills/` in this source repo.
- If you change a Codex skill's user-facing purpose, also update its `agents/openai.yaml` metadata.
- When writing skills: don't give obvious guidance. The agent is a highly capable LLM — handholding only pollutes the context.
