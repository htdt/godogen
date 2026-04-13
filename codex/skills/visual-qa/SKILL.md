---
name: visual-qa
description: |
  Visual quality assurance for gameplay screenshots. Use when you need to compare screenshots against a reference, inspect motion across frames, or answer a visual debugging question about a Godot game.
---

# Visual QA

CRITICAL: Your job is to find problems, not confirm that things look fine. Do not rationalize, justify, or explain away what you see. If it looks wrong, report it.

## Backend

- **Default (Gemini):** Run the script below. All queries go to `gemini-3-flash-preview`.
- If the request includes `--native`: inspect every referenced image directly with Codex's native image analysis. Do not run the Gemini script.
- If the request includes `--both`: run Gemini first, then do native image analysis. Aggregate verdicts as described below.

## Mode Detection

From the request text, including any explicit flags and file paths:

- Reference image mentioned + 1 screenshot -> Static mode
- Reference image + multiple frames -> Dynamic mode — frames are 0.5s apart (2 FPS cadence)
- No reference, just a question about screenshots -> Question mode

## Gemini Execution

Parse the request to construct the command. The script is at `.agents/skills/visual-qa/scripts/visual_qa.py`.

```bash
# Static
python3 .agents/skills/visual-qa/scripts/visual_qa.py --log .vqa.log [--context "Goal: ... Requirements: ... Verify: ..."] reference.png screenshot.png

# Dynamic
python3 .agents/skills/visual-qa/scripts/visual_qa.py --log .vqa.log [--context "..."] reference.png frame1.png frame2.png ...

# Question
python3 .agents/skills/visual-qa/scripts/visual_qa.py --log .vqa.log --question "the question" screenshot.png [frame2.png ...]
```

Always pass `--log .vqa.log`. Print the script output as your response.

## Native Execution

Inspect every image file referenced in the request directly. Analyze using the criteria and output format below. Never look at code — only images.

After producing output, append a debug log entry:

```bash
printf '%s\n' "$(cat <<'LOGEOF'
{"ts":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","mode":"MODE","model":"native","query":"QUERY","files":["FILE1","FILE2"],"output":"FIRST_LINE..."}
LOGEOF
)" >> .vqa.log
```

## Aggregated Mode (`--both`)

1. Run the Gemini script and capture its output
2. Inspect all images directly and do native analysis using the criteria below
3. Produce the combined verdict:
   - Either says `fail` -> `fail`
   - Either says `warning` and neither says `fail` -> `warning`
   - Both say `pass` -> `pass`
4. Merge issue lists from both and deduplicate by location + description
5. Label each issue source: `[gemini]`, `[native]`, or `[both]`
6. Log both outputs to `.vqa.log`

## Analysis Criteria

### Implementation Quality (static + dynamic)

Assets are usually fine — what breaks is how they are placed, scaled, and composed:

- Grid or uniform placement when the reference shows organic arrangement
- Uniform default scale when the reference shows varied, purposeful sizing
- Flat composition when the reference has depth and layering
- Stretched, tiled, or carelessly applied materials
- Objects unrelated to the environment, just placed on a flat plane
- Camera framing that does not match the reference perspective

### Visual Bugs

- Z-fighting (flickering overlapping surfaces)
- Texture stretching, tiling seams, missing textures (magenta/checkerboard)
- Geometry clipping (objects visibly intersecting)
- Floating objects that should be grounded
- Shadow artifacts (detached, through walls, missing)
- Lighting leaks through opaque geometry
- Culling errors (missing faces, disappearing objects)
- UI overlap, truncated text, offscreen elements

### Logical Inconsistencies

- Impossible orientations (sideways, upside-down, embedded in terrain)
- Scale mismatches (tree smaller than character, door too small)
- Misplaced objects (furniture on ceiling, rocks in sky)
- Broken spatial relationships (bridge not connecting, stairs into wall)

### Placeholder Remnants

- Untextured primitives contrasting with surrounding detail
- Default Godot materials (grey StandardMaterial3D, magenta missing shader)
- Debug artifacts (collision shapes, nav mesh, axis gizmos)

### Motion & Animation (dynamic mode only)

Compare consecutive frames (0.5s apart):

- Stuck entities (same position/pose across frames when movement is expected)
- Jitter or teleportation (large position jumps between frames)
- Sliding (position changes but pose is frozen)
- Physics breaks (objects through walls, endless bouncing, unnatural acceleration)
- Animation mismatches (walk anim at running speed, idle while moving)
- Camera issues (sudden jumps, clipping through geometry)
- Collision failures (overlapping objects that should collide)

## Output Format

### Static / Dynamic

```text
### Verdict: {pass | fail | warning}

### Reference Match
{1-3 sentences: does the game capture the reference's intent — placement logic, scaling, composition, camera? Distinguish lazy implementation from acceptable asset or engine limitations.}

### Goal Assessment
{1-3 sentences from Task Context. "No task context provided." if none.}

### Issues

{If none: "No issues detected." Otherwise:}

#### Issue {N}: {short title}
- **Type:** style mismatch | visual bug | logical inconsistency | motion anomaly | placeholder
- **Severity:** major | minor | note
- **Frames:** {dynamic only: which frames}
- **Location:** {where in frame}
- **Description:** {1-2 sentences}

### Summary
{One sentence.}
```

Severity: `major` and `minor` must be fixed. `note` is cosmetic.

### Question Mode

```text
### Answer
{Direct, specific, actionable answer. Reference locations, frames, colors, objects.}

### Visual Evidence
{What in the screenshots supports the answer. Reference specific frames and locations.}
```
