"""xAI Grok image and video generation backends."""

import io
import sys
from pathlib import Path

import requests
import xai_sdk
from PIL import Image

from .base import ImageBackend, VideoBackend, _image_data_uri, fail, result_json

GROK_MODEL = "grok-imagine-image"
GROK_COST = 2
GROK_SIZES = ["1K", "2K"]
GROK_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
    "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20", "auto",
]

VIDEO_MODEL = "grok-imagine-video"
VIDEO_COST_PER_SEC = 5  # cents


class GrokImageBackend(ImageBackend):
    name = "grok"
    supported_sizes = GROK_SIZES

    def get_cost(self, size: str) -> int:
        return GROK_COST

    def generate(self, prompt: str, output: Path, size: str,
                 aspect_ratio: str, ref_image: Path | None,
                 check_budget_fn, record_spend_fn) -> None:
        if size not in self.supported_sizes:
            fail(f"Grok does not support size {size}. Use: {', '.join(self.supported_sizes)}")

        cost = GROK_COST
        check_budget_fn(cost)
        output.parent.mkdir(parents=True, exist_ok=True)

        label = f"grok {size} {aspect_ratio}"
        if ref_image:
            label += " (image-to-image)"
        print(f"Generating image ({label})...", file=sys.stderr)

        image_url = None
        if ref_image:
            ref_path = Path(ref_image)
            if not ref_path.exists():
                fail(f"Reference image not found: {ref_path}")
            image_url = _image_data_uri(ref_path)

        try:
            client = xai_sdk.Client()
            resp = client.image.sample(
                prompt=prompt,
                model=GROK_MODEL,
                image_url=image_url,
                aspect_ratio=aspect_ratio,
                resolution=size.lower(),
            )
            # xAI returns JPEG; convert to real PNG
            img = Image.open(io.BytesIO(resp.image))
            img.save(output, format="PNG")
        except Exception as e:
            fail(str(e))

        print(f"Saved: {output}", file=sys.stderr)
        record_spend_fn(cost, "xai")
        result_json(True, path=str(output), cost_cents=cost)


class GrokVideoBackend(VideoBackend):
    name = "grok"
    cost_per_sec = VIDEO_COST_PER_SEC

    def generate(self, prompt: str, ref_image: Path, output: Path,
                 duration: int, resolution: str,
                 check_budget_fn, record_spend_fn) -> None:
        cost = duration * VIDEO_COST_PER_SEC
        check_budget_fn(cost)
        output.parent.mkdir(parents=True, exist_ok=True)

        if not ref_image.exists():
            fail(f"Reference image not found: {ref_image}")

        print(f"Generating {duration}s video ({resolution})...", file=sys.stderr)
        image_url = _image_data_uri(ref_image)

        try:
            client = xai_sdk.Client()
            resp = client.video.generate(
                prompt=prompt,
                model=VIDEO_MODEL,
                image_url=image_url,
                duration=duration,
                aspect_ratio="1:1",
                resolution=resolution,
            )
            # Download MP4
            print("  Downloading video...", file=sys.stderr)
            dl = requests.get(resp.url, timeout=120)
            dl.raise_for_status()
            output.write_bytes(dl.content)
        except Exception as e:
            fail(str(e))

        print(f"Saved: {output}", file=sys.stderr)
        record_spend_fn(cost, "xai-video")
        result_json(True, path=str(output), cost_cents=cost)
