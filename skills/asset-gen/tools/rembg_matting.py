"""Remove solid-color background from images using rembg mask + alpha matting.

Uses three alpha signals merged with a single rule:
  - Color-based physical lower bound (works everywhere)
  - Pymatting closed-form on mask edge band (smooth transitions)
  - Blurred mask floor (preserves small mask-detected elements)

bg-colored pixels → trust color; everything else → max of all signals.
"""

import argparse
from pathlib import Path

import numpy as np
import pymatting
from PIL import Image
from rembg import remove, new_session
from scipy.ndimage import binary_dilation, binary_erosion, gaussian_filter

BG_THRESH = 0.10


def sample_bg_color(img: np.ndarray, block: int = 2) -> np.ndarray:
    """Average color from 2x2 blocks at all 4 corners (16 pixels)."""
    corners = np.concatenate([
        img[:block, :block].reshape(-1, 3),
        img[:block, -block:].reshape(-1, 3),
        img[-block:, :block].reshape(-1, 3),
        img[-block:, -block:].reshape(-1, 3),
    ])
    return corners.mean(axis=0)


def compute_alpha_color(img: np.ndarray, bg_color: np.ndarray) -> np.ndarray:
    """Physical lower bound on alpha from compositing equation.

    pixel = alpha * fg + (1-alpha) * bg, with fg constrained to [0,1].
    Skips channels where bg is near 0 or 1 to avoid division instability.
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


def build_trimap(mask: np.ndarray, alpha_color: np.ndarray,
                 band_px: int) -> tuple[np.ndarray, np.ndarray]:
    """Build trimap from mask with color-guided unknown band.

    Returns (trimap, definite_fg).
    """
    definite_fg = binary_erosion(mask, iterations=band_px)
    bg_boundary = binary_dilation(mask, iterations=band_px)

    trimap = np.full(mask.shape, 0.5, dtype=np.float64)
    trimap[definite_fg] = 1.0
    trimap[~bg_boundary] = 0.0
    unknown = (trimap > 0) & (trimap < 1)
    trimap[unknown] = np.clip(alpha_color[unknown], 0.05, 0.95)

    return trimap, definite_fg


def recover_foreground(img: np.ndarray, alpha: np.ndarray,
                       bg_color: np.ndarray) -> np.ndarray:
    """Undo background compositing: fg = (pixel - (1-a)*bg) / a."""
    a = alpha[:, :, np.newaxis]
    bg = bg_color[np.newaxis, np.newaxis, :]
    safe_a = np.where(a > 0.02, a, 1.0)
    fg = np.clip((img - (1.0 - a) * bg) / safe_a, 0.0, 1.0)
    fg[alpha < 0.02] = 0.0
    return fg


def remove_background(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Remove solid background, returning RGBA uint8 array."""
    h, w = img.shape[:2]
    dim = min(h, w)

    bg_color = sample_bg_color(img)
    print(f"BG color: RGB({bg_color[0]*255:.0f}, {bg_color[1]*255:.0f}, {bg_color[2]*255:.0f})")

    # --- Three alpha signals ---

    # 1. Color-based physical lower bound
    alpha_color = compute_alpha_color(img, bg_color)

    # 2. Pymatting on mask edge band (color-guided for smooth transitions)
    band_px = max(3, round(dim * 0.02))
    trimap, definite_fg = build_trimap(mask, alpha_color, band_px)
    print(f"Trimap: band={band_px}px, unknown={((trimap > 0) & (trimap < 1)).sum()}")
    if definite_fg.any():
        print("Running pymatting (closed-form)...")
        alpha_matted = np.clip(pymatting.estimate_alpha_cf(img, trimap), 0.0, 1.0)
    else:
        print("No foreground in mask — skipping pymatting, using color-only alpha")
        alpha_matted = alpha_color

    # 3. Heavily blurred mask floor (preserves small elements, smooth edges)
    blur_sigma = max(1.0, dim * 0.012)
    mask_floor = gaussian_filter(mask.astype(np.float64), sigma=blur_sigma)

    # --- Merge ---
    mask_has_fg = definite_fg.any()
    if mask_has_fg:
        is_bg = alpha_color < BG_THRESH
        alpha = np.where(
            is_bg,
            alpha_color,
            np.maximum(np.maximum(alpha_matted, alpha_color), mask_floor),
        )
        alpha[definite_fg & ~is_bg] = 1.0
        alpha[alpha < 0.01] = 0.0
    else:
        # Mask failed — use color distance (not compositing math) for alpha
        dist = np.sqrt(np.sum((img - bg_color[None, None, :]) ** 2, axis=2))

        # Noise floor from corner regions (known background)
        corner = max(4, dim // 16)
        corner_dist = np.concatenate([
            dist[:corner, :corner].ravel(),
            dist[:corner, -corner:].ravel(),
            dist[-corner:, :corner].ravel(),
            dist[-corner:, -corner:].ravel(),
        ])
        noise = max(float(np.percentile(corner_dist, 99)), 0.03)
        low = noise * 1.5   # below → fully transparent
        high = noise * 4.0  # above → fully opaque
        print(f"Color distance: noise={noise:.3f}, low={low:.3f}, high={high:.3f}")
        alpha = np.clip((dist - low) / (high - low), 0.0, 1.0)

    # --- Foreground recovery & output ---
    if mask_has_fg:
        fg = recover_foreground(img, alpha, bg_color)
    else:
        # No mask — glow/color is intentional paint, not compositing artifact
        fg = img.copy()
        fg[alpha < 0.01] = 0.0

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[:, :, :3] = (fg * 255).clip(0, 255).astype(np.uint8)
    out[:, :, 3] = (alpha * 255).clip(0, 255).astype(np.uint8)
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Remove solid-color background using rembg + alpha matting")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output PNG path (default: <input>_nobg.png)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_stem(input_path.stem + "_nobg")

    # Load
    img_pil = Image.open(input_path).convert("RGBA")
    img = np.array(img_pil.convert("RGB"), dtype=np.float64) / 255.0
    h, w = img.shape[:2]
    print(f"Image: {w}x{h} ({input_path})")

    # Mask from rembg
    session = new_session("isnet-anime")
    mask_pil = remove(img_pil, session=session, only_mask=True, post_process_mask=True)
    mask = np.array(mask_pil, dtype=np.float64) / 255.0 > 0.5
    print(f"Mask: fg={mask.sum()}, bg={(~mask).sum()}")

    # Process
    out = remove_background(img, mask)

    # Save
    Image.fromarray(out).save(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Opaque: {(out[:,:,3] == 255).sum()}")
    print(f"  Transparent: {(out[:,:,3] == 0).sum()}")
    print(f"  Semi-transparent: {((out[:,:,3] > 0) & (out[:,:,3] < 255)).sum()}")



if __name__ == "__main__":
    main()
