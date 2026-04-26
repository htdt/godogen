"""Inject Claude lookup-skill frontmatter (context/model/agent) into SKILL.md."""

from __future__ import annotations

import sys
from pathlib import Path


CLAUDE_KEYS = ("context:", "model:", "agent:")
INJECTED = ("context: fork", "model: sonnet", "agent: Explore")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: inject_claude_lookup_frontmatter.py <SKILL.md>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    text = path.read_text()
    if not text.startswith("---\n"):
        return 0
    end = text.find("\n---", 4)
    if end == -1:
        return 0

    frontmatter = text[4:end]
    body = text[end:]

    keep = [
        line for line in frontmatter.splitlines()
        if not any(line.lstrip().startswith(key) for key in CLAUDE_KEYS)
    ]
    keep.extend(INJECTED)
    path.write_text("---\n" + "\n".join(keep) + body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
