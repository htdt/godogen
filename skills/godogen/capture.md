# Godot Capture

Screenshot and video capture for Godot projects. Supports macOS (Metal) and Linux (X11/xvfb + optional GPU).

The Godot project is the working directory. All paths below are relative to it.

## Setup (run once per session)

Detects platform, timeout command, GPU availability, and defines a `run_godot` wrapper that handles all platform differences. Capture commands below use `run_godot` directly.

```bash
PLATFORM=$(uname -s)

# Timeout command — GNU timeout not available on macOS by default
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout"
else
    timeout_fallback() { perl -e 'alarm shift; exec @ARGV' "$@"; }
    TIMEOUT_CMD="timeout_fallback"
fi

# Platform-specific Godot launcher
GPU_AVAILABLE=false
if [[ "$PLATFORM" == "Darwin" ]]; then
    GPU_AVAILABLE=true
    run_godot() { godot --rendering-method forward_plus "$@" 2>&1; }
else
    # Linux — probe for GPU display
    for sock in /tmp/.X11-unix/X*; do
        d=":${sock##*/X}"
        if DISPLAY=$d $TIMEOUT_CMD 2 glxinfo 2>/dev/null | grep -qi nvidia; then
            GPU_AVAILABLE=true
            eval "run_godot() { DISPLAY=$d godot --rendering-method forward_plus \"\$@\" 2>&1; }"
            break
        fi
    done
    if ! $GPU_AVAILABLE; then
        run_godot() { xvfb-run -a -s '-screen 0 1280x720x24' godot --rendering-driver vulkan "$@" 2>&1; }
    fi
fi
```

When `GPU_AVAILABLE` is true (macOS Metal or Linux with NVIDIA), Godot uses hardware rendering with `--rendering-method forward_plus` — real shadows, SSR, SSAO, glow, volumetric fog. Without a GPU, `xvfb-run` uses lavapipe (software rasterizer).

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
MOVIE=screenshots/{task_folder}
rm -rf "$MOVIE" && mkdir -p "$MOVIE"
touch screenshots/.gdignore
$TIMEOUT_CMD 30 run_godot \
    --write-movie "$MOVIE"/frame.png \
    --fixed-fps 10 --quit-after {N} \
    --script test/test_task.gd
```

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`). Use lowercase with underscores.

**Timeout:** `$TIMEOUT_CMD 30` is a safety net — `--quit-after` handles exit normally. Exit code 124 means timeout fired.

### Frame Rate and Duration

`--quit-after {N}` is the frame count. Choose based on scene type:
- **Static scenes** (decoration, terrain, UI): `--fixed-fps 1`. Adjust `--quit-after` for however many views needed (e.g. 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fixed-fps 10`. Low FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s (30-100 frames).

## Video Capture

Video capture requires hardware rendering (macOS Metal or Linux with GPU). Software rendering is too slow for video — skip and report to the caller if `GPU_AVAILABLE` is false.

```bash
if $GPU_AVAILABLE; then
    VIDEO=screenshots/presentation
    rm -rf "$VIDEO" && mkdir -p "$VIDEO"
    touch screenshots/.gdignore
    $TIMEOUT_CMD 60 run_godot \
        --write-movie "$VIDEO"/output.avi \
        --fixed-fps 30 --quit-after 900 \
        --script test/presentation.gd
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
