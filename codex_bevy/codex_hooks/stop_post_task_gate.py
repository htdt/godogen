#!/usr/bin/env python3
"""Codex Stop hook for post-task visual verification."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_RETRIES = 10


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def load_json(path: Path, default: dict[str, object]) -> dict[str, object]:
    if not path.is_file():
        return dict(default)
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return dict(default)


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["updated_at"] = iso_now()
    path.write_text(json.dumps(payload, indent=2) + "\n")


def run_verify(project_root: Path, metadata_only: bool) -> dict[str, object]:
    command = [
        "python3",
        str(project_root / ".codex" / "hooks" / "verify_result.py"),
        "--project-root",
        str(project_root),
    ]
    if metadata_only:
        command.append("--metadata-only")

    result = subprocess.run(command, capture_output=True, text=True, cwd=project_root, check=False)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "Verifier command failed."
        return {"ok": False, "status": "error", "message": message}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "ok": False,
            "status": "error",
            "message": f"Verifier returned invalid JSON: {result.stdout.strip()}",
        }


def allow_stop(message: str) -> dict[str, object]:
    return {
        "systemMessage": message,
        "stopReason": message,
    }


def block(reason: str) -> dict[str, object]:
    return {
        "decision": "block",
        "reason": reason,
    }


def next_result_hint(meta: dict[str, object]) -> str:
    index = int(meta.get("result_index", 0)) + 1
    return f"screenshots/result/{index}"


def summarize_issues(issues: list[dict[str, object]], limit: int = 4) -> str:
    lines: list[str] = []
    for issue in issues[:limit]:
        severity = str(issue.get("severity", "note")).upper()
        title = str(issue.get("title", "Issue"))
        frames = str(issue.get("frames", "")).strip()
        location = str(issue.get("location", "")).strip()
        description = str(issue.get("description", "")).strip()
        details: list[str] = []
        if frames:
            details.append(f"frames: {frames}")
        if location:
            details.append(f"location: {location}")
        detail_prefix = f" ({'; '.join(details)})" if details else ""
        if description:
            lines.append(f"- [{severity}] {title}{detail_prefix}: {description}")
        else:
            lines.append(f"- [{severity}] {title}{detail_prefix}")
    return "\n".join(lines)


def build_missing_task_reason(meta: dict[str, object]) -> str:
    details = str(meta.get("message", "task.md is missing at project root.")).strip()
    return (
        "Before stopping, write `task.md` at the project root containing the original task "
        "literal verbatim (no commentary, notes, or headers).\n\n"
        f"Blocker: {details}"
    )


def build_missing_reason(meta: dict[str, object]) -> str:
    target_dir = next_result_hint(meta)
    details = str(meta.get("message", "No valid result bundle is available.")).strip()
    return (
        f"Before stopping, write a fresh final proof bundle at `{target_dir}/`:\n"
        "- `video.mp4` (30 fps, 15-30s, encoded from the stored frames)\n"
        "- raw `frameXXX.png` files used to encode that video\n"
        "- `task_add.md` only if this bundle proves a slice narrower than the root `task.md`\n\n"
        f"Blocker: {details}"
    )


def build_retry_reason(verify: dict[str, object]) -> str:
    next_dir = f"screenshots/result/{int(verify['result_index']) + 1}"
    issues = summarize_issues(list(verify.get("issues", [])))
    summary = str(verify.get("summary", "")).strip()

    lines = [f"Proof bundle `{verify['result_dir_rel']}` failed visual verification."]
    if issues:
        lines.extend(["", "Issues:", issues])
    elif summary:
        lines.extend(["", summary])
    lines.extend(["", f"Fix these, then write a fresh bundle at `{next_dir}/`."])
    return "\n".join(lines)


def telegram_ready() -> bool:
    return bool(
        shutil.which("tg-push")
        and os.environ.get("TG_BOT_TOKEN")
        and os.environ.get("TG_CHAT_ID")
    )


def send_telegram_result(verify: dict[str, object]) -> None:
    if not telegram_ready():
        return

    summary = str(verify.get("summary", "")).strip()
    caption_lines = [
        f"Verdict: {str(verify.get('verdict', 'unknown')).upper()}",
        f"Summary: {summary}",
    ]
    caption = "\n".join(caption_lines)
    if len(caption) > 950:
        caption = caption[:947] + "..."

    subprocess.run(
        [
            "tg-push",
            "--text",
            caption,
            "--file",
            str(verify["video_path"]),
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    event = json.load(sys.stdin)
    project_root = repo_root_from(str(event.get("cwd", ".")))
    state_path = project_root / ".codex" / "hooks" / "state" / f"{event.get('session_id', 'default')}.json"
    state = load_json(
        state_path,
        {
            "last_fingerprint": None,
            "last_verdict": None,
            "retry_count": 0,
            "missing_count": 0,
        },
    )

    if not event.get("stop_hook_active"):
        state["retry_count"] = 0
        state["missing_count"] = 0

    meta = run_verify(project_root, metadata_only=True)
    if not meta.get("ok"):
        if meta.get("status") == "error":
            message = (
                "Visual gate could not run the verifier and is allowing stop: "
                f"{meta.get('message', 'unknown verifier error')}"
            )
            state["last_verdict"] = "error"
            save_json(state_path, state)
            print(json.dumps(allow_stop(message)))
            return

        missing_count = int(state.get("missing_count", 0)) + 1
        state["missing_count"] = missing_count
        state["last_verdict"] = str(meta.get("status"))
        save_json(state_path, state)

        if event.get("stop_hook_active") or missing_count >= 2:
            message = (
                "Visual gate stopped retrying because the latest proof bundle is still missing or invalid: "
                f"{meta.get('message', 'unknown error')}"
            )
            print(json.dumps(allow_stop(message)))
            return

        if meta.get("status") == "missing_task":
            print(json.dumps(block(build_missing_task_reason(meta))))
        else:
            print(json.dumps(block(build_missing_reason(meta))))
        return

    state["missing_count"] = 0
    current_fingerprint = str(meta.get("fingerprint"))
    last_fingerprint = state.get("last_fingerprint")
    last_verdict = state.get("last_verdict")

    if current_fingerprint == last_fingerprint:
        if last_verdict == "pass":
            print(json.dumps({}))
            return

        message = (
            "Visual gate already reviewed the unchanged latest proof bundle "
            f"({meta.get('result_dir_rel')}) and got `{last_verdict}`. "
            "Stopping to avoid an infinite retry loop."
        )
        print(json.dumps(allow_stop(message)))
        return

    verify = run_verify(project_root, metadata_only=False)
    if not verify.get("ok"):
        state["last_verdict"] = str(verify.get("status", "error"))
        save_json(state_path, state)
        message = (
            "Visual gate could not verify the latest proof bundle and is allowing stop: "
            f"{verify.get('message', 'unknown verifier error')}"
        )
        print(json.dumps(allow_stop(message)))
        return

    state["last_fingerprint"] = verify["fingerprint"]
    state["last_verdict"] = verify["verdict"]
    send_telegram_result(verify)

    if verify["verdict"] == "pass":
        state["retry_count"] = 0
        save_json(state_path, state)
        print(json.dumps({}))
        return

    retry_count = int(state.get("retry_count", 0)) + 1
    state["retry_count"] = retry_count
    save_json(state_path, state)

    if retry_count >= MAX_RETRIES:
        message = (
            f"Visual gate failed on {verify['result_dir_rel']} and exhausted its retry budget. "
            f"Latest summary: {verify.get('summary', '')}"
        )
        print(json.dumps(allow_stop(message)))
        return

    print(json.dumps(block(build_retry_reason(verify))))


if __name__ == "__main__":
    main()
