#!/usr/bin/env python3
"""Generate a 1024x1024 sprite sheet template with 4x4 grid, numbered circles."""

import argparse
from PIL import Image, ImageDraw, ImageFont

GRID = 4
CELL = 256  # 1024 / 4
SIZE = GRID * CELL  # 1024
LINE_W = 2
CIRCLE_R = 40
FONT_SIZE = 36


def _colors_clash(a: str, b: str, threshold: int = 60) -> bool:
    a, b = a.lstrip("#"), b.lstrip("#")
    return all(abs(int(a[i:i+2], 16) - int(b[i:i+2], 16)) < threshold for i in (0, 2, 4))

def make_template(out: str, bg: str = "#1a1a1a", line_color: str = "#ff0000",
                  circle_color: str = "#ffffff", text_color: str = "#000000"):
    if _colors_clash(bg, line_color):
        line_color = "#0000ff"
        assert not _colors_clash(bg, line_color), f"BG {bg} clashes with both red and blue line colors"
    img = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(img)

    # Grid lines
    for i in range(1, GRID):
        x = i * CELL
        draw.line([(x, 0), (x, SIZE - 1)], fill=line_color, width=LINE_W)
        draw.line([(0, x), (SIZE - 1, x)], fill=line_color, width=LINE_W)

    # Border
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=line_color, width=LINE_W)

    # Try to load a decent font, fall back to default
    font = None
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]:
        try:
            font = ImageFont.truetype(path, FONT_SIZE)
            break
        except (OSError, IOError):
            continue
    if font is None:
        font = ImageFont.load_default()

    # Numbered circles in each cell center
    for row in range(GRID):
        for col in range(GRID):
            num = row * GRID + col + 1
            cx = col * CELL + CELL // 2
            cy = row * CELL + CELL // 2

            # Circle
            draw.ellipse(
                [cx - CIRCLE_R, cy - CIRCLE_R, cx + CIRCLE_R, cy + CIRCLE_R],
                fill=circle_color, outline=line_color, width=3
            )

            # Number centered in circle
            label = str(num)
            bbox = draw.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = cx - tw // 2
            ty = cy - th // 2 - (bbox[1])  # compensate for font ascent offset
            draw.text((tx, ty), label, fill=text_color, font=font)

    img.save(out)
    print(f"Saved {out} ({SIZE}x{SIZE}, {GRID}x{GRID} grid)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sprite sheet template generator")
    p.add_argument("-o", "--output", default="spritesheet_template.png")
    p.add_argument("--bg", default="#1a1a1a", help="Background color")
    p.add_argument("--line-color", default="#ff0000", help="Grid line color")
    p.add_argument("--circle-color", default="#ffffff", help="Circle fill color")
    p.add_argument("--text-color", default="#000000", help="Number text color")
    args = p.parse_args()
    make_template(args.output, args.bg, args.line_color, args.circle_color, args.text_color)
