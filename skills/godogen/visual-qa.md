# Visual Quality Assurance

Analyze game screenshots against the visual reference. Runs in a forked context via the `visual-qa` skill. Default backend is Gemini 3 Flash; pass `--native` for Claude vision or `--both` for aggregated verdict.

## Static Mode

For scenes without meaningful motion (decoration, terrain, UI). Two images: reference + one game screenshot.

```
Skill(skill="visual-qa") "Check reference.png against screenshots/{task}/frame0003.png — Goal: ..., Requirements: ..., Verify: ..."
```

Pick a representative frame (not the first — often has init artifacts).

## Dynamic Mode

For scenes with motion, animation, or physics. Reference + frame sequence at **2 FPS cadence** — every Nth frame where N = capture_fps / 2.

```
# Example: captured at --fixed-fps 10 → step=5, select every 5th frame
# 30s at 10fps = 300 frames → 60 selected frames + 1 reference = 61 images
STEP=5  # capture_fps / 2
FRAMES=$(ls screenshots/{task}/frame*.png | awk "NR % $STEP == 0" | tr '\n' ' ')
Skill(skill="visual-qa") "Check reference.png against $FRAMES — Goal: ..., Requirements: ..., Verify: ..."
```

## Question Mode

For debugging and investigation — ask any question about screenshots without needing a reference image.

```
Skill(skill="visual-qa") "Are any surfaces showing magenta or default grey material? screenshots/{task}/frame0005.png"

Skill(skill="visual-qa") "Does the enemy patrol path form a loop? screenshots/{task}/frame0001.png screenshots/{task}/frame0010.png screenshots/{task}/frame0020.png"

Skill(skill="visual-qa") "The door should open when player approaches. Does it? InteractionSystem triggers at 2m, door uses AnimationPlayer. screenshots/{task}/frame*.png"
```

## Backend Selection

```
# Gemini 3 Flash (default)
Skill(skill="visual-qa") "Check reference.png against screenshots/{task}/frame0003.png — Goal: ..."

# Claude vision
Skill(skill="visual-qa") "--native Check reference.png against screenshots/{task}/frame0003.png — Goal: ..."

# Both — aggregated verdict (stricter wins, issues merged)
Skill(skill="visual-qa") "--both Check reference.png against screenshots/{task}/frame0003.png — Goal: ..."
```

## Context

Pass the task's **Goal**, **Requirements**, and **Verify** from PLAN.md as freeform text. The QA has two objectives:
1. **Quality verification (primary):** visual defects, bugs, implementation shortcuts — problems regardless of what the task asked for.
2. **Goal verification (secondary):** does the output match what was requested?

## Common

- Output: markdown report with verdict (`pass`/`fail`/`warning`), reference match, goal assessment, per-issue details
- Severity: `major`/`minor` = must fix; `note` = cosmetic, can ship
- Debug log appended to `.vqa.log` (JSONL: query, files, output)
- Question mode output goes to stdout — read directly
