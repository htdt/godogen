# Post-Task Visual Gate Plan

Shared design for adding a runtime hook that validates the final presentation video after an agent thinks the task is complete.

## Goal

Replace the current manual or skill-driven final visual QA step with an automatic post-task gate:

1. Agent stops.
2. Runtime hook checks for the presentation video.
3. If the video exists, send it to Gemini for inspection.
4. If Gemini fails the result, feed the issues back into the CLI as a new task.
5. Cap retries and stop on obvious non-progress.

## Scope

- Applies to `codex/` and `claude/`.
- Keep the implementation separate per runtime.
- Keep the verifier logic shared.
- Do not change Bevy variants unless requested later.

## Expected Inputs

- Final presentation video: `screenshots/presentation/gameplay.mp4`
- Optional supporting screenshots: `screenshots/{task_folder}/`

## Architecture

1. Add one shared verifier script.
2. Run it from a runtime stop hook.
3. The script scans artifacts, loads prior state, and returns one of:
   - `pass`
   - `retry`
   - `terminal_fail`
4. Runtime-specific hook adapters translate that result into the local hook protocol.

## Shared Verifier Script

Responsibilities:

- Find `screenshots/presentation/gameplay.mp4`
- Hash the current video content
- Persist and read per-session or per-task state
- Call Gemini with strict structured output
- Decide whether to pass, retry, or hard fail

Suggested state:

- `retry_count`
- `missing_count`
- `last_video_hash`
- `last_failed_hash`
- `last_verdict`

## Retry Policy

### Missing video

- First stop with no video: `retry`
- Second consecutive stop with no video: `terminal_fail`

### Failed Gemini verdict

- If Gemini says `fail`: `retry` with a compact fix summary
- On the next stop, compare the new video hash to the last failed hash
- If unchanged: count as no progress and `terminal_fail`

### Infinite-loop guard

- Add a small global retry cap, for example `2` or `3`
- Exceeding the cap returns `terminal_fail`

## Gemini Contract

Use structured JSON only. Suggested response shape:

```json
{
  "verdict": "pass | fail",
  "issues": [
    "..."
  ],
  "recommended_fix": "..."
}
```

Rules:

- Reject free-form prose as hook control input
- Convert Gemini output into a short deterministic continuation message
- Treat malformed or missing JSON as `terminal_fail`

## Runtime Adapters

### Codex

- Add repo-local `.codex/hooks.json`
- Enable `[features] codex_hooks = true`
- Use a `Stop` hook
- Map:
  - `pass` -> allow stop
  - `retry` -> block stop with continuation reason
  - `terminal_fail` -> stop with clear user-facing failure message

Notes:

- Hooks are experimental
- Windows support is currently disabled

### Claude Code

- Add a project hook config
- Use `Stop` for parity with Codex
- Optionally add `TaskCompleted` later if task completion should be gated before final stop
- Map:
  - `pass` -> allow stop
  - `retry` -> block stop and continue with hook feedback
  - `terminal_fail` -> stop with clear failure reason

## Edge Cases

Handle these as terminal conditions unless there is a specific recovery path:

- No GPU, so presentation video cannot be produced
- Video unreadable or corrupt
- Gemini request fails repeatedly
- Gemini returns invalid schema
- Retry budget exhausted

## Rollout Order

1. Logging-only mode
2. Missing-video detection and retry
3. Gemini inspection on existing video
4. Same-video detection via content hash
5. Retry cap and terminal failure rules
6. Replace the current final visual-QA step in docs and workflow
