#!/usr/bin/env python3
"""Asset Generator CLI - creates images (Gemini / xAI Grok) and GLBs (Tripo3D).

Subcommands:
  image     Generate a PNG from a prompt (Gemini 5-15¢ or Grok 2¢)
  video     Generate MP4 video from prompt + reference image (5¢/sec, Grok)
  glb       Convert a PNG to a static GLB (30¢ default, 60¢ hd)
  rig       Convert a PNG to a rigged biped GLB (preset + 25¢)
  retarget  Apply a biped preset animation to a rigged GLB (10¢)
  resume    Resume a timed-out Tripo3D job (glb/rig/retarget) from its sidecar — no extra cost

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import io
import json
import sys
from pathlib import Path

import requests
import xai_sdk
from google import genai
from google.genai import types
from PIL import Image

from tripo3d import (
    create_image_to_model_task,
    create_prerigcheck_task,
    create_retarget_task,
    create_rig_task,
    download_model,
    poll_task,
)

TOOLS_DIR = Path(__file__).parent
BUDGET_FILE = Path("assets/budget.json")

VIDEO_MODEL = "grok-imagine-video"
VIDEO_COST_PER_SEC = 5  # cents


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
    "default": {
        "face_limit": 30000,
        "geometry_quality": "standard",
        "texture_quality": "standard",
        "cost_cents": 30,
    },
    "hd": {
        "face_limit": None,
        "geometry_quality": "detailed",
        "texture_quality": "detailed",
        "cost_cents": 60,
    },
}

RIG_COST_CENTS = 25
RETARGET_COST_CENTS = 10


def result_json(ok: bool, path: str | None = None, cost_cents: int = 0, error: str | None = None):
    d = {"ok": ok, "cost_cents": cost_cents}
    if path:
        d["path"] = path
    if error:
        d["error"] = error
    print(json.dumps(d))


# --- Image backends ---

GEMINI_MODEL = "gemini-3.1-flash-image-preview"
GEMINI_SIZES = ["512", "1K", "2K", "4K"]
GEMINI_COSTS = {"512": 5, "1K": 7, "2K": 10, "4K": 15}
GEMINI_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]

GROK_MODEL = "grok-imagine-image"  # 2¢ flat
GROK_COST = 2
GROK_SIZES = ["1K", "2K"]
GROK_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
    "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20", "auto",
]

ALL_SIZES = ["512", "1K", "2K", "4K"]
ALL_ASPECT_RATIOS = sorted(set(GEMINI_ASPECT_RATIOS + GROK_ASPECT_RATIOS))


def _mime_for_image(path: Path) -> str:
    """Detect image MIME type from file extension."""
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/png")


def _image_data_uri(image_path: Path) -> str:
    """Load image and return as base64 data URI."""
    b64 = base64.b64encode(image_path.read_bytes()).decode()
    mime = _mime_for_image(image_path)
    return f"data:{mime};base64,{b64}"


def _generate_gemini(args, output: Path, cost: int):
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            image_size=args.size,
            aspect_ratio=args.aspect_ratio,
        ),
    )

    contents = []
    if args.image:
        ref_path = Path(args.image)
        if not ref_path.exists():
            result_json(False, error=f"Reference image not found: {ref_path}")
            sys.exit(1)
        contents.append(types.Part.from_bytes(data=ref_path.read_bytes(), mime_type=_mime_for_image(ref_path)))
    contents.append(args.prompt)

    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
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
            # Re-encode as real PNG (Gemini may return JPEG data)
            img = Image.open(io.BytesIO(part.inline_data.data))
            img.save(output, format="PNG")
            print(f"Saved: {output}", file=sys.stderr)
            record_spend(cost, "gemini")
            result_json(True, path=str(output), cost_cents=cost)
            return

    result_json(False, error="No image returned")
    sys.exit(1)


def _generate_grok(args, output: Path, cost: int):
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
            model=GROK_MODEL,
            image_url=image_url,
            aspect_ratio=args.aspect_ratio,
            resolution=args.size.lower(),
        )
        # xAI returns JPEG; convert to real PNG
        img = Image.open(io.BytesIO(resp.image))
        img.save(output, format="PNG")
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "xai")
    result_json(True, path=str(output), cost_cents=cost)


def cmd_image(args):
    backend = args.model
    size = args.size

    if backend == "gemini":
        if size not in GEMINI_SIZES:
            result_json(False, error=f"Gemini does not support size {size}. Use: {', '.join(GEMINI_SIZES)}")
            sys.exit(1)
        cost = GEMINI_COSTS[size]
    else:
        if size not in GROK_SIZES:
            result_json(False, error=f"Grok does not support size {size}. Use: {', '.join(GROK_SIZES)}")
            sys.exit(1)
        cost = GROK_COST

    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    label = f"{backend} {size} {args.aspect_ratio}"
    if args.image:
        label += " (image-to-image)"
    print(f"Generating image ({label})...", file=sys.stderr)

    if backend == "gemini":
        _generate_gemini(args, output, cost)
    else:
        _generate_grok(args, output, cost)


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


def _sidecar_path(output: Path) -> Path:
    return output.with_suffix(output.suffix + ".tripo.json")


def _write_sidecar(output: Path, data: dict) -> None:
    _sidecar_path(output).write_text(json.dumps(data, indent=2) + "\n")


def _read_sidecar(path: Path) -> dict:
    sc = _sidecar_path(path)
    if not sc.exists():
        raise FileNotFoundError(f"Sidecar not found: {sc} (run `rig` first)")
    return json.loads(sc.read_text())


def _resolve_preset(name: str) -> dict:
    if name not in QUALITY_PRESETS:
        result_json(False, error=f"Unknown quality: {name}. Use: {', '.join(QUALITY_PRESETS)}")
        sys.exit(1)
    return QUALITY_PRESETS[name]


def _resume_hint(output: Path) -> str:
    return f"Task is still processing on the server. Resume (no extra cost) with: asset_gen.py resume -o {output}"


def cmd_glb(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    preset = _resolve_preset(args.quality)
    check_budget(preset["cost_cents"])

    face_limit = args.face_limit if args.quality == "default" else preset["face_limit"]

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating GLB (quality={args.quality}, pbr={args.pbr}, face_limit={face_limit})...", file=sys.stderr)

    sidecar = {
        "kind": "mesh",
        "preset": args.quality,
        "pbr": args.pbr,
        "status": "pending",
    }
    try:
        task_id = create_image_to_model_task(
            image_path,
            face_limit=face_limit,
            pbr=args.pbr,
            geometry_quality=preset["geometry_quality"],
            texture_quality=preset["texture_quality"],
        )
        print(f"  image_to_model: {task_id}", file=sys.stderr)
        record_spend(preset["cost_cents"], "tripo3d-glb")
        sidecar["image_to_model_task_id"] = task_id
        _write_sidecar(output, sidecar)

        result = poll_task(task_id)
        download_model(result, output)
    except TimeoutError as e:
        result_json(False, error=f"{e}. {_resume_hint(output)}", cost_cents=preset["cost_cents"])
        sys.exit(1)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=preset["cost_cents"])


def cmd_rig(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    preset = _resolve_preset(args.quality)
    total_cost = preset["cost_cents"] + RIG_COST_CENTS
    check_budget(total_cost)

    face_limit = args.face_limit if args.quality == "default" else preset["face_limit"]

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating rigged GLB (quality={args.quality}, face_limit={face_limit})...", file=sys.stderr)

    sidecar = {
        "kind": "rig",
        "preset": args.quality,
        "pbr": args.pbr,
        "rig_type": "biped",
        "status": "pending",
    }
    try:
        gen_id = create_image_to_model_task(
            image_path,
            face_limit=face_limit,
            pbr=args.pbr,
            geometry_quality=preset["geometry_quality"],
            texture_quality=preset["texture_quality"],
        )
        print(f"  image_to_model: {gen_id}", file=sys.stderr)
        record_spend(preset["cost_cents"], "tripo3d-glb")
        sidecar["image_to_model_task_id"] = gen_id
        sidecar["stage"] = "image_to_model"
        _write_sidecar(output, sidecar)
        poll_task(gen_id)

        check_id = create_prerigcheck_task(gen_id)
        print(f"  animate_prerigcheck: {check_id}", file=sys.stderr)
        sidecar["prerigcheck_task_id"] = check_id
        sidecar["stage"] = "prerigcheck"
        _write_sidecar(output, sidecar)
        check_result = poll_task(check_id)
        check_out = check_result.get("output", {})
        rig_type = check_out.get("rig_type")
        if rig_type != "biped":
            result_json(False, error=(
                f"Rig pipeline is biped-only; prerigcheck reported rig_type={rig_type!r}. "
                f"Use `glb` for non-biped characters."
            ), cost_cents=preset["cost_cents"])
            sys.exit(1)

        rig_id = create_rig_task(gen_id, rig_type="biped")
        print(f"  animate_rig: {rig_id}", file=sys.stderr)
        record_spend(RIG_COST_CENTS, "tripo3d-rig")
        sidecar["animate_rig_task_id"] = rig_id
        sidecar["stage"] = "animate_rig"
        _write_sidecar(output, sidecar)
        rig_result = poll_task(rig_id)
        download_model(rig_result, output)
    except TimeoutError as e:
        result_json(False, error=f"{e}. {_resume_hint(output)}", cost_cents=0)
        sys.exit(1)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=total_cost)


def cmd_retarget(args):
    rigged = Path(args.rigged)
    if not rigged.exists():
        result_json(False, error=f"Rigged GLB not found: {rigged}")
        sys.exit(1)

    try:
        rigged_sidecar = _read_sidecar(rigged)
    except FileNotFoundError as e:
        result_json(False, error=str(e))
        sys.exit(1)

    rig_task_id = rigged_sidecar.get("animate_rig_task_id")
    if not rig_task_id or rigged_sidecar.get("kind") != "rig":
        result_json(False, error=f"Sidecar for {rigged} is not a rig output")
        sys.exit(1)

    check_budget(RETARGET_COST_CENTS)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Retargeting ({args.animation})...", file=sys.stderr)

    sidecar = {
        "kind": "anim",
        "animate_rig_task_id": rig_task_id,
        "animation": args.animation,
        "status": "pending",
    }
    try:
        task_id = create_retarget_task(rig_task_id, args.animation)
        print(f"  animate_retarget: {task_id}", file=sys.stderr)
        record_spend(RETARGET_COST_CENTS, "tripo3d-retarget")
        sidecar["animate_retarget_task_id"] = task_id
        _write_sidecar(output, sidecar)
        result = poll_task(task_id)
        download_model(result, output)
    except TimeoutError as e:
        result_json(False, error=f"{e}. {_resume_hint(output)}", cost_cents=RETARGET_COST_CENTS)
        sys.exit(1)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=RETARGET_COST_CENTS)


def cmd_resume(args):
    output = Path(args.output)
    try:
        sidecar = _read_sidecar(output)
    except FileNotFoundError as e:
        result_json(False, error=str(e))
        sys.exit(1)

    if sidecar.get("status") == "complete":
        print(f"Already complete: {output}", file=sys.stderr)
        result_json(True, path=str(output), cost_cents=0)
        return

    kind = sidecar.get("kind")
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        if kind == "mesh":
            task_id = sidecar["image_to_model_task_id"]
            print(f"  resuming image_to_model: {task_id}", file=sys.stderr)
            result = poll_task(task_id)
            download_model(result, output)

        elif kind == "rig":
            stage = sidecar.get("stage")
            gen_id: str = sidecar["image_to_model_task_id"]

            if stage == "image_to_model":
                print(f"  resuming image_to_model: {gen_id}", file=sys.stderr)
                poll_task(gen_id)
                check_id = create_prerigcheck_task(gen_id)
                print(f"  animate_prerigcheck: {check_id}", file=sys.stderr)
                sidecar["prerigcheck_task_id"] = check_id
                sidecar["stage"] = "prerigcheck"
                _write_sidecar(output, sidecar)
                stage = "prerigcheck"

            if stage == "prerigcheck":
                check_id = sidecar["prerigcheck_task_id"]
                print(f"  resuming animate_prerigcheck: {check_id}", file=sys.stderr)
                check_result = poll_task(check_id)
                rt = check_result.get("output", {}).get("rig_type")
                if rt != "biped":
                    result_json(False, error=f"prerigcheck: rig_type={rt!r}; rig pipeline is biped-only")
                    sys.exit(1)
                rig_id = create_rig_task(gen_id, rig_type="biped")
                print(f"  animate_rig: {rig_id}", file=sys.stderr)
                record_spend(RIG_COST_CENTS, "tripo3d-rig")
                sidecar["animate_rig_task_id"] = rig_id
                sidecar["stage"] = "animate_rig"
                _write_sidecar(output, sidecar)
                stage = "animate_rig"

            if stage == "animate_rig":
                rig_id = sidecar["animate_rig_task_id"]
                print(f"  resuming animate_rig: {rig_id}", file=sys.stderr)
                rig_result = poll_task(rig_id)
                download_model(rig_result, output)
            else:
                result_json(False, error=f"Unknown rig stage: {stage}")
                sys.exit(1)

        elif kind == "anim":
            task_id = sidecar["animate_retarget_task_id"]
            print(f"  resuming animate_retarget: {task_id}", file=sys.stderr)
            result = poll_task(task_id)
            download_model(result, output)

        else:
            result_json(False, error=f"Unknown sidecar kind: {kind!r}")
            sys.exit(1)

    except TimeoutError as e:
        result_json(False, error=f"{e}. Task still processing; retry resume.", cost_cents=0)
        sys.exit(1)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=0)


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
    parser = argparse.ArgumentParser(description="Asset Generator — images (Gemini / xAI Grok) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (Gemini 5-15¢ or Grok 2¢)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=["gemini", "grok"], default="grok",
                       help="Backend: grok (2¢, fast, simple images) or gemini (5-15¢, precise prompt following). Default: grok.")
    p_img.add_argument("--size", choices=ALL_SIZES, default="1K",
                       help="Resolution. Grok: 1K, 2K. Gemini: 512, 1K, 2K, 4K. Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=ALL_ASPECT_RATIOS, default="1:1",
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

    p_glb = sub.add_parser("glb", help="Convert PNG to static GLB (30¢ default, 60¢ hd)")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="default", choices=list(QUALITY_PRESETS.keys()),
                       help="default=30¢ v3.1 std (30k faces), hd=60¢ v3.1 detailed geom+HD texture")
    p_glb.add_argument("--no-pbr", dest="pbr", action="store_false", default=True,
                       help="Disable PBR (use if PBR output looks wrong)")
    p_glb.add_argument("--face-limit", type=int, default=30000,
                       help="Face cap for default quality, 10000-50000. Ignored when --quality hd. Default: 30000")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    p_rig = sub.add_parser("rig", help="Convert PNG to rigged biped GLB (preset cost + 25¢). Biped only.")
    p_rig.add_argument("--image", required=True, help="Input PNG path (biped character)")
    p_rig.add_argument("--quality", default="default", choices=list(QUALITY_PRESETS.keys()),
                       help="Underlying mesh preset (default or hd)")
    p_rig.add_argument("--no-pbr", dest="pbr", action="store_false", default=True,
                       help="Disable PBR")
    p_rig.add_argument("--face-limit", type=int, default=30000,
                       help="Face cap for default quality. Ignored when --quality hd. Default: 30000")
    p_rig.add_argument("-o", "--output", required=True, help="Output rigged GLB path")
    p_rig.set_defaults(func=cmd_rig)

    p_rt = sub.add_parser("retarget", help="Apply a preset:biped:* animation to a rigged GLB (10¢)")
    p_rt.add_argument("--rigged", required=True, help="Rigged GLB produced by `rig`")
    p_rt.add_argument("--animation", required=True, help="e.g. preset:biped:walk")
    p_rt.add_argument("-o", "--output", required=True, help="Output animated GLB path")
    p_rt.set_defaults(func=cmd_retarget)

    p_res = sub.add_parser("resume", help="Resume a timed-out Tripo3D job from its sidecar (no extra cost)")
    p_res.add_argument("-o", "--output", required=True, help="Output path whose .tripo.json sidecar holds the pending task id(s)")
    p_res.set_defaults(func=cmd_resume)

    p_budget = sub.add_parser("set_budget", help="Set the asset generation budget in cents")
    p_budget.add_argument("cents", type=int, help="Budget in cents")
    p_budget.set_defaults(func=cmd_set_budget)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
