---
triggers:
  - "gdscript reference"
  - "gdscript syntax"
  - "godot api docs"
  - "look up godot class"
description: |
  GDScript language reference and Godot API documentation.
  Provides syntax reference, type system, and per-class API lookup.
  Load this skill before writing any GDScript code.
write_style: "imperative"
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
