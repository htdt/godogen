#!/usr/bin/env python3
"""${AGENT_NAME} Stop hook: push the latest proof video to Telegram.

Best-effort. The hook never blocks stop. It silently no-ops when `tg-push` is
unavailable or no result bundle has been produced yet.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root_from(cwd: str) -> Path:
    result = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return Path(cwd).resolve()


def latest_video(project_root: Path) -> tuple[Path, str] | None:
    results_root = project_root / "screenshots" / "result"
    if not results_root.is_dir():
        return None
    numbered: list[tuple[int, Path]] = []
    for child in results_root.iterdir():
        if not child.is_dir():
            continue
        try:
            numbered.append((int(child.name), child))
        except ValueError:
            continue
    if not numbered:
        return None
    numbered.sort(key=lambda pair: pair[0])
    latest = numbered[-1][1]
    video = latest / "video.mp4"
    if not video.is_file():
        return None
    return video, str(latest.relative_to(project_root))


def telegram_ready() -> bool:
    return bool(
        shutil.which("tg-push")
        and os.environ.get("TG_BOT_TOKEN")
        and os.environ.get("TG_CHAT_ID")
    )


def main() -> None:
    event = json.load(sys.stdin)

    if not telegram_ready():
        print(json.dumps({}))
        return

    project_root = repo_root_from(str(event.get("cwd", ".")))
    found = latest_video(project_root)
    if found is None:
        print(json.dumps({}))
        return

    video_path, bundle_rel = found
    subprocess.run(
        ["tg-push", "--text", f"Bundle: {bundle_rel}", "--file", str(video_path)],
        check=False,
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(json.dumps({}))


if __name__ == "__main__":
    main()
