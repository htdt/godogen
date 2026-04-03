#!/usr/bin/env python3
"""Visual QA — analyze game screenshots via Gemini Flash.

Three modes:
  Static:   visual_qa.py [--context "..."] reference.png screenshot.png
  Dynamic:  visual_qa.py [--context "..."] reference.png frame1.png frame2.png ...
  Question: visual_qa.py --question "what's wrong?" screenshot.png [frame2.png ...]

Static mode (2 images): reference + single game screenshot. For static scenes.
Dynamic mode (3+ images): reference + frame sequence at 2 FPS cadence. For motion.
Question mode: free-form question + any number of screenshots. No reference needed.

--context: Task context (Goal, Requirements, Verify) for goal verification.
--question: Free-form question about the screenshots (replaces reference-based modes).
--model: Override model (default: gemini-3-flash).
--log: Path to JSONL log file for debug logging.
Requires: GEMINI_API_KEY or GOOGLE_API_KEY.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import types

PROMPTS_DIR = Path(__file__).parent
STATIC_PROMPT = PROMPTS_DIR / "static_prompt.md"
DYNAMIC_PROMPT = PROMPTS_DIR / "dynamic_prompt.md"
QUESTION_PROMPT = PROMPTS_DIR / "question_prompt.md"

DEFAULT_MODEL = "gemini-3-flash"


def log_entry(log_path, *, mode, model, query, files, output):
    """Append a JSONL log entry."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "model": model,
        "query": query,
        "files": files,
        "output": output,
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    args = sys.argv[1:]
    context = None
    question = None
    model = DEFAULT_MODEL
    log_path = None

    # Parse named flags
    while len(args) >= 2:
        if args[0] == "--context":
            context = args[1]
            args = args[2:]
        elif args[0] == "--question":
            question = args[1]
            args = args[2:]
        elif args[0] == "--model":
            model = args[1]
            args = args[2:]
        elif args[0] == "--log":
            log_path = args[1]
            args = args[2:]
        else:
            break

    if question:
        # Question mode: just screenshots, no reference
        if len(args) < 1:
            print(f"Usage: {sys.argv[0]} --question \"...\" <screenshot.png> [frame2.png ...]", file=sys.stderr)
            sys.exit(1)
        paths = [Path(p) for p in args]
        for p in paths:
            if not p.exists():
                print(f"Error: {p} not found", file=sys.stderr)
                sys.exit(1)

        prompt = QUESTION_PROMPT.read_text()
        prompt += f"\n\n## Question\n\n{question}\n"
        if context:
            prompt += f"\n## Additional Context\n\n{context}\n"

        client = genai.Client()
        contents: list[types.Part | str] = [prompt]

        for i, p in enumerate(paths, 1):
            label = "Screenshot:" if len(paths) == 1 else f"Frame {i}:"
            contents.append(label)
            contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))

        mode = "question"
        query = question
        desc = f"question ({len(paths)} image{'s' if len(paths) != 1 else ''})"
    else:
        # Reference-based modes (static/dynamic)
        if len(args) < 2:
            print(f"Usage: {sys.argv[0]} [--context \"...\"] <reference.png> <screenshot.png> [frame2.png ...]", file=sys.stderr)
            print(f"       {sys.argv[0]} --question \"...\" <screenshot.png> [frame2.png ...]", file=sys.stderr)
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
        contents = [prompt]

        contents.append("Reference (visual target):")
        contents.append(types.Part.from_bytes(data=paths[0].read_bytes(), mime_type="image/png"))

        if static:
            contents.append("Game screenshot:")
            contents.append(types.Part.from_bytes(data=paths[1].read_bytes(), mime_type="image/png"))
            mode = "static"
            desc = "static (reference + screenshot)"
        else:
            for i, p in enumerate(paths[1:], 1):
                contents.append(f"Frame {i}:")
                contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))
            mode = "dynamic"
            desc = f"dynamic (reference + {len(paths) - 1} frames)"

        query = context or ""

    print(f"Analyzing {desc} with {model}...", file=sys.stderr)
    try:
        response = client.models.generate_content(
            model=model,
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

    output = response.text
    print(output)

    if log_path:
        log_entry(log_path, mode=mode, model=model, query=query,
                  files=[str(p) for p in paths], output=output)


if __name__ == "__main__":
    main()
