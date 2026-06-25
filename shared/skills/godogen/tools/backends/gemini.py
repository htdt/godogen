"""Google Gemini image generation backend."""

import io
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from .base import ImageBackend, _mime_for_image, fail, result_json

GEMINI_MODEL = "gemini-3.1-flash-image-preview"
GEMINI_SIZES = ["512", "1K", "2K", "4K"]
GEMINI_COSTS = {"512": 5, "1K": 7, "2K": 10, "4K": 15}
GEMINI_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]


class GeminiBackend(ImageBackend):
    name = "gemini"
    supported_sizes = GEMINI_SIZES
    costs = GEMINI_COSTS

    def get_cost(self, size: str) -> int:
        return self.costs[size]

    def generate(self, prompt: str, output: Path, size: str,
                 aspect_ratio: str, ref_image: Path | None,
                 check_budget_fn, record_spend_fn) -> None:
        if size not in self.supported_sizes:
            fail(f"Gemini does not support size {size}. Use: {', '.join(self.supported_sizes)}")

        cost = self.get_cost(size)
        check_budget_fn(cost)

        output.parent.mkdir(parents=True, exist_ok=True)

        label = f"gemini {size} {aspect_ratio}"
        if ref_image:
            label += " (image-to-image)"
        print(f"Generating image ({label})...", file=sys.stderr)

        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                image_size=size,
                aspect_ratio=aspect_ratio,
            ),
        )

        contents = []
        if ref_image:
            ref_path = Path(ref_image)
            if not ref_path.exists():
                fail(f"Reference image not found: {ref_path}")
            contents.append(types.Part.from_bytes(
                data=ref_path.read_bytes(),
                mime_type=_mime_for_image(ref_path)
            ))
        contents.append(prompt)

        client = genai.Client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=config,
        )

        if response.parts is None:
            reason = "unknown"
            if response.candidates and response.candidates[0].finish_reason:
                reason = response.candidates[0].finish_reason
            fail(f"Generation blocked (reason: {reason})")

        for part in response.parts:
            if part.inline_data is not None:
                img = Image.open(io.BytesIO(part.inline_data.data))
                img.save(output, format="PNG")
                print(f"Saved: {output}", file=sys.stderr)
                record_spend_fn(cost, "gemini")
                result_json(True, path=str(output), cost_cents=cost)
                return

        fail("No image returned")
