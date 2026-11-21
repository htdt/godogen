#!/usr/bin/env python3
"""Asset Generator CLI - creates images, videos, speech and music (OpenAI GPT-Image / xAI Grok / Gemini / Lyria).

Subcommands:
  image     Generate one PNG / WebP / JPEG / GIF now (GPT-Image-2.6 Sunburst, billed from token usage)
  batch     Generate a JSONL list of images through the Batch API at half price
  video     Generate MP4 video from prompt + reference image (8-14¢/sec, Grok)
  speech    Speak a transcript with Gemini 3.8 TTS (~0.25¢ per 10 s line)
  voice     Design a persistent character voice (~2¢), list voices, delete one
  music     Generate music with Lyria (4¢ per 30 s clip, 8¢ per song)

3D models come from the `tripo` CLI (see api.md), not from here.

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import wave
from datetime import date
from pathlib import Path

import openai
import requests
import xai_sdk
from google import genai
from google.genai import types
from PIL import Image

TOOLS_DIR = Path(__file__).parent

VIDEO_MODEL = "grok-imagine-video-1.5"
VIDEO_COSTS_PER_SEC = {"480p": 8, "720p": 14}  # cents, +1¢ for the start frame; xAI's billed cost_usd is reported when present


def result_json(ok: bool, path: str | None = None, cost_cents: float = 0, error: str | None = None, **extra):
    d = {"ok": ok, "cost_cents": cost_cents}
    if path:
        d["path"] = path
    if error:
        d["error"] = error
    d.update(extra)
    print(json.dumps(d))


# --- Images (OpenAI GPT-Image-2.6) ---

IMAGE_MODELS = {"sunburst": "gpt-image-2.6-sunburst", "flare": "gpt-image-2.6-flare"}
IMAGE_QUALITIES = ["low", "medium", "high", "xhigh", "max"]
IMAGE_QUALITY = "medium"
IMAGE_FORMATS = {".png": "png", ".webp": "webp", ".jpg": "jpeg", ".jpeg": "jpeg", ".gif": "gif"}
IMAGE_USD_PER_M = {"text_in": 5.0, "image_in": 8.0, "image_out": 30.0}  # standard rates; Batch bills half
BATCH_DONE = {"completed", "failed", "expired", "cancelled"}


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


def _billed_cents(resp, estimate: int) -> int:
    """Cost xAI reports for the request, else the price-table estimate."""
    usd = resp.cost_usd
    return round(usd * 100) if usd else estimate


def _image_request(job: dict) -> tuple[str, dict]:
    """One image job -> (endpoint, JSON body). The same body goes live or into a Batch line."""
    out = Path(job["o"])
    fmt = IMAGE_FORMATS.get(out.suffix.lower())
    if fmt is None:
        raise ValueError(f"{out}: output extension must be one of {', '.join(IMAGE_FORMATS)}")
    model = job.get("model", "sunburst")
    if model not in IMAGE_MODELS:
        raise ValueError(f"{out}: model must be one of {', '.join(IMAGE_MODELS)}")
    quality = job.get("quality", IMAGE_QUALITY)
    if quality not in IMAGE_QUALITIES:
        raise ValueError(f"{out}: quality must be one of {', '.join(IMAGE_QUALITIES)}")
    body = {"model": IMAGE_MODELS[model], "prompt": job["prompt"], "quality": quality,
            "size": job.get("size") or ("auto" if fmt == "gif" else "1024x1024"), "output_format": fmt}
    if job.get("complexity"):
        body["complexity"] = job["complexity"]
    if job.get("transparent"):
        if fmt not in ("png", "webp", "gif"):  # GIF alpha is 1-bit
            raise ValueError(f"{out}: transparency needs a .png, .webp or .gif output")
        body["background"] = "transparent"
    if fmt == "gif":
        body["frame_count"] = job.get("frames", 9)
        body["frame_duration_ms"] = job.get("frame_ms", 200)
    elif "frames" in job or "frame_ms" in job:
        raise ValueError(f"{out}: frames / frame_ms need a .gif output")
    refs = job.get("image") or []
    if isinstance(refs, str):
        refs = [refs]
    if not refs:
        return "/v1/images/generations", body
    for ref in refs:
        if not Path(ref).exists():
            raise ValueError(f"Reference image not found: {ref}")
    body["images"] = [{"image_url": _image_data_uri(Path(ref))} for ref in refs]
    return "/v1/images/edits", body


def _image_cents(usage: dict | None, batch: bool) -> float:
    """Cost from the token usage the API reports."""
    if not usage:
        return 0.0
    details = usage.get("input_tokens_details") or {}
    text_in = details.get("text_tokens", 0 if details else usage.get("input_tokens", 0))
    usd = (text_in * IMAGE_USD_PER_M["text_in"] + details.get("image_tokens", 0) * IMAGE_USD_PER_M["image_in"]
           + usage.get("output_tokens", 0) * IMAGE_USD_PER_M["image_out"]) / 1e6
    return round(usd * 100 / (2 if batch else 1), 2)


ALPHA_FLOOR = 16  # edits with a transparent background leave a faint haze (alpha ~10) where it should be clear


def _save_image(resp: dict, output: Path, transparent: bool = False) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    data = base64.b64decode(resp["data"][0]["b64_json"])
    if transparent and output.suffix.lower() in (".png", ".webp"):
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        img.putalpha(img.getchannel("A").point(lambda a: 0 if a <= ALPHA_FLOOR else a))
        img.save(output, lossless=True) if output.suffix.lower() == ".webp" else img.save(output)
    else:
        output.write_bytes(data)
    return {k: resp[k] for k in ("size", "quality") if resp.get(k)}


def _job_from_args(args) -> dict:
    job = {"prompt": args.prompt, "o": args.output, "model": args.model, "quality": args.quality,
           "image": args.image, "transparent": args.transparent}
    for key, value in (("size", args.size), ("complexity", args.complexity),
                       ("frames", args.frames), ("frame_ms", args.frame_ms)):
        if value is not None:
            job[key] = value
    return job


def cmd_image(args):
    try:
        endpoint, body = _image_request(_job_from_args(args))
    except ValueError as e:
        result_json(False, error=str(e))
        sys.exit(1)

    label = f"{body['model']} {body['quality']} {body['size']} {body['output_format']}"
    if "images" in body:
        label += f", {len(body['images'])} reference(s)"
    print(f"Generating image ({label})...", file=sys.stderr)
    try:
        resp = openai.OpenAI().post(endpoint.removeprefix("/v1"), body=body, cast_to=object)
    except openai.APIError as e:
        result_json(False, error=str(e))
        sys.exit(1)

    output = Path(args.output)
    extra = _save_image(resp, output, args.transparent)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=_image_cents(resp.get("usage"), batch=False), **extra)


def _batch_errors(batch) -> str:
    errors = getattr(batch.errors, "data", None) or []
    return "; ".join(f"line {e.line}: {e.message}" if e.line else e.message for e in errors) or batch.status


def cmd_batch(args):
    jobs_path = Path(args.jobs)
    state_path = jobs_path.with_name(jobs_path.name + ".batch.json")
    lines = jobs_path.read_text()
    jobs = [json.loads(line) for line in lines.splitlines() if line.strip()]
    for job in jobs:
        job.setdefault("quality", args.quality)
        job.setdefault("model", args.model)
    jobs_hash = hashlib.sha256(json.dumps(jobs, sort_keys=True).encode()).hexdigest()[:16]

    client = openai.OpenAI()
    state = json.loads(state_path.read_text()) if state_path.exists() else None
    if state and state["jobs_hash"] == jobs_hash and "images" in state:
        images = state["images"]
        print(f"Already collected; delete {state_path} to generate again", file=sys.stderr)
        result_json(all(r["ok"] for r in images), cost_cents=round(sum(r.get("cost_cents", 0) for r in images), 2),
                    images=images)
        return
    if state and state["jobs_hash"] != jobs_hash:
        running = [b["id"] for b in state["batches"] if client.batches.retrieve(b["id"]).status not in BATCH_DONE]
        if running:
            result_json(False, error=f"{jobs_path} changed while batches {', '.join(running)} still run: "
                                     f"wait for them (rerun with the old file) or cancel them before resubmitting")
            sys.exit(1)
        state = None

    if state is None:
        groups: dict[tuple[str, str], list[str]] = {}
        requests_by_group: dict[tuple[str, str], list[str]] = {}
        problems = []
        for i, job in enumerate(jobs):
            try:
                endpoint, body = _image_request(job)
            except ValueError as e:
                problems.append(f"job {i + 1}: {e}")
                continue
            except KeyError as e:
                problems.append(f"job {i + 1}: missing {e}")
                continue
            key = (endpoint, body["model"])  # a batch takes one endpoint and one model
            groups.setdefault(key, []).append(str(i))
            requests_by_group.setdefault(key, []).append(
                json.dumps({"custom_id": str(i), "method": "POST", "url": endpoint, "body": body}))
        if problems:
            result_json(False, error="; ".join(problems))
            sys.exit(1)
        state = {"jobs_hash": jobs_hash, "batches": []}
        for (endpoint, model), lines_out in requests_by_group.items():
            data = ("\n".join(lines_out) + "\n").encode()
            upload = client.files.create(file=(f"{jobs_path.stem}.jsonl", io.BytesIO(data)), purpose="batch")
            batch = client.batches.create(input_file_id=upload.id, endpoint=endpoint, completion_window="24h")
            state["batches"].append({"id": batch.id, "endpoint": endpoint, "model": model,
                                     "jobs": groups[(endpoint, model)]})
            print(f"Submitted {batch.id}: {len(lines_out)} image(s), {model} {endpoint}", file=sys.stderr)
        state_path.write_text(json.dumps(state, indent=1))

    seen = {}
    while True:
        try:
            batches = [client.batches.retrieve(b["id"]) for b in state["batches"]]
        except (openai.APIConnectionError, openai.InternalServerError) as e:
            print(f"Status check failed, retrying: {e}", file=sys.stderr)
            time.sleep(args.poll)
            continue
        for b in batches:
            c = b.request_counts
            status = f"{b.status} {c.completed + c.failed}/{c.total}" if c else b.status
            if seen.get(b.id) != status:
                print(f"{b.id}: {status}", file=sys.stderr)
                seen[b.id] = status
        if all(b.status in BATCH_DONE for b in batches) or args.no_wait:
            break
        time.sleep(args.poll)

    if not all(b.status in BATCH_DONE for b in batches):
        result_json(True, state=str(state_path), status={b.id: seen[b.id] for b in batches},
                    note=f"still running; rerun `batch {args.jobs}` to wait and collect")
        return

    results: dict[str, dict] = {}
    for b in batches:
        for file_id in (b.output_file_id, b.error_file_id):
            if not file_id:
                continue
            for line in client.files.content(file_id).text.splitlines():
                row = json.loads(line)
                job = jobs[int(row["custom_id"])]
                resp = row.get("response") or {}
                body = resp.get("body") or {}
                if resp.get("status_code") == 200 and body.get("data"):
                    extra = _save_image(body, Path(job["o"]), bool(job.get("transparent")))
                    results[row["custom_id"]] = {"ok": True, "path": job["o"],
                                                 "cost_cents": _image_cents(body.get("usage"), batch=True), **extra}
                else:
                    err = (body.get("error") or row.get("error") or {}).get("message", "no image returned")
                    results[row["custom_id"]] = {"ok": False, "path": job["o"], "error": err}
        if b.status != "completed":  # failed validation, expired or cancelled: its unfinished jobs get the reason
            for custom_id in next(s for s in state["batches"] if s["id"] == b.id)["jobs"]:
                results.setdefault(custom_id, {"ok": False, "path": jobs[int(custom_id)]["o"],
                                               "error": f"batch {b.status}: {_batch_errors(b)}"})
    images = [results.get(str(i), {"ok": False, "path": job["o"], "error": "missing from batch output"})
              for i, job in enumerate(jobs)]
    total = round(sum(r.get("cost_cents", 0) for r in images), 2)
    state["images"] = images  # a rerun reports these instead of overwriting files edited since
    state_path.write_text(json.dumps(state, indent=1))
    print(f"Saved {sum(r['ok'] for r in images)}/{len(images)} image(s)", file=sys.stderr)
    result_json(all(r["ok"] for r in images), cost_cents=total, images=images)


def cmd_video(args):
    cost = args.duration * VIDEO_COSTS_PER_SEC[args.resolution] + 1
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
            generate_audio=False,
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
    result_json(True, path=str(output), cost_cents=_billed_cents(resp, cost))


# --- Audio (Gemini TTS, Lyria) ---

TTS_MODEL = "gemini-3.8-flash-tts"
# USD per 1M tokens: (text in, audio out), 25 audio tokens per second. Introductory prices, doubled from 2027-01-01.
TTS_USD_PER_M = {"gemini-3.8-flash-tts": (0.50, 9.00), "gemini-3.8-flash-lite-tts": (0.50, 6.00)}
TTS_TURN = re.compile(r"^([^:()]+?)\s*(?:\(([^)]*)\))?:\s*(.+)$")  # Name (style): text

MUSIC_MODELS = {"clip": ("lyria-3-clip-preview", 4), "song": ("lyria-3.5", 8)}  # (model, cents per call)
AUDIO_EXTS = {".wav", ".ogg", ".mp3", ".flac"}


def _check_audio_output(output: Path):
    if output.suffix.lower() not in AUDIO_EXTS:
        result_json(False, error=f"Unsupported audio extension {output.suffix!r}: use {', '.join(sorted(AUDIO_EXTS))}")
        sys.exit(1)
    output.parent.mkdir(parents=True, exist_ok=True)


def _ffmpeg_convert(src: Path, dst: Path):
    """Transcode with ffmpeg; codec follows dst's extension (ogg -> Vorbis)."""
    codec = {".ogg": ["-c:a", "libvorbis", "-q:a", "6"], ".mp3": ["-c:a", "libmp3lame", "-q:a", "2"],
             ".wav": ["-c:a", "pcm_s16le"], ".flac": ["-c:a", "flac"]}[dst.suffix.lower()]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *codec, str(dst)], check=True)


