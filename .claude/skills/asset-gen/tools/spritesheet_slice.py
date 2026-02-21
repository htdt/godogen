#!/usr/bin/env python3
"""Process a 4x4 sprite sheet for Godot: crop grid lines, optionally remove backgrounds.

Two modes:
  keep-bg:  crop red grid lines only, output clean sheet
  clean-bg: crop grid lines, run rembg_matting on each frame, reassemble
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

GRID = 4
LINE_W = 8  # pixels to crop from each cell edge (line is ~4px, extra margin for artifacts)
TOOLS_DIR = Path(__file__).parent
REMBG_SCRIPT = TOOLS_DIR / "rembg_matting.py"


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


def extract_frames(sheet: Image.Image) -> list[Image.Image]:
    """Split a clean sheet into 16 individual frame images."""
    w, h = sheet.size
    fw, fh = w // GRID, h // GRID
    frames = []
    for row in range(GRID):
        for col in range(GRID):
            x0, y0 = col * fw, row * fh
            frames.append(sheet.crop((x0, y0, x0 + fw, y0 + fh)))
    return frames


def reassemble(frames: list[Image.Image]) -> Image.Image:
    """Reassemble 16 frame images into a 4x4 sheet."""
    fw, fh = frames[0].size
    sheet = Image.new("RGBA", (fw * GRID, fh * GRID), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        row, col = divmod(i, GRID)
        sheet.paste(frame, (col * fw, row * fh))
    return sheet


def rembg_frame(input_path: Path, output_path: Path):
    """Run rembg_matting.py on a single frame."""
    subprocess.run(
        [sys.executable, str(REMBG_SCRIPT), str(input_path), "-o", str(output_path)],
        check=True,
    )


def process_sheet(src: Path, output: Path, clean: bool):
    sheet = Image.open(src).convert("RGBA")
    w, h = sheet.size
    cell_w, cell_h = w // GRID, h // GRID
    print(f"Sheet: {w}x{h}, cell: {cell_w}x{cell_h}")

    # Crop grid lines
    cleaned = crop_grid_lines(sheet)
    cw, ch = cleaned.size
    print(f"After grid crop: {cw}x{ch}, cell: {cw // GRID}x{ch // GRID}")

    if not clean:
        # keep-bg: just save the grid-cropped sheet
        output.parent.mkdir(parents=True, exist_ok=True)
        cleaned.save(output)
        print(f"Output: {output}")
        return

    # clean-bg: slice → rembg each frame → reassemble
    frames = extract_frames(cleaned)
    processed = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for i, frame in enumerate(frames):
            idx = i + 1
            in_path = tmp_dir / f"frame_{idx:02d}.png"
            out_path = tmp_dir / f"frame_{idx:02d}_clean.png"
            frame.save(in_path)
            print(f"  rembg frame {idx}/16...", end=" ", flush=True)
            rembg_frame(in_path, out_path)
            processed.append(Image.open(out_path).convert("RGBA"))
            print("done")

    result = reassemble(processed)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    print(f"Output: {output}")


def main():
    p = argparse.ArgumentParser(
        description="Process 4x4 sprite sheet: crop grid lines, optionally remove backgrounds")
    p.add_argument("mode", choices=["keep-bg", "clean-bg"],
                   help="keep-bg: crop grid lines only. clean-bg: also remove background per frame via rembg.")
    p.add_argument("input", help="Input sprite sheet image")
    p.add_argument("-o", "--output", required=True, help="Output sprite sheet PNG")
    args = p.parse_args()

    process_sheet(Path(args.input), Path(args.output), clean=(args.mode == "clean-bg"))


if __name__ == "__main__":
    main()
