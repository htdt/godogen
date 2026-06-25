"""Abstract base classes for asset generation backends."""

import base64
import io
import json
import sys
from pathlib import Path
from abc import ABC, abstractmethod


def result_json(ok: bool, path: str | None = None, cost_cents: int = 0, error: str | None = None):
    """Standard JSON output format shared by all backends."""
    d = {"ok": ok, "cost_cents": cost_cents}
    if path:
        d["path"] = path
    if error:
        d["error"] = error
    print(json.dumps(d))


def fail(error: str):
    """Print error JSON and exit."""
    result_json(False, error=error)
    sys.exit(1)


def _mime_for_image(path: Path) -> str:
    """Detect image MIME type from file extension."""
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/png")


def _image_data_uri(image_path: Path) -> str:
    """Load image and return as base64 data URI."""
    b64 = base64.b64encode(image_path.read_bytes()).decode()
    mime = _mime_for_image(image_path)
    return f"data:{mime};base64,{b64}"


class ImageBackend(ABC):
    """Abstract base for image generation backends."""
    name: str = ""
    supported_sizes: list[str] = []

    @abstractmethod
    def generate(self, prompt: str, output: Path, size: str,
                 aspect_ratio: str, ref_image: Path | None,
                 check_budget_fn, record_spend_fn) -> None:
        """Generate an image. Must call check_budget_fn before and record_spend_fn after."""
        ...


class VideoBackend(ABC):
    """Abstract base for video generation backends."""
    name: str = ""
    cost_per_sec: int = 0

    @abstractmethod
    def generate(self, prompt: str, ref_image: Path, output: Path,
                 duration: int, resolution: str,
                 check_budget_fn, record_spend_fn) -> None:
        """Generate a video. Must call check_budget_fn before and record_spend_fn after."""
        ...
