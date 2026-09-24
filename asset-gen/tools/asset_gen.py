#!/usr/bin/env python3
"""Asset Generator CLI - creates images, videos, speech and music (Gemini / xAI Grok / Lyria).

Subcommands:
  image     Generate a PNG from a prompt (Gemini 5-15¢ or Grok 6-8¢)
  video     Generate MP4 video from prompt + reference image (8-14¢/sec, Grok)
  speech    Speak a directed transcript with Gemini TTS (~0.5¢ per 10 s line)
  music     Generate music with Lyria (4¢ per 30 s clip, 8¢ per song)

3D models come from the `tripo` CLI (see api.md), not from here.

Output: JSON to stdout. Progress to stderr.
"""

import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

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


# --- Image backends ---

GEMINI_MODEL = "gemini-3.1-flash-image"
GEMINI_SIZES = ["512", "1K", "2K", "4K"]
GEMINI_COSTS = {"512": 5, "1K": 7, "2K": 10, "4K": 15}
GEMINI_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]

GROK_MODEL = "grok-imagine-image-2.0"
GROK_QUALITY = "medium"
GROK_SIZES = ["1K", "2K"]
GROK_COSTS = {"1K": 6, "2K": 8}  # medium quality; xAI's billed cost_usd is reported when present
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


def _billed_cents(resp, estimate: int) -> int:
    """Cost xAI reports for the request, else the price-table estimate."""
    usd = resp.cost_usd
    return round(usd * 100) if usd else estimate


def _default_backend() -> str | None:
    """Gemini when its key is set (faster, same quality), else Grok."""
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("XAI_API_KEY"):
        return "grok"
    return None


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
            quality=GROK_QUALITY,
        )
        # xAI returns JPEG; convert to real PNG
        img = Image.open(io.BytesIO(resp.image))
        img.save(output, format="PNG")
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=_billed_cents(resp, cost))


def cmd_image(args):
    backend = args.model or _default_backend()
    size = args.size

    if backend is None:
        result_json(False, error="No image API key: set GEMINI_API_KEY (or GOOGLE_API_KEY) or XAI_API_KEY")
        sys.exit(1)

    if backend == "gemini":
        if size not in GEMINI_SIZES:
            result_json(False, error=f"Gemini does not support size {size}. Use: {', '.join(GEMINI_SIZES)}")
            sys.exit(1)
        cost = GEMINI_COSTS[size]
    else:
        if size not in GROK_SIZES:
            result_json(False, error=f"Grok does not support size {size}. Use: {', '.join(GROK_SIZES)}")
            sys.exit(1)
        cost = GROK_COSTS[size]

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

TTS_MODEL = "gemini-3.1-flash-tts-preview"
TTS_USD_PER_M = {"input": 1.00, "output": 20.00}  # text in, audio out
TTS_VOICES = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", "Callirrhoe", "Autonoe",
    "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina", "Erinome", "Algenib", "Rasalgethi",
    "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird", "Zubenelgenubi",
    "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]
TTS_ATTEMPTS = 3  # the model sometimes emits text instead of audio and the request fails; retrying fixes it

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


def _speech_config(args) -> types.SpeechConfig:
    def voice(name: str) -> types.VoiceConfig:
        match = next((v for v in TTS_VOICES if v.lower() == name.lower()), None)
        if not match:
            result_json(False, error=f"Unknown voice {name!r}. Voices: {', '.join(TTS_VOICES)}")
            sys.exit(1)
        return types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=match))

    if args.speakers:
        pairs = [s.split("=", 1) for s in args.speakers.split(",")]
        if len(pairs) > 2 or any(len(p) != 2 or not p[0].strip() for p in pairs):
            result_json(False, error="--speakers takes up to 2 NAME=VOICE pairs, e.g. 'Hero=Puck,Witch=Gacrux'")
            sys.exit(1)
        return types.SpeechConfig(multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[types.SpeakerVoiceConfig(speaker=n.strip(), voice_config=voice(v.strip()))
                                   for n, v in pairs]))
    return types.SpeechConfig(voice_config=voice(args.voice))


