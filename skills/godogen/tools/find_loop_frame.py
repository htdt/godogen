#!/usr/bin/env python3
"""Find the best loop point in a sequence of frames.

Compares all frames (after a skip window) to frame 1 using cosine similarity
of downscaled pixel embeddings. Prints the best matching frame number.

Usage:
    python3 find_loop_frame.py <frames_dir> [--skip 10] [--top 5]

Output (JSON to stdout):
    {"loop_frame": 27, "similarity": 0.9997, "total_frames": 73}
"""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


EMBED_SIZE = 32


def embed(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB").resize((EMBED_SIZE, EMBED_SIZE))
    v = np.array(img, dtype=np.float32).flatten()
    return v / (np.linalg.norm(v) + 1e-8)


def main():
    parser = argparse.ArgumentParser(description="Find best loop frame by similarity to first frame")
    parser.add_argument("frames_dir", help="Directory containing numbered frame PNGs")
    parser.add_argument("--skip", type=int, default=10, help="Skip first N frames (default: 10)")
    parser.add_argument("--top", type=int, default=5, help="Show top N matches (default: 5)")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    paths = sorted(frames_dir.glob("*.png"))
    if len(paths) < args.skip + 1:
        print(json.dumps({"error": f"Not enough frames ({len(paths)}) for skip={args.skip}"}))
        return

    ref = embed(paths[0])
    scores = []
    for p in paths[args.skip:]:
        sim = float(np.dot(ref, embed(p)))
        scores.append((p.name, sim))

    scores.sort(key=lambda x: -x[1])

    # Frame number from filename (1-indexed)
    best_name = scores[0][0]
    best_num = int(Path(best_name).stem.lstrip("0") or "0")

    print(json.dumps({
        "loop_frame": best_num,
        "similarity": round(scores[0][1], 4),
        "total_frames": len(paths),
    }))

    import sys
    for name, sim in scores[:args.top]:
        print(f"  {name}  cosine={sim:.4f}", file=sys.stderr)


if __name__ == "__main__":
    main()
