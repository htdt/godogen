#!/usr/bin/env bash
set -euo pipefail

RESULT="${1:-screenshots/result/1}"
SCRIPT="${2:-test/Presentation.cs}"
FRAMES="${3:-450}"
FPS="${4:-30}"

mkdir -p screenshots
touch screenshots/.gdignore
rm -rf "$RESULT"
mkdir -p "$RESULT"

timeout 60 dotnet build 2>&1

if [ -x .capture/run_godot ]; then
    timeout 60 .capture/run_godot --headless --import 2>&1
    timeout 90 .capture/run_godot \
        --write-movie "$RESULT/frame.png" \
        --fixed-fps "$FPS" --quit-after "$FRAMES" \
        --script "$SCRIPT"
else
    timeout 60 godot --headless --import 2>&1

    cmd=(godot --path .)
    if [ "$(uname -s)" != "Darwin" ] && [ -z "${DISPLAY:-}" ] && [ -z "${WAYLAND_DISPLAY:-}" ]; then
        cmd=(xvfb-run -a -s "-screen 0 1920x1080x24" "${cmd[@]}")
    fi

    NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
    if [ "$(uname -s)" = "Darwin" ]; then
        cmd+=(--rendering-method forward_plus)
    elif [ -f "$NVIDIA_ICD" ]; then
        cmd=(env "VK_ICD_FILENAMES=$NVIDIA_ICD" "${cmd[@]}" --rendering-method forward_plus)
    elif command -v vulkaninfo >/dev/null 2>&1 && vulkaninfo --summary 2>&1 | grep -Eq "deviceType *= PHYSICAL_DEVICE_TYPE_(DISCRETE_GPU|INTEGRATED_GPU|VIRTUAL_GPU)"; then
        cmd+=(--rendering-method forward_plus)
    else
        cmd+=(--rendering-driver vulkan)
    fi

    timeout 90 "${cmd[@]}" \
        --write-movie "$RESULT/frame.png" \
        --fixed-fps "$FPS" --quit-after "$FRAMES" \
        --script "$SCRIPT"
fi

ffmpeg -y -framerate "$FPS" -pattern_type glob -i "$RESULT/frame*.png" \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    "$RESULT/video.mp4"
