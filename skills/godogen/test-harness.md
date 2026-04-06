# Test Harness & Visual Verification

Write `test/TestXxx.cs` (e.g., `test/TestT3.cs`) — a SceneTree script that loads the scene under test and verifies the task's goal. Do NOT call `Quit()` — the movie writer handles exit.

## SceneTree Script Contract

Tests must extend `SceneTree` (not Node). Key details:
- `_Initialize()` for setup (not `_Ready()`)
- `_Process(double delta)` returns `bool` — return `false` to keep running
- Camera needs `_cam.Current = true` to activate
- Must be `public partial class`
- Must run `dotnet build` before capture

## Console Assertions

The test harness stdout is captured alongside screenshots. Use `GD.Print("ASSERT PASS/FAIL: ...")` to verify behavioral properties that are hard to judge visually (exact positions, velocities, state changes). After capture, check stdout for any `ASSERT FAIL` lines — these must be fixed before the task is complete.

## Simulated Input

For tests needing player input, use a Timer to trigger actions:

```csharp
var timer = new Timer();
timer.WaitTime = 1.0;
timer.OneShot = true;
timer.Timeout += () => Input.ActionPress("move_forward");
Root.AddChild(timer);
timer.Start();
```

### Sustained movement — use closed-loop steering (default)

Open-loop input (timed press/release sequences) causes visible drift, edge-sticking, and tightening spirals as per-frame errors compound. **Default to closed-loop waypoint steering:** read the actual position each frame and steer toward the next waypoint. This applies to all tests with sustained movement, not just presentation scripts.
