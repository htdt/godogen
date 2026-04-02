# Task Execution

Implementation workflow and debugging reference.

## Phases

### Risk tasks (if PLAN.md has any)

Implement each risk feature in isolation before the main build:
1. Set up minimal environment — only the nodes needed to exercise the risk
2. Run the implementation loop until the risk task's **Verify** criteria pass
3. Commit

### Main build

Implement everything in PLAN.md's **Main Build**:
1. Generate scenes first, then scripts (scenes create nodes that scripts attach to)
2. Run the implementation loop until **After main build** verification criteria pass
3. Run **Final** verification including presentation video
4. Commit

## Implementation Loop

1. **Import assets** — `timeout 60 godot --headless --import` (generates `.import` files for textures/GLBs — without this, `load()` fails). Re-run after modifying assets.
2. **Generate scenes** — write scene builder scripts, compile to `.tscn`
3. **Generate scripts** — write `.gd` files
4. **Pre-validate** — `timeout 30 godot --headless --check-only -s <path>` for each new/modified `.gd`
5. **Validate project** — `timeout 60 godot --headless --quit 2>&1`
6. **Fix errors** — if validation fails, fix and re-validate
7. **Capture** — write test harness, run with `--write-movie`, produce screenshots
8. **Verify** — check captures against the current phase's verification criteria + reference.png consistency. Check stdout for `ASSERT FAIL`.
9. **Visual QA** — run automated VQA when applicable
10. If verification fails -> fix and repeat from step 2

After each phase: update PLAN.md, write discoveries to MEMORY.md, git commit.

## Iteration Tracking

Steps 2-9 form an **implement -> screenshot -> verify -> VQA** loop.

There is no fixed iteration limit — use judgment:
- If there is progress — even in small, iterative steps — keep going. Screenshots and file updates are cheap.
- If you recognize a **fundamental limitation** (wrong architecture, missing engine feature, broken assumption), stop early — even after 2-5 iterations. More loops won't help.
- The signal to stop is **"I'm making the same kind of fix repeatedly without convergence"**.

## Commands

```bash
# Import new/modified assets (MUST run before scene builders):
timeout 60 godot --headless --import

# Compile a scene builder (produces .tscn):
timeout 60 godot --headless --script <path_to_gd_builder>

# Pre-validate a single script (exits 0 if valid, 1 with errors):
timeout 30 godot --headless --check-only -s <path_to_gd>

# Validate all project scripts (parse check):
timeout 60 godot --headless --quit 2>&1
```

**Common errors:**
- `Parser Error` — syntax error in GDScript, fix the line indicated
- `Invalid call` / `method not found` — wrong node type or API usage, look up the class via `Skill(skill="godot-api")`
- `Cannot infer type` — `:=` used with `instantiate()` or polymorphic math functions, see type inference rules
- Script hangs — missing `quit()` call in scene builder; kill the process and add `quit()`

## Project Memory

Read `MEMORY.md` before starting work — it contains discoveries from previous tasks (workarounds, Godot quirks, asset details, architectural decisions). After completing your task, write back anything useful you learned: what worked, what failed, technical specifics later tasks will need.

## Visual Debugging

When something looks wrong in screenshots but the cause isn't obvious, use `Skill(skill="visual-qa")` in question mode to get a second pair of eyes. This is especially useful for issues that are hard to detect from code alone.

### Isolate and Capture

Don't debug in a complex scene — isolate the problem:

1. **Minimal repro scene** — write a throwaway `test/debug_{issue}.gd` that sets up only the relevant nodes (the animation, the physics body). Strip everything else. Capture screenshots of just this.
2. **Targeted frames** — for animation/motion issues, capture at `--fixed-fps 10` for 3-5 seconds and feed the full sequence. Single frames cannot show timing bugs.
3. **Before/after** — capture with the fix applied and without. Ask "What changed between these two sets?".

### Animation Failures

Animations are the #1 source of silent failures — they "work" (no errors) but produce wrong results. The current pipeline is bad at detecting these because validation only checks for parse errors.

Common animation issues to probe:
- **Frozen pose** — capture 3-5s at 10 FPS, feed all frames: "Does the character's pose change between frames, or is it the same pose throughout?"
- **Wrong animation** — same multi-frame capture: "Describe how the character's limbs and body move across frames. Does it look like walking, idling, attacking, or something else?"
- **Animation not blending** — same: "Are there any sudden pose jumps between consecutive frames, or do poses transition smoothly?"
- **AnimationPlayer vs AnimationTree conflicts** — both trying to control the same skeleton
- **Animation on wrong node** — player set up correctly but targeting a different skeleton path
- **Bone/track mismatches** — animation was made for a different model, tracks don't map

When you suspect animation failure, always capture dynamic (multi-frame) and ask specifically about motion between frames.

### 3D Object Not Visible

When a 3D object should be on-screen but isn't, run this checklist in order — each step isolates one failure mode:

1. **Confirm the object exists** — add `print(node.name, " at ", node.global_position)` in `_ready()`. If it doesn't print, the node isn't in the tree.
2. **Add a debug marker** — place a small emissive sphere (`emission_enabled = true`, bright color, 0.5m radius) at the object's position. If the sphere is visible, the object's mesh/material is the problem. If the sphere is also invisible, the camera is the problem.
3. **Check camera direction** — print `camera.global_position` and `camera.global_transform.basis.z` (the camera looks along -Z). Use `camera.look_at(object.global_position)` to force the camera toward the object.
4. **Check occlusion** — another object may be blocking the view. Temporarily hide large geometry (`terrain.visible = false`) to see if the target appears behind it.
5. **Check scale** — `print(node.scale)` — a scale of `Vector3(0.001, 0.001, 0.001)` makes the object sub-pixel. Also check if the object is enormous and the camera is inside it.
6. **Check material** — `StandardMaterial3D` with `transparency = ALPHA` and `albedo_color.a = 0` is invisible. Set `albedo_color = Color.RED` temporarily.

### Other Debug Scenarios

- **"Is this node even visible?"** — capture and ask. Nodes can be hidden by z-order, wrong layer, zero alpha, off-camera, or wrong viewport.
- **Physics not working** — capture a sequence and ask "Do any objects move due to gravity or collision?". RigidBodies silently do nothing if collision shapes are missing.
- **UI layout broken** — capture and ask "Are any UI elements overlapping, cut off, or positioned outside the visible area?"
- **Shader/material issues** — ask "Are any surfaces showing magenta, checkerboard, or default grey material?"

### Special Debug Scene Pattern

In test/debug_{issue}.gd:
1. Load only the relevant nodes
2. Set up camera to frame the issue
3. Add visible markers (colored boxes, labels) to confirm positions
4. Run for enough frames to capture the behavior
5. Capture and feed to visual-qa question mode

This is cheaper than re-running the full task scene and gives the VQA a cleaner signal.
