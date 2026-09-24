#!/usr/bin/env python3
"""Cut a seamless loop out of a music or ambience file.

Takes `length` seconds from `start`, then equal-power crossfades the audio that follows the cut into the
loop's head, so the end flows back into the start with no click or gap. The result loops in any engine
with plain looping on — no loop points needed.

    loop_audio.py track.mp3 --bpm 120 --bars 8 -o loop.ogg            # 8 bars of 4/4 = 16 s
    loop_audio.py track.mp3 --bpm 120 --bars 8 --start-bars 2 -o loop.ogg   # skip a 2-bar intro
    loop_audio.py rain.wav --start 1 --length 20 -o rain_loop.ogg

Needs ffmpeg/ffprobe. Output: JSON to stdout ({"ok", "path", "start", "length", "xfade"}).
"""

import argparse
import json
import subprocess
import sys
from typing import NoReturn

import numpy as np


def fail(msg: str) -> NoReturn:
    print(json.dumps({"ok": False, "error": msg}))
    sys.exit(1)


def probe(path: str) -> tuple[int, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                          "stream=sample_rate,channels", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    rate, channels = out.split(",")[:2]
    return int(rate), int(channels)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True, help="Output .ogg / .wav / .mp3 / .flac")
    ap.add_argument("--start", type=float, default=0.0, help="Loop start in seconds (default 0)")
    ap.add_argument("--length", type=float, help="Loop length in seconds")
    ap.add_argument("--bpm", type=float, help="Tempo; with --bars sets the length (4/4)")
    ap.add_argument("--bars", type=int, help="Loop length in bars (needs --bpm)")
    ap.add_argument("--start-bars", type=int, help="Loop start in bars (needs --bpm), overrides --start")
    ap.add_argument("--beats-per-bar", type=int, default=4)
    ap.add_argument("--xfade", type=float, default=0.5, help="Crossfade seconds (default 0.5)")
    args = ap.parse_args()

    bar = args.beats_per_bar * 60.0 / args.bpm if args.bpm else None
    length = args.bars * bar if (bar and args.bars) else args.length
    start = args.start_bars * bar if (bar and args.start_bars is not None) else args.start
    if not length or length <= 0:
        fail("give --length, or --bpm with --bars")

    try:
        rate, channels = probe(args.input)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", args.input, "-f", "f32le", "-acodec", "pcm_f32le", "-"],
                             capture_output=True, check=True).stdout
    except (subprocess.CalledProcessError, ValueError) as e:
        fail(f"cannot read {args.input}: {e}")
    audio = np.frombuffer(raw, dtype=np.float32).reshape(-1, channels)

    s, n, x = int(start * rate), int(length * rate), int(args.xfade * rate)
    if s + n + x > len(audio):
        fail(f"need {start + length + args.xfade:.2f} s of audio from the start of the loop, "
             f"input is {len(audio) / rate:.2f} s — shorten --length/--bars or move --start earlier")
    loop = audio[s:s + n].copy()
    t = np.linspace(0.0, 1.0, x, dtype=np.float32)[:, None]
    loop[:x] = audio[s:s + x] * np.sqrt(t) + audio[s + n:s + n + x] * np.sqrt(1.0 - t)

    codec = {".ogg": ["-c:a", "libvorbis", "-q:a", "6"], ".mp3": ["-c:a", "libmp3lame", "-q:a", "2"],
             ".wav": ["-c:a", "pcm_s16le"], ".flac": ["-c:a", "flac"]}
    ext = args.output[args.output.rfind("."):].lower()
    if ext not in codec:
        fail(f"unsupported output extension {ext!r}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(rate), "-ac", str(channels), "-i", "-",
                    *codec[ext], args.output], input=loop.tobytes(), check=True)
    print(json.dumps({"ok": True, "path": args.output, "start": round(start, 3), "length": round(length, 3),
                      "xfade": args.xfade}))


if __name__ == "__main__":
    main()
