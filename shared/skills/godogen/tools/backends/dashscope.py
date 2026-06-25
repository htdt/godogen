"""Alibaba DashScope (Tongyi Wanxiang) image and video generation backends."""

import json
import os
import sys
import time
from pathlib import Path

import requests

from .base import ImageBackend, VideoBackend, fail, result_json

# DashScope API configuration
DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
DASHSCOPE_VIDEO_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis"
DASHSCOPE_TASK_URL = "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

# Image models
DASHSCOPE_IMAGE_MODELS = {
    "wan2.1-t2i-turbo": {"cost_cents": 2, "desc": "Fast (~2s)"},
    "wan2.1-t2i-plus": {"cost_cents": 5, "desc": "High quality (~10s)"},
}
DASHSCOPE_DEFAULT_IMAGE_MODEL = "wan2.1-t2i-turbo"

# Size mapping (CLI size -> DashScope size)
DASHSCOPE_SIZE_MAP = {
    "512": "512*512",
    "1K": "1024*1024",
    "2K": "1280*1280",
    "4K": "1280*1280",  # DashScope max is 1280
}
DASHSCOPE_SIZES = ["512", "1K", "2K", "4K"]

# Video models
DASHSCOPE_VIDEO_MODEL = "wanx2.1-t2v-turbo"
DASHSCOPE_VIDEO_COST_PER_SEC = 3  # cents (~0.2 RMB/s)


def _get_api_key() -> str:
    """Get DashScope API key from environment."""
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        fail("DASHSCOPE_API_KEY environment variable is not set. "
             "Get your key from: https://bailian.console.aliyun.com/")
    return key


