"""Remove solid-color background using color matting + BiRefNet soft mask.

Three regimes based on mask quality:
  trust   — mask looks good: keep all fg, aggressively remove bg
  adapt   — mask too big/small: adaptive threshold for both fg and bg
  color   — mask failed: remove bg color with fixed threshold, no mask

Usage:
  python rembg_matting.py image.png                    # auto-detect regime
  python rembg_matting.py image.png -m trust           # force regime
  python rembg_matting.py image.png -o out.png         # custom output path
  python rembg_matting.py image.png --bg-thresh 0.08   # tune thresholds
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from rembg import remove, new_session

# Mask coverage thresholds for regime auto-detection
MASK_MIN_PCT = 5.0    # below this % → mask failed
MASK_MAX_PCT = 70.0   # above this % → mask too big (bg leak)
MASK_MIN_PX = 100     # absolute minimum fg pixels

# Default thresholds per regime
DEFAULTS = {
    "trust": {"bg_thresh": 0.05, "fg_thresh": 1.0},   # keep all fg
    "adapt": {"bg_thresh": 0.05, "fg_thresh": 0.20},   # adaptive
    "color": {"bg_thresh": 0.10, "fg_thresh": 0.10},   # uniform
}


def sample_bg_color(img: np.ndarray, block: int = 2) -> np.ndarray:
    """Average color from 2x2 blocks at all 4 corners."""
    corners = np.concatenate([
        img[:block, :block].reshape(-1, 3),
        img[:block, -block:].reshape(-1, 3),
        img[-block:, :block].reshape(-1, 3),
        img[-block:, -block:].reshape(-1, 3),
    ])
    return corners.mean(axis=0)


def compute_alpha_color(img: np.ndarray, bg_color: np.ndarray) -> np.ndarray:
    """Physical lower bound on alpha from compositing equation.

    pixel = alpha * fg + (1-alpha) * bg, with fg in [0,1].
    """
    diff = img - bg_color[None, None, :]
    alpha = np.zeros(img.shape[:2], dtype=np.float64)
    for c in range(3):
        if 1.0 - bg_color[c] > 0.05:
            alpha = np.maximum(alpha,
                np.maximum(diff[:, :, c], 0) / (1.0 - bg_color[c]))
        if bg_color[c] > 0.05:
            alpha = np.maximum(alpha,
                np.maximum(-diff[:, :, c], 0) / bg_color[c])
    return np.clip(alpha, 0.0, 1.0)


def get_soft_mask(img_pil: Image.Image) -> np.ndarray:
    """Get soft mask from BiRefNet (0-1 float, not binary)."""
    session = new_session("birefnet-general")
    mask_pil = remove(img_pil, session=session, only_mask=True,
                      post_process_mask=False)
    return np.array(mask_pil, dtype=np.float64) / 255.0


def recover_foreground(img: np.ndarray, alpha: np.ndarray,
                       bg_color: np.ndarray) -> np.ndarray:
    """Undo background compositing: fg = (pixel - (1-a)*bg) / a."""
    a = alpha[:, :, np.newaxis]
    bg = bg_color[np.newaxis, np.newaxis, :]
    safe_a = np.where(a > 0.02, a, 1.0)
    fg = np.clip((img - (1.0 - a) * bg) / safe_a, 0.0, 1.0)
    fg[alpha < 0.02] = 0.0
    return fg


def detect_regime(mask_soft: np.ndarray) -> str:
    """Auto-detect regime from mask coverage."""
    mask_fg = (mask_soft > 0.5).sum()
    pct = mask_fg / mask_soft.size * 100

    if mask_fg < MASK_MIN_PX or pct < MASK_MIN_PCT:
        return "color"
    elif pct > MASK_MAX_PCT:
        return "adapt"
    else:
        return "trust"


def remove_background(img: np.ndarray, img_pil: Image.Image,
                      regime: str = "auto",
                      bg_thresh: float | None = None,
                      fg_thresh: float | None = None) -> np.ndarray:
    """Remove solid background, returning RGBA uint8 array.

    Regimes:
      trust — mask is good: keep all fg (mask_soft > 0.5 never removed),
              aggressively remove bg
      adapt — mask imperfect: adaptive threshold interpolated by mask,
              fg pixels protected but bg-colored ones can be removed
      color — mask failed: color matting only with fixed threshold
    """
    h, w = img.shape[:2]

    # 1. Background color from corners
    bg_color = sample_bg_color(img)
    print(f"BG color: RGB({bg_color[0]*255:.0f}, {bg_color[1]*255:.0f}, {bg_color[2]*255:.0f})")

    # 2. Color matting
    alpha_color = compute_alpha_color(img, bg_color)

    # 3. Soft mask from BiRefNet
    mask_soft = get_soft_mask(img_pil)
    mask_fg = (mask_soft > 0.5).sum()
    mask_pct = mask_fg / mask_soft.size * 100
    print(f"Mask: fg={mask_fg} ({mask_pct:.1f}%)")

    # 4. Regime selection
    if regime == "auto":
        regime = detect_regime(mask_soft)
    bt = bg_thresh if bg_thresh is not None else DEFAULTS[regime]["bg_thresh"]
    ft = fg_thresh if fg_thresh is not None else DEFAULTS[regime]["fg_thresh"]
    print(f"Regime: {regime} (bg_thresh={bt}, fg_thresh={ft})")

    # 5. Compute alpha
    if regime == "color":
        # No usable mask — color only
        is_bg = alpha_color < bt
        alpha = alpha_color

    elif regime == "trust":
        # Trust mask fully: never remove fg pixels (mask > 0.5)
        is_bg = (alpha_color < bt) & (mask_soft < 0.5)
        alpha = np.where(is_bg, alpha_color,
                         np.maximum(alpha_color, mask_soft))

    else:  # adapt
        # Adaptive threshold, but fg pixels CAN be removed if very bg-colored
        thresh = bt + mask_soft * (ft - bt)
        is_bg = alpha_color < thresh
        alpha = np.where(is_bg, alpha_color,
                         np.maximum(alpha_color, mask_soft))

    alpha[alpha < 0.01] = 0.0

    # 6. Foreground recovery
    fg = recover_foreground(img, alpha, bg_color)

    # 7. Output RGBA
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[:, :, :3] = (fg * 255).clip(0, 255).astype(np.uint8)
    out[:, :, 3] = (alpha * 255).clip(0, 255).astype(np.uint8)
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Remove solid-color background using color matting + BiRefNet mask")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output PNG path (default: <input>_nobg.png)")
    parser.add_argument("-m", "--mode", choices=["auto", "trust", "adapt", "color"],
                        default="auto", help="Regime: auto, trust, adapt, color")
    parser.add_argument("--bg-thresh", type=float, default=None,
                        help="Background threshold override")
    parser.add_argument("--fg-thresh", type=float, default=None,
                        help="Foreground threshold override")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else \
        input_path.with_stem(input_path.stem + "_nobg")

    # Load
    img_pil = Image.open(input_path).convert("RGBA")
    img = np.array(img_pil.convert("RGB"), dtype=np.float64) / 255.0
    h, w = img.shape[:2]
    print(f"Image: {w}x{h} ({input_path})")

    # Process
    out = remove_background(img, img_pil, regime=args.mode,
                            bg_thresh=args.bg_thresh, fg_thresh=args.fg_thresh)

    # Save
    Image.fromarray(out).save(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Opaque: {(out[:,:,3] == 255).sum()}")
    print(f"  Transparent: {(out[:,:,3] == 0).sum()}")
    print(f"  Semi-transparent: {((out[:,:,3] > 0) & (out[:,:,3] < 255)).sum()}")


if __name__ == "__main__":
    main()
