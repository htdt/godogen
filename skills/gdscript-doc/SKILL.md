---
name: gdscript-doc
description: |
  This skill should be used when writing GDScript code, looking up Godot class APIs, or needing GDScript syntax reference. Provides syntax reference, type system, and per-class API lookup. Load before writing any GDScript code.
---

# GDScript Documentation

## Bootstrap

Run `bash .claude/skills/gdscript-doc/tools/ensure_doc_api.sh` (no-ops if already present).

## References

Read `.claude/skills/gdscript-doc/gdscript.md` — GDScript syntax, types, operators, control flow, classes, signals, annotations, math, input handling, physics gotchas.

## API Lookup

Per-class docs live at `.claude/skills/gdscript-doc/doc_api/`:

1. Read `.claude/skills/gdscript-doc/doc_api/_common.md` — index of ~128 commonly used classes.
2. If not found, read `.claude/skills/gdscript-doc/doc_api/_other.md` — index of ~730 remaining classes.
3. Read `.claude/skills/gdscript-doc/doc_api/{ClassName}.md` — full API reference for a specific class.
