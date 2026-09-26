# Workstation Setup

Shared workstation setup for the consolidated Godogen source repo.

## .NET 9 SDK

Godot 4.5+ C# projects require .NET 9.

### Linux (Ubuntu/Debian)

```bash
wget -q https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh
chmod +x /tmp/dotnet-install.sh
/tmp/dotnet-install.sh --channel 9.0 --install-dir ~/.dotnet
```

Add to `~/.bashrc`:

```bash
export PATH="$HOME/.dotnet:$PATH"
export DOTNET_ROOT="$HOME/.dotnet"
```

### macOS

```bash
brew install dotnet@9
```

## Rust

Bevy projects require a current Rust toolchain:

```bash
rustup update stable
cargo --version
rustc --version
```

## Node.js And Browser

Babylon.js and three.js projects need Node.js 22.12+; the optional Tripo CLI (`npm install -g tripo-cli`) needs 20+:

```bash
node --version
npm --version
```

Browser capture requires Chrome or Chromium with hardware WebGL2. Install one system browser and set `CHROME_BIN` if it is not on a common path:

```bash
command -v google-chrome || command -v chromium || command -v chromium-browser
export CHROME_BIN=/path/to/chrome
```

Browser capture prefers hardware WebGL2. A fallback to a software renderer (SwiftShader, llvmpipe, lavapipe, etc.) on a GPU-equipped host means the browser GPU path is misconfigured and worth fixing; on a GPU-less host it still captures, at reduced quality and speed.

## System Packages

```bash
sudo apt-get install vulkan-tools xvfb ffmpeg imagemagick
```

- **vulkan-tools** — `vulkaninfo` for GPU validation
- **xvfb** — virtual X11 display for headless Godot/Bevy runs and capture
- **ffmpeg** — MP4 encoding of proof videos and sprite frame extraction
- **imagemagick** — image resize, flip, crop for sprite pipelines

On macOS:

```bash
brew install coreutils ffmpeg dotnet@9
```

## Python

Requires Python 3.10+.

```bash
python3 --version
pip install -U -r asset-gen/tools/requirements.txt
```

In a published game repo, the same asset-generation requirements file lives at:

- `.claude/skills/asset-gen/tools/requirements.txt` for Claude Code
- `.agents/skills/asset-gen/tools/requirements.txt` for Codex

`asset_gen.py` needs `google-genai` 2.25+ for Gemini images, TTS, voice design and Lyria.

## Godot

C# projects (`--engine godot`) need the **.NET edition**: the standard build cannot run C# scripts. GDScript projects (`--engine godot-gdscript`) run on either, so an installed .NET edition covers both; for GDScript alone, the [standard build](#standard-build-gdscript-only) is enough.

### .NET edition, Linux

```bash
VERSION=$(curl -s https://api.github.com/repos/godotengine/godot/releases/latest | grep -oP '"tag_name": "\K[^"]+' | sed 's/-stable//')
echo "Installing Godot .NET $VERSION"
cd /tmp
wget https://github.com/godotengine/godot/releases/download/${VERSION}-stable/Godot_v${VERSION}-stable_mono_linux_x86_64.zip
unzip Godot_v${VERSION}-stable_mono_linux_x86_64.zip
sudo mv Godot_v${VERSION}-stable_mono_linux_x86_64/Godot_v${VERSION}-stable_mono_linux.x86_64 /usr/local/bin/godot
sudo mv Godot_v${VERSION}-stable_mono_linux_x86_64/GodotSharp /usr/local/bin/GodotSharp
```

`GodotSharp/` must live next to the `godot` binary. Godot resolves it relative to itself.

### .NET edition, macOS

```bash
brew install --cask godot-mono
sudo rm -f /usr/local/bin/godot   # clear any symlink first: tee would write through it onto the Godot binary
printf '#!/bin/sh\nexec /Applications/Godot_mono.app/Contents/MacOS/Godot "$@"\n' | sudo tee /usr/local/bin/godot >/dev/null
sudo chmod +x /usr/local/bin/godot
```

`godot` must be a wrapper script, not a symlink. Godot resolves `GodotSharp/` (in the bundle's `Contents/Resources/`) from the path it was invoked as, so through a symlink it looks in `/usr/local/bin/` and fails — as a silent hang, since macOS shows fatal errors in a modal that `--headless` can't dismiss. For C#, skip the plain `godot` cask: its `godot` command runs the build without C#.

### Standard build (GDScript only)

```bash
# Linux
VERSION=$(curl -s https://api.github.com/repos/godotengine/godot/releases/latest | grep -oP '"tag_name": "\K[^"]+' | sed 's/-stable//')
cd /tmp
wget https://github.com/godotengine/godot/releases/download/${VERSION}-stable/Godot_v${VERSION}-stable_linux.x86_64.zip
unzip Godot_v${VERSION}-stable_linux.x86_64.zip
sudo mv Godot_v${VERSION}-stable_linux.x86_64 /usr/local/bin/godot

# macOS
brew install --cask godot
```

### Verify

```bash
dotnet --version                    # 9.0.x
godot --version                     # 4.x.x.stable.mono (.NET edition)
timeout 60 godot --headless --quit  # may show harmless RID warnings
```

Assembly errors (Linux) or a timeout with output ending at `.NET: Initializing module...` (macOS) mean `godot` can't find `GodotSharp/`:

```bash
ls "$(dirname "$(which godot)")"/GodotSharp/   # Linux: must sit next to the binary
head -2 "$(which godot)"                       # macOS: must be the wrapper script above
```

## Local Asset Generation

Assets are generated locally by default with [godogen_assets](https://github.com/htdt/godogen_assets): images, textured 3D models, rigged humanoids with generated moves and lip-sync, sound effects and voice lines, free on the machine's NVIDIA GPU (reference: RTX 3060 12 GB, 24 GB RAM). Without it, every asset goes to the paid APIs below.

GPUs and drivers differ too much for one script, so its [README](https://github.com/htdt/godogen_assets#setup) (Setup) is a manual for a Claude Code or Codex agent to follow on the machine at hand. Once its commands are on `PATH` (`./setup.sh link`), record the checkout in this repo — `publish.sh` writes the path into every published asset-gen skill:

```bash
echo "$PWD" > /path/to/godogen/.godogen_assets   # run in the godogen_assets checkout; git-ignored
```

## API Keys (Optional)

Paid generation covers what the local tools can't make — or every asset, on a machine without them. Set in environment:

- `GOOGLE_API_KEY` — Gemini images, Gemini TTS voice acting, Lyria music
- `XAI_API_KEY` — xAI Grok images and animated-sprite video
- `TRIPO_API_KEY` — image-to-3D and non-humanoid rigging via the `tripo` CLI (`npm install -g tripo-cli`, Node 20+)

With both image keys, Gemini is the default and quality-critical images are generated on each.

## Verify Rendering

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json vulkaninfo --summary 2>&1 | grep "deviceName"
xvfb-run -a godot --headless --quit
```
