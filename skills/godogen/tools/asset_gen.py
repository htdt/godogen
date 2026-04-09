#!/usr/bin/env python3
"""Asset Generator CLI - creates images (Gemini / xAI Grok / OpenRouter) and GLBs (Tripo3D).

Subcommands:
  image   Generate a PNG from a prompt (Gemini 5-15¢, Grok 2¢, or OpenRouter ~5¢ auto-detected)
  video   Generate MP4 video from prompt + reference image (5¢/sec, Grok)
  glb     Convert a PNG to a GLB 3D model via Tripo3D (30-60¢)

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import io
import json
import os
import sys
from pathlib import Path

import requests
import xai_sdk
from google import genai
from google.genai import types
from PIL import Image

from tripo3d import MODEL_P1, MODEL_V31, image_to_glb

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
        "model_version": MODEL_P1,
        "texture_quality": "standard",
        "cost_cents": 50,
    },
    "high": {
        "model_version": MODEL_V31,
        "texture_quality": "detailed",
        "cost_cents": 40,
    },
}


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

# --- OpenRouter ---
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_DEFAULT_MODEL = "openai/gpt-5-image-mini"
OPENROUTER_SIZES = ["512", "1K", "2K", "4K"]
OPENROUTER_FALLBACK_COST = 5  # cents — used only when pricing lookup fails
OPENROUTER_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
]
# Models whose output_modalities include text; for others, request image-only.
_OPENROUTER_TEXT_CAPABLE_MODELS: set[str] | None = None  # lazily populated

ALL_SIZES = ["512", "1K", "2K", "4K"]
ALL_ASPECT_RATIOS = sorted(set(GEMINI_ASPECT_RATIOS + GROK_ASPECT_RATIOS + OPENROUTER_ASPECT_RATIOS))


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


_openrouter_models_cache: list[dict] | None = None


def _fetch_openrouter_models() -> list[dict]:
    """Fetch the OpenRouter model catalog (cached for the process lifetime)."""
    global _openrouter_models_cache
    if _openrouter_models_cache is not None:
        return _openrouter_models_cache
    try:
        resp = requests.get(OPENROUTER_MODELS_URL, timeout=15)
        resp.raise_for_status()
        _openrouter_models_cache = resp.json().get("data", [])
    except Exception as e:
        print(f"Warning: could not fetch OpenRouter models: {e}", file=sys.stderr)
        _openrouter_models_cache = []
    return _openrouter_models_cache


def _openrouter_model_cost_cents(model_id: str) -> int:
    """Estimate cost in cents for a single image generation on OpenRouter.

    Checks pricing fields in order:
    1. per-image (pricing.image) — flat per-image cost
    2. per-request (pricing.request) — flat per-request cost
    3. per-token (pricing.prompt + pricing.completion) — estimated with
       300 prompt + 1200 completion tokens (typical for image generation)
    Falls back to OPENROUTER_FALLBACK_COST if the model isn't found.
    """
    models = _fetch_openrouter_models()
    for m in models:
        if m.get("id") == model_id:
            pricing = m.get("pricing", {})
            try:
                # Per-image or per-request flat pricing (USD per generation)
                for flat_key in ("image", "request"):
                    flat = pricing.get(flat_key)
                    if flat is not None and float(flat) > 0:
                        return max(1, round(float(flat) * 100))

                # Per-token pricing
                prompt_per_tok = float(pricing.get("prompt", 0))
                completion_per_tok = float(pricing.get("completion", 0))
                if prompt_per_tok > 0 or completion_per_tok > 0:
                    cost_usd = prompt_per_tok * 300 + completion_per_tok * 1200
                    return max(1, round(cost_usd * 100))
            except (TypeError, ValueError):
                break
    return OPENROUTER_FALLBACK_COST


def _openrouter_model_supports_text(model_id: str) -> bool:
    """Check whether a model's output_modalities include 'text'."""
    global _OPENROUTER_TEXT_CAPABLE_MODELS
    if _OPENROUTER_TEXT_CAPABLE_MODELS is None:
        _OPENROUTER_TEXT_CAPABLE_MODELS = set()
        for m in _fetch_openrouter_models():
            arch = m.get("architecture", {})
            out_mods = arch.get("output_modalities", []) if isinstance(arch, dict) else []
            if "text" in out_mods and "image" in out_mods:
                _OPENROUTER_TEXT_CAPABLE_MODELS.add(m.get("id", ""))
    return model_id in _OPENROUTER_TEXT_CAPABLE_MODELS


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


def _extract_openrouter_image(data: dict) -> bytes:
    """Extract image bytes from OpenRouter response, handling multiple formats.

    Supported response structures:
    1. choices[0].message.content[].image_url.url (base64 data URL or HTTP URL)
    2. choices[0].message.images[].image_url.url (some models)
    3. data[].b64_json (DALL-E style)

    Returns raw image bytes or raises ValueError with a descriptive message.
    """
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("No choices in response")

    message = choices[0].get("message", {})

    # Strategy 1: content array with image_url entries
    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "image_url":
                url = part.get("image_url", {}).get("url", "")
                if url:
                    return _fetch_image_url(url)

    # Strategy 2: images array
    images = message.get("images", [])
    if images:
        entry = images[0]
        url = ""
        if isinstance(entry, dict):
            url = entry.get("image_url", {}).get("url", "") or entry.get("url", "")
        if url:
            return _fetch_image_url(url)

    # Strategy 3: DALL-E style data array
    dall_e_data = data.get("data", [])
    if dall_e_data and isinstance(dall_e_data[0], dict):
        b64 = dall_e_data[0].get("b64_json", "")
        if b64:
            return base64.b64decode(b64)
        url = dall_e_data[0].get("url", "")
        if url:
            return _fetch_image_url(url)

    raise ValueError(f"Could not find image in response. Keys: choices[0].message keys={list(message.keys())}")


