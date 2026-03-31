---
name: godot-task
description: |
  Execute a single Godot development task — generate scenes and/or scripts, verify visually.
context: fork
---

# Godot Task Executor

All files below are in `${CLAUDE_SKILL_DIR}/`. Load progressively — read each file when its phase begins, not upfront.

| File | Purpose | When to read |
|------|---------|--------------|
| `quirks.md` | Known Godot gotchas and workarounds | Before writing any code |
| `gdscript.md` | GDScript syntax reference | Before writing any code |
| `scene-generation.md` | Building `.tscn` files via headless GDScript builders | Targets include `.tscn` |
| `script-generation.md` | Writing runtime `.gd` scripts for node behavior | Targets include `.gd` |
| `coordination.md` | Ordering scene + script generation | Targets include both `.tscn` and `.gd` |
| `test-harness.md` | Writing `test/test_{id}.gd` verification scripts | Before writing test harness |
| `capture.md` | Screenshot/video capture with GPU detection | Before capturing screenshots |
| `visual-qa.md` | Automated screenshot comparison against reference | `reference.png` exists and task has visual output |
| `doc_api/_common.md` | Index of ~128 common Godot classes (one-line each) | Need API ref; scan to find class names |
| `doc_api/_other.md` | Index of ~732 remaining Godot classes | Need API ref; class isn't in `_common.md` |
| `doc_api/{ClassName}.md` | Full API reference for a single Godot class | Need API ref; look up specific class |

Bootstrap doc_api: `bash ${CLAUDE_SKILL_DIR}/tools/ensure_doc_api.sh`

Execute a single development task from PLAN.md:

$ARGUMENTS

## Workflow

1. **Analyze the task** — read the task's **Targets** to determine what to generate:
   - `scenes/*.tscn` targets → generate scene builder(s)
   - `scripts/*.gd` targets → generate runtime script(s)
   - Both → generate scenes FIRST, then scripts (scenes create nodes that scripts attach to)
2. **Import assets** — run `timeout 60 godot --headless --import` to generate `.import` files for any new textures, GLBs, or resources. Without this, `load()` fails with "No loader found" errors. Re-run after modifying existing assets.
3. **Generate scene(s)** — write GDScript scene builder, compile to produce `.tscn`
4. **Generate script(s)** — write `.gd` files to `scripts/`
5. **Pre-validate scripts** — catch compilation errors early before full project validation. For each newly written or modified `.gd` file, run `timeout 30 godot --headless --quit 2>&1` and filter the output for errors mentioning that file's path.
6. **Validate** — run `timeout 60 godot --headless --quit 2>&1` to parse-check all project scripts.
7. **Fix errors** — if Godot reports errors, read output, fix files, re-run. Repeat until clean.
8. **Generate test harness** — write `test/test_{task_id}.gd` implementing the task's **Verify** scenario.
9. **Capture screenshots** — run test with GPU display (or xvfb fallback) and `--write-movie` to produce PNGs
10. **Verify visually** — read captured PNGs and check three things:
   - **Task goal:** does the screenshot match the **Verify** description?
   - **Visual consistency:** if `reference.png` exists, compare against it — color palette, scale proportions, camera angle, and visual density should be consistent.
   - **Visual quality & logic:** look for obvious bugs — geometry clipping, objects floating, wrong assets, text overflow, UI elements overlapping or cut off.
   Also check harness stdout for `ASSERT FAIL`.
   If any check fails, identify the issue, fix scene/script/test, and repeat from step 3.
11. **Visual QA** — run automated visual QA when applicable.
12. **Store final evidence** — save screenshots in `screenshots/{task_folder}/` before reporting completion.

## Iteration Tracking

Steps 3-11 form an **implement → screenshot → verify → VQA** loop.

There is no fixed iteration limit — use judgment:
- If there is progress — even in small, iterative steps — keep going. Screenshots and file updates are cheap.
- If you recognize a **fundamental limitation** (wrong architecture, missing engine feature, broken assumption), stop early — even after 2-5 iterations. More loops won't help.
- The signal to stop is **"I'm making the same kind of fix repeatedly without convergence"**.

## Reporting to Orchestrator

Always end your response with:
- **Screenshot path:** `screenshots/{task_folder}/` and which frames best represent the result (e.g., `frame0003.png`, `frame0006.png`)
- **What each screenshot shows** — one line per frame
- **VQA report:** path to `visual-qa/{N}.md` (or "skipped" if non-visual), note which mode (static/dynamic)

