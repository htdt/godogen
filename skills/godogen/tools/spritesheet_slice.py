#!/usr/bin/env python3
"""Process a 4x4 sprite sheet for Godot: crop grid lines, optionally remove backgrounds.

Modes:
  keep-bg:    crop grid lines, output clean sheet (animation)
  clean-bg:   crop grid lines, batch rembg all frames, reassemble sheet (animation)
  split-bg:   crop grid lines, save 16 individual PNGs with background (items/objects)
  split-clean: crop grid lines, batch rembg all frames, save 16 individual PNGs (items/objects)
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

GRID = 4
TOOLS_DIR = Path(__file__).parent
REMBG_SCRIPT = TOOLS_DIR / "rembg_matting.py"


def crop_grid_lines(sheet: Image.Image, margin: int) -> Image.Image:
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
    """Reassemble frame images into a 4x4 sheet."""
    fw, fh = frames[0].size
    sheet = Image.new("RGBA", (fw * GRID, fh * GRID), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        row, col = divmod(i, GRID)
        sheet.paste(frame, (col * fw, row * fh))
    return sheet


def rembg_batch(input_dir: Path, output_dir: Path):
    """Run rembg_matting.py in batch mode."""
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(REMBG_SCRIPT), "--batch", str(input_dir),
         "-o", str(output_dir)],
        check=True,
    )


def save_split(frames: list[Image.Image], output_dir: Path, names: list[str] | None):
    """Save frames as individual PNGs into output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, frame in enumerate(frames):
        name = names[i] if names else f"{i + 1:02d}"
        path = output_dir / f"{name}.png"
        frame.save(path)
        print(f"  {path}")


def process_sheet(src: Path, output: Path, mode: str, names: list[str] | None,
                  drop_first: bool = False):
    sheet = Image.open(src).convert("RGBA")
    w, h = sheet.size
    cell_w, cell_h = w // GRID, h // GRID
    margin = max(4, cell_w // 64)
    print(f"Sheet: {w}x{h}, cell: {cell_w}x{cell_h}, crop margin: {margin}px")

    cleaned = crop_grid_lines(sheet, margin=margin)
    cw, ch = cleaned.size
    print(f"After grid crop: {cw}x{ch}, cell: {cw // GRID}x{ch // GRID}")

    if mode == "keep-bg":
        output.parent.mkdir(parents=True, exist_ok=True)
        cleaned.save(output)
        print(f"Output: {output}")
        return

    frames = extract_frames(cleaned)

    if drop_first:
        print("Dropping cell 1 (reference)")
        frames = frames[1:]

    if mode == "split-bg":
        save_split(frames, output, names)
        return

    # clean-bg / split-clean: batch rembg
    with tempfile.TemporaryDirectory() as tmp:
        in_dir = Path(tmp) / "in"
        out_dir = Path(tmp) / "out"
        in_dir.mkdir()

        for i, frame in enumerate(frames):
            frame.save(in_dir / f"{i + 1:02d}.png")

        print(f"Batch rembg on {len(frames)} frames...")
        rembg_batch(in_dir, out_dir)

        processed = []
        for i in range(len(frames)):
            processed.append(Image.open(out_dir / f"{i + 1:02d}.png").convert("RGBA"))

    if mode == "split-clean":
        save_split(processed, output, names)
    else:
        result = reassemble(processed)
        output.parent.mkdir(parents=True, exist_ok=True)
        result.save(output)
        print(f"Output: {output}")


def parse_names(names_str: str, count: int = 16) -> list[str]:
    """Parse comma-separated names into a list of filenames."""
    names = [n.strip() for n in names_str.split(",")]
    if len(names) != count:
        print(f"Error: --names must have exactly {count} entries, got {len(names)}", file=sys.stderr)
        sys.exit(1)
    return names


def main():
    p = argparse.ArgumentParser(
        description="Process 4x4 sprite sheet: crop grid lines, optionally remove backgrounds or split into individual images")
    p.add_argument("mode", choices=["keep-bg", "clean-bg", "split-bg", "split-clean"],
                   help="keep-bg/clean-bg: output single sheet. split-bg/split-clean: output 16 individual PNGs.")
    p.add_argument("input", help="Input sprite sheet image")
    p.add_argument("-o", "--output", required=True,
                   help="Output PNG path (keep-bg/clean-bg) or output directory (split-bg/split-clean)")
    p.add_argument("--keep-first", action="store_true",
                   help="Keep cell 1 in output. By default cell 1 (reference) is dropped.")
    p.add_argument("--names", default=None,
                   help="Comma-separated filenames (without .png) for split modes. Default: 01..N")
    args = p.parse_args()

    names = parse_names(args.names) if args.names else None
    process_sheet(Path(args.input), Path(args.output), mode=args.mode, names=names,
                  drop_first=not args.keep_first)


if __name__ == "__main__":
    main()