def _tts_cents(model: str, usage) -> float:
    """Cost from the token usage the API reports; thinking tokens billed as output."""
    if not usage:
        return 0.0
    usd_in, usd_out = TTS_USD_PER_M.get(model.removeprefix("models/"), TTS_USD_PER_M[TTS_MODEL])
    if date.today() >= date(2027, 1, 1):
        usd_in, usd_out = 2 * usd_in, 2 * usd_out
    out_tokens = (usage.total_output_tokens or 0) + (usage.total_thought_tokens or 0)
    return round(((usage.total_input_tokens or 0) * usd_in + out_tokens * usd_out) / 1e4, 3)


def _save_wav(wav: bytes, output: Path) -> float:
    """Write WAV bytes to output (transcoding by extension); return the duration in seconds."""
    with wave.open(io.BytesIO(wav)) as w:
        seconds = w.getnframes() / w.getframerate()
    if output.suffix.lower() == ".wav":
        output.write_bytes(wav)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "speech.wav"
            src.write_bytes(wav)
            _ffmpeg_convert(src, output)
    return round(seconds, 2)


def _speech_turns(args, text: str) -> tuple[list, dict | list]:
    """Transcript -> (content turns, speech_config). Dialogue lines are `Name: text` or `Name (style): text`."""
    def turn(line: str, speaker: str | None = None, style: str | None = None) -> dict:
        item: dict = {"type": "text", "text": line.strip()}
        meta = {k: v for k, v in (("speaker", speaker), ("style", style)) if v}
        if meta:
            item["annotations"] = [{"type": "speech_metadata", **meta}]
        return item

    if not args.speakers:
        return [turn(text, style=args.style)], [{"voice": args.voice}]
    pairs = [s.split("=", 1) for s in args.speakers.split(",")]
    if len(pairs) != 2 or any(len(p) != 2 or not p[0].strip() or not p[1].strip() for p in pairs):
        result_json(False, error="--speakers takes 2 NAME=VOICE pairs, e.g. 'Hero=Puck,Goblin=voice_abc123'")
        sys.exit(1)
    voices = {n.strip(): v.strip() for n, v in pairs}
    turns = []
    for line in filter(None, map(str.strip, text.splitlines())):
        m = TTS_TURN.match(line)
        if not m or m.group(1) not in voices:
            result_json(False, error=f"Dialogue line must start with {' or '.join(voices)} and a colon: {line!r}")
            sys.exit(1)
        turns.append(turn(m.group(3), m.group(1), m.group(2) or args.style))
    config = {"mode": "conversational", "speakers": [{"speaker": n, "voice": v} for n, v in voices.items()]}
    return turns, config


