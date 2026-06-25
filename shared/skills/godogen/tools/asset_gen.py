#!/usr/bin/env python3
"""Asset Generator CLI - creates images (Gemini / Grok / DashScope) and GLBs (Tripo3D).

Subcommands:
  image     Generate a PNG from a prompt (Gemini 5-15¢, Grok 2¢, or DashScope 2-5¢)
  video     Generate MP4 video from prompt + reference image (Grok 5¢/sec or DashScope)
  glb       Convert a PNG to a static GLB (30¢ default, 60¢ hd)
  rig       Convert a PNG to a rigged biped GLB (preset + 25¢)
  retarget  Apply a biped preset animation to a rigged GLB (10¢)
  resume    Resume a timed-out Tripo3D job (glb/rig/retarget) from its sidecar — no extra cost

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import json
import sys
from pathlib import Path

from backends import get_image_backend, get_video_backend
from backends.base import result_json
from backends.grok import GROK_SIZES, GROK_ASPECT_RATIOS
from backends.gemini import GEMINI_SIZES, GEMINI_ASPECT_RATIOS

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


# --- Image backend constants for CLI ---

ALL_SIZES = ["512", "1K", "2K", "4K"]
ALL_ASPECT_RATIOS = sorted(set(GEMINI_ASPECT_RATIOS + GROK_ASPECT_RATIOS))


def cmd_image(args):
    backend = get_image_backend(args.model)
    ref_image = Path(args.image) if args.image else None
    backend.generate(
        prompt=args.prompt,
        output=Path(args.output),
        size=args.size,
        aspect_ratio=args.aspect_ratio,
        ref_image=ref_image,
        check_budget_fn=check_budget,
        record_spend_fn=record_spend,
    )


def cmd_video(args):
    backend = get_video_backend(args.video_backend)
    backend.generate(
        prompt=args.prompt,
        ref_image=Path(args.image),
        output=Path(args.output),
        duration=args.duration,
        resolution=args.resolution,
        check_budget_fn=check_budget,
        record_spend_fn=record_spend,
    )


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
    parser = argparse.ArgumentParser(description="Asset Generator — images (Gemini / Grok / DashScope) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (Gemini 5-15¢, Grok 2¢, or DashScope 2-5¢)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=["gemini", "grok", "dashscope"], default=None,
                       help="Backend: grok (2¢), gemini (5-15¢), or dashscope (2-5¢). Default: $ASSET_BACKEND or grok.")
    p_img.add_argument("--size", choices=ALL_SIZES, default="1K",
                       help="Resolution. Grok: 1K, 2K. Gemini: 512, 1K, 2K, 4K. Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=ALL_ASPECT_RATIOS, default="1:1",
                       help="Aspect ratio. Default: 1:1")
    p_img.add_argument("--image", default=None, help="Reference image for image-to-image edit")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_vid = sub.add_parser("video", help="Generate MP4 video from prompt + reference image")
    p_vid.add_argument("--prompt", required=True, help="Video generation prompt")
    p_vid.add_argument("--video-backend", choices=["grok", "dashscope"], default=None,
                       help="Video backend. Default: $ASSET_BACKEND or grok.")
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
