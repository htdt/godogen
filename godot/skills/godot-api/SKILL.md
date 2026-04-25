---
name: godot-api
display_name: Godot API Lookup
short_description: Targeted Godot class and C# API lookup
default_prompt: "Use ${GODOT_API_COMMAND} to answer a specific Godot API or C# Godot syntax question."
allow_implicit_invocation: false
description: |
  Look up Godot engine class APIs, methods, properties, signals, enums, or C# Godot syntax. Use when you need a targeted Godot API answer or a specific engine-class recommendation.
---

# Godot API Lookup

This skill is a narrow reference tool. Keep answers targeted to the caller's question.

Do not list or enumerate `${GODOT_API_SKILL_DIR}/doc_api/` or `${GODOT_API_SKILL_DIR}/doc_source/`. Those directories contain nearly a thousand files and listing them wastes context. Navigate through `_common.md`, `_other.md`, and the specific class file you actually need.

## How to answer

1. If you already know the class or likely class, search `${GODOT_API_SKILL_DIR}/doc_api/_common.md` and `_other.md` for the class name instead of reading the whole index files.
2. If the caller does not name a class, use `${GODOT_API_SKILL_DIR}/doc_api/_common.md` and `_other.md` to identify likely candidates, then read only the relevant docs.
3. Read only the relevant `${GODOT_API_SKILL_DIR}/doc_api/{ClassName}.md` file or files.
4. Return only what the caller needs:
   - **Specific question** (for example, "how to detect collisions") -> return the relevant methods, signals, or patterns with short descriptions
   - **Full API request** (for example, "full API for CharacterBody3D") -> return the whole class doc summary

**C# syntax reference:** `${GODOT_API_SKILL_DIR}/csharp.md` — C# Godot syntax, patterns, and recipes. Read it when the caller asks about C# Godot syntax, idioms, or common patterns such as input handling, tweens, state machines, or signals.

Bootstrap if `doc_api` is empty:

```bash
bash ${GODOT_API_SKILL_DIR}/tools/ensure_doc_api.sh
```
