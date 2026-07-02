# Godogen Source Repo

This repository is not a published game repo. It is the source that `publish.sh` renders into a runtime game repo for a chosen engine and host agent.

## Source Layout

- `prompts/runtime.md` — the engine-agnostic runtime manifest text
- `asset-gen/` — the asset-generation skill (CLI tools + docs), the one skill every published repo carries
- `engines/babylon.md`, `engines/godot.md`, `engines/bevy.md` — per-engine guides (stack, project sketch, capture recipe, silent-failure traps)
- `publish.sh` — renders a runtime repo with `--engine {godot,bevy,babylon}`, `--agent {claude,codex}`
- `scripts/` — render helpers: `render_dir.py` (token substitution), `generate_codex_metadata.py` (Codex `openai.yaml`)

## Editing Rules

- Do not create or maintain `.claude/skills/` or `.agents/skills/` in this source repo.
- Don't give obvious guidance. The agent is a highly capable LLM, and the deliverable (a recorded video, or a live URL the user watches) surfaces its own mistakes — so keep the guides to what the model can't infer or discover fast.
- When you change or remove a feature, describe the new state on its own terms. Name the new thing as if it were always the design.
