"""Backend registry and factory functions."""

import os
import sys
import json

from .base import ImageBackend, VideoBackend


def _fail(msg: str):
    print(json.dumps({"ok": False, "cost_cents": 0, "error": msg}))
    sys.exit(1)


def get_image_backend(name: str | None = None) -> ImageBackend:
    """Get image backend by name. Falls back to ASSET_BACKEND env var, then 'grok'."""
    backend_name = name or os.environ.get("ASSET_BACKEND", "grok")

    if backend_name == "gemini":
        from .gemini import GeminiBackend
        return GeminiBackend()
    elif backend_name == "grok":
        from .grok import GrokImageBackend
        return GrokImageBackend()
    elif backend_name == "dashscope":
        from .dashscope import DashScopeImageBackend
        return DashScopeImageBackend()
    else:
        _fail(f"Unknown image backend: {backend_name}. Available: gemini, grok, dashscope")


def get_video_backend(name: str | None = None) -> VideoBackend:
    """Get video backend by name. Falls back to ASSET_BACKEND env var, then 'grok'."""
    backend_name = name or os.environ.get("ASSET_BACKEND", "grok")

    if backend_name == "grok":
        from .grok import GrokVideoBackend
        return GrokVideoBackend()
    elif backend_name == "dashscope":
        from .dashscope import DashScopeVideoBackend
        return DashScopeVideoBackend()
    else:
        _fail(f"Unknown video backend: {backend_name}. Available: grok, dashscope")
