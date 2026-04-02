# Test Harness & Visual Verification

Write `test/test_{task_id}.gd` (e.g., `test/test_T3.gd`) — a SceneTree script that loads the scene under test and verifies the task's goal. Do NOT call `quit()` — the movie writer handles exit.

## SceneTree Script Contract

Tests must `extend SceneTree` (not Node). Key details:
- `_initialize()` for setup (not `_ready()`)
- `_process(delta: float) -> bool` — return `false` to keep running
- Camera needs `_cam.current = true` to activate

## Console Assertions

The test harness stdout is captured alongside screenshots. Use `print("ASSERT PASS/FAIL: ...")` to verify behavioral properties that are hard to judge visually (exact positions, velocities, state changes). After capture, check stdout for any `ASSERT FAIL` lines — these must be fixed before the task is complete.

## Simulated Input

For tests needing player input, use a Timer to trigger actions:

```gdscript
    var timer := Timer.new()
    timer.wait_time = 1.0
    timer.one_shot = true
    timer.timeout.connect(func(): Input.action_press("move_forward"))
    root.add_child(timer)
    timer.start()
```

### Sustained movement (presentation scripts)

Open-loop input (timed press/release sequences) doesn't work for 30-second videos — per-frame errors compound into visible drift, edge-sticking, and tightening carve spirals. Use closed-loop waypoint steering based on actual position each frame.