def _fetch_image_url(url: str) -> bytes:
    """Fetch image bytes from a base64 data URL or HTTP URL."""
    if url.startswith("data:"):
        # "data:image/png;base64,..."
        if "," not in url:
            raise ValueError("Malformed data URL: no comma separator")
        b64_data = url.split(",", 1)[1]
        return base64.b64decode(b64_data)
    elif url.startswith("http"):
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        return resp.content
    else:
        raise ValueError(f"Unrecognized image URL format: {url[:80]}")


def _generate_openrouter(args, output: Path, cost: int):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        result_json(False, error="OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)

    or_model = getattr(args, 'openrouter_model', None) or OPENROUTER_DEFAULT_MODEL

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages_content = []
    if args.image:
        ref_path = Path(args.image)
        if not ref_path.exists():
            result_json(False, error=f"Reference image not found: {ref_path}")
            sys.exit(1)
        data_uri = _image_data_uri(ref_path)
        messages_content.append({
            "type": "image_url",
            "image_url": {"url": data_uri},
        })
    messages_content.append({"type": "text", "text": args.prompt})

    # Only request text modality if the model supports it; image-only models
    # (e.g. FLUX, Seedream) reject requests that include text output.
    modalities = ["image", "text"] if _openrouter_model_supports_text(or_model) else ["image"]

    payload = {
        "model": or_model,
        "messages": [{"role": "user", "content": messages_content}],
        "modalities": modalities,
        "image_config": {
            "aspect_ratio": args.aspect_ratio,
            "image_size": args.size,
        },
    }

    print(f"Generating via OpenRouter ({or_model})...", file=sys.stderr)
    try:
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
        if not resp.ok:
            # Extract API error message before raising
            try:
                err_data = resp.json()
                err_msg = err_data.get("error", {}).get("message", "") or json.dumps(err_data)
            except Exception:
                err_msg = resp.text[:500] if resp.text else f"HTTP {resp.status_code}"
            result_json(False, error=f"OpenRouter API error ({resp.status_code}): {err_msg}")
            sys.exit(1)

        data = resp.json()

        # Check for business-level error in 2xx response
        if "error" in data and not data.get("choices"):
            err_msg = data["error"].get("message", json.dumps(data["error"]))
            result_json(False, error=f"OpenRouter: {err_msg}")
            sys.exit(1)

        img_bytes = _extract_openrouter_image(data)
        img = Image.open(io.BytesIO(img_bytes))
        img.save(output, format="PNG")
    except SystemExit:
        raise
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "openrouter")
    result_json(True, path=str(output), cost_cents=cost)


def cmd_image(args):
    backend = args.model
    size = args.size
    ar = args.aspect_ratio

    if backend == "gemini":
        if size not in GEMINI_SIZES:
            result_json(False, error=f"Gemini does not support size {size}. Use: {', '.join(GEMINI_SIZES)}")
            sys.exit(1)
        if ar not in GEMINI_ASPECT_RATIOS:
            result_json(False, error=f"Gemini does not support aspect ratio {ar}. Use: {', '.join(GEMINI_ASPECT_RATIOS)}")
            sys.exit(1)
        cost = GEMINI_COSTS[size]
    elif backend == "openrouter":
        if size not in OPENROUTER_SIZES:
            result_json(False, error=f"OpenRouter does not support size {size}. Use: {', '.join(OPENROUTER_SIZES)}")
            sys.exit(1)
        if ar not in OPENROUTER_ASPECT_RATIOS:
            result_json(False, error=f"OpenRouter does not support aspect ratio {ar}. Use: {', '.join(OPENROUTER_ASPECT_RATIOS)}")
            sys.exit(1)
        or_model = getattr(args, 'openrouter_model', None) or OPENROUTER_DEFAULT_MODEL
        cost = _openrouter_model_cost_cents(or_model)
    else:
        if size not in GROK_SIZES:
            result_json(False, error=f"Grok does not support size {size}. Use: {', '.join(GROK_SIZES)}")
            sys.exit(1)
        if ar not in GROK_ASPECT_RATIOS:
            result_json(False, error=f"Grok does not support aspect ratio {ar}. Use: {', '.join(GROK_ASPECT_RATIOS)}")
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
    elif backend == "openrouter":
        _generate_openrouter(args, output, cost)
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


def cmd_glb(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    preset = QUALITY_PRESETS.get(args.quality, QUALITY_PRESETS["default"])
    check_budget(preset["cost_cents"])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting to GLB (quality={args.quality})...", file=sys.stderr)

    try:
        image_to_glb(
            image_path,
            output,
            model_version=preset["model_version"],
            texture_quality=preset["texture_quality"],
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
    parser = argparse.ArgumentParser(description="Asset Generator — images (Gemini / xAI Grok / OpenRouter) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (Gemini 5-15¢, Grok 2¢, or OpenRouter ~5¢)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=["gemini", "grok", "openrouter"], default="grok",
                       help="Backend: grok (2¢, fast, simple images), gemini (5-15¢, precise prompt following), or openrouter (~5¢, flexible model selection). Default: grok.")
    p_img.add_argument("--openrouter-model", default=None,
                       help="OpenRouter model ID (default: openai/gpt-5-image-mini). Only used when --model openrouter.")
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

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model (30-60 cents)")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="default", choices=list(QUALITY_PRESETS.keys()), help="Quality preset")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    p_budget = sub.add_parser("set_budget", help="Set the asset generation budget in cents")
    p_budget.add_argument("cents", type=int, help="Budget in cents")
    p_budget.set_defaults(func=cmd_set_budget)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