def _gemini() -> genai.Client:
    """TTS, voices and Lyria are served only on v1beta; google-genai defaults the Gemini API to v1."""
    if os.environ.get("GOOGLE_GENAI_API_VERSION"):
        return genai.Client()
    return genai.Client(http_options=types.HttpOptions(api_version="v1beta"))


def cmd_speech(args):
    output = Path(args.output)
    _check_audio_output(output)
    text = Path(args.text_file).read_text() if args.text_file else args.text
    if not text or not text.strip():
        result_json(False, error="Empty text: pass --text or --text-file")
        sys.exit(1)
    turns, speech_config = _speech_turns(args, text)

    label = f"speakers {args.speakers}" if args.speakers else f"voice {args.voice}"
    print(f"Generating speech ({args.model}, {label})...", file=sys.stderr)
    client = _gemini()
    try:
        resp = client.interactions.create(
            model=args.model, input=[{"type": "user_input", "content": turns}],
            response_format={"type": "audio"},
            # passed raw: the SDK's typed speech_config drops "mode"
            extra_body={"generation_config": {"speech_config": speech_config}})
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)
    cents = _tts_cents(args.model, resp.usage)
    if resp.output_audio is None or not resp.output_audio.data:
        result_json(False, error=f"No audio returned (status: {resp.status})", cost_cents=cents)
        sys.exit(1)

    seconds = _save_wav(base64.b64decode(resp.output_audio.data), output)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=cents, seconds=seconds)


