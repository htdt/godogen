#!/usr/bin/env python3
"""Asset Generator CLI - creates images (xAI Grok) and GLBs (Tripo3D).

Subcommands:
  image   Generate a PNG from a prompt (2¢ standard, 7¢ pro)
  glb     Convert a PNG to a GLB 3D model via Tripo3D (30-60¢)

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests

from tripo3d import MODEL_V3, image_to_glb

TOOLS_DIR = Path(__file__).parent
BUDGET_FILE = Path("assets/budget.json")

XAI_API_URL = "https://api.x.ai/v1/images/generations"


def get_xai_api_key() -> str:
    key = os.environ.get("XAI_API_KEY")
    if not key:
        raise ValueError("XAI_API_KEY environment variable not set")
    return key


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


IMAGE_MODEL = "grok-imagine-image"          # 2¢
IMAGE_MODEL_PRO = "grok-imagine-image-pro"  # 7¢
IMAGE_MODELS = {"standard": IMAGE_MODEL, "pro": IMAGE_MODEL_PRO}
IMAGE_COSTS = {"standard": 2, "pro": 7}
IMAGE_SIZES = ["1K", "2K"]
IMAGE_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
    "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20", "auto",
]


def cmd_image(args):
    tier = args.model
    cost = IMAGE_COSTS[tier]
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    model = IMAGE_MODELS[tier]
    label = f"{tier} {args.size} {args.aspect_ratio}"
    print(f"Generating image ({label})...", file=sys.stderr)

    key = get_xai_api_key()
    resp = requests.post(
        XAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": args.prompt,
            "n": 1,
            "response_format": "b64_json",
            "resolution": args.size.lower(),
            "aspect_ratio": args.aspect_ratio,
        },
        timeout=120,
    )

    if resp.status_code != 200:
        try:
            err = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            err = resp.text
        result_json(False, error=f"xAI API error {resp.status_code}: {err}")
        sys.exit(1)

    data = resp.json().get("data", [])
    if not data or "b64_json" not in data[0]:
        result_json(False, error="No image returned")
        sys.exit(1)

    output.write_bytes(base64.b64decode(data[0]["b64_json"]))
    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "xai")
    result_json(True, path=str(output), cost_cents=cost)


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
    parser = argparse.ArgumentParser(description="Asset Generator — images (xAI Grok) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (2¢ standard, 7¢ pro)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=list(IMAGE_MODELS.keys()), default="standard",
                       help="Model tier: standard (2¢, fast) or pro (7¢, higher quality). Default: standard.")
    p_img.add_argument("--size", choices=IMAGE_SIZES, default="1K",
                       help="Resolution: 1K or 2K. Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=IMAGE_ASPECT_RATIOS, default="1:1",
                       help="Aspect ratio. Default: 1:1")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model (30-60 cents)")
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
