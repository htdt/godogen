# Godot Capture

Screenshot and video capture for Godot projects. GPU gives hardware rendering (shadows, SSR, SSAO, glow); without GPU, screenshots still work via software Vulkan (lavapipe) but video capture is skipped.

The Godot project is the working directory. All paths below are relative to it.

## Setup (run once per session)

Detects platform, timeout command, GPU availability, and defines a `run_godot` wrapper.

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

GPU_AVAILABLE=false
if [[ "$PLATFORM" == "Darwin" ]]; then
    GPU_AVAILABLE=true
    run_godot() { godot --rendering-method forward_plus "$@" 2>&1; }
else
    # Linux — try NVIDIA Vulkan ICD (no X server required)
    NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
    if [[ -f "$NVIDIA_ICD" ]] && VK_ICD_FILENAMES=$NVIDIA_ICD vulkaninfo --summary 2>&1 | grep -q "NVIDIA"; then
        GPU_AVAILABLE=true
        run_godot() {
            VK_ICD_FILENAMES=$NVIDIA_ICD \
            godot --rendering-method forward_plus "$@" 2>&1
        }
    else
        echo "WARNING: No NVIDIA GPU detected — using software rendering (lavapipe)"
        echo "Screenshots will work but video capture will be skipped"
        run_godot() {
            xvfb-run -a -s '-screen 0 1280x720x24' \
            godot --rendering-driver vulkan "$@" 2>&1
        }
    fi
fi
```

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
# Build C# before capture
timeout 60 dotnet build

MOVIE=screenshots/{task_folder}
rm -rf "$MOVIE" && mkdir -p "$MOVIE"
touch screenshots/.gdignore
$TIMEOUT_CMD 30 run_godot \
    --write-movie "$MOVIE"/frame.png \
    --fixed-fps 10 --quit-after {N} \
    --script test/TestTask.cs
```

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`). Use lowercase with underscores.

**Timeout:** `$TIMEOUT_CMD 30` is a safety net — `--quit-after` handles exit normally. Exit code 124 means timeout fired.

### Frame Rate and Duration

`--quit-after {N}` is the frame count. Choose based on scene type:
- **Static scenes** (decoration, terrain, UI): `--fixed-fps 1`. Adjust `--quit-after` for however many views needed (e.g. 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fixed-fps 10`. Low FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s (30-100 frames).

## Video Capture

Video capture requires a GPU. Software rendering is too slow — skip and report if `GPU_AVAILABLE` is false.

```bash
if ! $GPU_AVAILABLE; then
    echo "No GPU available — skipping video capture"
else
    VIDEO=screenshots/presentation
    rm -rf "$VIDEO" && mkdir -p "$VIDEO"
    touch screenshots/.gdignore
    $TIMEOUT_CMD 60 run_godot \
        --write-movie "$VIDEO"/output.avi \
        --fixed-fps 30 --quit-after 900 \
        --script test/Presentation.cs
    # Convert AVI (MJPEG) to MP4 (H.264)
    ffmpeg -i "$VIDEO"/output.avi \
        -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow \
        -vf "scale='min(1280,iw)':-2" \
        -movflags +faststart \
        "$VIDEO"/gameplay.mp4 2>&1
fi
```

**AVI to MP4:** Godot outputs MJPEG AVI. ffmpeg converts to H.264 MP4. CRF 28 + `-preset slow` targets ~2-5MB for a 30s clip at 720p. `-movflags +faststart` enables Telegram preview streaming. Scale filter caps width at 1280px (no-op if already smaller).
