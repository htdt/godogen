---
name: visual-qa
description: >
  This skill sends reference image + 6 game screenshots to
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
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 .claude/skills/visual-qa/scripts/visual_qa.py reference.png <consec1..4.png> <diverse1.png> <diverse2.png> > visual-qa/${N}.md
```

- Exactly 7 PNG paths: 1 reference + 4 consecutive + 2 diverse
- First argument must be `reference.png` (the visual target generated at pipeline start)
- Pick the 4 consecutive frames from the **middle** of the capture (not the very first or last frames)
- Outputs a markdown report to stdout with verdict (`pass`/`fail`/`warning`), reference match assessment, and per-issue details (severity: major/minor = must fix, note = can skip)
- Caller saves stdout to `visual-qa/{N}.md` (N = next sequential number) — committed as test evidence
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Depends on `google-genai` Python package (same as asset-gen)

## Handling Failures

When verdict is **fail**, treat the issues as user feedback — VQA is usually accurate. Read each issue and act:

- **Fixable** (placement, scale, materials, spatial bugs, clipping, z-fighting) — fix it, re-capture, re-run VQA.
- **Unfixable from here** (wrong assets, wrong approach, architectural mismatch) — stop. Report failure to the orchestrator with the VQA issues so it can replan or change assets.

Max 3 fix-and-rerun cycles. If still failing after 3, the root cause is upstream — report all remaining issues to the orchestrator rather than continuing to iterate on symptoms.
