# Workstation Setup

## System Packages

```bash
sudo apt-get install mesa-utils ffmpeg
```

- **mesa-utils** — provides `glxinfo` for GPU detection
- **ffmpeg** — AVI→MP4 conversion

No xvfb needed when a GPU is available.

## Python

Requires Python 3.10+.

```bash
python3 --version
pip install -r skills/godogen/tools/requirements.txt
```

## Godot

Fetch the latest version and install:

```bash
VERSION=$(curl -s https://api.github.com/repos/godotengine/godot/releases/latest | grep -oP '"tag_name": "\K[^"]+' | sed 's/-stable//')
echo "Installing Godot $VERSION"
cd /tmp
wget https://github.com/godotengine/godot/releases/download/${VERSION}-stable/Godot_v${VERSION}-stable_linux.x86_64.zip
unzip Godot_v${VERSION}-stable_linux.x86_64.zip
sudo mv Godot_v${VERSION}-stable_linux.x86_64 /usr/local/bin/godot
```

## API Keys

Set in environment:

- `XAI_API_KEY` — xAI Grok image generation
- `TRIPO3D_API_KEY` — image-to-3D conversion (3D games only)
- `GEMINI_API_KEY` — visual QA with Gemini Flash

## Verify

```bash
godot --version
nvidia-smi
python3 -c "import rembg; print('rembg ok')"
```

GPU detection needs X11 sockets in `/tmp/.X11-unix/`. Confirm with:

```bash
for sock in /tmp/.X11-unix/X*; do
  d=":${sock##*/X}"
  DISPLAY=$d glxinfo 2>/dev/null | grep -i "opengl renderer" && echo "GPU on $d"
done
```
