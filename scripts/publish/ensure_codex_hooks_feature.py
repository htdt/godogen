"""Ensure `[features] codex_hooks = true` is present in Codex config.toml."""

from __future__ import annotations

import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: ensure_codex_hooks_feature.py <config.toml>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)

    text = path.read_text() if path.exists() else ""
    if not text.strip():
        path.write_text("[features]\ncodex_hooks = true\n")
        return 0

    lines = text.splitlines()
    features_start = next(
        (i for i, line in enumerate(lines) if line.strip() == "[features]"),
        None,
    )

    if features_start is None:
        suffix = "" if text.endswith("\n") else "\n"
        path.write_text(text + suffix + "[features]\ncodex_hooks = true\n")
        return 0

    features_end = len(lines)
    for i in range(features_start + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            features_end = i
            break

    for i in range(features_start + 1, features_end):
        stripped = lines[i].lstrip()
        if stripped.startswith("codex_hooks"):
            indent = lines[i][: len(lines[i]) - len(stripped)]
            lines[i] = f"{indent}codex_hooks = true"
            path.write_text("\n".join(lines) + "\n")
            return 0

    lines.insert(features_start + 1, "codex_hooks = true")
    path.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
