#!/usr/bin/env python3
"""Visual QA — analyze game screenshots against reference via Gemini 3 Flash.

Two modes:
  Static:  visual_qa.py [--context "..."] reference.png screenshot.png
  Dynamic: visual_qa.py [--context "..."] reference.png frame1.png frame2.png ...

Static mode (2 images): reference + single game screenshot. For static scenes.
Dynamic mode (3+ images): reference + frame sequence at 2 FPS cadence. For motion.

--context: Task context (Goal, Requirements, Verify) for goal verification.
Uses MEDIA_RESOLUTION_HIGH. Requires: GEMINI_API_KEY or GOOGLE_API_KEY.
"""

import sys
from pathlib import Path

from google import genai
from google.genai import types

STATIC_PROMPT = Path(__file__).parent / "static_prompt.md"
DYNAMIC_PROMPT = Path(__file__).parent / "dynamic_prompt.md"


def main():
    args = sys.argv[1:]
    context = None
    if len(args) >= 2 and args[0] == "--context":
        context = args[1]
        args = args[2:]

    if len(args) < 2:
        print(f"Usage: {sys.argv[0]} [--context \"task context\"] <reference.png> <screenshot.png> [frame2.png ...]", file=sys.stderr)
        sys.exit(1)

    paths = [Path(p) for p in args]
    for p in paths:
        if not p.exists():
            print(f"Error: {p} not found", file=sys.stderr)
            sys.exit(1)

    static = len(paths) == 2
    prompt = (STATIC_PROMPT if static else DYNAMIC_PROMPT).read_text()
    if context:
        prompt += f"\n\n## Task Context\n\n{context}\n"

    client = genai.Client()
    contents: list[types.Part | str] = [prompt]

    contents.append("Reference (visual target):")
    contents.append(types.Part.from_bytes(data=paths[0].read_bytes(), mime_type="image/png"))

    if static:
        contents.append("Game screenshot:")
        contents.append(types.Part.from_bytes(data=paths[1].read_bytes(), mime_type="image/png"))
        desc = "static (reference + screenshot)"
    else:
        for i, p in enumerate(paths[1:], 1):
            contents.append(f"Frame {i}:")
            contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))
        desc = f"dynamic (reference + {len(paths) - 1} frames)"

    print(f"Analyzing {desc} with Gemini 3 Flash...", file=sys.stderr)
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contents,  # type: ignore[arg-type]
            config=types.GenerateContentConfig(
                media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
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
