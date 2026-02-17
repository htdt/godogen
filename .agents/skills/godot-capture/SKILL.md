---
name: godot-capture
description: |
  Capture screenshots and video from Godot projects with GPU-first execution.
  Handles NVIDIA display detection, xvfb fallback, and MP4 conversion.

  **When to use:** Load from `godot-task` for screenshot/video capture and verification artifacts.
---

# Godot Capture

Screenshot and video capture workflow for Godot projects. Detect GPU display first (target environment: NVIDIA T4 on VM), then fall back to `xvfb` + software Vulkan when GPU is unavailable.

`{game_dir}` is where Godot runs (`game/` by default). `$PROJECT_ROOT` must be set before running commands below.

## GPU Detection

Run once per session:

```bash
GPU_DISPLAY=""
for d in :0 :1; do
  if DISPLAY=$d timeout 2 glxinfo 2>/dev/null | grep -qi nvidia; then
    GPU_DISPLAY=$d
    break
  fi
done
```

If `GPU_DISPLAY` is set, run Godot with hardware Vulkan via `--rendering-method forward_plus`.
If not set, use the fallback `xvfb-run` capture command.

## Screenshot Capture

Screenshots are stored outside the project in `$PROJECT_ROOT/screenshots/{task_folder}`.

```bash
MOVIE=$PROJECT_ROOT/screenshots/{task_folder}
rm -rf $MOVIE && mkdir -p $MOVIE

cd $PROJECT_ROOT/{game_dir} && mkdir -p _captures
if [ -n "$GPU_DISPLAY" ]; then
  timeout 20 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
      --write-movie _captures/frame.png \
      --fixed-fps 10 --quit-after {N} \
      --script test/test_task.gd 2>&1
else
  timeout 20 xvfb-run -a -s '-screen 0 1280x720x24' \
      godot --rendering-driver vulkan \
      --write-movie _captures/frame.png \
      --fixed-fps 10 --quit-after {N} \
      --script test/test_task.gd 2>&1
fi

mv $PROJECT_ROOT/{game_dir}/_captures/* $MOVIE/
rm -rf $PROJECT_ROOT/{game_dir}/_captures
```

`{task_folder}` should be lowercase with underscores, for example `task_01_terrain`.

`--write-movie` path must be relative and inside the Godot project; capture into `_captures/` then move files out.

## Frame Rate and Duration

`--quit-after {N}` is frame count.

- Static scenes (placement/UI): use `--fixed-fps 1` and enough frames for multiple viewpoints.
- Dynamic scenes (physics/gameplay): use `--fixed-fps 10` to keep physics stable.

## Video Capture

Video capture requires GPU (`$GPU_DISPLAY` set). If no GPU display is found, skip video and report the blocker.

```bash
VIDEO=$PROJECT_ROOT/screenshots/presentation
rm -rf $VIDEO && mkdir -p $VIDEO

cd $PROJECT_ROOT/{game_dir} && mkdir -p _captures
timeout 60 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
    --write-movie _captures/output.avi \
    --fixed-fps 30 --quit-after 900 \
    --script test/presentation.gd 2>&1

ffmpeg -i $PROJECT_ROOT/{game_dir}/_captures/output.avi \
    -c:v libx264 -pix_fmt yuv420p -crf 20 \
    $VIDEO/gameplay.mp4 2>&1

mv $PROJECT_ROOT/{game_dir}/_captures/output.avi $VIDEO/
rm -rf $PROJECT_ROOT/{game_dir}/_captures
```

Godot outputs MJPEG AVI; convert to H.264 MP4 for compact sharing.
