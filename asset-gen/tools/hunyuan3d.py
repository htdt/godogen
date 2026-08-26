"""Tencent Hunyuan 3D client for image-to-GLB generation."""

import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


def _client():
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        raise ValueError("TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY must be set")
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ai3d.v20250513 import ai3d_client
    except ImportError as error:
        raise RuntimeError("Install tencentcloud-sdk-python from requirements.txt") from error

    http_profile = HttpProfile(endpoint="ai3d.tencentcloudapi.com")
    profile = ClientProfile(httpProfile=http_profile)
    return ai3d_client.Ai3dClient(
        credential.Credential(secret_id, secret_key),
        os.environ.get("TENCENTCLOUD_REGION", "ap-guangzhou"),
        profile,
    )


def _request(name: str, payload: dict) -> dict:
    try:
        from tencentcloud.ai3d.v20250513 import models
    except ImportError as error:
        raise RuntimeError("Install tencentcloud-sdk-python from requirements.txt") from error
    request_type = getattr(models, f"{name}Request")
    request = request_type()
    request.from_json_string(json.dumps(payload))
    response = getattr(_client(), name)(request)
    return json.loads(response.to_json_string())


def _find_glb_url(value: object) -> str | None:
    if isinstance(value, str) and urlparse(value).path.lower().endswith(".glb"):
        return value
    if isinstance(value, dict):
        for item in value.values():
            found = _find_glb_url(item)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_glb_url(item)
            if found:
                return found
    return None


def create_image_to_model_task(image_path: Path, *, face_limit: int | None = None, pbr: bool = True, quality: str = "default") -> str:
    payload = {
        "ImageUrl": "data:image/png;base64," + __import__("base64").b64encode(image_path.read_bytes()).decode("ascii"),
        "EnablePBR": pbr,
        "GenerateType": "Normal" if quality == "default" else "High",
    }
    if face_limit is not None:
        payload["FaceCount"] = face_limit
    response = _request("SubmitHunyuanTo3DProJob", payload)
    task_id = response.get("JobId")
    if not task_id:
        raise RuntimeError(f"Hunyuan 3D returned no JobId: {response}")
    return task_id


def poll_task(task_id: str, timeout: int = 900, interval: int = 5) -> dict:
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        response = _request("QueryHunyuanTo3DProJob", {"JobId": task_id})
        status = str(response.get("Status", "")).upper()
        if status in {"DONE", "SUCCESS", "SUCCEEDED"}:
            return response
        if status in {"FAIL", "FAILED", "CANCELLED", "CANCELED"}:
            raise RuntimeError(f"Hunyuan 3D task {task_id} {status}: {response}")
        time.sleep(interval)
    raise TimeoutError(f"Hunyuan 3D task {task_id} timed out after {timeout}s")


def download_model(task_result: dict, output_path: Path) -> Path:
    url = _find_glb_url(task_result)
    if not url:
        raise RuntimeError(f"Hunyuan 3D returned no GLB URL: {task_result}")
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return output_path
