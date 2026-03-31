# Visual Quality Assurance

Analyze game screenshots against the visual reference. Two modes based on scene type.

## Static Mode

For scenes without meaningful motion (decoration, terrain, UI). Two images: reference + one game screenshot.

```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --context "Goal: ...\nRequirements: ...\nVerify: ..." \
  reference.png screenshots/{task}/frame0003.png > visual-qa/${N}.md
```

Pick a representative frame (not the first — often has init artifacts).

## Dynamic Mode

For scenes with motion, animation, or physics. Reference + all frames at **2 FPS cadence** — every Nth frame where N = capture_fps / 2.

```bash
# Example: captured at --fixed-fps 10 → step=5, select every 5th frame
# 30s at 10fps = 300 frames → 60 selected frames + 1 reference = 61 images
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
STEP=5  # capture_fps / 2
FRAMES=$(ls screenshots/{task}/frame*.png | awk "NR % $STEP == 0")
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --context "Goal: ...\nRequirements: ...\nVerify: ..." \
  reference.png $FRAMES > visual-qa/${N}.md
```

Gemini handles 60+ images well in a single request.

## --context

Pass the task's **Goal**, **Requirements**, and **Verify** from PLAN.md. The QA has two objectives:
1. **Quality verification (primary):** visual defects, bugs, implementation shortcuts — problems regardless of what the task asked for.
2. **Goal verification (secondary):** does the output match what was requested?

## Question Mode

For debugging and investigation — ask any question about screenshots without needing a reference image. Use this to diagnose specific issues: animation failures, visual glitches, unexpected behavior.

```bash
# Single screenshot — static questions only
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --question "Are any surfaces showing magenta or default grey material?" \
  screenshots/{task}/frame0005.png

# Frame sequence — for motion/animation analysis
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --question "Does the enemy patrol path form a loop? Do they stop or reverse?" \
  screenshots/{task}/frame0001.png screenshots/{task}/frame0010.png screenshots/{task}/frame0020.png

# With additional context
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --question "The door should open when player approaches. Does it?" \
  --context "InteractionSystem triggers at 2m range, door uses AnimationPlayer" \
  screenshots/{task}/frame*.png
```

Combine `--question` with `--context` for richer analysis. Output goes to stdout — read it directly, don't save to `visual-qa/`. That directory is for structured QA runs only.

## Common

- Output: markdown report with verdict (`pass`/`fail`/`warning`), reference match, goal assessment, per-issue details
- Severity: `major`/`minor` = must fix; `note` = cosmetic, can ship
- Caller saves stdout to `visual-qa/{N}.md` (sequential) — committed as test evidence
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment
- Depends on `google-genai` Python package

## Handling Failures

When verdict is **fail**, treat the issues as user feedback — VQA is usually accurate. Read each issue and act:

- **Fixable** (placement, scale, materials, spatial bugs, clipping, z-fighting, animation logic) — fix it, re-capture, re-run VQA.
- **Unfixable from here** (wrong assets, wrong approach, architectural mismatch) — stop. Report failure to the orchestrator with the VQA issues so it can replan or change assets.

Max 3 fix-and-rerun cycles. If still failing after 3, the root cause is upstream — report all remaining issues to the orchestrator.