def cmd_speech(args):
    output = Path(args.output)
    _check_audio_output(output)
    text = Path(args.text_file).read_text() if args.text_file else args.text
    if not text or not text.strip():
        result_json(False, error="Empty text: pass --text or --text-file")
        sys.exit(1)
    config = types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=_speech_config(args))
    client = genai.Client()

    label = f"speakers {args.speakers}" if args.speakers else f"voice {args.voice}"
    print(f"Generating speech ({args.model}, {label})...", file=sys.stderr)
    pcm, rate, cents, last_error = None, 24000, 0.0, "no audio returned"
    for attempt in range(1, TTS_ATTEMPTS + 1):
        try:
            resp = client.models.generate_content(model=args.model, contents=text, config=config)
            usage = resp.usage_metadata
            if usage:
                cents += ((usage.prompt_token_count or 0) * TTS_USD_PER_M["input"]
                          + (usage.candidates_token_count or 0) * TTS_USD_PER_M["output"]) / 1e4
            for part in resp.parts or []:
                if part.inline_data is not None and (part.inline_data.mime_type or "").startswith("audio/"):
                    pcm = part.inline_data.data
                    m = re.search(r"rate=(\d+)", part.inline_data.mime_type or "")
                    rate = int(m.group(1)) if m else 24000
                    break
            if pcm:
                break
            reason = resp.candidates[0].finish_reason if resp.candidates else "unknown"
            last_error = f"no audio returned (finish reason: {reason})"
        except Exception as e:
            last_error = str(e)
        print(f"  attempt {attempt} failed: {last_error}", file=sys.stderr)
        time.sleep(2 * attempt)
    if not pcm:
        result_json(False, error=last_error, cost_cents=round(cents, 2))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = output if output.suffix.lower() == ".wav" else Path(tmp) / "speech.wav"
        with wave.open(str(wav_path), "wb") as w:  # raw 16-bit little-endian mono PCM
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes(pcm)
        if wav_path != output:
            _ffmpeg_convert(wav_path, output)
    seconds = round(len(pcm) / (2 * rate), 2)
    print(f"Saved: {output}", file=sys.stderr)
    result_json(True, path=str(output), cost_cents=round(cents, 2), seconds=seconds)


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
    client = genai.Client()  # keep a reference: a temporary Client closes its connection before the call
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
    parser = argparse.ArgumentParser(description="Asset Generator — images, videos, speech and music (Gemini / xAI Grok / Lyria)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image (Gemini 5-15¢ or Grok 6-8¢)")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument("--model", choices=["gemini", "grok"], default=None,
                       help="Backend: gemini (5-15¢, ~10s) or grok (6-8¢, 1-2 min); same quality. "
                            "Default: gemini if GEMINI_API_KEY/GOOGLE_API_KEY is set, else grok.")
    p_img.add_argument("--size", choices=ALL_SIZES, default="1K",
                       help="Resolution. Grok: 1K, 2K. Gemini: 512, 1K, 2K, 4K. Default: 1K.")
    p_img.add_argument("--aspect-ratio", choices=ALL_ASPECT_RATIOS, default="1:1",
                       help="Aspect ratio. Default: 1:1")
    p_img.add_argument("--image", default=None, help="Reference image for image-to-image edit")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_vid = sub.add_parser("video", help="Generate MP4 video from prompt + reference image (8¢/sec 480p, 14¢/sec 720p)")
    p_vid.add_argument("--prompt", required=True, help="Video generation prompt")
    p_vid.add_argument("--image", required=True, help="Reference image path (starting frame)")
    p_vid.add_argument("--duration", type=int, required=True, help="Duration in seconds (1-15)")
    p_vid.add_argument("--resolution", choices=["480p", "720p"], default="720p",
                       help="Video resolution. Default: 720p")
    p_vid.add_argument("-o", "--output", required=True, help="Output MP4 path")
    p_vid.set_defaults(func=cmd_video)

    p_sp = sub.add_parser("speech", help="Speak a directed transcript with Gemini TTS (~0.5¢ per 8 s)")
    src = p_sp.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Full TTS prompt: optional direction, then the transcript (audio tags allowed)")
    src.add_argument("--text-file", help="Read the prompt from a file")
    who = p_sp.add_mutually_exclusive_group(required=True)
    who.add_argument("--voice", help="Prebuilt voice for a single speaker, e.g. Kore")
    who.add_argument("--speakers", help="Two-speaker dialogue: 'Name1=Voice1,Name2=Voice2' (names as in the transcript)")
    p_sp.add_argument("--model", default=TTS_MODEL, help=f"TTS model. Default: {TTS_MODEL}")
    p_sp.add_argument("-o", "--output", required=True, help="Output .wav (24 kHz mono) / .ogg / .mp3 / .flac")
    p_sp.set_defaults(func=cmd_speech)

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
