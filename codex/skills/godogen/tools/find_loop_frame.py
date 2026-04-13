#!/usr/bin/env python3
"""Find the best loop point in a sequence of frames.

Finds top similarity candidates, deduplicates nearby frames (within
min_gap), then picks the most distant (latest) one — maximizing clip
length among high-quality matches.

Strategy:
  1. 7-frame window: rank by similarity, dedupe, pick latest
  2. Fallback to 1-frame if 7-window has no candidates
  3. Use whole clip if nothing scores well

Usage:
    python3 find_loop_frame.py <frames_dir> [--skip 10] [--top 10] [--min-gap 5]

Output (JSON to stdout):
    {"loop_frame": 54, "similarity": 0.9983, "window": 7, "total_frames": 73}
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


EMBED_SIZE = 32
MIN_SIM = 0.90
TOP_K = 10


def embed(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB").resize((EMBED_SIZE, EMBED_SIZE))
    v = np.array(img, dtype=np.float32).flatten()
    return v / (np.linalg.norm(v) + 1e-8)


def window_similarity(embeddings: list[np.ndarray], ref_start: int, candidate_start: int, window: int) -> float:
    total = 0.0
    for offset in range(window):
        total += float(np.dot(embeddings[ref_start + offset], embeddings[candidate_start + offset]))
    return total / window


def dedupe(candidates: list[tuple[int, float]], min_gap: int) -> list[tuple[int, float]]:
    """Keep highest-sim representative from each cluster of nearby frames."""
    if not candidates:
        return []
    # Sort by similarity descending
    by_sim = sorted(candidates, key=lambda c: -c[1])
    kept = []
    for idx, sim in by_sim:
        if all(abs(idx - k) >= min_gap for k, _ in kept):
            kept.append((idx, sim))
    return kept


def find_loop(embeddings: list[np.ndarray], skip: int, window: int, min_gap: int):
    """Find best loop point. Returns (index, similarity) or (None, 0)."""
    n = len(embeddings)
    first = skip + window
    last = n - window
    if first > last:
        return None, 0.0, []

    # Score all candidates
    all_candidates = []
    for start in range(first, last + 1):
        sim = window_similarity(embeddings, 0, start, window)
        all_candidates.append((start, sim))

    # Take top K by similarity
    top = sorted(all_candidates, key=lambda c: -c[1])[:TOP_K]

    # Deduplicate nearby frames
    peaks = dedupe(top, min_gap)

    if not peaks:
        return None, 0.0, []

    # Pick latest if its similarity is close to the top; otherwise prefer top sim
    top_sim = max(p[1] for p in peaks)
    latest = max(peaks, key=lambda c: c[0])
    if top_sim - latest[1] < 0.01:
        best = latest
    else:
        best = max(peaks, key=lambda c: c[1])
    return best[0], best[1], peaks


def main():
    parser = argparse.ArgumentParser(description="Find best loop frame")
    parser.add_argument("frames_dir", help="Directory containing numbered frame PNGs")
    parser.add_argument("--skip", type=int, default=10, help="Skip first N frames (default: 10)")
    parser.add_argument("--min-gap", type=int, default=5, help="Min frames between candidates (default: 5)")
    parser.add_argument("--top", type=int, default=5, help="Show top N in stderr (default: 5)")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    paths = sorted(frames_dir.glob("*.png"))
    if len(paths) < args.skip + 2:
        print(json.dumps({"error": f"Not enough frames ({len(paths)}) for skip={args.skip}"}))
        return

    embeddings = [embed(p) for p in paths]

    for window in (7, 1):
        idx, sim, peaks = find_loop(embeddings, args.skip, window, args.min_gap)

        if idx is not None and sim >= MIN_SIM:
            print(json.dumps({
                "loop_frame": idx + 1,
                "similarity": round(sim, 4),
                "window": window,
                "total_frames": len(paths),
            }))
            for i, (ci, cs) in enumerate(sorted(peaks, key=lambda c: -c[0])[:args.top]):
                tag = " <-- chosen" if ci == idx else ""
                print(f"  #{i+1} frame {ci+1}  sim={cs:.4f}{tag}", file=sys.stderr)
            return

    print(json.dumps({
        "loop_frame": len(paths),
        "similarity": 0.0,
        "window": 0,
        "total_frames": len(paths),
        "note": "no good loop point found, using whole clip",
    }))
    print("  No good loop candidates, using whole clip", file=sys.stderr)


if __name__ == "__main__":
    main()
