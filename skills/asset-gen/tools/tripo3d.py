"""Tripo3D API client for image-to-3D model conversion.

API docs: https://platform.tripo3d.ai/docs/generation

Model versions:
- Turbo-v1.0-20250506: Fast generation
- v3.0-20250812: Latest, supports geometry_quality=detailed (Ultra Mode)
- v2.5-20250123: Default in API
"""

import os
import time
from pathlib import Path

import requests

API_BASE = "https://api.tripo3d.ai/v2/openapi"

# Model version constants
MODEL_TURBO = "Turbo-v1.0-20250506"
MODEL_V3 = "v3.0-20250812"
MODEL_V25 = "v2.5-20250123"


def get_api_key() -> str:
    key = os.environ.get("TRIPO3D_API_KEY")
    if not key:
        raise ValueError("TRIPO3D_API_KEY environment variable not set")
    return key


def create_task(
    image_path: Path,
    model_version: str = MODEL_V3,
    face_limit: int | None = None,
    smart_low_poly: bool = False,
    texture_quality: str = "standard",
    geometry_quality: str = "standard",
) -> str:
    """Create image-to-model task, returns task_id.

    Args:
        image_path: Path to input image
        model_version: API model version (MODEL_V3, MODEL_TURBO, etc)
        face_limit: Max faces (1000-20000 for smart_low_poly, adaptive if None)
        smart_low_poly: Hand-crafted low-poly topology (better for game assets)
        texture_quality: "standard" or "detailed"
        geometry_quality: "standard" or "detailed" (Ultra Mode, v3.0+ only)
    """
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    # Upload image first
    upload_url = f"{API_BASE}/upload"
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/png")}
        resp = requests.post(upload_url, headers=headers, files=files)
        resp.raise_for_status()
        upload_data = resp.json()

    image_token = upload_data["data"]["image_token"]

    # Create task
    task_url = f"{API_BASE}/task"
    payload = {
        "type": "image_to_model",
        "model_version": model_version,
        "file": {"type": "png", "file_token": image_token},
        "texture": True,
        "pbr": True,
    }

    if face_limit is not None:
        payload["face_limit"] = face_limit
    if smart_low_poly:
        payload["smart_low_poly"] = True
    if texture_quality != "standard":
        payload["texture_quality"] = texture_quality
    # geometry_quality only valid for v3.0+
    if geometry_quality != "standard" and "v3.0" in model_version:
        payload["geometry_quality"] = geometry_quality

    resp = requests.post(task_url, headers=headers, json=payload)
    resp.raise_for_status()
    task_data = resp.json()

    return task_data["data"]["task_id"]


def poll_task(task_id: str, timeout: int = 300, interval: int = 5) -> dict:
    """Poll task until completion, returns task result."""
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{API_BASE}/task/{task_id}"

    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()["data"]

        status = data["status"]
        if status == "success":
            return data
        elif status in ("failed", "cancelled", "unknown"):
            raise RuntimeError(f"Task {task_id} failed with status: {status}")

        time.sleep(interval)

    raise TimeoutError(f"Task {task_id} timed out after {timeout}s")


def download_model(task_result: dict, output_path: Path) -> Path:
    """Download GLB model from task result."""
    # API returns pbr_model (with textures) or base_model
    model_url = task_result["output"].get("pbr_model") or task_result["output"].get("base_model")
    if not model_url:
        raise ValueError(f"No model URL in task output: {task_result['output'].keys()}")
    resp = requests.get(model_url)
    resp.raise_for_status()
    output_path.write_bytes(resp.content)
    return output_path


def image_to_glb(
    image_path: Path,
    output_path: Path,
    model_version: str = MODEL_V3,
    face_limit: int | None = None,
    smart_low_poly: bool = False,
    texture_quality: str = "standard",
    geometry_quality: str = "standard",
    timeout: int = 300,
) -> Path:
    """Convert image to GLB model using Tripo3D API.

    Args:
        image_path: Path to input image (PNG)
        output_path: Path to save GLB file
        model_version: MODEL_V3, MODEL_TURBO, or MODEL_V25
        face_limit: Max faces (1000-20000 for smart_low_poly)
        smart_low_poly: Better topology for game assets
        texture_quality: "standard" or "detailed"
        geometry_quality: "standard" or "detailed" (Ultra Mode, v3.0+ only)
        timeout: Max seconds to wait for generation

    Returns:
        Path to downloaded GLB file
    """
    task_id = create_task(
        image_path,
        model_version=model_version,
        face_limit=face_limit,
        smart_low_poly=smart_low_poly,
        texture_quality=texture_quality,
        geometry_quality=geometry_quality,
    )
    print(f"  Tripo3D task: {task_id} (model={model_version}, geo={geometry_quality})")

    result = poll_task(task_id, timeout=timeout)
    print(f"  Tripo3D completed")

    return download_model(result, output_path)