def cmd_voice_design(args):
    output = Path(args.output)
    _check_audio_output(output)
    voice: dict = {"model": args.model, "type": "prompted", "display_name": args.name, "prompted": {"input": args.prompt}}
    if args.gender:
        voice["gender"] = args.gender
    if args.language:
        voice["language_code"] = args.language

    print(f"Designing voice {args.name!r} ({args.model})...", file=sys.stderr)
    client = _gemini()  # keep a reference: a temporary Client closes its connection before the call
    try:
        created = client.voices.create(store=True, voice=voice)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)
    cents = _tts_cents(args.model, created.usage)
    extra = {"voice": created.id, "expires": created.expire_time.date().isoformat() if created.expire_time else None}
    if not created.sample_audio or not created.sample_audio.data:
        result_json(False, error="Voice created but no sample audio returned", cost_cents=cents, **extra)
        sys.exit(1)
    seconds = _save_wav(base64.b64decode(created.sample_audio.data), output)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=cents, seconds=seconds, **extra)


def cmd_voice_list(args):
    filters = {"page_size": args.limit}
    for key, value in (("language_code", args.language), ("gender", args.gender), ("pitch", args.pitch)):
        if value:
            filters[key] = value.split(",")
    if args.search:
        filters["search"] = args.search
    if args.mine:
        filters["type_"] = ["prompted", "replicated"]
    client = _gemini()
    try:
        resp = client.voices.list(**filters)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)
    for voice in resp.voices or []:
        row = {
            "voice": voice.id, "name": voice.display_name, "language": voice.language_code, "accent": voice.accent,
            "gender": voice.gender, "pitch": voice.pitch, "description": voice.description,
            "prompt": voice.prompted.input if voice.prompted else None,
            "expires": voice.expire_time.date().isoformat() if voice.expire_time else None,
        }
        print(json.dumps({k: v for k, v in row.items() if v}, ensure_ascii=False))


