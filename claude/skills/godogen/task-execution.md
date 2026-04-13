# Task Execution

Implementation workflow and debugging reference.

## Planning Each Task

`PLAN.md` from the decomposer captures risks and verification criteria — not an implementation strategy. Before coding any task (risk or main build), produce a concrete approach using the built-in planning mechanism. Decomposer tells you *what* to watch out for; the planning step decides *how* to build it.

Prefer spawning the `Plan` subagent (via the `Agent` tool with `subagent_type: "Plan"`) — it returns a plan as text with no approval prompt, so execution proceeds automatically. Only use interactive plan mode if the user explicitly asks to review plans before execution.

## Phases

### Risk tasks (if PLAN.md has any)

Implement each risk feature in isolation before the main build:
1. Set up minimal environment — only the nodes needed to exercise the risk
2. Run the implementation loop until the risk task's **Verify** criteria pass
3. Commit

### Main build

Implement everything in PLAN.md's **Main Build**:
1. Generate scenes first, then scripts
2. Run the implementation loop until **After main build** verification criteria pass
3. Run **Final** verification including presentation video
4. Commit

## Implementation Loop

1. **Import assets** — `timeout 60 godot --headless --import`. Re-run after modifying assets.
2. **Generate scenes** — write scene builder C# files, compile, run to produce `.tscn`
3. **Generate scripts** — write `.cs` files
4. **Build** — `timeout 60 dotnet build 2>&1`
5. **Validate** — `timeout 60 godot --headless --quit 2>&1`
6. **Capture** — write test harness, run with `--write-movie`, produce screenshots
7. **Verify** — check captures against the current phase's verification criteria + reference.png consistency. Check stdout for `ASSERT FAIL`.
8. **Visual QA** — run automated VQA when applicable
9. If verification fails -> fix and repeat from step 2

After each phase: update PLAN.md, write discoveries to MEMORY.md, git commit.

## Iteration Tracking

Steps 2-8 form an **implement -> screenshot -> verify -> VQA** loop.

There is no fixed iteration limit — use judgment:
- If there is progress, keep going. Screenshots and file updates are cheap.
- If you recognize a **fundamental limitation** (wrong architecture, missing engine feature, broken assumption), stop early. More loops won't help.
- The signal to stop is **"I'm making the same kind of fix repeatedly without convergence"**.

## Godot C# Gotchas

- All Godot classes must be `partial` (`CS0260`)
- Godot API is PascalCase — `CS1061` usually means wrong casing or wrong base class
- `Instantiate()` returns `Node` — cast explicitly (`CS0029`)
- Scene builder hangs — missing `Quit()` call; kill and add it
- `GD.Load()` returns null — assets not imported, run `godot --headless --import`
- Signal not firing — delegate name must end in `EventHandler`, and class must be `partial`

## Visual Debugging

When something looks wrong in screenshots but the cause isn't obvious, use `Skill(skill="visual-qa")` in question mode to get a second pair of eyes. This is especially useful for issues that are hard to detect from code alone.

### Isolate and Capture

Don't debug in a complex scene — isolate the problem:

1. **Minimal repro scene** — write a throwaway `test/DebugIssue.cs` that sets up only the relevant nodes (the animation, the physics body). Strip everything else. Capture screenshots of just this.
2. **Targeted frames** — for animation/motion issues, capture at `--fixed-fps 10` for 3-5 seconds and feed the full sequence. Single frames cannot show timing bugs.
3. **Before/after** — capture with the fix applied and without. Ask "What changed between these two sets?".

### Animation Failures

Animations are the #1 source of silent failures — they "work" (no errors) but produce wrong results. The current pipeline is bad at detecting these because validation only checks for compile errors.

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

1. **Confirm the object exists** — add `GD.Print($"{node.Name} at {node.GlobalPosition}")` in `_Ready()`. If it doesn't print, the node isn't in the tree.
2. **Add a debug marker** — place a small emissive sphere (`EmissionEnabled = true`, bright color, 0.5m radius) at the object's position. If the sphere is visible, the object's mesh/material is the problem. If the sphere is also invisible, the camera is the problem.
3. **Check camera direction** — print `camera.GlobalPosition` and `camera.GlobalTransform.Basis.Z` (the camera looks along -Z). Use `camera.LookAt(obj.GlobalPosition)` to force the camera toward the object.
4. **Check occlusion** — another object may be blocking the view. Temporarily hide large geometry (`terrain.Visible = false`) to see if the target appears behind it.
5. **Check scale** — `GD.Print(node.Scale)` — a scale of `new Vector3(0.001f, 0.001f, 0.001f)` makes the object sub-pixel. Also check if the object is enormous and the camera is inside it.
6. **Check material** — `StandardMaterial3D` with `Transparency = BaseMaterial3D.TransparencyEnum.Alpha` and `AlbedoColor.A = 0` is invisible. Set `AlbedoColor = Colors.Red` temporarily.

### Other Debug Scenarios

- **"Is this node even visible?"** — capture and ask. Nodes can be hidden by z-order, wrong layer, zero alpha, off-camera, or wrong viewport.
- **Physics not working** — capture a sequence and ask "Do any objects move due to gravity or collision?". RigidBodies silently do nothing if collision shapes are missing.
- **UI layout broken** — capture and ask "Are any UI elements overlapping, cut off, or positioned outside the visible area?"
- **Shader/material issues** — ask "Are any surfaces showing magenta, checkerboard, or default grey material?"

### Special Debug Scene Pattern

In `test/DebugIssue.cs`:
1. Load only the relevant nodes
2. Set up camera to frame the issue
3. Add visible markers (colored boxes, labels) to confirm positions
4. Run for enough frames to capture the behavior
5. Capture and feed to visual-qa question mode

This is cheaper than re-running the full task scene and gives the VQA a cleaner signal.
