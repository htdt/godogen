---
name: bevy-api
description: |
  Look up current Bevy engine APIs, crates, examples, and patterns. Use when you need a targeted Bevy API answer or a specific Bevy type/module recommendation.
---

# Bevy API Lookup

This skill is a narrow reference tool. Keep answers targeted to the caller's question.

Single-version policy:

- Support the Bevy release installed in this skill's local docs cache.
- When the repo upgrades Bevy, update this skill forward and republish.
- Do not carry legacy compatibility guidance unless the caller explicitly asks about migration.
- If the project cannot be resolved to one current Bevy version, or it clearly targets a different release than the installed docs, stop and ask instead of blending sources from multiple versions.

This skill assumes the local docs cache is already installed. Do not try to install, refresh, or retarget it from inside this skill.

Required local paths:

- `.agents/skills/bevy-api/docs/rustdoc/`
- `.agents/skills/bevy-api/docs/bevy/`
- `.agents/skills/bevy-api/docs/bevy-website/`

If any required path is missing or unreadable, stop with an error and say the local `bevy-api` docs cache is unavailable.

Resolve the installed docs release from `.agents/skills/bevy-api/docs/bevy/`, then compare it with the target project's Bevy dependency from `Cargo.toml`, workspace manifests, and `Cargo.lock` when present.

If the project is not a Cargo package or workspace yet, or the Bevy version still cannot be resolved exactly, stop and ask what release to target.

Lookup order:

1. `.agents/skills/bevy-api/docs/rustdoc/`
2. `.agents/skills/bevy-api/docs/bevy/` plus `examples/` for the installed release
3. `.agents/skills/bevy-api/docs/bevy-website/` Learn content for the current release
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
- If compiler output or runtime behavior disagrees with the local docs, call out a likely version mismatch or stale local cache instead of guessing.

Do not dump whole rustdoc pages or enumerate large directories.
