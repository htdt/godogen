# Godot Capture

Screenshot and video capture. GPU gives hardware rendering (shadows, SSR, SSAO, glow); without GPU, screenshots still work via software Vulkan (lavapipe) but video capture is skipped.

Working directory is the Godot project.

## Setup (run once per session)

Detects platform and GPU. Writes `.capture/run_godot` — a persistent wrapper script compatible with `timeout`.

```bash
set -e
mkdir -p .capture
touch .capture/.gdignore

PLATFORM=$(uname -s)
GPU=none

# --- Timeout command ---
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD=timeout
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD=gtimeout
else
    cat > .capture/ptimeout << 'PERL'
#!/usr/bin/env perl
use POSIX; my $s=shift; my $p; $SIG{ALRM}=sub{kill 'TERM',$p;exit 124};
alarm $s; die "fork: $!" unless defined($p=fork); exec @ARGV unless $p; waitpid $p,0; exit($?>>8);
PERL
    chmod +x .capture/ptimeout
    TIMEOUT_CMD="$(pwd)/.capture/ptimeout"
fi

# --- GPU detection ---
NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
if [[ "$PLATFORM" == "Darwin" ]]; then
    GPU=metal
elif [[ -f "$NVIDIA_ICD" ]] && VK_ICD_FILENAMES=$NVIDIA_ICD vulkaninfo --summary 2>&1 | grep -q "NVIDIA"; then
    GPU=nvidia
fi

# --- Persistent run_godot wrapper ---
cat > .capture/run_godot << 'WRAPPER'
#!/usr/bin/env bash
set -o pipefail
NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
NOISE="leaked RID|Leaked instance|ObjectDB instances"
cmd=()

# Linux without a display session → xvfb
if [[ "$(uname -s)" != "Darwin" && -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    cmd+=(xvfb-run -a -s '-screen 0 1920x1080x24')
fi

# Renderer
if [[ "$(uname -s)" == "Darwin" ]]; then
    cmd+=(godot --rendering-method forward_plus)
elif [[ -f "$NVIDIA_ICD" ]]; then
    cmd+=(env "VK_ICD_FILENAMES=$NVIDIA_ICD" godot --rendering-method forward_plus)
else
    cmd+=(godot --rendering-driver vulkan)
fi

"${cmd[@]}" "$@" 2>&1 | { grep -v "$NOISE" || true; }
WRAPPER
chmod +x .capture/run_godot

# --- Env for sourcing in subsequent bash calls ---
GPU_AVAILABLE=$([[ "$GPU" != "none" ]] && echo true || echo false)
cat > .capture/env << ENV
GPU_AVAILABLE=$GPU_AVAILABLE
TIMEOUT_CMD=$TIMEOUT_CMD
ENV

echo "=== Capture ready: Platform=$PLATFORM  GPU=$GPU ==="
$GPU_AVAILABLE || echo "WARNING: No GPU — screenshots via lavapipe, video capture skipped"
```

After setup: source `.capture/env` for `$GPU_AVAILABLE` and `$TIMEOUT_CMD`. Use `.capture/run_godot` instead of bare `godot` for all rendering.

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
source .capture/env

timeout 60 dotnet build

MOVIE=screenshots/{task_folder}
rm -rf "$MOVIE" && mkdir -p "$MOVIE"
touch screenshots/.gdignore
$TIMEOUT_CMD 30 .capture/run_godot \
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

Requires GPU. Software rendering is too slow — skip and report if `GPU_AVAILABLE` is false.

```bash
source .capture/env

if ! $GPU_AVAILABLE; then
    echo "No GPU — skipping video capture"
else
    VIDEO=screenshots/presentation
    rm -rf "$VIDEO" && mkdir -p "$VIDEO"
    touch screenshots/.gdignore
    $TIMEOUT_CMD 60 .capture/run_godot \
        --write-movie "$VIDEO"/output.avi \
        --fixed-fps 30 --quit-after 900 \
        --script test/Presentation.cs
    ffmpeg -i "$VIDEO"/output.avi \
        -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow \
        -vf "scale='min(1280,iw)':-2" \
        -movflags +faststart \
        "$VIDEO"/gameplay.mp4 2>&1
fi
```

**AVI to MP4:** Godot outputs MJPEG AVI. ffmpeg converts to H.264 MP4. CRF 28 + `-preset slow` targets ~2-5MB for a 30s clip at 720p. `-movflags +faststart` enables streaming preview. Scale filter caps width at 1280px.
