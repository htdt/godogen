# Background Removal

Background removal CLI, prompting strategy, troubleshooting, and batch mode. Read when you're about to generate or process an asset that needs transparency.

Applies to: characters, props, icons, UI elements, animated sprite frames.
Does NOT apply to: textures, backgrounds, 3D model references (Tripo3D needs the solid white bg).

**CRITICAL: Never prompt for "transparent background" — the generator draws a checkerboard. Always use a solid color background, then remove it.**

## BG color strategy

Pick a prompt bg color that is (1) **distinct from the subject** so the mask separates cleanly, and (2) **close to the expected in-game environment** so residual fringe blends naturally.

Examples: forest game → `dark-green`; sky/water → `steel-blue`; dungeon → `dark-gray`; generic → `medium-gray`.

Avoid pure chromakey colors like `#00FF00` — they create unnatural green fringing.

The prompt must include a solid flat background color. Without it, the generator draws a detailed/noisy background that the mask cannot cleanly separate:
```
{name}, {description}. Centered on a solid {bg_color} background.
```

## GPU acceleration

The script auto-detects NVIDIA GPUs and uses CUDA when available. If a GPU is present but CUDA deps are missing, it prints a clear warning and falls back to CPU.

Required for GPU:
```bash
pip install onnxruntime-gpu nvidia-cudnn-cu12==9.*
```

Verify CUDA is working:
```bash
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Should include 'CUDAExecutionProvider'
```

If the script warns about GPU detected but CUDA unavailable — install the deps above. CPU fallback works but is significantly slower, especially for batch processing.

## CLI

Dependencies in `${GODOGEN_SKILL_DIR}/tools/requirements.txt`. If rembg is not installed:
```bash
pip install rembg[gpu,cli]   # use rembg[cpu,cli] if no GPU
```

### Single image

```bash
python3 ${GODOGEN_SKILL_DIR}/tools/rembg_matting.py \
  assets/img/car.png -o assets/img/car_nobg.png --preview
```

### Batch (video frames)

```bash
python3 ${GODOGEN_SKILL_DIR}/tools/rembg_matting.py \
  --batch frames_dir/ -o clean_dir/
```

- BiRefNet session loads once (not per-frame)
- BG color sampled per-frame from corners — handles color drift across video
- Same flags apply to all frames

## Modes

`-m auto` (default) selects based on mask coverage:

| Mode | Auto when | Behavior |
|------|-----------|----------|
| `trust` | 5–70% mask fg | Keep all mask-fg pixels, aggressively remove bg |
| `adapt` | >70% mask fg | Adaptive threshold — fg pixels CAN be removed if bg-colored |
| `color` | <5% mask fg | Color matting only, no mask — rough fallback |

## Reading output

```
BG color: RGB(74, 106, 65)     ← sampled from corners
Mask: fg=52480 (20.0%)         ← mask coverage → mode selection
Regime: trust (bg_thresh=0.05) ← auto-selected mode + thresholds
```

**BG color wrong** (corners aren't bg) → regenerate image with subject centered on solid bg.

**Transparent: 0** in final stats → same cause, bg detection failed entirely.

## QA verification

Always pass `--preview` when removing backgrounds. This generates a `_qa.png` file — the transparent result composited on a contrasting solid color (white if the original bg was dark, black if light). Read the `_qa` image to check for remnants, fringing, or missing foreground. Delete the `_qa` file after inspection.

${AGENT_NAME} cannot evaluate transparency directly from the raw PNG alone — the preview is the only reliable way to visually verify the result.

## Fixing results

Read output PNG. Then:

**Background remnants** → `--bg-thresh 0.03` (lower = more aggressive). Also reduces fringing.

**Missing foreground** → `-m trust` (never removes mask-fg pixels). Or in adapt: `--fg-thresh 0.30` (higher = more protective).

**Fringing** (colored edge halo) → `-m adapt --fg-thresh 0.10` (lower = less protective of edges). Also try `--bg-thresh 0.03`. If persists, bg color too close to subject — regenerate with more distinct bg.

**Mask failed** (color mode) → result rough. Usually means source image needs regenerating.

Tune `--bg-thresh` and `--fg-thresh` together to trade off bg removal vs fg preservation.

For batch: tune on a single frame first, then apply flags to the full batch.
