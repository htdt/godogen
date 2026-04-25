#!/usr/bin/env bash
set -euo pipefail

RESULT="${1:-screenshots/result/1}"
CAPTURE_BIN="${2:-capture}"
FRAMES="${3:-450}"
FPS="${4:-30}"

rm -rf "$RESULT"
mkdir -p "$RESULT"

cargo fmt
cargo check
cargo build
cargo run --bin "$CAPTURE_BIN" -- frames "$RESULT" "$FRAMES"

ffmpeg -y -framerate "$FPS" -pattern_type glob -i "$RESULT/frame*.png" \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    "$RESULT/video.mp4"
