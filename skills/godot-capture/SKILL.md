---
name: godot-capture
description: |
  This skill should be used when capturing screenshots or video from a Godot project. Handles GPU detection, xvfb fallback, and ffmpeg conversion. Loaded by godot-task for screenshot and video capture.
---

# Godot Capture

Screenshot and video capture for Godot projects. Detects GPU (T4 via headless Xorg) and falls back to xvfb + lavapipe.

The Godot project is the working directory. All paths below are relative to it.

## GPU Detection

Run once per session:
```bash
GPU_DISPLAY=""
for d in :0 :1; do
  if DISPLAY=$d timeout 2 glxinfo 2>/dev/null | grep -qi nvidia; then
    GPU_DISPLAY=$d; break
  fi
done
```

When `GPU_DISPLAY` is set, Godot uses hardware Vulkan (NVIDIA T4) with `--rendering-method forward_plus` — real shadows, SSR, SSAO, glow, volumetric fog. Without it, `xvfb-run` uses lavapipe (software rasterizer).

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
MOVIE=screenshots/{task_folder}
rm -rf $MOVIE && mkdir -p $MOVIE && mkdir -p _captures
touch screenshots/.gdignore _captures/.gdignore
if [ -n "$GPU_DISPLAY" ]; then
  timeout 30 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
      --write-movie _captures/frame.png \
      --fixed-fps 10 --quit-after {N} \
      --script test/test_task.gd 2>&1
else
  timeout 30 xvfb-run -a -s '-screen 0 1280x720x24' godot --rendering-driver vulkan \
      --write-movie _captures/frame.png \
      --fixed-fps 10 --quit-after {N} \
      --script test/test_task.gd 2>&1
fi
mv _captures/* $MOVIE/ && rm -rf _captures
```

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`). Use lowercase with underscores.

**`--write-movie` path:** MUST be relative and inside the Godot project directory. That's why we write to `_captures/` then move frames out.

**Timeout:** `timeout 30` is a safety net — `--quit-after` handles exit normally. Exit code 124 means timeout fired.

### Frame Rate and Duration

`--quit-after {N}` is the frame count. Choose based on scene type:
- **Static scenes** (decoration, terrain, UI): `--fixed-fps 1`. Adjust `--quit-after` for however many views needed (e.g. 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fixed-fps 10`. Low FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s (30-100 frames).

## Video Capture

**Requires GPU** — video capture only works with a GPU display (`$GPU_DISPLAY` set). Software rendering is too slow and low quality for video. If no GPU is available, skip video capture and report that to the caller.

```bash
VIDEO=screenshots/presentation
rm -rf $VIDEO && mkdir -p $VIDEO && mkdir -p _captures
touch screenshots/.gdignore _captures/.gdignore
timeout 60 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
    --write-movie _captures/output.avi \
    --fixed-fps 30 --quit-after 900 \
    --script test/presentation.gd 2>&1
# Convert AVI (MJPEG) to MP4 (H.264)
ffmpeg -i _captures/output.avi \
    -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow \
    -vf "scale='min(1280,iw)':-2" \
    -movflags +faststart \
    $VIDEO/gameplay.mp4 2>&1
mv _captures/output.avi $VIDEO/
rm -rf _captures
```

**AVI to MP4:** Godot outputs MJPEG AVI. ffmpeg converts to H.264 MP4. CRF 28 + `-preset slow` targets ~2-5MB for a 30s clip at 720p. `-movflags +faststart` enables Telegram preview streaming. Scale filter caps width at 1280px (no-op if already smaller).
