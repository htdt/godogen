#!/usr/bin/env python3
"""Asset Generator CLI for Wan images/videos and Tencent Hunyuan 3D GLBs.

All external generation calls use China mainland cloud services. Commands print
JSON to stdout and send progress messages to stderr.
"""

import argparse
import json
import sys
from pathlib import Path

from dashscope import generate_image, generate_video
from hunyuan3d import create_image_to_model_task, download_model, poll_task

QUALITY_PRESETS = {"default": {"face_limit": 30000}, "hd": {"face_limit": None}}
IMAGE_SIZES = ["1K", "2K", "4K"]
ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
VIDEO_RESOLUTIONS = {"480p": "832*480", "720p": "1280*720", "1080p": "1920*1080"}


def result_json(ok: bool, path: str | None = None, cost_cents: int = 0, error: str | None = None) -> None:
    result = {"ok": ok, "cost_cents": cost_cents}
    if path:
        result["path"] = path
    if error:
        result["error"] = error
    print(json.dumps(result))


def _sidecar_path(output: Path) -> Path:
    return output.with_suffix(output.suffix + ".hunyuan.json")


def _write_sidecar(output: Path, data: dict) -> None:
    _sidecar_path(output).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _read_sidecar(output: Path) -> dict:
    sidecar = _sidecar_path(output)
    if not sidecar.exists():
        raise FileNotFoundError(f"Sidecar not found: {sidecar}")
    return json.loads(sidecar.read_text(encoding="utf-8"))


def _require_file(path: str, label: str) -> Path:
    value = Path(path)
    if not value.exists():
        result_json(False, error=f"{label} not found: {value}")
        sys.exit(1)
    return value


def cmd_image(args: argparse.Namespace) -> None:
    reference = _require_file(args.image, "Reference image") if args.image else None
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Generating Wan image ({args.size}, {args.aspect_ratio})...", file=sys.stderr)
    try:
        generate_image(args.prompt, output, size=args.size, aspect_ratio=args.aspect_ratio, reference=reference)
    except Exception as error:
        result_json(False, error=str(error))
        sys.exit(1)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output))


def cmd_video(args: argparse.Namespace) -> None:
    image = _require_file(args.image, "Reference image")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Generating Wan video ({args.duration}s, {args.resolution})...", file=sys.stderr)
    try:
        generate_video(args.prompt, image, output, duration=args.duration, resolution=VIDEO_RESOLUTIONS[args.resolution])
    except Exception as error:
        result_json(False, error=str(error))
        sys.exit(1)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output))


def cmd_glb(args: argparse.Namespace) -> None:
    image = _require_file(args.image, "Image")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    preset = QUALITY_PRESETS[args.quality]
    sidecar = {"kind": "mesh", "quality": args.quality, "pbr": args.pbr, "status": "pending"}
    print(f"Generating Hunyuan 3D GLB (quality={args.quality}, pbr={args.pbr})...", file=sys.stderr)
    try:
        task_id = create_image_to_model_task(
            image, face_limit=args.face_limit if args.quality == "default" else preset["face_limit"], pbr=args.pbr, quality=args.quality
        )
        sidecar["job_id"] = task_id
        _write_sidecar(output, sidecar)
        download_model(poll_task(task_id), output)
    except TimeoutError as error:
        result_json(False, error=f"{error}. Resume with: asset_gen.py resume -o {output}")
        sys.exit(1)
    except Exception as error:
        result_json(False, error=str(error))
        sys.exit(1)
    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output))


def cmd_resume(args: argparse.Namespace) -> None:
    output = Path(args.output)
    try:
        sidecar = _read_sidecar(output)
    except FileNotFoundError as error:
        result_json(False, error=str(error))
        sys.exit(1)
    if sidecar.get("status") == "complete":
        result_json(True, path=str(output))
        return
    try:
        download_model(poll_task(sidecar["job_id"]), output)
    except TimeoutError as error:
        result_json(False, error=f"{error}. Task is still running; retry resume.")
        sys.exit(1)
    except Exception as error:
        result_json(False, error=str(error))
        sys.exit(1)
    sidecar["status"] = "complete"
    _write_sidecar(output, sidecar)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output))


def main() -> None:
    parser = argparse.ArgumentParser(description="Asset Generator — Wan images/videos and Tencent Hunyuan 3D GLBs")
    subcommands = parser.add_subparsers(dest="command", required=True)

    image = subcommands.add_parser("image", help="Generate a PNG with Wan")
    image.add_argument("--prompt", required=True)
    image.add_argument("--size", choices=IMAGE_SIZES, default="1K")
    image.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1")
    image.add_argument("--image", help="Reference image for image-to-image generation")
    image.add_argument("-o", "--output", required=True)
    image.set_defaults(func=cmd_image)

    video = subcommands.add_parser("video", help="Generate an MP4 with Wan from a reference image")
    video.add_argument("--prompt", required=True)
    video.add_argument("--image", required=True)
    video.add_argument("--duration", type=int, choices=[5, 10], default=5)
    video.add_argument("--resolution", choices=list(VIDEO_RESOLUTIONS), default="720p")
    video.add_argument("-o", "--output", required=True)
    video.set_defaults(func=cmd_video)

    glb = subcommands.add_parser("glb", help="Convert an image to a static GLB with Hunyuan 3D")
    glb.add_argument("--image", required=True)
    glb.add_argument("--quality", choices=list(QUALITY_PRESETS), default="default")
    glb.add_argument("--no-pbr", dest="pbr", action="store_false", default=True)
    glb.add_argument("--face-limit", type=int, default=30000)
    glb.add_argument("-o", "--output", required=True)
    glb.set_defaults(func=cmd_glb)

    resume = subcommands.add_parser("resume", help="Resume a timed-out Hunyuan 3D job")
    resume.add_argument("-o", "--output", required=True)
    resume.set_defaults(func=cmd_resume)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
