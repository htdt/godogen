---
name: bevy-api
description: |
  Look up current Bevy engine APIs, crates, examples, and patterns. Use when you need a targeted Bevy API answer or a specific Bevy type/module recommendation.
context: fork
model: sonnet
agent: Explore
---

# Bevy API Lookup

$ARGUMENTS

This skill is a narrow reference tool. Keep answers targeted to the caller's question.

Single-version policy:

- Support the Bevy release used by the current project.
- When the repo upgrades Bevy, update this skill forward.
- Do not carry legacy compatibility guidance unless the caller explicitly asks about migration.
- If the project context cannot be resolved to one current Bevy version, stop and ask instead of blending sources from multiple versions.

Resolve the target project context first:

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/resolve_bevy_context.py
```

Prefer an explicit project path when the current working directory is not the game root.

If the project is not a Cargo package or workspace yet, stop and ask what Bevy release to target.

If `resolve_bevy_context.py` reports an unresolved version, treat that as a hard stop for exact API guidance.

This skill expects `docs/rustdoc`, `docs/bevy`, and `docs/bevy-website` to already be set up.

In the source repo, run `./setup_bevy_docs.sh /path/to/bevy-docs` before publishing.

Each skill install exposes that shared cache through local symlinks:

- `${CLAUDE_SKILL_DIR}/docs/rustdoc/`
- `${CLAUDE_SKILL_DIR}/docs/bevy/`
- `${CLAUDE_SKILL_DIR}/docs/bevy-website/`

Keep that `docs/` directory gitignored. Treat the symlinks and shared cache as local working data, not authored source.

Bootstrap or refresh the local cache with:

```bash
bash ${CLAUDE_SKILL_DIR}/tools/create_docs.sh
```

Without a project path, this uses the latest stable Bevy tag from the local `bevy` checkout, not `main`.

If you already have a target Bevy project and want rustdoc aligned to it:

```bash
bash ${CLAUDE_SKILL_DIR}/tools/create_docs.sh path/to/project
```

Lookup order:

1. Project rustdoc
2. `${CLAUDE_SKILL_DIR}/docs/bevy/` plus `examples/` for the current release
3. `${CLAUDE_SKILL_DIR}/docs/bevy-website/` Learn content for the current release
4. Small local notes in this skill, if any
5. Web fallback only when the caller explicitly asks for it or the local stack is unavailable

Use only the minimum source needed:

- Exact API or symbol names: rustdoc first, then source if implementation details matter
- "How do I do X?": examples first, then rustdoc for exact names and signatures
- Recommendation or best-practice: examples, then rustdoc, then Learn content
- Behavior, warnings, or "why did Bevy do this?": crate source first, then rustdoc if you need the public surface
- Migration questions: only compare old and new APIs if the caller asked for migration help

Problem-shape heuristics:

- Pattern or architecture question -> examples first
- Warning, propagation, auto-inserted behavior, or hierarchy/debug question -> crate source first
- Exact symbol, trait bound, or signature question -> rustdoc first

Bevy-specific source traps:

- If behavior seems automatic, inspect component attributes such as `#[require(...)]` and `#[component(on_insert = ...)]` in crate source.
- Rustdoc is best for public names and signatures, but it often hides the internal reason a behavior occurs.
- Learn content is advisory. If it disagrees with examples or crate source for the checked-out release, trust examples and source.

Common entry points:

- App setup: `App`, `Plugin`, schedules, states, runners, `DefaultPlugins`
- ECS: `Commands`, `Component`, `Bundle`, `Query`, resources, messages/events/observers, run conditions
- Assets and scenes: `AssetServer`, handles, `Assets<T>`, scene loading and spawning types
- Cameras and rendering: camera setup, render layers, clear color, lighting examples
- UI: `bevy_ui` node, text, button, image, layout, and interaction types
- Spatial setup: `Transform`, `GlobalTransform`, hierarchy helpers, 2D vs 3D camera patterns

When answering:

- Start with the concrete answer, not version boilerplate.
- Name the exact files or pages you checked.
- Separate doc facts from inference.
- Mention feature gates or crate boundaries only when they affect the answer.
- If you give code, use only symbols you verified in the current sources.
- If compiler output or runtime behavior disagrees with the local docs, say the cache may be stale and refresh it before answering confidently.

Do not dump whole rustdoc pages or enumerate large directories.
