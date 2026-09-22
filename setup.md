# Workstation Setup

Shared workstation setup for the consolidated Godogen source repo.

## .NET 9 SDK

Godot 4.5+ requires .NET 9.

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

The Tripo CLI needs Node.js 20+ for every engine (`npm install -g tripo-cli`); Babylon.js projects need 22.12+:

```bash
node --version
npm --version
```

Browser capture requires Chrome or Chromium with hardware WebGL2. Install one system browser and set `CHROME_BIN` if it is not on a common path:

```bash
command -v google-chrome || command -v chromium || command -v chromium-browser
export CHROME_BIN=/path/to/chrome
```

Babylon capture prefers hardware WebGL2. A fallback to a software renderer (SwiftShader, llvmpipe, lavapipe, etc.) on a GPU-equipped host means the browser GPU path is misconfigured and worth fixing; on a GPU-less host it still captures, at reduced quality and speed.

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
pip install -r asset-gen/tools/requirements.txt
pip install google-genai
```

In a published game repo, the same asset-generation requirements file lives at:

- `.claude/skills/asset-gen/tools/requirements.txt` for Claude Code
- `.agents/skills/asset-gen/tools/requirements.txt` for Codex

`google-genai` is required by `asset_gen.py` for Gemini image generation.

## Godot (.NET edition)

The **.NET edition** is required for Godot projects. The standard Godot build cannot run C# scripts.

### Linux

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

### macOS

```bash
brew install --cask godot-mono
sudo ln -sf /Applications/Godot_mono.app/Contents/MacOS/Godot /usr/local/bin/godot
```

### Verify

```bash
dotnet --version                 # 9.0.x
godot --version                  # 4.x.x.stable.mono
godot --headless --quit          # may show harmless RID warnings
```

If `godot --headless --quit` crashes with assembly errors, check that `GodotSharp/` is next to the binary:

```bash
ls "$(dirname "$(which godot)")"/GodotSharp/
```

## Character Animation (Optional)

Custom humanoid animation (the asset-gen skill's `motion.md`) additionally requires:

- NVIDIA GPU with a working CUDA driver. Modest is fine: the text encoder runs on CPU (needs ≥20 GB free RAM), diffusion peaks ~2.5 GB VRAM; ~35 GB disk
- `cmake` — the Kimodo install builds a compiled extension

### Dependency layout

The animation stack is machine-level: one copy per workstation, shared by every game project. It lives under a single directory, with these exact names:

```
$KIMODO_HOME/
├── kimodo-practical/   # the animation lib — reference clone; projects clone their workspace from it
├── kimodo/             # upstream NVIDIA Kimodo checkout, editable-installed into kimenv/
├── kimenv/             # the pipeline venv — run the lib's python tools with kimenv/bin/python
└── text_encoders/      # local Llama-3 encoder mirror (built by the lib's setup_text_encoder.py)
```

Model weights — the ~3 GB Kimodo checkpoint and the 16 GB Llama base — live in `~/.cache/huggingface`; `text_encoders/` is symlinks into it. Install steps for all four entries: `kimodo-practical/KIMODO.md` §1, run from `$KIMODO_HOME`. The venv is not relocatable (absolute shebangs, editable install) — pick the location once, or rebuild the venv after a move.

Export in `~/.bashrc` (and `~/.zshrc`):

```bash
export KIMODO_HOME="$HOME/Documents/kimodo-home"
```

A set `KIMODO_HOME` is the signal agents key on: the stack is installed and complete under it — reuse it, never re-fetch or search the filesystem. It is the only animation env var; upstream Kimodo's own variables derive from the fixed layout and are set per command (`TEXT_ENCODERS_DIR="$KIMODO_HOME/text_encoders"`, `TEXT_ENCODER_DEVICE=cpu`), as `motion.md` and the lib's docs instruct.

Verify:

```bash
"$KIMODO_HOME/kimenv/bin/python" -c "import kimodo, torch; print(torch.cuda.is_available())"  # True
ls "$KIMODO_HOME/text_encoders/llama3-8b-instruct-base/config.json"
```

## Local Image Generation (Optional)

A `qwen-image` command on `PATH` runs [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) on the local GPU. When the asset-gen skill finds it, simple images are generated there for free; otherwise they go to the paid APIs.

Requires an NVIDIA GPU with a working CUDA driver and ~33 GB of weights to download. Unquantized, the model wants ~40 GB VRAM; quantized with CPU offload, a 12 GB card with 23 GB RAM runs it at ~2.5 min per 1024² image.

GPUs, drivers, and memory differ too much for one recipe, so there isn't one: on the target machine, have Claude Code build the command from the brief below.

### Brief

Goal: a `qwen-image` command on `PATH` that runs Qwen-Image-2.1 (https://huggingface.co/Qwen/Qwen-Image-2.1, diffusers `QwenImage21Pipeline`) locally with the interface below. Download the model, quantize/offload if the local GPU needs it, implement the CLI in its own isolated Python environment. One-shot command, not a server. It must behave the same from any directory and shell, whatever the caller's environment (an active venv, `PYTHONPATH`, `LD_LIBRARY_PATH`) — game agents call it from their own project shells.

- `qwen-image generate PROMPT` | `qwen-image rgba PROMPT` (transparent PNG; the command adds the model's RGBA prompt phrasing itself) | `qwen-image edit -i IMG [-i IMG ...] PROMPT` | `qwen-image info`
- `PROMPT` of `-` reads stdin.
- Options: `-o/--out PATH`, `--size WxH`, `--resolution N` (default 1024), `--steps N` (default 40), `--seed N` (random if omitted), `--cfg F`, `--negative TEXT`, `--json`.
- stdout: absolute output path, or with `--json` `{output, width, height, mode, prompt, seed, steps, cfg, inputs, seconds, peak_vram_gb}` / `{"error": ...}`. Progress on stderr. Exit 0 on success, 1 on failure. Output is PNG.

Known trap: don't quantize the transformer with bitsandbytes LLM.int8 (`load_in_8bit`). Its kernel casts activations to fp16, which overflows on this DiT and returns the same noise for every prompt. NF4 or torchao int8 weight-only are clean.

Verify:

```bash
qwen-image info
qwen-image rgba --resolution 512 --steps 10 "a red apple" -o /tmp/apple.png   # look at it
magick identify -format '%[opaque]\n' /tmp/apple.png                           # False (has transparency)
```

## API Keys

Set in environment:

- `GOOGLE_API_KEY` — Gemini image generation
- `XAI_API_KEY` — xAI Grok image/video generation
- `TRIPO_API_KEY` — image-to-3D conversion via the `tripo` CLI (`npm install -g tripo-cli`, Node 20+)

## Verify Rendering

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json vulkaninfo --summary 2>&1 | grep "deviceName"
xvfb-run -a godot --headless --quit
```
