---
name: visual-qa
description: >
  This skill should be used when the user asks to "check visual quality",
  "run visual QA", "analyze screenshots for bugs", "check for visual bugs",
  "check game screenshots", or when performing visual quality assurance on
  Godot game screenshots. Sends 4 sequential frames to Gemini for automated
  defect detection and returns a pass/fail/warning verdict.
---

# Visual Quality Assurance

Analyze 4 sequential game screenshots for visual bugs, logical inconsistencies,
placeholder remnants, and motion anomalies using Gemini 3 Flash vision.

## CLI

```bash
python3 .claude/skills/visual-qa/scripts/visual_qa.py <frame1> <frame2> <frame3> <frame4>
```

- Exactly 4 PNG paths required (sequential frames from the same capture session)
- Outputs a markdown report to stdout with verdict (`pass`/`fail`/`warning`) and per-issue details
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Depends on `google-genai` Python package (same as asset-gen)
