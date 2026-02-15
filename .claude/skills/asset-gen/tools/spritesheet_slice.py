#!/usr/bin/env python3
"""Clean a 4x4 sprite sheet: crop out grid lines, optionally remove BG color.

Primary output: a single sprite sheet for Godot (Sprite2D hframes=4 vframes=4).
Grid lines are removed by cropping at known positions (not color detection).
Optional: --gif for preview, --frames to also export individual PNGs.
"""

import argparse
from pathlib import Path

from PIL import Image
import numpy as np

GRID = 4
LINE_W = 6  # pixels to crop from each cell edge to remove grid lines


def crop_grid_lines(sheet: Image.Image, margin: int = LINE_W) -> Image.Image:
    """Crop grid lines by extracting cell interiors and reassembling."""
    w, h = sheet.size
    cell_w, cell_h = w // GRID, h // GRID
    inner_w = cell_w - 2 * margin
    inner_h = cell_h - 2 * margin

    out = Image.new("RGBA", (inner_w * GRID, inner_h * GRID), (0, 0, 0, 0))
    for row in range(GRID):
        for col in range(GRID):
            x0 = col * cell_w + margin
            y0 = row * cell_h + margin
            cell = sheet.crop((x0, y0, x0 + inner_w, y0 + inner_h))
            out.paste(cell, (col * inner_w, row * inner_h))
    return out


def remove_bg_color(img: Image.Image, hex_color: str, tolerance: int = 30) -> Image.Image:
    """Remove pixels matching a specific hex color (e.g. '#00FF00')."""
    hex_color = hex_color.lstrip("#")
    tr, tg, tb = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    rgba = img.convert("RGBA")
    data = np.array(rgba, dtype=np.int16)
    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    mask = (
        (np.abs(r - tr) < tolerance) &
        (np.abs(g - tg) < tolerance) &
        (np.abs(b - tb) < tolerance)
    )
    data[mask, 3] = 0
    return Image.fromarray(data.astype(np.uint8))


def clean_sheet(src: Path, output: Path, bg_color: str | None = None,
                frames_dir: Path | None = None,
                gif_path: Path | None = None, fps: int = 10):
    sheet = Image.open(src).convert("RGBA")
    w, h = sheet.size
    cell_w, cell_h = w // GRID, h // GRID
    print(f"Sheet: {w}x{h}, cell: {cell_w}x{cell_h}")

    # Crop grid lines by position
    cleaned = crop_grid_lines(sheet)
    cw, ch = cleaned.size
    inner_w, inner_h = cw // GRID, ch // GRID
    print(f"After grid crop: {cw}x{ch}, cell: {inner_w}x{inner_h}")

    # Optionally remove BG color
    if bg_color:
        cleaned = remove_bg_color(cleaned, bg_color)
        print(f"Removed BG color: {bg_color}")

    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.save(output)
    print(f"Output: {output}")

    # Optional: extract individual frames or GIF
    if frames_dir or gif_path:
        frames = []
        for row in range(GRID):
            for col in range(GRID):
                idx = row * GRID + col + 1
                x0, y0 = col * inner_w, row * inner_h
                cell = cleaned.crop((x0, y0, x0 + inner_w, y0 + inner_h))
                frames.append(cell)

                if frames_dir:
                    frames_dir.mkdir(parents=True, exist_ok=True)
                    cell.save(frames_dir / f"frame_{idx:02d}.png")

        if gif_path:
            gif_frames = []
            for f in frames:
                bg = Image.new("RGBA", f.size, (255, 255, 255, 255))
                bg.paste(f, mask=f)
                gif_frames.append(bg.convert("RGB"))

            gif_path.parent.mkdir(parents=True, exist_ok=True)
            gif_frames[0].save(
                gif_path, save_all=True, append_images=gif_frames[1:],
                duration=1000 // fps, loop=0,
            )
            print(f"GIF: {gif_path} ({len(gif_frames)} frames, {fps} fps)")


def main():
    p = argparse.ArgumentParser(description="Clean 4x4 sprite sheet: crop grid lines, optionally remove BG")
    p.add_argument("input", help="Input sprite sheet image")
    p.add_argument("-o", "--output", required=True, help="Output cleaned sprite sheet PNG")
    p.add_argument("--remove-bg", default=None, metavar="COLOR",
                   help="Hex color to remove (e.g. '#00FF00'). If omitted, BG is kept as-is.")
    p.add_argument("--frames", default=None, help="Also export individual frames to this directory")
    p.add_argument("--gif", default=None, help="Also export animated GIF for preview")
    p.add_argument("--fps", type=int, default=10, help="GIF frame rate")
    args = p.parse_args()
    clean_sheet(
        Path(args.input), Path(args.output), args.remove_bg,
        Path(args.frames) if args.frames else None,
        Path(args.gif) if args.gif else None,
        args.fps,
    )


if __name__ == "__main__":
    main()
