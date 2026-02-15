#!/usr/bin/env python3
"""Asset Generator CLI - creates images (Gemini) and GLBs (Tripo3D).

Subcommands:
  image  Generate a PNG from a prompt (4 cents)
  glb    Convert a PNG to a GLB 3D model via Tripo3D (30-40 cents)

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import json
import sys
from pathlib import Path

from google import genai
from google.genai import types

from tripo3d import MODEL_V3, image_to_glb

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


def cmd_image(args):
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating image...", file=sys.stderr)

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[args.prompt],
        config=types.GenerateContentConfig(response_modalities=["image"]),
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
            result_json(True, path=str(output), cost_cents=4)
            return

    result_json(False, error="No image returned")
    sys.exit(1)


def cmd_glb(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    preset = QUALITY_PRESETS.get(args.quality, QUALITY_PRESETS["medium"])
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
    result_json(True, path=str(output), cost_cents=preset["cost_cents"])


def main():
    parser = argparse.ArgumentParser(description="Asset Generator — images (Gemini) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (4 cents)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model (30-40 cents)")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="medium", choices=list(QUALITY_PRESETS.keys()), help="Quality preset")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
