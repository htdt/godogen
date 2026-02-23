---
name: visual-qa
description: >
  This skill should be used when the user asks to "check visual quality",
  "run visual QA", "analyze screenshots for bugs", "check for visual bugs",
  "check game screenshots", or when performing visual quality assurance on
  Godot game screenshots. Sends reference image + 6 game screenshots to
  Gemini for defect detection and style/quality verification against the
  visual target. Returns a pass/fail/warning verdict.
---

# Visual Quality Assurance

Analyze game screenshots against the visual reference for style fidelity,
visual bugs, logical inconsistencies, placeholders, and motion anomalies
using Gemini 3 Flash vision.

- **Image 1:** `reference.png` — the visual target (art style, palette, camera, quality bar)
- **Frames 1-4:** consecutive from mid-capture — motion/animation analysis
- **Frames 5-6:** different parts of the game — diverse coverage

## CLI

```bash
python3 .claude/skills/visual-qa/scripts/visual_qa.py reference.png <consec1..4.png> <diverse1.png> <diverse2.png> > visual-qa/{N}.md
```

- Exactly 7 PNG paths: 1 reference + 4 consecutive + 2 diverse
- First argument must be `reference.png` (the visual target generated at pipeline start)
- Pick the 4 consecutive frames from the **middle** of the capture (not the very first or last frames)
- Outputs a markdown report to stdout with verdict (`pass`/`fail`/`warning`), reference match assessment, and per-issue details
- Caller saves stdout to `visual-qa/{N}.md` (N = next sequential number) — committed as test evidence
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Depends on `google-genai` Python package (same as asset-gen)
