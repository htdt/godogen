# Godot Capture

Screenshot and video capture for Godot projects. Supports macOS (Metal) and Linux (X11/xvfb + optional GPU).

The Godot project is the working directory. All paths below are relative to it.

## Platform Detection

Run once per session to set platform-specific variables:
```bash
PLATFORM=$(uname -s)  # Darwin or Linux

# Timeout command — GNU timeout not available on macOS by default
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout"
else
    # POSIX fallback for macOS without coreutils
    timeout_fallback() { perl -e 'alarm shift; exec @ARGV' "$@"; }
    TIMEOUT_CMD="timeout_fallback"
fi
```

## GPU Detection (Linux only)

Skip on macOS — Metal rendering is always available natively.

```bash
GPU_DISPLAY=""
if [[ "$PLATFORM" == "Linux" ]]; then
    for sock in /tmp/.X11-unix/X*; do
      d=":${sock##*/X}"
      if DISPLAY=$d $TIMEOUT_CMD 2 glxinfo 2>/dev/null | grep -qi nvidia; then
        GPU_DISPLAY=$d; break
      fi
    done
fi
```

When `GPU_DISPLAY` is set, Godot uses hardware Vulkan with `--rendering-method forward_plus` — real shadows, SSR, SSAO, glow, volumetric fog. On macOS, Metal provides equivalent rendering natively. On Linux without a GPU, `xvfb-run` uses lavapipe (software rasterizer).

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
MOVIE=screenshots/{task_folder}
rm -rf "$MOVIE" && mkdir -p "$MOVIE"
touch screenshots/.gdignore
if [[ "$PLATFORM" == "Darwin" ]]; then
    # macOS — Metal rendering, no display server needed
    $TIMEOUT_CMD 30 godot --rendering-method forward_plus \
        --write-movie "$MOVIE"/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
elif [[ -n "$GPU_DISPLAY" ]]; then
    # Linux with GPU
    $TIMEOUT_CMD 30 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
        --write-movie "$MOVIE"/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
else
    # Linux software rendering (lavapipe)
    $TIMEOUT_CMD 30 xvfb-run -a -s '-screen 0 1280x720x24' godot --rendering-driver vulkan \
        --write-movie "$MOVIE"/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
fi
```

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`). Use lowercase with underscores.

**Timeout:** `$TIMEOUT_CMD 30` is a safety net — `--quit-after` handles exit normally. Exit code 124 means timeout fired.

### Frame Rate and Duration

`--quit-after {N}` is the frame count. Choose based on scene type:
- **Static scenes** (decoration, terrain, UI): `--fixed-fps 1`. Adjust `--quit-after` for however many views needed (e.g. 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fixed-fps 10`. Low FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s (30-100 frames).

## Video Capture

Video capture requires hardware rendering — macOS (Metal) or Linux with GPU. Software rendering is too slow and low quality for video. If neither is available, skip video capture and report that to the caller.

```bash
if [[ "$PLATFORM" == "Darwin" ]] || [[ -n "$GPU_DISPLAY" ]]; then
    VIDEO=screenshots/presentation
    rm -rf "$VIDEO" && mkdir -p "$VIDEO"
    touch screenshots/.gdignore
    if [[ "$PLATFORM" == "Darwin" ]]; then
        $TIMEOUT_CMD 60 godot --rendering-method forward_plus \
            --write-movie "$VIDEO"/output.avi \
            --fixed-fps 30 --quit-after 900 \
            --script test/presentation.gd 2>&1
    else
        $TIMEOUT_CMD 60 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
            --write-movie "$VIDEO"/output.avi \
            --fixed-fps 30 --quit-after 900 \
            --script test/presentation.gd 2>&1
    fi
    # Convert AVI (MJPEG) to MP4 (H.264)
    ffmpeg -i "$VIDEO"/output.avi \
        -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow \
        -vf "scale='min(1280,iw)':-2" \
        -movflags +faststart \
        "$VIDEO"/gameplay.mp4 2>&1
else
    echo "No GPU available — skipping video capture"
fi
```

**AVI to MP4:** Godot outputs MJPEG AVI. ffmpeg converts to H.264 MP4. CRF 28 + `-preset slow` targets ~2-5MB for a 30s clip at 720p. `-movflags +faststart` enables Telegram preview streaming. Scale filter caps width at 1280px (no-op if already smaller).
