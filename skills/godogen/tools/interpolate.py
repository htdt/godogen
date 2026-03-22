#!/usr/bin/env python3
"""RIFE-based frame interpolation for sprite animation.

Takes a directory of keyframes, generates smooth in-between frames using
rife-ncnn-vulkan, outputs to a directory and optionally a GIF.

Usage:
  python3 interpolate.py frames_dir/ -o smooth_frames/ --mid 3
  python3 interpolate.py frames_dir/ -o smooth_frames/ --mid 3 --gif anim.gif --fps 18
"""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

RIFE_BIN = "rife-ncnn-vulkan"
RIFE_MODEL = "rife-v4.6"


def interpolate_pair(frame1: Path, frame2: Path, num_mid: int) -> list[Path]:
    """Generate intermediate frames between two keyframes."""
    mid_frames = []
    for i in range(1, num_mid + 1):
        t = i / (num_mid + 1)
        tmp = Path(tempfile.NamedTemporaryFile(suffix=".png", delete=False).name)
        result = subprocess.run(
            [RIFE_BIN, "-0", str(frame1), "-1", str(frame2),
             "-o", str(tmp), "-s", str(t), "-m", RIFE_MODEL],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  RIFE error (t={t:.2f}): {result.stderr}")
            continue
        mid_frames.append(tmp)
    return mid_frames


def interpolate_sequence(keyframes: list[Path], output_dir: Path,
                         num_mid: int = 3, gif_path: Path | None = None,
                         fps: int = 18):
    """Interpolate between sequential keyframes, save results."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_paths: list[Path] = []
    idx = 0

    for i, kf in enumerate(keyframes):
        # Copy keyframe
        out = output_dir / f"frame_{idx:04d}.png"
        shutil.copy2(kf, out)
        all_paths.append(out)
        idx += 1

        if i < len(keyframes) - 1:
            print(f"Interpolating {i+1} → {i+2}...")
            mid = interpolate_pair(kf, keyframes[i + 1], num_mid)
            for tmp in mid:
                out = output_dir / f"frame_{idx:04d}.png"
                shutil.move(str(tmp), out)
                all_paths.append(out)
                idx += 1

    print(f"Total frames: {len(all_paths)} ({len(keyframes)} keyframes + {len(all_paths) - len(keyframes)} interpolated)")

    if gif_path:
        frames = [Image.open(p) for p in all_paths]
        duration_ms = int(1000 / fps)
        frames[0].save(gif_path, save_all=True, append_images=frames[1:],
                       duration=duration_ms, loop=0)
        print(f"GIF: {gif_path}")


def main():
    p = argparse.ArgumentParser(
        description="RIFE frame interpolation for sprite keyframes")
    p.add_argument("input", help="Directory of keyframe PNGs (sorted alphabetically)")
    p.add_argument("-o", "--output", required=True, help="Output directory for interpolated frames")
    p.add_argument("--mid", type=int, default=3,
                   help="Interpolated frames between each keyframe pair (default: 3)")
    p.add_argument("--gif", help="Optional: also save as animated GIF")
    p.add_argument("--fps", type=int, default=18, help="GIF frame rate (default: 18)")
    args = p.parse_args()

    keyframes = sorted(Path(args.input).glob("*.png"))
    if len(keyframes) < 2:
        print(f"Need at least 2 keyframes, found {len(keyframes)}")
        return

    print(f"Keyframes: {len(keyframes)}, mid frames: {args.mid}")
    gif = Path(args.gif) if args.gif else None
    interpolate_sequence(keyframes, Path(args.output), num_mid=args.mid,
                         gif_path=gif, fps=args.fps)


if __name__ == "__main__":
    main()
