#!/usr/bin/env python3
"""Video QA — send gameplay video to Gemini for motion/animation analysis.

Usage:
  python3 .claude/skills/visual-qa/scripts/video_qa.py [--verify "criteria"] gameplay.mp4

Output: Markdown report to stdout.
Requires: GEMINI_API_KEY or GOOGLE_API_KEY in environment.
"""

import sys
from pathlib import Path

from google import genai
from google.genai import types

PROMPT_FILE = Path(__file__).parent / "video_prompt.md"


def main():
    args = sys.argv[1:]
    verify = None
    if len(args) >= 2 and args[0] == "--verify":
        verify = args[1]
        args = args[2:]

    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} [--verify \"criteria\"] <video.mp4>", file=sys.stderr)
        sys.exit(1)

    video = Path(args[0])
    if not video.exists():
        print(f"Error: {video} not found", file=sys.stderr)
        sys.exit(1)

    size_mb = video.stat().st_size / (1024 * 1024)
    if size_mb > 100:
        print(f"Error: video is {size_mb:.0f}MB — expected <10MB (30s, CRF 28, 720p). Check ffmpeg settings.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(http_options={"api_version": "v1alpha"})
    prompt = PROMPT_FILE.read_text()
    if verify:
        prompt += f"\n\n## Task-Specific Verify Criteria\n\nIn addition to the checks above, verify: {verify}\n"

    video_part = types.Part.from_bytes(data=video.read_bytes(), mime_type="video/mp4")

    print("Analyzing video with Gemini 3 Flash...", file=sys.stderr)
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, video_part],  # type: ignore[arg-type]
            config=types.GenerateContentConfig(
                media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
            ),
        )
    except Exception as e:
        print(f"Error: Gemini API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not response.text:
        print("Error: Gemini returned no text (possible safety block)", file=sys.stderr)
        sys.exit(1)

    print(response.text)


if __name__ == "__main__":
    main()
