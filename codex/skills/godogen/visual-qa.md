# Visual Quality Assurance

Analyze game screenshots against the visual reference. Default backend is `gemini-3-flash-preview`; pass `--native` for native image analysis or `--both` for an aggregated verdict.

Context policy: run Gemini inline. For `--native` or `--both`, use a helper agent so image review starts from a fresh context.

## Mode choice

Pick Dynamic whenever the task or goal mentions smooth, transition, handoff, blend, state change, or any verb that implies motion (idle/walk, walk/attack, run/jump, place/pickup). Static one-frame check cannot catch timing, frozen poses, or pops — and those are the failures that actually ship.

Static is for decoration, terrain, UI/HUD, title — scenes with no motion contract.

## Static Mode

For scenes without meaningful motion (decoration, terrain, UI). Two images: reference + one game screenshot.

```text
$visual-qa Check reference.png against screenshots/{task}/frame00000003.png — Goal: ..., Requirements: ..., Verify: ...
```

Pick a representative frame (not the first — often has init artifacts).

## Dynamic Mode

For scenes with motion, animation, or physics. Reference + frame sequence at **2 FPS cadence** — every Nth frame where N = capture_fps / 2.

```text
# Example: captured at --fixed-fps 10 -> step=5, select every 5th frame
# 30s at 10fps = 300 frames -> 60 selected frames + 1 reference = 61 images
STEP=5
FRAMES=$(ls screenshots/{task}/frame*.png | awk "NR % $STEP == 0" | tr '\n' ' ')
$visual-qa Check reference.png against $FRAMES — Goal: ..., Requirements: ..., Verify: ...
```

## Question Mode

For debugging and investigation — ask any question about screenshots without needing a reference image.

```text
$visual-qa Are any surfaces showing magenta or default grey material? screenshots/{task}/frame0005.png

$visual-qa Does the enemy patrol path form a loop? screenshots/{task}/frame0001.png screenshots/{task}/frame0010.png screenshots/{task}/frame0020.png

$visual-qa The door should open when player approaches. Does it? InteractionSystem triggers at 2m, door uses AnimationPlayer. screenshots/{task}/frame*.png
```

## Backend Selection

```text
# Gemini (`gemini-3-flash-preview`) default
$visual-qa Check reference.png against screenshots/{task}/frame00000003.png — Goal: ...

# Native image analysis
$visual-qa --native Check reference.png against screenshots/{task}/frame00000003.png — Goal: ...

# Both — aggregated verdict (stricter wins, issues merged)
$visual-qa --both Check reference.png against screenshots/{task}/frame00000003.png — Goal: ...
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
