#!/usr/bin/env python3
"""Visual QA — send 7 game screenshots to Gemini for quality analysis.

Usage:
  python3 .claude/skills/visual-qa/scripts/visual_qa.py f1.png f2.png f3.png f4.png f5.png f6.png f7.png

Frames 1-4: consecutive (for motion analysis). Frames 5-7: diverse locations.
Output: Markdown report to stdout.
Requires: GEMINI_API_KEY or GOOGLE_API_KEY in environment.
"""

import sys
from pathlib import Path

from google import genai
from google.genai import types

PROMPT = """\
You are a visual QA agent examining screenshots of a game built in Godot. You receive 7 screenshots. Frames 1-4 are consecutive frames from the same capture session — use these for motion and animation analysis. Frames 5-7 are from different parts of the game — use these for broader coverage of visual bugs and coherence. Your job is to identify visual bugs, logical inconsistencies, placeholders, and motion anomalies. You do NOT judge gameplay design or artistic quality — only correctness.

## What to Look For

### Visual Bugs (rendering/geometry errors)
- Z-fighting: flickering or overlapping surfaces competing for the same depth
- Texture stretching, tiling seams, or missing textures (magenta/checkerboard)
- Geometry clipping: objects visibly intersecting each other (e.g., wheels sunk into ground, character halfway through a wall)
- Floating objects that should be grounded (trees hovering above terrain, items in mid-air)
- Shadow artifacts: detached shadows, shadows through solid walls, missing shadows on lit objects
- Lighting leaks: bright spots bleeding through geometry that should be opaque
- Culling errors: missing faces, objects visibly disappearing at edges
- UI elements overlapping, truncated text, elements drawn offscreen

### Logical Inconsistencies (things that violate common sense)
- Characters or objects in impossible orientations (sideways, upside-down, embedded in terrain)
- Scale mismatches: a tree smaller than a character, a door too small to walk through, a car larger than a building
- Misplaced objects: furniture on a ceiling, fish above water, rocks floating in sky
- Broken spatial relationships: a bridge not connecting to anything, stairs leading into a wall
- UI showing impossible values: negative health, score decreasing when it shouldn't, timers behaving erratically

### Placeholder Remnants & Coherence (signs of incomplete integration)
- Primitive geometry standing in for real objects: untextured cubes, spheres, cylinders, or capsules that contrast sharply with surrounding detail level
- Detail level mismatches: one element is clearly placeholder-quality (flat color, no texture) while neighboring elements have full materials and textures
- Default Godot materials: the characteristic grey of unassigned StandardMaterial3D, or magenta indicating a missing shader
- Debug or development artifacts: visible collision shapes (wireframe outlines), navigation mesh overlays, axis gizmos, path visualization lines
- Leftover test geometry: the flat colored boxes or simple ramps typical of placeholder environments that weren't removed after merge
- Inconsistent art style: one object is photorealistic while others are low-poly, or one uses pixel-art textures alongside smooth-shaded meshes — suggesting a placeholder was never replaced
- Orphaned UI elements: "Score: 0" labels sitting at default positions, unstyled buttons with default Godot theme amid custom UI

### Motion Analysis (from consecutive frames 1-4)
Compare frames 1-4 in order to detect:
- Stuck entities: an object or character in the exact same position/pose across all 4 frames when movement is expected
- Jitter/teleportation: an object in drastically different positions between consecutive frames with no plausible trajectory
- Animation freezes: a character mid-stride in the same pose across frames while clearly having moved position (sliding)
- Camera issues: sudden jumps in viewpoint, camera clipping through geometry, wildly inconsistent framing
- Physics anomalies: objects accelerating unnaturally, bouncing endlessly, drifting sideways without cause
## Output Format

### Verdict: {pass | fail | warning}

### Issues

If no issues found, write "No issues detected."

Otherwise, list each issue:

#### Issue {N}: {short title}
- **Type:** visual bug | logical inconsistency | motion anomaly | placeholder
- **Severity:** major | minor
- **Frames:** {which frames, e.g., "1-2", "all", "5 only", "5-7"}
- **Location:** {where in the frame, e.g., "center foreground", "top-right corner"}
- **Description:** {one or two sentences explaining what's wrong and why it matters}

### Summary

{One-sentence overall assessment.}
"""


def main():
    if len(sys.argv) != 8:
        print(f"Usage: {sys.argv[0]} <frame1..7.png> (4 consecutive + 3 diverse)", file=sys.stderr)
        sys.exit(1)

    paths = [Path(p) for p in sys.argv[1:]]
    for p in paths:
        if not p.exists():
            print(f"Error: {p} not found", file=sys.stderr)
            sys.exit(1)

    client = genai.Client()

    labels = [
        "Frame 1 (consecutive):", "Frame 2 (consecutive):",
        "Frame 3 (consecutive):", "Frame 4 (consecutive):",
        "Frame 5 (diverse):", "Frame 6 (diverse):", "Frame 7 (diverse):",
    ]
    contents: list[types.Part | str] = [PROMPT]
    for label, p in zip(labels, paths):
        contents.append(label)
        contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))

    print("Analyzing 7 frames with Gemini 3 Flash...", file=sys.stderr)
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contents,  # type: ignore[arg-type]
        )
    except Exception as e:
        print(f"Error: Gemini API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not response.text:
        print("Error: Gemini returned no text (possible safety block)", file=sys.stderr)
        sys.exit(1)

    print(response.text)


if __name__ == "__main__":
    main()