def cmd_voice_delete(args):
    client = _gemini()
    try:
        client.voices.delete(id=args.voice_id)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)
    result_json(True, voice=args.voice_id)


def cmd_music(args):
    output = Path(args.output)
    _check_audio_output(output)
    model, cost = MUSIC_MODELS[args.length]
    contents = []
    if args.image:
        ref_path = Path(args.image)
        if not ref_path.exists():
            result_json(False, error=f"Reference image not found: {ref_path}")
            sys.exit(1)
        contents.append(types.Part.from_bytes(data=ref_path.read_bytes(), mime_type=_mime_for_image(ref_path)))
    contents.append(args.prompt)

    print(f"Generating music ({model})...", file=sys.stderr)
    client = _gemini()  # keep a reference: a temporary Client closes its connection before the call
    try:
        resp = client.models.generate_content(
            model=model, contents=contents,
            config=types.GenerateContentConfig(response_modalities=["AUDIO", "TEXT"]))
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    audio, texts = None, []
    for part in resp.parts or []:
        if part.text:
            texts.append(part.text.strip())
        elif part.inline_data is not None and (part.inline_data.mime_type or "").startswith("audio/"):
            audio = part.inline_data.data
    if not audio:
        reason = resp.candidates[0].finish_reason if resp.candidates else "unknown"
        result_json(False, error=f"No audio returned (reason: {reason})", text="\n".join(texts))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:  # Lyria returns MP3 (44.1 kHz stereo)
        if output.suffix.lower() == ".mp3":
            output.write_bytes(audio)
        else:
            src = Path(tmp) / "music.mp3"
            src.write_bytes(audio)
            _ffmpeg_convert(src, output)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            str(output)], capture_output=True, text=True)
    seconds = round(float(probe.stdout.strip() or 0), 2)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=cost, seconds=seconds, text="\n".join(texts))


