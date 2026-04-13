---
name: godot-api
description: |
  Look up Godot engine class APIs, methods, properties, signals, enums, or C# Godot syntax. Use when you need a targeted Godot API answer or a specific engine-class recommendation.
---

# Godot API Lookup

This skill is a narrow reference tool. Keep answers targeted to the caller's question.

Do not list or enumerate `.agents/skills/godot-api/doc_api/` or `.agents/skills/godot-api/doc_source/`. Those directories contain nearly a thousand files and listing them wastes context. Navigate through `_common.md`, `_other.md`, and the specific class file you actually need.

## How to answer

1. If you already know the class or likely class, search `.agents/skills/godot-api/doc_api/_common.md` and `_other.md` for the class name instead of reading the whole index files.
2. If the caller does not name a class, use `.agents/skills/godot-api/doc_api/_common.md` and `_other.md` to identify likely candidates, then read only the relevant docs.
3. Read only the relevant `.agents/skills/godot-api/doc_api/{ClassName}.md` file or files.
4. Return only what the caller needs:
   - **Specific question** (for example, "how to detect collisions") -> return the relevant methods, signals, or patterns with short descriptions
   - **Full API request** (for example, "full API for CharacterBody3D") -> return the whole class doc summary

**C# syntax reference:** `.agents/skills/godot-api/csharp.md` — C# Godot syntax, patterns, and recipes. Read it when the caller asks about C# Godot syntax, idioms, or common patterns such as input handling, tweens, state machines, or signals.

Bootstrap if `doc_api` is empty:

```bash
bash .agents/skills/godot-api/tools/ensure_doc_api.sh
```
