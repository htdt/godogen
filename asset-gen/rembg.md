# Background Removal

Matte a solid background out of frames that need transparency: video sprite frames, and GIF frames whose edges are too soft for 1-bit alpha.

Stills don't need it: `asset_gen.py image --transparent` and `qwen-image rgba` return real alpha. Never matte textures, backgrounds or 3D model references (Tripo needs the solid bg; `gen3d` removes it itself).

**Never prompt for a "transparent background" — a generator without a transparency flag draws a checkerboard. Prompt a solid color, then remove it.**

## BG color strategy

Pick a prompt bg color that is (1) **distinct from the subject** so the mask separates cleanly, and (2) **close to the expected in-game environment** so residual fringe blends. Forest → `dark-green`; sky/water → `steel-blue`; dungeon → `dark-gray`; generic → `medium-gray`. Avoid pure chromakey (`#00FF00`) — it leaves unnatural fringing.

```
{name}, {description}. Centered on a solid {bg_color} background.
```

## CLI

Deps in `${ASSET_GEN_SKILL_DIR}/tools/requirements.txt` (`pip install rembg[gpu,cli]`, or `rembg[cpu,cli]`). The script auto-detects CUDA and falls back to CPU with a warning.

```bash
# single frame
python3 ${ASSET_GEN_SKILL_DIR}/tools/rembg_matting.py frames/0001.png -o clean/0001.png --preview
# batch: BiRefNet loads once, bg sampled per-frame for color drift
python3 ${ASSET_GEN_SKILL_DIR}/tools/rembg_matting.py --batch frames/ -o clean/
```

## Modes

`-m auto` (default) selects by mask coverage:

| Mode | Auto when | Behavior |
|------|-----------|----------|
| `trust` | 5–70% mask fg | Keep all mask-fg pixels, aggressively remove bg |
| `adapt` | >70% mask fg | Adaptive threshold — fg pixels can be removed if bg-colored |
| `color` | <5% mask fg | Color matting only, no mask — rough fallback |

Output reports `BG color`, `Mask: fg=… (%)`, and the selected `Regime`. If the bg color is wrong (corners aren't bg) or `Transparent: 0`, regenerate the image with the subject centered on a solid bg.

## Preview

Alpha doesn't show in a raw PNG. `--preview` writes a `_qa.png` (the result composited on a contrasting color) so the matte can be seen; delete it afterwards.

## Fixing results

- **Background remnants** → `--bg-thresh 0.03` (lower = more aggressive; also reduces fringing).
- **Missing foreground** → `-m trust`, or in adapt `--fg-thresh 0.30` (higher = more protective).
- **Fringing** (colored halo) → `-m adapt --fg-thresh 0.10`; if it persists, the bg is too close to the subject — regenerate with a more distinct color.

Tune `--bg-thresh`/`--fg-thresh` together. For batches, tune on one frame, then apply the flags to the whole set.
