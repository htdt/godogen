#!/usr/bin/env python3
"""Generate a sprite sheet template with 4x4 grid, numbered circles, optional reference image in cell 1."""

import argparse
from PIL import Image, ImageDraw, ImageFont

GRID = 4


def _colors_clash(a: str, b: str, threshold: int = 60) -> bool:
    a, b = a.lstrip("#"), b.lstrip("#")
    return all(abs(int(a[i:i+2], 16) - int(b[i:i+2], 16)) < threshold for i in (0, 2, 4))


def make_template(out: str, bg: str = "#1a1a1a", line_color: str = "#ff0000",
                  circle_color: str = "#ffffff", text_color: str = "#000000",
                  size: int = 2048, reference: str | None = None):
    cell = size // GRID
    line_w = max(2, size // 512)
    circle_r = cell // 6
    font_size = max(16, cell // 7)

    if _colors_clash(bg, line_color):
        line_color = "#0000ff"
        assert not _colors_clash(bg, line_color), f"BG {bg} clashes with both red and blue line colors"

    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)

    # Paste reference image into cell 1 (before grid lines so lines draw on top)
    if reference:
        ref_img = Image.open(reference).convert("RGB")
        inner = cell - line_w * 2
        ref_img = ref_img.resize((inner, inner), Image.Resampling.LANCZOS)
        img.paste(ref_img, (line_w, line_w))

    # Grid lines
    for i in range(1, GRID):
        x = i * cell
        draw.line([(x, 0), (x, size - 1)], fill=line_color, width=line_w)
        draw.line([(0, x), (size - 1, x)], fill=line_color, width=line_w)

    # Border
    draw.rectangle([0, 0, size - 1, size - 1], outline=line_color, width=line_w)

    # Font
    font = None
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except (OSError, IOError):
            continue
    if font is None:
        font = ImageFont.load_default()

    # Numbered circles — skip cell 1 when reference is provided
    start = 1 if reference else 0
    for idx in range(start, GRID * GRID):
        row, col = divmod(idx, GRID)
        num = idx + 1
        cx = col * cell + cell // 2
        cy = row * cell + cell // 2

        draw.ellipse(
            [cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r],
            fill=circle_color, outline=line_color, width=max(2, line_w)
        )

        label = str(num)
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = cx - tw // 2
        ty = cy - th // 2 - bbox[1]
        draw.text((tx, ty), label, fill=text_color, font=font)

    img.save(out)
    print(f"Saved {out} ({size}x{size}, {GRID}x{GRID} grid)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sprite sheet template generator")
    p.add_argument("-o", "--output", default="spritesheet_template.png")
    p.add_argument("--bg", default="#1a1a1a", help="Background color")
    p.add_argument("--line-color", default="#ff0000", help="Grid line color")
    p.add_argument("--circle-color", default="#ffffff", help="Circle fill color")
    p.add_argument("--text-color", default="#000000", help="Number text color")
    p.add_argument("--size", type=int, default=2048, help="Template size in pixels (default: 2048)")
    p.add_argument("--reference", help="Reference image to embed in cell 1")
    args = p.parse_args()
    make_template(args.output, args.bg, args.line_color, args.circle_color, args.text_color,
                  args.size, args.reference)
