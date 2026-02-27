---
name: visual-qa
description: >
  Screenshot QA (reference + 6 frames) and video QA (gameplay MP4) via
  Gemini 3 Flash vision. Returns pass/fail/warning verdicts.
---

# Visual Quality Assurance

## Screenshot QA

Analyze game screenshots against the visual reference for style fidelity,
visual bugs, logical inconsistencies, placeholders, and motion anomalies.

- **Image 1:** `reference.png` — the visual target (art style, palette, camera, quality bar)
- **Frames 1-4:** consecutive from mid-capture — motion/animation analysis
- **Frames 5-6:** different parts of the game — diverse coverage

```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 .claude/skills/visual-qa/scripts/visual_qa.py [--verify "criteria"] reference.png <consec1..4.png> <diverse1.png> <diverse2.png> > visual-qa/${N}.md
```

- Exactly 7 PNG paths: 1 reference + 4 consecutive + 2 diverse
- First argument must be `reference.png` (the visual target generated at pipeline start)
- Pick the 4 consecutive frames from the **middle** of the capture (not the very first or last frames)
- `--verify` — optional, pass the task's Verify criteria so Gemini checks task-specific goals too
- Outputs markdown report to stdout with verdict (`pass`/`fail`/`warning`), reference match assessment, and per-issue details (severity: major/minor = must fix, note = can skip)

## Video QA

Analyze a gameplay video for motion/animation correctness and basic aesthetics — stuck entities, sliding, teleportation, physics breaks, camera issues, scene composition.

```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 .claude/skills/visual-qa/scripts/video_qa.py [--verify "criteria"] screenshots/presentation/gameplay.mp4 > visual-qa/${N}.md
```

- Single MP4 path. Errors if >100MB (expected <10MB for 30s CRF 28 720p).
- `--verify` — optional, pass the task's Verify criteria
- Uses `MEDIA_RESOLUTION_LOW` — cheap: ~1k tokens for a 10s clip.

## Common

- Caller saves stdout to `visual-qa/{N}.md` (N = next sequential number) — committed as test evidence
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Depends on `google-genai` Python package (same as asset-gen)

## Handling Failures

When verdict is **fail**, treat the issues as user feedback — VQA is usually accurate. Read each issue and act:

- **Fixable** (placement, scale, materials, spatial bugs, clipping, z-fighting, animation logic) — fix it, re-capture, re-run VQA.
- **Unfixable from here** (wrong assets, wrong approach, architectural mismatch) — stop. Report failure to the orchestrator with the VQA issues so it can replan or change assets.

Max 3 fix-and-rerun cycles. If still failing after 3, the root cause is upstream — report all remaining issues to the orchestrator rather than continuing to iterate on symptoms.
