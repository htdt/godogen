#!/usr/bin/env python3
"""Asset Generator CLI - creates images (xAI Grok), GLBs (Tripo3D), and audio (Gemini).

Subcommands:
  image   Generate a PNG from a prompt (2¢ standard, 7¢ pro)
  video   Generate MP4 video from prompt + reference image (5¢/sec)
  glb     Convert a PNG to a GLB 3D model via Tripo3D (30-60¢)
  audio   Generate audio from a text prompt via Gemini (3¢)

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

import requests
import xai_sdk

from tripo3d import MODEL_V3, image_to_glb

TOOLS_DIR = Path(__file__).parent
BUDGET_FILE = Path("assets/budget.json")

VIDEO_MODEL = "grok-imagine-video"
VIDEO_COST_PER_SEC = 5  # cents

AUDIO_MODEL = "gemini-2.5-flash"
AUDIO_COST = 3  # cents


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


def _image_data_uri(image_path: Path) -> str:
    """Load image and return as base64 data URI."""
    b64 = base64.b64encode(image_path.read_bytes()).decode()
    return f"data:image/png;base64,{b64}"


def cmd_image(args):
    tier = args.model
    cost = IMAGE_COSTS[tier]
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    model = IMAGE_MODELS[tier]
    label = f"{tier} {args.size} {args.aspect_ratio}"
    if args.image:
        label += " (image-to-image)"
    print(f"Generating image ({label})...", file=sys.stderr)

    image_url = None
    if args.image:
        ref_path = Path(args.image)
        if not ref_path.exists():
            result_json(False, error=f"Reference image not found: {ref_path}")
            sys.exit(1)
        image_url = _image_data_uri(ref_path)

    try:
        client = xai_sdk.Client()
        resp = client.image.sample(
            prompt=args.prompt,
            model=model,
            image_url=image_url,
            aspect_ratio=args.aspect_ratio,
            resolution=args.size.lower(),
        )
        output.write_bytes(resp.image)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "xai")
    result_json(True, path=str(output), cost_cents=cost)


def cmd_video(args):
    cost = args.duration * VIDEO_COST_PER_SEC
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Reference image not found: {image_path}")
        sys.exit(1)

    print(f"Generating {args.duration}s video ({args.resolution})...", file=sys.stderr)
    image_url = _image_data_uri(image_path)

    try:
        client = xai_sdk.Client()
        resp = client.video.generate(
            prompt=args.prompt,
            model=VIDEO_MODEL,
            image_url=image_url,
            duration=args.duration,
            aspect_ratio="1:1",
            resolution=args.resolution,
        )
        # Download MP4
        print("  Downloading video...", file=sys.stderr)
        dl = requests.get(resp.url, timeout=120)
        dl.raise_for_status()
        output.write_bytes(dl.content)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "xai-video")
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


def cmd_audio(args):
    """Generate audio from a text prompt via Gemini."""
    import google.genai as genai
    from google.genai import types

    check_budget(AUDIO_COST)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    prompt = f"{args.prompt}. Duration: approximately {args.duration} seconds."

    client = genai.Client()

    response = client.models.generate_content(
        model=AUDIO_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
        ),
    )

    if not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts:
        reason = getattr(response.candidates[0], "finish_reason", "unknown") if response.candidates else "no candidates"
        result_json(False, error=f"Audio generation failed: {reason}")
        sys.exit(1)

    audio_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
            audio_data = part.inline_data.data
            break

    if audio_data is None:
        result_json(False, error="No audio data in response")
        sys.exit(1)

    # Write raw audio, then convert to OGG via ffmpeg
    tmp_path = output.with_suffix(".tmp.wav")
    tmp_path.write_bytes(audio_data)

    ret = subprocess.run(
        ["ffmpeg", "-y", "-i", str(tmp_path), "-c:a", "libvorbis", "-q:a", "4", str(output)],
        capture_output=True, text=True,
    )
    tmp_path.unlink(missing_ok=True)

    if ret.returncode != 0:
        result_json(False, error=f"ffmpeg conversion failed: {ret.stderr[:200]}")
        sys.exit(1)

    record_spend(AUDIO_COST, "gemini_audio")
    result_json(True, path=str(output), cost_cents=AUDIO_COST)


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
    parser = argparse.ArgumentParser(description="Asset Generator — images (xAI Grok), GLBs (Tripo3D), and audio (Gemini)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (2¢ standard, 7¢ pro)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=list(IMAGE_MODELS.keys()), default="standard",
                       help="Model tier: standard (2¢, fast) or pro (7¢, higher quality). Default: standard.")
    p_img.add_argument("--size", choices=IMAGE_SIZES, default="1K",
                       help="Resolution: 1K or 2K. Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=IMAGE_ASPECT_RATIOS, default="1:1",
                       help="Aspect ratio. Default: 1:1")
    p_img.add_argument("--image", default=None, help="Reference image for image-to-image edit")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_vid = sub.add_parser("video", help="Generate MP4 video from prompt + reference image (5¢/sec)")
    p_vid.add_argument("--prompt", required=True, help="Video generation prompt")
    p_vid.add_argument("--image", required=True, help="Reference image path (starting frame)")
    p_vid.add_argument("--duration", type=int, required=True, help="Duration in seconds (1-15)")
    p_vid.add_argument("--resolution", choices=["480p", "720p"], default="720p",
                       help="Video resolution. Default: 720p")
    p_vid.add_argument("-o", "--output", required=True, help="Output MP4 path")
    p_vid.set_defaults(func=cmd_video)

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model (30-60 cents)")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="medium", choices=list(QUALITY_PRESETS.keys()), help="Quality preset")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    p_budget = sub.add_parser("set_budget", help="Set the asset generation budget in cents")
    p_budget.add_argument("cents", type=int, help="Budget in cents")
    p_budget.set_defaults(func=cmd_set_budget)

    p_audio = sub.add_parser("audio", help="Generate audio from prompt (3¢, Gemini)")
    p_audio.add_argument("--prompt", required=True)
    p_audio.add_argument("--duration", type=float, default=2.0, help="Target duration in seconds")
    p_audio.add_argument("-o", "--output", required=True)
    p_audio.set_defaults(func=cmd_audio)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
