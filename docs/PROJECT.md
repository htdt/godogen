# Godogen — From Prompt to Playable Game

Godogen is an autonomous development pipeline for turning a natural-language game brief into a playable Godot or Bevy project. It plans the game, generates visual direction and assets, writes code, captures media from the running engine, and verifies the final result visually.

It is not a game engine, a code generator, or an asset marketplace. It is a source repo for runtime skills that are published into a fresh game repo and then executed by Claude Code or Codex.

## Source Model

The repo is organized by engine:

- `shared/` — engine-agnostic `godogen` stages, shared verification hooks, and common published-repo instructions
- `godot/` — Godot-specific `godogen` stages and `godot-api`
- `bevy/` — Bevy-specific `godogen` stages and `bevy-help`

Claude Code vs Codex is selected at render time:

```bash
./publish.sh --engine godot --agent claude --out ~/game
./publish.sh --engine godot --agent codex --out ~/game
./publish.sh --engine bevy --agent claude --out ~/game
./publish.sh --engine bevy --agent codex --out ~/game
```

Publishing writes `CLAUDE.md` plus `.claude/skills/` for Claude Code, or `AGENTS.md` plus `.agents/skills/` for Codex. Codex `agents/openai.yaml` files are generated from each rendered `SKILL.md` frontmatter.

## Pipeline

The `godogen` skill orchestrates the run and loads stage-specific files only when they are needed:

1. **Visual target** — generate `reference.png` and write art direction into `ASSETS.md`.
2. **Decomposition** — write `task.md` and `PLAN.md`, isolating only genuinely risky features.
3. **Scaffold** — create or update the engine project shell and `STRUCTURE.md`.
4. **Asset planning and generation** — spend the user-provided budget on the assets that matter most.
5. **Task execution** — implement risk slices first, then the main build.
6. **Capture** — create a fresh `screenshots/result/{N}/` bundle with raw `frameXXX.png` files and `video.mp4`.
7. **Verification** — the shared stop hook checks the latest proof bundle with Gemini and blocks completion when the visible result fails.

The document protocol is deliberate. `task.md`, `PLAN.md`, `STRUCTURE.md`, `ASSETS.md`, and `MEMORY.md` survive context compaction and let the run resume from files instead of conversational memory.

## Engine Support

Godot output is a Godot 4 C#/.NET project. The Godot runtime skill uses scene builders for generated `.tscn` files, runtime scripts for gameplay, `godot-api` for targeted engine lookup, and a Godot capture helper for final proof bundles.

Bevy output is a Rust/Bevy project. The Bevy runtime skill uses code-first scene construction, local Bevy rustdoc/examples through `bevy-help`, and a dedicated capture path for final proof bundles.

Both engines share the same final verification contract: `task.md` at project root plus the latest numeric `screenshots/result/{N}/` folder.

## What Makes This Different

**Visual verification, not just code generation.** The pipeline captures actual frames from the game and verifies them with a vision model. It catches bugs that text-only analysis misses: z-fighting, floating objects, missing materials, clipped UI, frozen motion, and placeholder remnants.

**Progressive loading.** The orchestrator reads only the stage file it needs at the moment. Support skills keep large engine references out of the main context.

**Budget-aware asset generation.** Gemini, Grok, and Tripo3D are used where they make economic sense, and generated assets are assigned back into `PLAN.md` so implementation does not lose them.

**Engine-specific expertise without agent duplication.** Godot and Bevy are different enough to keep their engine docs separate. Claude and Codex are similar enough to render from one source.

## Runtime Limitations

The current runtime does not ship audio. Godot supports debug APK export when requested; Bevy Android export is not implemented yet.
