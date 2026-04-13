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
import shutil
import subprocess
import sys
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


def _has_nvidia_gpu() -> bool:
    """Check if an NVIDIA GPU is present via nvidia-smi."""
    if not shutil.which("nvidia-smi"):
        return False
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=5)
        return r.returncode == 0 and bool(r.stdout.strip())
    except Exception:
        return False


def _check_cuda_available() -> bool:
    """Check if onnxruntime can actually use CUDA."""
    try:
        import onnxruntime as ort
        return "CUDAExecutionProvider" in ort.get_available_providers()
    except Exception:
        return False


def create_session(model: str = "birefnet-general"):
    """Create a rembg session with GPU acceleration when available.

    Tries CUDA first, falls back to CPU. Warns loudly if GPU is present
    but CUDA providers are missing (missing deps).
    """
    has_gpu = _has_nvidia_gpu()
    cuda_ok = _check_cuda_available() if has_gpu else False

    if has_gpu and cuda_ok:
        print("rembg: using GPU (CUDAExecutionProvider)", file=sys.stderr)
        return new_session(model, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])

    if has_gpu and not cuda_ok:
        print(
            "\n"
            "WARNING: NVIDIA GPU detected but CUDA is not available for rembg/onnxruntime.\n"
            "  Background removal will run on CPU (much slower).\n"
            "  To fix, install GPU dependencies:\n"
            "    pip install onnxruntime-gpu nvidia-cudnn-cu12==9.*\n"
            "  Then verify:\n"
            "    python -c \"import onnxruntime; print(onnxruntime.get_available_providers())\"\n"
            "  Expected output should include 'CUDAExecutionProvider'.\n",
            file=sys.stderr,
        )

    # CPU fallback
    print("rembg: using CPU", file=sys.stderr)
    return new_session(model, providers=["CPUExecutionProvider"])


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


def get_soft_mask(img_pil: Image.Image, session=None) -> np.ndarray:
    """Get soft mask from BiRefNet (0-1 float, not binary)."""
    if session is None:
        session = create_session("birefnet-general")
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
                      fg_thresh: float | None = None,
                      session=None,
                      bg_color_override: np.ndarray | None = None) -> np.ndarray:
    """Remove solid background, returning RGBA uint8 array.

    Regimes:
      trust — mask is good: keep all fg (mask_soft > 0.5 never removed),
              aggressively remove bg
      adapt — mask imperfect: adaptive threshold interpolated by mask,
              fg pixels protected but bg-colored ones can be removed
      color — mask failed: color matting only with fixed threshold
    """
    h, w = img.shape[:2]

    # 1. Background color from corners (or override for batch consistency)
    bg_color = bg_color_override if bg_color_override is not None else sample_bg_color(img)
    print(f"BG color: RGB({bg_color[0]*255:.0f}, {bg_color[1]*255:.0f}, {bg_color[2]*255:.0f})")

    # 2. Color matting
    alpha_color = compute_alpha_color(img, bg_color)

    # 3. Soft mask from BiRefNet
    mask_soft = get_soft_mask(img_pil, session=session)
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
        is_bg = (alpha_color < bt) | (mask_soft < 0.05)
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


def make_qa_preview(rgba: np.ndarray, output_path: Path,
                    bg_color: np.ndarray) -> Path:
    """Composite RGBA on a contrasting solid color for visual QA.

    Picks white or black — whichever contrasts more with the original bg.
    """
    lum = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]
    qa_rgb = (0, 0, 0) if lum > 0.5 else (255, 255, 255)

    img_rgba = Image.fromarray(rgba)
    bg_layer = Image.new("RGBA", img_rgba.size, qa_rgb + (255,))
    bg_layer.paste(img_rgba, mask=img_rgba.split()[3])
    preview_path = output_path.with_stem(output_path.stem + "_qa")
    bg_layer.convert("RGB").save(preview_path)
    return preview_path


def process_batch(input_dir: Path, output_dir: Path, regime: str = "auto",
                  bg_thresh: float | None = None, fg_thresh: float | None = None):
    """Process all PNGs in input_dir with shared BiRefNet session and BG color."""
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = sorted(input_dir.glob("*.png"))
    if not frames:
        print("No PNG files found", file=sys.stderr)
        sys.exit(1)

    session = create_session("birefnet-general")
    print(f"Processing {len(frames)} frames...")

    for i, frame_path in enumerate(frames):
        img_pil = Image.open(frame_path).convert("RGBA")
        img = np.array(img_pil.convert("RGB"), dtype=np.float64) / 255.0
        out = remove_background(img, img_pil, regime=regime,
                                bg_thresh=bg_thresh, fg_thresh=fg_thresh,
                                session=session)
        out_path = output_dir / frame_path.name
        Image.fromarray(out).save(out_path)
        print(f"  [{i+1}/{len(frames)}] {out_path.name}", file=sys.stderr)

    print(f"\nBatch complete: {len(frames)} frames → {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove solid-color background using color matting + BiRefNet mask")
    parser.add_argument("input", nargs="?", help="Input image path (single mode)")
    parser.add_argument("-o", "--output", help="Output path (file for single, directory for batch)")
    parser.add_argument("--batch", metavar="DIR",
                        help="Batch mode: process all PNGs in DIR")
    parser.add_argument("-m", "--mode", choices=["auto", "trust", "adapt", "color"],
                        default="auto", help="Regime: auto, trust, adapt, color")
    parser.add_argument("--bg-thresh", type=float, default=None,
                        help="Background threshold override")
    parser.add_argument("--fg-thresh", type=float, default=None,
                        help="Foreground threshold override")
    parser.add_argument("--preview", action="store_true",
                        help="Generate QA preview on contrasting solid bg")
    args = parser.parse_args()

    if args.batch:
        if not args.output:
            print("Error: --batch requires -o OUTPUT_DIR", file=sys.stderr)
            sys.exit(1)
        process_batch(Path(args.batch), Path(args.output), regime=args.mode,
                      bg_thresh=args.bg_thresh, fg_thresh=args.fg_thresh)
        return

    if not args.input:
        parser.error("input is required in single mode (or use --batch DIR)")

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

    # QA preview: composite on contrasting solid bg for visual inspection
    if args.preview:
        preview_path = make_qa_preview(out, output_path, bg_color)
        print(f"  QA preview: {preview_path}")


if __name__ == "__main__":
    main()
