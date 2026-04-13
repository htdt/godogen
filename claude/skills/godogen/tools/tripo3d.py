"""Tripo3D API client.

Docs:
  https://platform.tripo3d.ai/docs/generation
  https://platform.tripo3d.ai/docs/animation

Mesh generation uses v3.1-20260211. The rigger auto-picks v1.0-20240301
(biped-tuned) when model_version is omitted; the animation pipeline is
biped-only.
"""

import os
import time
from pathlib import Path

import requests

API_BASE = "https://api.tripo3d.ai/v2/openapi"

MODEL_V31 = "v3.1-20260211"


def get_api_key() -> str:
    key = os.environ.get("TRIPO3D_API_KEY")
    if not key:
        raise ValueError("TRIPO3D_API_KEY environment variable not set")
    return key


def _headers() -> dict:
    return {"Authorization": f"Bearer {get_api_key()}"}


def upload_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/png")}
        resp = requests.post(f"{API_BASE}/upload", headers=_headers(), files=files)
    resp.raise_for_status()
    return resp.json()["data"]["image_token"]


def _submit_task(payload: dict) -> str:
    resp = requests.post(f"{API_BASE}/task", headers=_headers(), json=payload)
    if not resp.ok:
        raise RuntimeError(f"Tripo3D task submit failed: HTTP {resp.status_code}: {resp.text}")
    return resp.json()["data"]["task_id"]


def create_image_to_model_task(
    image_path: Path,
    *,
    face_limit: int | None = 30000,
    pbr: bool = True,
    geometry_quality: str = "standard",
    texture_quality: str = "standard",
) -> str:
    """image_to_model on v3.1. face_limit=None omits the cap (HD preset)."""
    image_token = upload_image(image_path)
    payload = {
        "type": "image_to_model",
        "model_version": MODEL_V31,
        "file": {"type": "png", "file_token": image_token},
        "texture": True,
        "pbr": pbr,
        "auto_size": True,
        "orientation": "default",
        "enable_image_autofix": True,
        "geometry_quality": geometry_quality,
        "texture_quality": texture_quality,
    }
    if face_limit is not None:
        payload["face_limit"] = face_limit
    return _submit_task(payload)


def create_prerigcheck_task(model_task_id: str) -> str:
    return _submit_task({
        "type": "animate_prerigcheck",
        "original_model_task_id": model_task_id,
    })


def create_rig_task(model_task_id: str, rig_type: str = "biped") -> str:
    """Omits model_version so the server picks v1.0-20240301 (biped-tuned)."""
    return _submit_task({
        "type": "animate_rig",
        "original_model_task_id": model_task_id,
        "out_format": "glb",
        "rig_type": rig_type,
        "spec": "tripo",
    })


def create_retarget_task(rig_task_id: str, animation: str) -> str:
    return _submit_task({
        "type": "animate_retarget",
        "original_model_task_id": rig_task_id,
        "out_format": "glb",
        "animation": animation,
        "bake_animation": True,
    })


def poll_task(task_id: str, timeout: int = 600, interval: int = 5) -> dict:
    start = time.time()
    url = f"{API_BASE}/task/{task_id}"
    while time.time() - start < timeout:
        resp = requests.get(url, headers=_headers())
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data["status"]
        if status == "success":
            return data
        if status in ("failed", "cancelled", "unknown"):
            raise RuntimeError(f"Task {task_id} {status}: {data}")
        time.sleep(interval)
    raise TimeoutError(f"Task {task_id} timed out after {timeout}s")


def download_model(task_result: dict, output_path: Path) -> Path:
    out = task_result.get("output", {})
    url = out.get("pbr_model") or out.get("model") or out.get("base_model")
    if not url:
        raise ValueError(f"No model URL in output: {list(out.keys())}")
    resp = requests.get(url)
    resp.raise_for_status()
    output_path.write_bytes(resp.content)
    return output_path


def image_to_glb(
    image_path: Path,
    output_path: Path,
    *,
    face_limit: int | None = 30000,
    pbr: bool = True,
    geometry_quality: str = "standard",
    texture_quality: str = "standard",
    timeout: int = 600,
) -> tuple[Path, str]:
    """Full image_to_model → download. Returns (path, task_id)."""
    task_id = create_image_to_model_task(
        image_path,
        face_limit=face_limit,
        pbr=pbr,
        geometry_quality=geometry_quality,
        texture_quality=texture_quality,
    )
    print(f"  Tripo3D image_to_model: {task_id}")
    result = poll_task(task_id, timeout=timeout)
    download_model(result, output_path)
    return output_path, task_id
