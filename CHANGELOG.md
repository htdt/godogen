# Changelog

**2026-07-02 — Docs-only runtime**
- Replaced the multi-stage skill pipeline with a thin runtime: a single engine-agnostic manifest (`prompts/runtime.md`), a one-page per-engine guide, and the cross-engine `asset-gen` skill. The model plans, scaffolds, and decomposes the work itself.
- One runtime manifest covers delivery. The agent reads the task and the user's presence in-run: an engaged user gets the live game early and checkpoints at taste/scope/cost decisions; an unattended run finishes on reasonable calls and closes with a 15–20s proof recording, watched back before done. Run/show/capture mechanics live in the engine guides and serve both paths.
- Dropped the planner/decomposer/architecture/scene/scaffold/quirks/capture skill docs, the Vite scaffold, the `godot-api` / `bevy-help` / `babylon-help` lookup skills, and all hooks. The engine-specific traps and capture recipes that survive a compile but fail at runtime moved into the engine guide.
- Trimmed asset docs to generation only; `asset-gen` is now the sole published skill.
- Reorganized the source tree: engine-agnostic runtime text lives in `prompts/runtime.md`, and the asset skill lives at top-level `asset-gen/`.
- Continues the 2026-04-26 "dropped Gemini verification" trajectory — removing guidance the current model no longer needs.

**2026-05-18 — Babylon.js support**
- Added Babylon.js as a first-class engine alongside Godot and Bevy
- Disposable TypeScript/Vite scaffold with scene-level hot reload through a custom Vite plugin (`godogen:scene-change`); engine and canvas persist across edits
- Browser capture through Playwright + Chrome/Chromium; hardware WebGL2 preferred, software-renderer fallback warns prominently but still produces media
- `babylon-help` skill uses installed npm package types as the primary local reference
- `publish.sh` extended to `--engine babylon`

**2026-04-26 — Bevy support**
- Added Bevy as a first-class engine alongside Godot
- Replaced the four Claude/Codex source trees with `shared/`, `godot/`, and `bevy/`
- Added one root `publish.sh` switcher: `--engine godot|bevy` × `--agent claude|codex`
- Dropped Gemini verification — Opus 4.7 / GPT 5.5 self-verify from captured frames; external pass added no signal; the stop hook pushes the latest proof video to Telegram

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
