#!/usr/bin/env python3
"""Visual QA — send reference image + 6 game screenshots to Gemini for quality analysis.

Usage:
  python3 .claude/skills/visual-qa/scripts/visual_qa.py [--verify "criteria"] reference.png c1..c4.png d1.png d2.png

Image 1: reference (visual target). Frames 2-5: consecutive from mid-capture (motion).
Frames 6-7: diverse locations. Output: Markdown report to stdout.
Requires: GEMINI_API_KEY or GOOGLE_API_KEY in environment.
"""

import sys
from pathlib import Path

from google import genai
from google.genai import types

PROMPT_FILE = Path(__file__).parent / "prompt.md"


def main():
    args = sys.argv[1:]
    verify = None
    if len(args) >= 2 and args[0] == "--verify":
        verify = args[1]
        args = args[2:]

    if len(args) != 7:
        print(f"Usage: {sys.argv[0]} [--verify \"criteria\"] <reference.png> <consec1..4.png> <diverse1..2.png>", file=sys.stderr)
        sys.exit(1)

    paths = [Path(p) for p in args]
    for p in paths:
        if not p.exists():
            print(f"Error: {p} not found", file=sys.stderr)
            sys.exit(1)

    client = genai.Client()

    prompt = PROMPT_FILE.read_text()
    if verify:
        prompt += f"\n\n## Task-Specific Verify Criteria\n\nIn addition to the checks above, verify: {verify}\n"

    labels = [
        "Reference (visual target):",
        "Frame 1 (consecutive):", "Frame 2 (consecutive):",
        "Frame 3 (consecutive):", "Frame 4 (consecutive):",
        "Frame 5 (diverse):", "Frame 6 (diverse):",
    ]
    contents: list[types.Part | str] = [prompt]
    for label, p in zip(labels, paths):
        contents.append(label)
        contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))

    print("Analyzing reference + 6 frames with Gemini 3 Flash...", file=sys.stderr)
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contents,  # type: ignore[arg-type]
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