def _submit_image_task(prompt: str, model: str, size: str, n: int = 1) -> str:
    """Submit an image generation task. Returns task_id."""
    api_key = _get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    payload = {
        "model": model,
        "input": {
            "prompt": prompt,
        },
        "parameters": {
            "size": size,
            "n": n,
        },
    }
    resp = requests.post(DASHSCOPE_API_URL, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        fail(f"DashScope API error {resp.status_code}: {resp.text}")
    data = resp.json()
    task_id = data.get("output", {}).get("task_id")
    if not task_id:
        fail(f"No task_id in response: {data}")
    return task_id


def _poll_task(task_id: str, timeout: int = 300) -> dict:
    """Poll task until completion. Returns output dict."""
    api_key = _get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    url = DASHSCOPE_TASK_URL.format(task_id=task_id)

    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            fail(f"Poll error {resp.status_code}: {resp.text}")
        data = resp.json()
        status = data.get("output", {}).get("task_status")
        if status == "SUCCEEDED":
            return data.get("output", {})
        elif status == "FAILED":
            msg = data.get("output", {}).get("message", "Unknown error")
            fail(f"DashScope task failed: {msg}")
        # Still running, wait and retry
        time.sleep(3)

    fail(f"Task {task_id} timed out after {timeout}s")


def _download_image(url: str, output: Path) -> None:
    """Download image from URL and save as PNG."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    # Save as PNG (DashScope returns PNG data)
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(resp.content))
    img.save(output, format="PNG")


class DashScopeImageBackend(ImageBackend):
    name = "dashscope"
    supported_sizes = DASHSCOPE_SIZES

    def get_cost(self, size: str) -> int:
        model = os.environ.get("DASHSCOPE_IMAGE_MODEL", DASHSCOPE_DEFAULT_IMAGE_MODEL)
        return DASHSCOPE_IMAGE_MODELS.get(model, DASHSCOPE_IMAGE_MODELS[DASHSCOPE_DEFAULT_IMAGE_MODEL])["cost_cents"]

    def generate(self, prompt: str, output: Path, size: str,
                 aspect_ratio: str, ref_image: Path | None,
                 check_budget_fn, record_spend_fn) -> None:
        if size not in self.supported_sizes:
            fail(f"DashScope does not support size {size}. Use: {', '.join(self.supported_sizes)}")

        cost = self.get_cost(size)
        check_budget_fn(cost)
        output.parent.mkdir(parents=True, exist_ok=True)

        model = os.environ.get("DASHSCOPE_IMAGE_MODEL", DASHSCOPE_DEFAULT_IMAGE_MODEL)
        ds_size = DASHSCOPE_SIZE_MAP[size]

        label = f"dashscope/{model} {size}"
        if ref_image:
            label += " (image-to-image)"
        print(f"Generating image ({label})...", file=sys.stderr)

        if ref_image:
            # Image-to-image: use reference image with prompt
            self._generate_img2img(prompt, ref_image, output, model, ds_size)
        else:
            # Text-to-image
            self._generate_txt2img(prompt, output, model, ds_size)

        print(f"Saved: {output}", file=sys.stderr)
        record_spend_fn(cost, "dashscope")
        result_json(True, path=str(output), cost_cents=cost)

    def _generate_txt2img(self, prompt: str, output: Path, model: str, size: str) -> None:
        """Text-to-image generation."""
        task_id = _submit_image_task(prompt, model, size)
        print(f"  Task submitted: {task_id}", file=sys.stderr)

        result = _poll_task(task_id)
        results = result.get("results", [])
        if not results:
            fail("No images in DashScope response")

        img_url = results[0].get("url")
        if not img_url:
            fail(f"No URL in result: {results[0]}")

        _download_image(img_url, output)

    def _generate_img2img(self, prompt: str, ref_image: Path, output: Path,
                          model: str, size: str) -> None:
        """Image-to-image generation using reference image."""
        api_key = _get_api_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        }

        # Upload reference image as base64
        import base64
        img_data = base64.b64encode(ref_image.read_bytes()).decode()
        ref_url = f"data:image/png;base64,{img_data}"

        payload = {
            "model": model,
            "input": {
                "prompt": prompt,
                "ref_img": ref_url,
            },
            "parameters": {
                "size": size,
                "n": 1,
            },
        }
        resp = requests.post(DASHSCOPE_API_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            fail(f"DashScope img2img error {resp.status_code}: {resp.text}")
        data = resp.json()
        task_id = data.get("output", {}).get("task_id")
        if not task_id:
            fail(f"No task_id in response: {data}")

        print(f"  Task submitted: {task_id}", file=sys.stderr)
        result = _poll_task(task_id)
        results = result.get("results", [])
        if not results:
            fail("No images in DashScope response")

        img_url = results[0].get("url")
        if not img_url:
            fail(f"No URL in result: {results[0]}")

        _download_image(img_url, output)


class DashScopeVideoBackend(VideoBackend):
    name = "dashscope"
    cost_per_sec = DASHSCOPE_VIDEO_COST_PER_SEC

    def generate(self, prompt: str, ref_image: Path, output: Path,
                 duration: int, resolution: str,
                 check_budget_fn, record_spend_fn) -> None:
        cost = duration * DASHSCOPE_VIDEO_COST_PER_SEC
        check_budget_fn(cost)
        output.parent.mkdir(parents=True, exist_ok=True)

        if not ref_image.exists():
            fail(f"Reference image not found: {ref_image}")

        print(f"Generating {duration}s video (DashScope {resolution})...", file=sys.stderr)

        api_key = _get_api_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        }

        # Upload reference image as base64
        import base64
        img_data = base64.b64encode(ref_image.read_bytes()).decode()
        ref_url = f"data:image/png;base64,{img_data}"

        payload = {
            "model": DASHSCOPE_VIDEO_MODEL,
            "input": {
                "prompt": prompt,
                "img_url": ref_url,
            },
            "parameters": {
                "duration": duration,
                "resolution": resolution,
            },
        }

        resp = requests.post(DASHSCOPE_VIDEO_API_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            fail(f"DashScope video API error {resp.status_code}: {resp.text}")
        data = resp.json()
        task_id = data.get("output", {}).get("task_id")
        if not task_id:
            fail(f"No task_id in response: {data}")

        print(f"  Task submitted: {task_id}", file=sys.stderr)

        # Poll for video completion
        result = _poll_task(task_id, timeout=600)  # Video takes longer
        video_url = result.get("video_url")
        if not video_url:
            # Try results array
            results = result.get("results", [])
            if results:
                video_url = results[0].get("url")
        if not video_url:
            fail(f"No video URL in result: {result}")

        # Download video
        print("  Downloading video...", file=sys.stderr)
        dl = requests.get(video_url, timeout=120)
        dl.raise_for_status()
        output.write_bytes(dl.content)

        print(f"Saved: {output}", file=sys.stderr)
        record_spend_fn(cost, "dashscope-video")
        result_json(True, path=str(output), cost_cents=cost)