On failure, also include:
- What's still wrong
- What you tried and why it didn't fix it
- Your best guess at the root cause (include VQA report content if relevant)

The caller (godogen orchestrator) will decide whether to adjust the task, re-scaffold, or accept the current state.

## Debugging with Gemini

When something looks wrong in screenshots but the cause isn't obvious, use `visual_qa.py --question` to get a second pair of eyes. This is especially useful for issues that are hard to detect from code alone.

### Isolate and Capture

Don't debug in a complex scene — isolate the problem:

1. **Minimal repro scene** — write a throwaway `test/debug_{issue}.gd` that sets up only the relevant nodes (the animation, the physics body, the UI element). Strip everything else. Capture screenshots of just this.
2. **Targeted frames** — for animation/motion issues, capture at `--fixed-fps 10` for 3-5 seconds and feed the full sequence to `--question`. Single frames miss timing bugs.
3. **Before/after** — capture with the fix applied and without. Feed both sets to `--question "What changed between these two sets?"`.

### Animation Failures

Animations are the #1 source of silent failures — they "work" (no errors) but produce wrong results. The current pipeline is bad at detecting these because validation only checks for parse errors.

Common animation issues to probe:
- **Frozen pose** — capture 3-5s at 10 FPS, feed all frames: `--question "Does the character's pose change between frames, or is it the same pose throughout?"`
- **Wrong animation** — same multi-frame capture: `--question "Describe how the character's limbs and body move across frames. Does it look like walking, idling, attacking, or something else?"`
- **Animation not blending** — same: `--question "Are there any sudden pose jumps between consecutive frames, or do poses transition smoothly?"`
- **AnimationPlayer vs AnimationTree conflicts** — both trying to control the same skeleton
- **Animation on wrong node** — player set up correctly but targeting a different skeleton path
- **Bone/track mismatches** — animation was made for a different model, tracks don't map

When you suspect animation failure, always capture dynamic (multi-frame) and ask Gemini specifically about motion between frames.

### Other Debug Scenarios

- **"Is this node even visible?"** — capture and ask. Nodes can be hidden by z-order, wrong layer, zero alpha, off-camera, or wrong viewport.
- **Physics not working** — capture a sequence and ask `"Do any objects move due to gravity or collision?"`. RigidBodies silently do nothing if collision shapes are missing.
- **UI layout broken** — capture and ask `"Are any UI elements overlapping, cut off, or positioned outside the visible area?"`
- **Shader/material issues** — ask `"Are any surfaces showing magenta, checkerboard, or default grey material?"`

### Special Debug Scene Pattern

```
# In test/debug_{issue}.gd:
# 1. Load only the relevant nodes
# 2. Set up camera to frame the issue
# 3. Add visible markers (colored boxes, labels) to confirm positions
# 4. Run for enough frames to capture the behavior
# Then capture and feed to --question
```

This is cheaper than re-running the full task scene and gives Gemini a cleaner signal.

## Commands

```bash
# Import new/modified assets (MUST run before scene builders):
timeout 60 godot --headless --import

# Compile a scene builder (produces .tscn):
timeout 60 godot --headless --script <path_to_gd_builder>

# Validate all project scripts (parse check):
timeout 60 godot --headless --quit 2>&1
```

**Structured error recovery:** When a compilation error is caught:
1. Parse the error — extract the file path, line number, and error type from Godot's output
2. Look up the class — if the error mentions an unknown method or property, read `doc_api/{ClassName}.md` for the class involved
3. Check quirks — cross-reference against `quirks.md` for known patterns (`:=` with `instantiate()`, polymorphic math functions, Camera2D `current`, etc.)
4. Fix and re-validate — edit the specific file, then re-run the pre-validation step on that file only before proceeding

**Error handling:** Parse Godot's stderr/stdout for error lines. Common issues:
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class in `doc_api`
- `Cannot infer type` — `:=` used with `instantiate()` or polymorphic math functions, see type inference rules
- Script hangs — missing `quit()` call in scene builder; kill the process and add `quit()`

## Project Memory

Read `MEMORY.md` before starting work — it contains discoveries from previous tasks (workarounds, Godot quirks, asset details, architectural decisions). After completing your task, write back anything useful you learned: what worked, what failed, technical specifics others will need.
