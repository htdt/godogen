#!/usr/bin/env python3
"""Slice a grid image into individual PNGs.

Usage:
    python3 grid_slice.py <input> -o <output_dir> [--grid 2x2] [--names "sword,shield,potion,helm"]

Output: individual PNGs saved to output_dir, named 01.png..N.png or by --names.
"""

import argparse
import json
from pathlib import Path

from PIL import Image


def slice_grid(src: Path, output_dir: Path, cols: int, rows: int, names: list[str] | None):
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    cell_w, cell_h = w // cols, h // rows
    output_dir.mkdir(parents=True, exist_ok=True)

    total = cols * rows
    if names and len(names) != total:
        print(json.dumps({"ok": False, "error": f"--names has {len(names)} entries, grid is {total} cells"}))
        return

    paths = []
    for i in range(total):
        row, col = divmod(i, cols)
        x0, y0 = col * cell_w, row * cell_h
        cell = img.crop((x0, y0, x0 + cell_w, y0 + cell_h))
        name = names[i] if names else f"{i + 1:02d}"
        path = output_dir / f"{name}.png"
        cell.save(path)
        paths.append(str(path))

    print(json.dumps({"ok": True, "cells": total, "cell_size": f"{cell_w}x{cell_h}", "paths": paths}))


def main():
    p = argparse.ArgumentParser(description="Slice grid image into individual PNGs")
    p.add_argument("input", help="Input grid image")
    p.add_argument("-o", "--output", required=True, help="Output directory")
    p.add_argument("--grid", default="2x2", help="Grid layout, e.g. 2x2, 3x3, 2x4 (ColsxRows). Default: 2x2")
    p.add_argument("--names", default=None, help="Comma-separated names (without .png). Default: 01, 02, ...")
    args = p.parse_args()

    cols, rows = (int(x) for x in args.grid.lower().split("x"))
    names = [n.strip() for n in args.names.split(",")] if args.names else None
    slice_grid(Path(args.input), Path(args.output), cols, rows, names)


if __name__ == "__main__":
    main()
