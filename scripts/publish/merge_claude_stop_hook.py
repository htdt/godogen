"""Add or refresh the godogen Stop hook entry in Claude Code settings.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


COMMAND = 'python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/stop_post_task_gate.py'
GATE_ENTRY = {
    "type": "command",
    "command": COMMAND,
    "timeout": 60,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: merge_claude_stop_hook.py <settings.json>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {}
    if path.exists():
        raw = path.read_text().strip()
        if raw:
            data = json.loads(raw)
            if not isinstance(data, dict):
                print(f"error: {path} is not a JSON object", file=sys.stderr)
                return 1

    hooks = data.setdefault("hooks", {})
    stop_entries = hooks.setdefault("Stop", [])

    for entry in stop_entries:
        inner = entry.get("hooks") if isinstance(entry, dict) else None
        if not isinstance(inner, list):
            continue
        for idx, hook in enumerate(inner):
            if isinstance(hook, dict) and hook.get("command") == COMMAND:
                inner[idx] = GATE_ENTRY
                path.write_text(json.dumps(data, indent=2) + "\n")
                return 0

    stop_entries.append({"hooks": [GATE_ENTRY]})
    path.write_text(json.dumps(data, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
