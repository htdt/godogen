---
name: godot-api
description: |
  Look up Godot engine class APIs — methods, properties, signals, enums.
  Use when you need to find which class to use or look up specific API details.
context: fork
model: sonnet
agent: Explore
---

# Godot API Lookup

$ARGUMENTS

## How to answer

1. Read `${CLAUDE_SKILL_DIR}/doc_api/_common.md` — index of ~128 common classes
2. If the class isn't there, read `${CLAUDE_SKILL_DIR}/doc_api/_other.md`
3. Read `${CLAUDE_SKILL_DIR}/doc_api/{ClassName}.md` — full API with descriptions for all methods, properties, signals, constants, and virtual methods
4. Return what the caller needs:
   - **Specific question** (e.g. "how to detect collisions") → return relevant methods/signals with descriptions
   - **Full API request** (e.g. "full API for CharacterBody3D") → return the entire class doc

**GDScript syntax reference:** `${CLAUDE_SKILL_DIR}/gdscript.md` — language syntax, patterns, and recipes. Read when the caller asks about GDScript syntax, idioms, or common patterns (input handling, tweens, state machines, etc.).

Bootstrap if doc_api is empty: `bash ${CLAUDE_SKILL_DIR}/tools/ensure_doc_api.sh`
