#!/usr/bin/env bash
# Remove everything in build/ except assets.json, img/, and glb/
set -euo pipefail

BUILD_DIR="$(cd "$(dirname "$0")" && pwd)/build"

if [ ! -d "$BUILD_DIR" ]; then
  echo "No build directory found"
  exit 0
fi

find "$BUILD_DIR" -mindepth 1 -maxdepth 1 \
  ! -name 'assets.json' \
  ! -name 'img' \
  ! -name 'glb' \
  -exec rm -rf {} +

echo "Cleaned build/ (kept assets.json, img/, glb/)"
