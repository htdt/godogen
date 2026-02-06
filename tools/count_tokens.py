#!/usr/bin/env python3
"""Count tokens in a file using Anthropic's tokenizer."""

import sys
from pathlib import Path
from anthropic import Anthropic


def main():
    if len(sys.argv) != 2:
        print("Usage: count_tokens.py <file>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: File '{path}' not found", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    client = Anthropic()
    result = client.messages.count_tokens(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": text}],
    )
    print(result.input_tokens)


if __name__ == "__main__":
    main()
