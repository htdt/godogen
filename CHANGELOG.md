# Changelog

**2026-04-24 — Source consolidation**
- Added Bevy as a first-class engine alongside Godot
- Replaced the four Claude/Codex source trees with `shared/`, `godot/`, and `bevy/`
- Added one root `publish.sh` switcher: `--engine godot|bevy` × `--agent claude|codex`
- Codex `agents/openai.yaml` metadata is generated from rendered `SKILL.md` frontmatter
- Dropped the Gemini visual-verification hook — the agent already inspects its own captured frames; the stop hook pushes the latest proof video to Telegram

**2026-04-14 — Codex support**
- Added a parallel Codex source tree alongside the existing Claude Code one
- Each variant publishes to its own runtime layout (`.claude/skills/` vs `.agents/skills/`)

**2026-04-06 — C# migration**
- All skills and generated code migrated from GDScript to C# / .NET 9 ([comparison](docs/gdscript-vs-csharp.md))
- `dotnet build` replaces per-file validation loops

**2026-04-03 — Single-context architecture**
- Orchestrator and task execution merged into one main pipeline
- Added Godot API lookup and visual QA support flows

**2026-03-25 — xAI Grok video**
- Added Grok video generation for animated sprite workflows
- Background removal rewritten with BiRefNet multi-signal matting

**2026-03-09 — Initial release**
- Initial Godogen release with image generation, 3D conversion, screenshot QA, and video capture
