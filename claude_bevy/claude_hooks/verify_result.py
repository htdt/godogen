#!/usr/bin/env python3
"""Verify the latest final result bundle with Gemini Flash."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

DEFAULT_MODEL = "gemini-flash-latest"
DEFAULT_REVIEW_FPS = 5.0
DEFAULT_MAX_FRAMES = 150
MIN_DURATION_SECONDS = 15.0
MAX_DURATION_SECONDS = 30.0
DURATION_TOLERANCE_SECONDS = 0.5
REQUIRED_VIDEO_FPS = 30.0
VIDEO_FPS_TOLERANCE = 0.5

PROMPT_PATH = Path(__file__).with_name("verify_result_prompt.md")


class VerificationIssue(BaseModel):
    title: str
    type: Literal[
        "style mismatch",
        "visual bug",
        "logical inconsistency",
        "motion anomaly",
        "placeholder",
    ]
    severity: Literal["major", "minor", "note"]
    frames: str
    location: str
    description: str


class VerificationVerdict(BaseModel):
    verdict: Literal["pass", "fail"]
    goal_assessment: str
    issues: list[VerificationIssue] = Field(default_factory=list)
    summary: str


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def natural_sort_key(path: Path) -> list[object]:
    parts: list[object] = []
    current = ""
    for char in path.name:
        if char.isdigit():
            current += char
            continue
        if current:
            parts.append(int(current))
            current = ""
        parts.append(char)
    if current:
        parts.append(int(current))
    return parts


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def list_result_dirs(results_root: Path) -> list[Path]:
    if not results_root.is_dir():
        return []
    result_dirs: list[Path] = []
    for child in results_root.iterdir():
        if not child.is_dir():
            continue
        try:
            int(child.name)
        except ValueError:
            continue
        result_dirs.append(child)
    return sorted(result_dirs, key=lambda path: int(path.name))


def load_video_metadata(video_path: Path) -> tuple[float, float]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=avg_frame_rate",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(video_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")

    payload = json.loads(result.stdout)
    duration_raw = payload.get("format", {}).get("duration")
    streams = payload.get("streams") or []
    fps_raw = streams[0].get("avg_frame_rate") if streams else None

    if not duration_raw:
        raise RuntimeError("ffprobe did not report video duration")
    if not fps_raw or fps_raw in {"0/0", "0"}:
        raise RuntimeError("ffprobe did not report a usable video frame rate")

    numerator, denominator = fps_raw.split("/", 1) if "/" in fps_raw else (fps_raw, "1")
    fps = float(numerator) / float(denominator)
    duration = float(duration_raw)
    if fps <= 0 or duration <= 0:
        raise RuntimeError("video metadata reported a non-positive duration or fps")
    return fps, duration


def select_review_frames(
    frames: list[Path],
    video_fps: float,
    review_fps: float,
    max_frames: int,
) -> tuple[list[Path], list[float]]:
    if not frames:
        return [], []
    if len(frames) <= max_frames or review_fps <= 0 or video_fps <= 0:
        timestamps = [index / video_fps for index in range(len(frames))]
        return frames, timestamps

    duration_seconds = len(frames) / video_fps
    sample_times = [0.0]
    interval_seconds = 1.0 / review_fps
    next_time = interval_seconds
    while next_time < duration_seconds and len(sample_times) < max_frames - 1:
        sample_times.append(next_time)
        next_time += interval_seconds
    sample_times.append(max(duration_seconds - (1.0 / video_fps), 0.0))

    selected_frames: list[Path] = []
    selected_times: list[float] = []
    seen_indexes: set[int] = set()
    for sample_time in sample_times:
        frame_index = int(round(sample_time * video_fps))
        frame_index = max(0, min(frame_index, len(frames) - 1))
        if frame_index in seen_indexes:
            continue
        seen_indexes.add(frame_index)
        selected_frames.append(frames[frame_index])
        selected_times.append(frame_index / video_fps)

    if selected_frames[-1] != frames[-1]:
        if len(selected_frames) >= max_frames:
            selected_frames[-1] = frames[-1]
            selected_times[-1] = (len(frames) - 1) / video_fps
        else:
            selected_frames.append(frames[-1])
            selected_times.append((len(frames) - 1) / video_fps)

    return selected_frames, selected_times


def build_metadata(project_root: Path, review_fps: float, max_frames: int) -> dict[str, object]:
    results_root = project_root / "screenshots" / "result"
    task_path = project_root / "task.md"
    if not task_path.is_file():
        return {
            "ok": False,
            "status": "missing_task",
            "message": "task.md is missing at project root; write the original task literal there.",
            "task_path": str(task_path),
            "task_path_rel": "task.md",
        }
    task_text = task_path.read_text().strip()
    if not task_text:
        return {
            "ok": False,
            "status": "missing_task",
            "message": "task.md at project root is empty; write the original task literal there.",
            "task_path": str(task_path),
            "task_path_rel": "task.md",
        }

    result_dirs = list_result_dirs(results_root)
    if not result_dirs:
        return {
            "ok": False,
            "status": "missing_result",
            "message": "No numeric directories exist under screenshots/result.",
            "results_root": str(results_root),
        }

    result_dir = result_dirs[-1]
    video_path = result_dir / "video.mp4"
    task_add_path = result_dir / "task_add.md"
    frames = sorted(result_dir.glob("frame*.png"), key=natural_sort_key)

    if not video_path.is_file():
        return {
            "ok": False,
            "status": "invalid_result",
            "message": f"{video_path.relative_to(project_root)} is missing.",
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }
    if not frames:
        return {
            "ok": False,
            "status": "invalid_result",
            "message": f"{result_dir.relative_to(project_root)} does not contain any frame*.png files.",
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }

    task_add_text: str | None = None
    task_add_sha: str | None = None
    if task_add_path.is_file():
        candidate = task_add_path.read_text().strip()
        if candidate:
            task_add_text = candidate
            task_add_sha = hashlib.sha256(candidate.encode("utf-8")).hexdigest()

    try:
        video_fps, duration_seconds = load_video_metadata(video_path)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "status": "invalid_result",
            "message": f"Could not read video timing from {video_path.relative_to(project_root)}: {exc}",
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }

    raw_frame_rate = len(frames) / duration_seconds
    if abs(raw_frame_rate - video_fps) / max(video_fps, 0.001) > 0.15:
        return {
            "ok": False,
            "status": "invalid_result",
            "message": (
                f"Raw frames and video timing disagree for {result_dir.relative_to(project_root)}: "
                f"{len(frames)} frame(s), video fps {video_fps:.3f}, duration {duration_seconds:.3f}s."
            ),
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }

    if (
        duration_seconds < MIN_DURATION_SECONDS - DURATION_TOLERANCE_SECONDS
        or duration_seconds > MAX_DURATION_SECONDS + DURATION_TOLERANCE_SECONDS
    ):
        return {
            "ok": False,
            "status": "invalid_result",
            "message": (
                f"video.mp4 in {result_dir.relative_to(project_root)} is "
                f"{duration_seconds:.2f}s; the final proof must be "
                f"{MIN_DURATION_SECONDS:.0f}-{MAX_DURATION_SECONDS:.0f}s long."
            ),
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }

    if abs(video_fps - REQUIRED_VIDEO_FPS) > VIDEO_FPS_TOLERANCE:
        return {
            "ok": False,
            "status": "invalid_result",
            "message": (
                f"video.mp4 in {result_dir.relative_to(project_root)} is encoded at "
                f"{video_fps:.3f} fps; the final proof must be exactly "
                f"{REQUIRED_VIDEO_FPS:.0f} fps so it plays back smoothly."
            ),
            "result_dir": str(result_dir),
            "result_index": int(result_dir.name),
        }

    selected_frames, selected_times = select_review_frames(frames, video_fps, review_fps, max_frames)
    task_sha = hashlib.sha256(task_text.encode("utf-8")).hexdigest()
    video_sha = sha256_file(video_path)

    reference_path = project_root / "reference.png"
    reference_str: str | None = None
    reference_rel: str | None = None
    reference_sha: str | None = None
    if reference_path.is_file():
        reference_str = str(reference_path)
        reference_rel = str(reference_path.relative_to(project_root))
        reference_sha = sha256_file(reference_path)

    current_index = int(result_dir.name)
    previous_verify: dict[str, object] | None = None
    if current_index > 1:
        prev_verify_path = results_root / str(current_index - 1) / "verify.json"
        if prev_verify_path.is_file():
            try:
                previous_verify = json.loads(prev_verify_path.read_text())
            except json.JSONDecodeError:
                previous_verify = None

    fingerprint = hashlib.sha256(
        "\n".join(
            [
                result_dir.name,
                task_sha,
                task_add_sha or "no-task-add",
                video_sha,
                str(len(frames)),
                f"{video_fps:.6f}",
                reference_sha or "no-reference",
            ]
        ).encode("utf-8")
    ).hexdigest()

    return {
        "ok": True,
        "status": "ready",
        "project_root": str(project_root),
        "result_dir": str(result_dir),
        "result_dir_rel": str(result_dir.relative_to(project_root)),
        "result_index": current_index,
        "video_path": str(video_path),
        "video_path_rel": str(video_path.relative_to(project_root)),
        "task_path": str(task_path),
        "task_path_rel": str(task_path.relative_to(project_root)),
        "task_text": task_text,
        "task_add_path": str(task_add_path) if task_add_text else None,
        "task_add_path_rel": str(task_add_path.relative_to(project_root)) if task_add_text else None,
        "task_add_text": task_add_text,
        "task_add_sha256": task_add_sha,
        "frame_count": len(frames),
        "selected_frame_count": len(selected_frames),
        "selected_frames": [str(frame) for frame in selected_frames],
        "selected_frames_rel": [str(frame.relative_to(project_root)) for frame in selected_frames],
        "selected_frame_times": selected_times,
        "video_fps": video_fps,
        "review_fps": review_fps,
        "duration_seconds": duration_seconds,
        "raw_frame_rate": raw_frame_rate,
        "task_sha256": task_sha,
        "video_sha256": video_sha,
        "reference_path": reference_str,
        "reference_path_rel": reference_rel,
        "reference_sha256": reference_sha,
        "previous_verify": previous_verify,
        "fingerprint": fingerprint,
    }


def load_verdict(response: object) -> VerificationVerdict:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, VerificationVerdict):
        return parsed

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no JSON text")
    return VerificationVerdict.model_validate(json.loads(text))


def _format_previous_verify(previous_verify: dict[str, object]) -> str:
    prev_index = str(previous_verify.get("result_index", "")).strip()
    prev_verdict = str(previous_verify.get("verdict", "")).strip().lower() or "n/a"
    prev_summary = str(previous_verify.get("summary", "")).strip()
    prev_issues_raw = previous_verify.get("issues") or []
    prev_issues: list[str] = []
    for issue in prev_issues_raw[:8]:
        if not isinstance(issue, dict):
            continue
        sev = str(issue.get("severity", "note")).upper()
        title = str(issue.get("title", "Issue"))
        frames = str(issue.get("frames", "")).strip()
        description = str(issue.get("description", "")).strip()
        frames_part = f" ({frames})" if frames else ""
        desc_part = f": {description}" if description else ""
        prev_issues.append(f"- [{sev}] {title}{frames_part}{desc_part}")

    header = f"## Previous Verify Context (bundle {prev_index}, verdict: {prev_verdict})"
    lines: list[str] = [header, ""]
    if prev_summary:
        lines.append(f"Summary: {prev_summary}")
        lines.append("")
    if prev_issues:
        lines.append("Issues previously flagged:")
        lines.extend(prev_issues)
    else:
        lines.append("(no prior issues were recorded)")
    return "\n".join(lines)


def verify_result(metadata: dict[str, object], model: str) -> dict[str, object]:
    reference_path_value = metadata.get("reference_path")
    has_reference = bool(reference_path_value)
    task_add_text = metadata.get("task_add_text")
    previous_verify = metadata.get("previous_verify")

    prompt = PROMPT_PATH.read_text().strip()
    prompt += "\n\n## Task (Original)\n\n"
    prompt += str(metadata["task_text"]).strip()
    if task_add_text:
        prompt += (
            "\n\n## Focus of This Attempt\n\n"
            "This bundle is scoped to the slice below, narrower than the original task.\n\n"
        )
        prompt += str(task_add_text).strip()
    if isinstance(previous_verify, dict):
        prompt += "\n\n" + _format_previous_verify(previous_verify)
    prompt += "\n\n## Sampling Metadata\n\n"
    prompt += f"- Source bundle: {metadata['result_dir_rel']}\n"
    prompt += f"- Source video fps: {float(metadata['video_fps']):.3f} (required: {REQUIRED_VIDEO_FPS:.0f})\n"
    prompt += f"- Source video duration: {float(metadata['duration_seconds']):.3f}s (expected window: {MIN_DURATION_SECONDS:.0f}-{MAX_DURATION_SECONDS:.0f}s)\n"
    prompt += f"- Review fps: {float(metadata['review_fps']):.3f}\n"
    prompt += f"- Raw frame count: {int(metadata['frame_count'])}\n"
    prompt += f"- Selected frame count: {int(metadata['selected_frame_count'])}\n"
    prompt += f"- Reference image: {'attached as Reference' if has_reference else 'none'}\n"

    contents: list[types.Part | str] = [prompt]
    project_root = Path(str(metadata["project_root"]))
    selected_frames = [Path(path) for path in metadata["selected_frames"]]
    selected_times = [float(value) for value in metadata["selected_frame_times"]]

    if has_reference:
        reference_path = Path(str(reference_path_value))
        contents.append(f"Reference ({reference_path.name}):")
        contents.append(types.Part.from_bytes(data=reference_path.read_bytes(), mime_type="image/png"))

    for index, frame_path in enumerate(selected_frames, start=1):
        frame_time = selected_times[index - 1]
        contents.append(f"Frame {index} ({frame_path.name}, source time ~{frame_time:.2f}s):")
        contents.append(types.Part.from_bytes(data=frame_path.read_bytes(), mime_type="image/png"))

    client = genai.Client()
    response = client.models.generate_content(
        model=model,
        contents=contents,  # type: ignore[arg-type]
        config=types.GenerateContentConfig(
            media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
            response_mime_type="application/json",
            response_schema=VerificationVerdict,
            temperature=0.1,
        ),
    )

    verdict = load_verdict(response)
    verify_path = Path(str(metadata["result_dir"])) / "verify.json"
    metadata_for_payload = {key: value for key, value in metadata.items() if key != "previous_verify"}
    payload = {
        "ok": True,
        "status": "verified",
        "verified_at": iso_now(),
        "model": model,
        **metadata_for_payload,
        "verdict": verdict.verdict,
        "goal_assessment": verdict.goal_assessment,
        "issues": [issue.model_dump() for issue in verdict.issues],
        "summary": verdict.summary,
        "verify_path": str(verify_path),
        "verify_path_rel": str(verify_path.relative_to(project_root)),
    }
    verify_path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the latest final result bundle.")
    parser.add_argument("--project-root", default=".", help="Project root containing screenshots/result/")
    parser.add_argument("--metadata-only", action="store_true", help="Only inspect bundle metadata; skip Gemini.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--review-fps",
        type=float,
        default=DEFAULT_REVIEW_FPS,
        help=f"Frame cadence to send to Gemini (default: {DEFAULT_REVIEW_FPS})",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=DEFAULT_MAX_FRAMES,
        help=f"Maximum number of frames to send to Gemini (default: {DEFAULT_MAX_FRAMES})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()

    try:
        metadata = build_metadata(project_root, args.review_fps, args.max_frames)
        if args.metadata_only or not metadata.get("ok"):
            print(json.dumps(metadata))
            return
        print(json.dumps(verify_result(metadata, args.model)))
    except Exception as exc:  # noqa: BLE001
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "error",
                    "message": str(exc),
                    "project_root": str(project_root),
                }
            )
        )


if __name__ == "__main__":
    main()
