# Background Removal Guide

Always read after running `rembg_matting.py`. Auto mode works most of the time — use this to verify and fix.

## Modes

`-m auto` (default) selects based on mask coverage:

| Mode | Auto when | Behavior |
|------|-----------|----------|
| `trust` | 5–70% mask fg | Keep all mask-fg pixels, aggressively remove bg |
| `adapt` | >70% mask fg | Adaptive threshold — fg pixels CAN be removed if bg-colored |
| `color` | <5% mask fg | Color matting only, no mask — rough fallback |

## Output

```
BG color: RGB(74, 106, 65)     ← sampled from corners
Mask: fg=52480 (20.0%)         ← mask coverage → mode selection
Regime: trust (bg_thresh=0.05) ← auto-selected mode + thresholds
```

**BG color wrong** (corners aren't bg) → regenerate image with subject centered on solid bg.

**Transparent: 0** in final stats → same cause, bg detection failed entirely.

## Fixing results

Read output PNG. Then:

**Background remnants** → `--bg-thresh 0.03` (lower = more aggressive). Also reduces fringing.

**Missing foreground** → `-m trust` (never removes mask-fg pixels). Or in adapt: `--fg-thresh 0.30` (higher = more protective).

**Fringing** (colored edge halo) → `-m adapt --fg-thresh 0.10` (lower = less protective of edges). Also try `--bg-thresh 0.03`. If persists, bg color too close to subject — regenerate with more distinct bg.

**Mask failed** (color mode) → result rough. Usually means source image needs regenerating.

Tune `--bg-thresh` and `--fg-thresh` together to trade off bg removal vs fg preservation.
