# Godogen — From Prompt to Playable Game

Godogen turns a natural-language game brief into a playable Godot, Bevy, Babylon.js, three.js, or HTML project. The agent builds the game, generates assets, and runs the engine.

It is not a game engine, a code generator, or an asset marketplace. It is a source repo that publishes a thin runtime — a manifest, an engine guide, and an asset skill — into a fresh game repo that Claude Code or Codex then builds in.

## Source Model

The repo is organized by engine, with the cross-engine pieces shared:

- `prompts/runtime.md` — the runtime manifest
- `asset-gen/` — the `asset-gen` skill
- `engines/godot.md` (C#), `engines/godot-gdscript.md`, `engines/bevy.md`, `engines/babylon.md`, `engines/threejs.md`, `engines/html.md` — per-engine guides

Engine and host agent are selected at render time:

```bash
./publish.sh --engine godot   --agent claude --out ~/game
./publish.sh --engine babylon --agent codex  --out ~/game
```

Publishing writes `CLAUDE.md` + `.claude/skills/` for Claude Code, or `AGENTS.md` + `.agents/skills/` for Codex, plus the `<engine>.md` guide. Codex `agents/openai.yaml` is generated from the `asset-gen` `SKILL.md` frontmatter.

## How a run works

The runtime manifest is short: read the brief, build the game, keep durable status in `README.md`, generate assets with `asset-gen`, and follow the engine guide for stack, project sketch, and capture. There is no fixed multi-stage pipeline, no prescribed document protocol, and no verification or delivery protocol — a capable model plans the work, checks it, and decides what to hand back. The manifest fixes only *where durable state lives* (`README.md`, so a run survives compaction) and that paid generation waits for the user's go-ahead.

The engine guide carries only what the model can't infer or discover quickly: the project sketch (what stack and layout to stand up), the capture recipe (how to render the running game headlessly), and the handful of silent-failure traps that pass a compile but break at runtime.

## Engine Support

- **Godot** — Godot 4 C#/.NET. Scenes are generated at build time by headless `SceneTree` scripts; the guide carries the serialization rules (owner chain, GLB-recursion trap, post-pack validation) and the `--write-movie` + ffmpeg capture recipe.
- **Godot (GDScript)** — the same engine, scene builders, and capture in statically typed GDScript on any Godot build. With no compiler, the guide gates on `--check-only` per script and on `SCRIPT ERROR` in the log, since a runtime error leaves the exit code at 0.
- **Bevy** — Rust, current stable Bevy resolved and pinned at build time, ECS scenes spawned `OnEnter`. The guide points the agent at the installed source for current APIs and gives the offscreen `RenderTarget::Image` capture recipe.
- **Babylon.js** — TypeScript/Vite, served at a live URL. The guide covers the side-effect-import trap, Havok physics, and headless Chrome capture.
- **three.js** — TypeScript/Vite, served at a live URL; the agent picks physics (Rapier) and UI itself. The guide covers color space, physical lights, rigged clones, the WebGPU fallback, and step-driven headless Chrome capture.
- **HTML** — text-first 2D in the DOM with CSS and TypeScript/Vite, served at a live URL. The guide covers saves that survive the dev server's reloads, re-render and glyph-fallback traps, background-tab timing, and the audio gesture rule.

[README.md](../README.md#choosing-an-engine) has the guide to choosing between them.

## What Makes This Different

**Trust the model.** The runtime ships no scaffold, no planner, and no review or delivery rules. The model recreates boilerplate from a short sketch, decomposes the work, and decides how to check it and what to hand back; the guides spend their words only on building blocks it genuinely can't know.

**Local-first asset generation.** Assets come from [godogen_assets](https://github.com/htdt/godogen_assets), free on the machine's GPU; paid APIs (Gemini, Grok, Tripo3D, Lyria) fill only what it can't make, with the cost confirmed with the user first. The asset manifest in `README.md` tracks paths, in-game sizes, and costs so implementation doesn't lose them.

**One source, many targets.** Engine and host agent are render-time choices over one source tree.

## Runtime Limitations

The runtime does not ship mobile/native packaging.
