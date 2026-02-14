#!/usr/bin/env bash
# Remove game/ project files (keeps assets/ untouched)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
GAME_DIR="$REPO_ROOT/game"

if [ ! -d "$GAME_DIR" ]; then
  echo "No game directory found"
  exit 0
fi

rm -rf "$GAME_DIR"
echo "Removed game/"

# Clean up any leftover worktrees
if [ -d "$REPO_ROOT/worktrees" ]; then
  rm -rf "$REPO_ROOT/worktrees"
  echo "Removed worktrees/"
fi

# Clean up screenshots
if [ -d "$REPO_ROOT/screenshots" ]; then
  rm -rf "$REPO_ROOT/screenshots"
  echo "Removed screenshots/"
fi

echo "Clean. assets/ preserved."
