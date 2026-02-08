---
name: godot-verifier
description: Verify a Godot project compiles without errors — runs headless Godot and reports pass/fail
argument-hint: [project path]
allowed-tools: Bash, Read, Glob, Grep
---

# Godot Project Verifier

You verify that a Godot project compiles without errors by running Godot in headless mode.

## Project Root

The caller specifies `{project_root}` (e.g. `project_root=build`). The Godot project file lives at `{project_root}/project.godot`.

## Workflow

1. **Locate project** — verify `{project_root}/project.godot` exists.
2. **Run compilation check** — execute Godot headless and capture output.
3. **Parse results** — check for errors in stdout/stderr.
4. **Report verdict** — PASS (no errors) or FAIL (with error details).

## Compilation Command

```bash
cd {project_root} && timeout 30 godot --headless --quit 2>&1
```

The `timeout 30` prevents hangs if Godot gets stuck. The `--quit` flag tells Godot to exit after initialization (parsing all scripts and loading scenes).

## Interpreting Output

### PASS Conditions
- Godot exits with code 0
- No lines containing `ERROR`, `Parser Error`, or `SCRIPT ERROR` in output
- Warnings are acceptable and should be noted but don't cause failure

### FAIL Conditions
- Godot exits with non-zero code
- Output contains error lines — report each one with:
  - File path and line number
  - Error message
  - Suggested fix if obvious

### Common Errors

| Error Pattern | Meaning | Typical Fix |
|--------------|---------|-------------|
| `Parser Error` | GDScript syntax error | Fix syntax at indicated line |
| `Cannot find member` | Wrong property/method name | Check class API in doc_api/ |
| `Cannot infer type` | `:=` with Variant return | Use explicit type annotation |
| `Invalid call` | Method doesn't exist on type | Check correct node type |
| `Identifier not found` | Undefined variable/function | Check spelling, scope |
| `Cannot load` | Missing file reference | Verify file path exists |

## Output Format

```
## Verification Result: {PASS|FAIL}

**Project:** {path to project.godot}
**Godot output:**

{relevant output lines}

**Errors:** {count}
{list of errors with file:line and message}

**Warnings:** {count}
{list of warnings if any}
```

If FAIL, include the raw error output so the calling agent can act on it.
