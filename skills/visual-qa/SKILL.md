---
name: visual-qa
description: >
  This skill should be used when the user asks to "check visual quality",
  "run visual QA", "analyze screenshots for bugs", "check for visual bugs",
  "check game screenshots", "triage VQA report", or when performing visual
  quality assurance on Godot game screenshots. Sends reference image + 6 game
  screenshots to Gemini for defect detection and style/quality verification
  against the visual target. Returns a pass/fail/warning verdict. Includes
  triage process for failed reports.
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

## Report Triage

When verdict is **fail**, triage before delegating fixes. Never pass a fail report directly to a developer agent — it will rationalize issues away.

### Process

1. Read the VQA report (`visual-qa/{N}.md`)
2. Classify each issue individually into exactly one category
3. Write `visual-qa/{N}_triage.md`
4. Delegate only after triage is written

### Categories

| Category | Meaning | Action |
|----------|---------|--------|
| **fix** | Addressable within current architecture | Delegate with explicit fix instructions |
| **mitigate** | Can't fully solve but can visibly improve | Delegate with mitigation strategy and acceptance threshold |
| **replan** | Requires architectural change — wrong approach, wrong dimension, wrong technique | Stop current work. Reassess architecture. New scaffold/decompose. |

**No "dismiss" or "skip" category.** Every issue requires action or escalation.

### Classification Rules

- Classify each issue INDIVIDUALLY — never batch-classify (e.g., "all of these are inherent to 2D")
- "Inherent to the approach" is not a dismissal — it means the approach is wrong → **replan**
- Unsure between fix and mitigate → choose **fix**
- VQA flags an intentional design choice → **fix** with action "no change needed — intentional per user request" and cite the specific user instruction. This is the ONLY path to a no-op.

### Triage File

Write `visual-qa/{N}_triage.md`:

```markdown
# VQA Triage: Report {N}

**Report verdict:** fail
**Triage result:** {fix | replan}

---

### Issue 1: {title from report}
- **VQA type:** {type from report}
- **VQA severity:** {severity from report}
- **Classification:** fix | mitigate | replan
- **Reasoning:** {1-2 sentences. Be specific.}
- **Action:** {Concrete fix instructions, OR "replan: {what needs to change}"}
- **Done when:** {Screenshot-verifiable result}
```

Triage result is **replan** ONLY if any issue is classified replan AND has major severity.
Minor/note replan issues demote to mitigate → triage result is **fix**.

### Decision Logic

**Priority: replan > fix > mitigate**

**Any major replan issue:**
1. Do NOT fix or mitigate other issues first — they're in the blast radius of the architectural change
2. Record all fix/mitigate issues in triage file (deferred, not lost)
3. Re-scaffold/decompose with corrected approach, and trigger asset-planner if new assets are needed
5. Fresh VQA cycle after rebuild — old issues may no longer exist

**All fix/mitigate (no major replan):**
1. Delegate ALL issues to developer agent in a single pass with triage file path
2. After fixes applied, run VQA again on new screenshots
3. Repeat triage → fix → VQA until verdict is **pass**
4. Maximum 3 fix cycles. If still failing after 3, escalate entire triage to replan. Persistent failures across 3 cycles indicate the root cause is upstream — wrong assets, wrong generation parameters, or a fundamentally mismatched approach. Replan should reexamine initial assumptions rather than continue iterating on symptoms.

### Gate

Do not proceed to next pipeline phase while:
- Any **fix** issue remains unresolved
- Any **mitigate** issue has not been attempted
- Any **replan** issue has not been escalated
