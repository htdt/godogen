#!/usr/bin/env python3
"""Asset Generator CLI - creates images (Gemini/OpenAI gpt-image-1) and GLBs (Tripo3D).

Subcommands:
  image        Generate a PNG from a prompt (5-15 cents depending on size)
  spritesheet  Generate a 4x4 sprite sheet with template (7 cents)
  glb          Convert a PNG to a GLB 3D model via Tripo3D (30-40 cents)

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types
from openai import OpenAI

from tripo3d import MODEL_V3, image_to_glb

TOOLS_DIR = Path(__file__).parent
TEMPLATE_SCRIPT = TOOLS_DIR / "spritesheet_template.py"
BUDGET_FILE = Path("assets/budget.json")


def _load_budget():
    if not BUDGET_FILE.exists():
        return None
    return json.loads(BUDGET_FILE.read_text())


def _spent_total(budget):
    return sum(v for entry in budget.get("log", []) for v in entry.values())


def check_budget(cost_cents: int):
    """Check remaining budget. Exit with error JSON if insufficient."""
    budget = _load_budget()
    if budget is None:
        return
    spent = _spent_total(budget)
    remaining = budget.get("budget_cents", 0) - spent
    if cost_cents > remaining:
        result_json(False, error=f"Budget exceeded: need {cost_cents}¢ but only {remaining}¢ remaining ({spent}¢ of {budget['budget_cents']}¢ spent)")
        sys.exit(1)


def record_spend(cost_cents: int, service: str):
    """Append a generation record to the budget log."""
    budget = _load_budget()
    if budget is None:
        return
    budget.setdefault("log", []).append({service: cost_cents})
    BUDGET_FILE.write_text(json.dumps(budget, indent=2) + "\n")

SPRITESHEET_SYSTEM_TPL = """\
Using the attached template image as an exact layout guide: generate a sprite sheet.
The image is a 4x4 grid of 16 equal cells separated by red lines.
Replace each numbered cell with the corresponding content, reading left-to-right, top-to-bottom (cell 1 = first, cell 16 = last).

