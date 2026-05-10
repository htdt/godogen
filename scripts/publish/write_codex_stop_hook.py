"""Write the Godogen Stop hook in current Codex config.toml syntax."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


COMMAND = 'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/stop_post_task_gate.py"'
STATUS_MESSAGE = "Pushing latest proof video to Telegram"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: write_codex_stop_hook.py <config.toml>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)

    text = f"""[features]
hooks = true

[[hooks.Stop]]
[[hooks.Stop.hooks]]
type = "command"
command = '{COMMAND}'
statusMessage = "{STATUS_MESSAGE}"
timeout = 60
"""

    tomllib.loads(text)
    path.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