def main():
    parser = argparse.ArgumentParser(description="Asset Generator — images (GPT-Image-2.6), video (Grok), speech and music (Gemini, Lyria)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate one image now at the standard rate (GPT-Image-2.6)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("-o", "--output", required=True,
                       help="Output path; the extension picks the format: .png .webp .jpg .gif")
    p_img.add_argument("--model", choices=list(IMAGE_MODELS), default="sunburst",
                       help="sunburst (detail, consistent edits) or flare (fast drafts). Default: sunburst")
    p_img.add_argument("--quality", choices=IMAGE_QUALITIES, default=IMAGE_QUALITY,
                       help=f"Rendering quality. Default: {IMAGE_QUALITY}")
    p_img.add_argument("--size", default=None,
                       help="WIDTHxHEIGHT (multiples of 16, ratio 1:3-3:1, edge <=3840) or auto. "
                            "Default: 1024x1024; auto for GIF (size of each frame)")
    p_img.add_argument("--image", action="append", default=None,
                       help="Reference image (repeat for up to 16); the first is the one edited")
    p_img.add_argument("--transparent", action="store_true", help="Real alpha background (.png/.webp; 1-bit in .gif)")
    p_img.add_argument("--complexity", choices=["low", "medium", "high"], default=None,
                       help="How much the model plans the scene. API default: high")
    p_img.add_argument("--frames", type=int, default=None, help="GIF frame count, 2-16. Default: 9")
    p_img.add_argument("--frame-ms", type=int, default=None, help="GIF delay per frame, 20-2000 ms. Default: 200")
    p_img.set_defaults(func=cmd_image)

    p_bat = sub.add_parser("batch", help="Generate a JSONL list of images via the Batch API at half price")
    p_bat.add_argument("jobs", help="JSONL, one image per line: {\"prompt\", \"o\"} plus any of "
                                    "image (path or list), quality, model, size, transparent, complexity, frames, frame_ms")
    p_bat.add_argument("--quality", choices=IMAGE_QUALITIES, default=IMAGE_QUALITY,
                       help=f"Quality for jobs that don't set one. Default: {IMAGE_QUALITY}")
    p_bat.add_argument("--model", choices=list(IMAGE_MODELS), default="sunburst",
                       help="Model for jobs that don't set one. Default: sunburst")
    p_bat.add_argument("--no-wait", action="store_true",
                       help="Submit (or check) and return; rerun the same command to wait and collect")
    p_bat.add_argument("--poll", type=int, default=15, help="Seconds between status checks. Default: 15")
    p_bat.set_defaults(func=cmd_batch)

    p_vid = sub.add_parser("video", help="Generate MP4 video from prompt + reference image (8¢/sec 480p, 14¢/sec 720p)")
    p_vid.add_argument("--prompt", required=True, help="Video generation prompt")
    p_vid.add_argument("--image", required=True, help="Reference image path (starting frame)")
    p_vid.add_argument("--duration", type=int, required=True, help="Duration in seconds (1-15)")
    p_vid.add_argument("--resolution", choices=["480p", "720p"], default="720p",
                       help="Video resolution. Default: 720p")
    p_vid.add_argument("-o", "--output", required=True, help="Output MP4 path")
    p_vid.set_defaults(func=cmd_video)

    tts_models = list(TTS_USD_PER_M)
    p_sp = sub.add_parser("speech", help="Speak a transcript with Gemini 3.8 TTS (~0.25¢ per 10 s)")
    src = p_sp.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Verbatim transcript with inline <tags>; with --speakers, one 'Name (style): text' per line")
    src.add_argument("--text-file", help="Read the transcript from a file")
    who = p_sp.add_mutually_exclusive_group(required=True)
    who.add_argument("--voice", help="Voice for a single speaker: prebuilt name (Kore), library id, or designed voice_...")
    who.add_argument("--speakers", help="Two-speaker dialogue: 'Name1=Voice1,Name2=Voice2' (names as in the transcript)")
    p_sp.add_argument("--style", help="Short delivery direction for the whole line, e.g. 'whispered urgently'")
    p_sp.add_argument("--model", choices=tts_models, default=TTS_MODEL, help=f"TTS model. Default: {TTS_MODEL}")
    p_sp.add_argument("-o", "--output", required=True, help="Output .wav (24 kHz mono) / .ogg / .mp3 / .flac")
    p_sp.set_defaults(func=cmd_speech)

    p_vo = sub.add_parser("voice", help="Gemini voices: design a character voice, list, delete")
    vsub = p_vo.add_subparsers(dest="voice_command", required=True)
    p_vd = vsub.add_parser("design", help="Create a persistent voice from a description (~2¢, kept 1 year)")
    p_vd.add_argument("--prompt", required=True, help="1-2 sentences: who, age, timbre, texture, accent, baseline attitude")
    p_vd.add_argument("--name", required=True, help="Display name, e.g. the character's name")
    p_vd.add_argument("--gender", choices=["female", "male", "neutral"], default=None)
    p_vd.add_argument("--language", default=None, help="BCP-47 language of the lines, e.g. en-GB, ja-JP")
    p_vd.add_argument("--model", choices=tts_models, default=TTS_MODEL, help=f"Design model. Default: {TTS_MODEL}")
    p_vd.add_argument("-o", "--output", required=True, help="Audition clip the voice speaks in character (~50 s)")
    p_vd.set_defaults(func=cmd_voice_design)
    p_vl = vsub.add_parser("list", help="Browse the voice library and your designed voices (free), one JSON line each")
    p_vl.add_argument("--search", help="Substring of name or description, e.g. 'gravelly', '62-year-old'")
    p_vl.add_argument("--language", help="BCP-47 codes, comma-separated, e.g. ja-JP or en-GB,en-IE")
    p_vl.add_argument("--gender", help="female, male, neutral (comma-separated)")
    p_vl.add_argument("--pitch", help="low, medium, high (comma-separated)")
    p_vl.add_argument("--mine", action="store_true", help="Only voices designed in this project")
    p_vl.add_argument("--limit", type=int, default=50, help="Max voices. Default: 50")
    p_vl.set_defaults(func=cmd_voice_list)
    p_vx = vsub.add_parser("delete", help="Delete a designed voice (a project holds at most 200)")
    p_vx.add_argument("voice_id")
    p_vx.set_defaults(func=cmd_voice_delete)

    p_mu = sub.add_parser("music", help="Generate music with Lyria (clip 4¢ = 30 s, song 8¢ = ~2 min)")
    p_mu.add_argument("--prompt", required=True, help="Music prompt: genre first, instruments, mood, BPM, key, structure")
    p_mu.add_argument("--length", choices=list(MUSIC_MODELS), default="clip",
                      help="clip: lyria-3-clip-preview, always 30 s (4¢). song: lyria-3.5, length set in the prompt (8¢)")
    p_mu.add_argument("--image", default=None, help="Optional reference image to set the mood")
    p_mu.add_argument("-o", "--output", required=True, help="Output .mp3 (native) / .ogg / .wav / .flac")
    p_mu.set_defaults(func=cmd_music)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