Rules:
- KEEP the red grid lines exactly where they are in the template — do not remove, shift, or paint over them
- Each cell's content must be CENTERED in its cell and must NOT cross into adjacent cells
- CRITICAL: fill ALL empty space in every cell with flat solid {bg_color} — no gradients, no scenery, no patterns, just the plain color
- Maintain consistent style, lighting direction, and proportions across all 16 cells
- CRITICAL: do NOT draw the numbered circles from the template onto the output — replace them entirely with the actual drawing content"""

# Spritesheet prompt for OpenAI gpt-image-1 (no image input as layout)
SPRITESHEET_OPENAI_PROMPT_TPL = """\
Generate a sprite sheet as a 4x4 grid of 16 equal cells.
CRITICAL: Draw distinct red lines separating the 4x4 grid cells.
The image must have a flat solid {bg_color} background — no gradients, no scenery.
Content: {prompt}
Rules:
- Each cell's content must be centered and stay within its cell boundaries.
- Keep consistent style, lighting, and proportions across all 16 cells.
- Do not add any text, numbers, or UI elements.
- Ensure the red grid lines are perfectly straight and clearly visible."""

QUALITY_PRESETS = {
    "lowpoly": {
        "face_limit": 5000,
        "smart_low_poly": True,
        "texture_quality": "standard",
        "geometry_quality": "standard",
        "cost_cents": 40,
    },
    "medium": {
        "face_limit": 20000,
        "smart_low_poly": False,
        "texture_quality": "standard",
        "geometry_quality": "standard",
        "cost_cents": 30,
    },
    "high": {
        "face_limit": None,
        "smart_low_poly": False,
        "texture_quality": "detailed",
        "geometry_quality": "standard",
        "cost_cents": 40,
    },
    "ultra": {
        "face_limit": None,
        "smart_low_poly": False,
        "texture_quality": "detailed",
        "geometry_quality": "detailed",
        "cost_cents": 60,
    },
}


def result_json(ok: bool, path: str | None = None, cost_cents: int = 0, error: str | None = None):
    d = {"ok": ok, "cost_cents": cost_cents}
    if path:
        d["path"] = path
    if error:
        d["error"] = error
    print(json.dumps(d))


IMAGE_MODEL = "gemini-3.1-flash-image-preview"
IMAGE_SIZES = ["512", "1K", "2K", "4K"]
IMAGE_COSTS = {"512": 5, "1K": 7, "2K": 10, "4K": 15}
IMAGE_ASPECT_RATIOS = ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"]

OPENAI_MODEL = "gpt-image-1"
OPENAI_SIZES = ["1024x1024", "1024x1536", "1536x1024"]
OPENAI_COSTS = {"1024x1024": 5, "1024x1536": 7, "1536x1024": 7}  # medium quality


def cmd_image(args):
    provider = args.provider
    if provider == "openai":
        cmd_image_openai(args)
    else:
        cmd_image_gemini(args)


def cmd_image_gemini(args):
    size = args.size
    cost = IMAGE_COSTS[size]
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            image_size=size,
            aspect_ratio=args.aspect_ratio,
        ),
    )
    label = f"{size} {args.aspect_ratio}"

    print(f"Generating image ({label}) via Gemini...", file=sys.stderr)

    client = genai.Client()
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[args.prompt],
        config=config,
    )

    if response.parts is None:
        reason = "unknown"
        if response.candidates and response.candidates[0].finish_reason:
            reason = response.candidates[0].finish_reason
        result_json(False, error=f"Generation blocked (reason: {reason})")
        sys.exit(1)

    for part in response.parts:
        if part.inline_data is not None:
            output.write_bytes(part.inline_data.data)
            print(f"Saved: {output}", file=sys.stderr)
            record_spend(cost, "gemini")
            result_json(True, path=str(output), cost_cents=cost)
            return

    result_json(False, error="No image returned")
    sys.exit(1)


def cmd_image_openai(args):
    # gpt-image-1 supports 1024x1024, 1024x1536, 1536x1024
    size_str = "1024x1024"
    if args.aspect_ratio in ["9:16", "3:4", "4:5", "1:4", "1:8"]:
        size_str = "1024x1536"
    elif args.aspect_ratio in ["16:9", "4:3", "3:2", "4:1", "8:1", "21:9"]:
        size_str = "1536x1024"

    cost = OPENAI_COSTS.get(size_str, 5)
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating image ({size_str}) via OpenAI...", file=sys.stderr)

    client = OpenAI()
    try:
        response = client.images.generate(
            model=OPENAI_MODEL,
            prompt=args.prompt,
            size=size_str,
            quality="medium",
            n=1,
        )
        img_data = base64.b64decode(response.data[0].b64_json)
        output.write_bytes(img_data)
        print(f"Saved: {output}", file=sys.stderr)
        record_spend(cost, "openai")
        result_json(True, path=str(output), cost_cents=cost)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)


def generate_template(bg_color: str) -> bytes:
    """Generate a template PNG on the fly with the given BG color. Returns PNG bytes."""
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp = f.name
    subprocess.run(
        [sys.executable, str(TEMPLATE_SCRIPT), "-o", tmp, "--bg", bg_color],
        check=True, capture_output=True,
    )
    data = Path(tmp).read_bytes()
    Path(tmp).unlink()
    return data


def cmd_spritesheet(args):
    provider = args.provider
    if provider == "openai":
        cmd_spritesheet_openai(args)
    else:
        cmd_spritesheet_gemini(args)


def cmd_spritesheet_gemini(args):
    cost = IMAGE_COSTS["1K"]  # 7 cents
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    bg = args.bg
    template_bytes = generate_template(bg)
    system = SPRITESHEET_SYSTEM_TPL.format(bg_color=bg)
    print(f"Generating sprite sheet (bg={bg}) via Gemini...", file=sys.stderr)

    client = genai.Client()
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[
            types.Part.from_bytes(data=template_bytes, mime_type="image/png"),
            args.prompt,
        ],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            system_instruction=system,
            image_config=types.ImageConfig(
                image_size="1K",
                aspect_ratio="1:1",
            ),
        ),
    )

    if response.parts is None:
        reason = "unknown"
        if response.candidates and response.candidates[0].finish_reason:
            reason = response.candidates[0].finish_reason
        result_json(False, error=f"Generation blocked (reason: {reason})")
        sys.exit(1)

    for part in response.parts:
        if part.inline_data is not None:
            output.write_bytes(part.inline_data.data)
            print(f"Saved: {output}", file=sys.stderr)
            record_spend(cost, "gemini")
            result_json(True, path=str(output), cost_cents=cost)
            return

    result_json(False, error="No image returned")
    sys.exit(1)


def cmd_spritesheet_openai(args):
    cost = 5  # gpt-image-1 medium 1024x1024
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    bg = args.bg
    prompt = SPRITESHEET_OPENAI_PROMPT_TPL.format(bg_color=bg, prompt=args.prompt)
    print(f"Generating sprite sheet (bg={bg}) via OpenAI...", file=sys.stderr)

    client = OpenAI()
    try:
        response = client.images.generate(
            model=OPENAI_MODEL,
            prompt=prompt,
            size="1024x1024",
            quality="medium",
            n=1,
        )
        img_data = base64.b64decode(response.data[0].b64_json)
        output.write_bytes(img_data)
        print(f"Saved: {output}", file=sys.stderr)
        record_spend(cost, "openai")
        result_json(True, path=str(output), cost_cents=cost)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)


def cmd_glb(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    preset = QUALITY_PRESETS.get(args.quality, QUALITY_PRESETS["medium"])
    check_budget(preset["cost_cents"])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting to GLB (quality={args.quality})...", file=sys.stderr)

    try:
        image_to_glb(
            image_path,
            output,
            model_version=MODEL_V3,
            face_limit=preset["face_limit"],
            smart_low_poly=preset["smart_low_poly"],
            texture_quality=preset["texture_quality"],
            geometry_quality=preset["geometry_quality"],
        )
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(preset["cost_cents"], "tripo3d")
    result_json(True, path=str(output), cost_cents=preset["cost_cents"])


def cmd_set_budget(args):
    BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    budget = {"budget_cents": args.cents, "log": []}
    if BUDGET_FILE.exists():
        old = json.loads(BUDGET_FILE.read_text())
        budget["log"] = old.get("log", [])
    BUDGET_FILE.write_text(json.dumps(budget, indent=2) + "\n")
    spent = _spent_total(budget)
    print(json.dumps({"ok": True, "budget_cents": args.cents, "spent_cents": spent, "remaining_cents": args.cents - spent}))


def main():
    parser = argparse.ArgumentParser(description="Asset Generator — images (Gemini/OpenAI) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (5-15¢ depending on size)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--size", choices=IMAGE_SIZES, default="1K",
                       help="Resolution: 512 (5¢), 1K (7¢), 2K (10¢), 4K (15¢). Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=IMAGE_ASPECT_RATIOS, default="1:1",
                       help="Aspect ratio. Default: 1:1")
    p_img.add_argument("--provider", choices=["gemini", "openai"], default="gemini", help="Provider to use. Default: gemini")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_ss = sub.add_parser("spritesheet", help="Generate 4x4 sprite sheet (4-7 cents)")
    p_ss.add_argument("--prompt", required=True, help="What to generate (animation description or item list)")
    p_ss.add_argument("--bg", default="#00FF00", help="Background color hex (default: #00FF00 green). Choose a color absent from the subject.")
    p_ss.add_argument("--provider", choices=["gemini", "openai"], default="gemini", help="Provider to use. Default: gemini")
    p_ss.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_ss.set_defaults(func=cmd_spritesheet)

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model (30-40 cents)")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="medium", choices=list(QUALITY_PRESETS.keys()), help="Quality preset")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    p_budget = sub.add_parser("set_budget", help="Set the asset generation budget in cents")
    p_budget.add_argument("cents", type=int, help="Budget in cents")
    p_budget.set_defaults(func=cmd_set_budget)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
