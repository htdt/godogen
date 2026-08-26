"""DashScope helpers for Wan image and video generation."""

import base64
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

API_BASE = os.environ.get("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/api/v1")


def _api_key() -> str:
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    return key


def _headers(async_task: bool = False) -> dict[str, str]:
    headers = {"Authorization": f"Bearer {_api_key()}", "Content-Type": "application/json"}
    if async_task:
        headers["X-DashScope-Async"] = "enable"
    return headers


def image_data_uri(image_path: Path) -> str:
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(
        image_path.suffix.lower(), "image/png"
    )
    data = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _find_url(value: object, extensions: tuple[str, ...]) -> str | None:
    if isinstance(value, str):
        path = urlparse(value).path.lower()
        return value if path.endswith(extensions) else None
    if isinstance(value, dict):
        for item in value.values():
            found = _find_url(item, extensions)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_url(item, extensions)
            if found:
                return found
    return None


def _submit(payload: dict, endpoint: str) -> dict:
    response = requests.post(f"{API_BASE}{endpoint}", headers=_headers(async_task=True), json=payload, timeout=60)
    if not response.ok:
        raise RuntimeError(f"DashScope submit failed: HTTP {response.status_code}: {response.text}")
    return response.json()


def _wait_for_task(task_id: str, timeout: int = 900, interval: int = 5) -> dict:
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        response = requests.get(f"{API_BASE}/tasks/{task_id}", headers=_headers(), timeout=60)
        if not response.ok:
            raise RuntimeError(f"DashScope task query failed: HTTP {response.status_code}: {response.text}")
        data = response.json()
        status = str(data.get("output", {}).get("task_status", "")).upper()
        if status in {"SUCCEEDED", "SUCCESS"}:
            return data
        if status in {"FAILED", "CANCELED", "CANCELLED", "UNKNOWN"}:
            raise RuntimeError(f"DashScope task {task_id} {status}: {data}")
        time.sleep(interval)
    raise TimeoutError(f"DashScope task {task_id} timed out after {timeout}s")


def _download(url: str, output_path: Path) -> Path:
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return output_path


def generate_image(prompt: str, output_path: Path, *, size: str, aspect_ratio: str, reference: Path | None = None) -> str:
    content: list[dict[str, str]] = [{"text": prompt}]
    if reference:
        content.insert(0, {"image": image_data_uri(reference)})
    payload = {
        "model": os.environ.get("WAN_IMAGE_MODEL", "wan2.7-image"),
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": {"size": size, "aspect_ratio": aspect_ratio, "watermark": False},
    }
    submitted = _submit(payload, "/services/aigc/multimodal-generation/generation")
    task_id = submitted.get("output", {}).get("task_id")
    result = _wait_for_task(task_id) if task_id else submitted
    image_url = _find_url(result.get("output", {}), (".png", ".jpg", ".jpeg", ".webp"))
    if not image_url:
        raise RuntimeError(f"DashScope returned no image URL: {result}")
    _download(image_url, output_path)
    return task_id or "synchronous"


def generate_video(prompt: str, image_path: Path, output_path: Path, *, duration: int, resolution: str) -> str:
    payload = {
        "model": os.environ.get("WAN_VIDEO_MODEL", "wan2.7-i2v-2026-04-25"),
        "input": {"prompt": prompt, "img_url": image_data_uri(image_path)},
        "parameters": {"duration": duration, "size": resolution, "watermark": False},
    }
    submitted = _submit(payload, "/services/aigc/video-generation/video-synthesis")
    task_id = submitted.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"DashScope returned no task id: {submitted}")
    result = _wait_for_task(task_id)
    video_url = _find_url(result.get("output", {}), (".mp4", ".mov", ".webm"))
    if not video_url:
        raise RuntimeError(f"DashScope returned no video URL: {result}")
    _download(video_url, output_path)
    return task_id
