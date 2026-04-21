# Workstation Setup

Shared workstation setup for both source trees in this repo.

## Bevy Docs Cache

If you work on the Bevy source trees in this repo, choose a shared docs folder and populate it once after clone:

```bash
./setup_bevy_docs.sh /absolute/or/user/path/to/bevy-docs
```

This script:

- links both Bevy skill trees to one shared docs cache
- clones or updates `bevy` and `bevy-website`
- builds local rustdoc for the current stable Bevy release

It exposes:

- `codex_bevy/skills/bevy-help/docs/{rustdoc,bevy,bevy-website}`
- `claude_bevy/skills/bevy-help/docs/{rustdoc,bevy,bevy-website}`

No default path is assumed. Pick a writable folder on your machine.

If you later publish `codex_bevy/` or `claude_bevy/`, the publish script reuses the source repo's configured docs symlinks.

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

### Verify

```bash
dotnet --version   # 9.0.x
```

## System Packages

```bash
sudo apt-get install vulkan-tools xvfb ffmpeg imagemagick
```

- **vulkan-tools** — `vulkaninfo` for GPU validation
- **xvfb** — virtual X11 display. Godot needs a display server for **any** rendering (including offscreen `--write-movie`), even with an NVIDIA GPU. On headless machines (SSH, CI), xvfb provides this.
- **ffmpeg** — AVI→MP4 conversion, video frame extraction
- **imagemagick** — image resize, flip, crop for sprite pipelines

```bash
# ImageMagick 7 (provides `magick` CLI — apt only has v6)
wget https://imagemagick.org/archive/binaries/magick
chmod +x magick
sudo mv magick /usr/local/bin/
```


## macOS

```bash
brew install coreutils ffmpeg dotnet@9
```

- **coreutils** — provides `gtimeout`; the capture script falls back to a perl-based timeout if missing
- **ffmpeg** — AVI→MP4 conversion
- macOS uses Metal natively — no xvfb or Vulkan setup needed.

## Python

Requires Python 3.10+.

```bash
python3 --version
pip install -r claude/skills/godogen/tools/requirements.txt
# or
pip install -r codex/skills/godogen/tools/requirements.txt
```

The two requirements files should stay aligned. Install either one in the source repo.

In a published game repo, the same file lives at:

- `.claude/skills/godogen/tools/requirements.txt` for Claude Code
- `.agents/skills/godogen/tools/requirements.txt` for Codex

## Godot (.NET edition)

The **.NET edition** is required — the standard Godot build cannot run C# scripts. Download from the **Mono/.NET** column on the Godot downloads page.

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

`GodotSharp/` must live next to the `godot` binary. Godot resolves it relative to itself — if you symlink `godot`, the directory must be next to the real binary, not the symlink.

### macOS

```bash
# Download .NET build from godotengine.org, or:
brew install --cask godot-mono
```

Godot must be on PATH as `godot`. If installed from the .app bundle:
```bash
sudo ln -sf /Applications/Godot_mono.app/Contents/MacOS/Godot /usr/local/bin/godot
```

### Verify

```bash
godot --version          # should show version
godot --headless --quit  # should exit cleanly (may show RID warnings — harmless)
```

If `godot --headless --quit` crashes with assembly errors, `GodotSharp/` is not being found. Check it's next to the binary:
```bash
ls "$(dirname "$(which godot)")"/GodotSharp/
```

## Android Export

### OpenJDK 17

```bash
sudo apt-get install -y openjdk-17-jdk
```

### Android SDK

Download command-line tools from https://developer.android.com/studio#command-line-tools-only and install:

```bash
sudo mkdir -p /opt/android-sdk/cmdline-tools
cd /tmp && wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
sudo unzip -o cmdline-tools.zip -d /opt/android-sdk/cmdline-tools/
sudo mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest
```

Install required SDK components:

```bash
sudo /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/opt/android-sdk \
  "platform-tools" "build-tools;35.0.1" "platforms;android-35" \
  "cmake;3.10.2.4988404" "ndk;28.1.13356709"
```

### Export Templates

Download the TPZ matching your Godot version and unpack:

```bash
VERSION=$(godot --version | cut -d. -f1-3)
TEMPLATE_DIR=~/.local/share/godot/export_templates/${VERSION}.stable
mkdir -p "$TEMPLATE_DIR"
cd /tmp
wget -q "https://github.com/godotengine/godot/releases/download/${VERSION}-stable/Godot_v${VERSION}-stable_export_templates.tpz" -O export_templates.tpz
unzip -o export_templates.tpz -d /tmp/tpz_extract
mv /tmp/tpz_extract/templates/* "$TEMPLATE_DIR/"
```

### Debug Keystore

Generate once (Godot uses this for debug signing):

```bash
mkdir -p ~/.local/share/godot/keystores
keytool -genkey -v -keystore ~/.local/share/godot/keystores/debug.keystore \
  -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass android -keypass android \
  -dname "CN=Android Debug,O=Android,C=US"
```

### Godot Editor Settings

Run `godot --headless --quit` once in any project to generate the settings file, then set Android paths in `~/.config/godot/editor_settings-4.5.tres`:

```ini
export/android/debug_keystore = "/home/<user>/.local/share/godot/keystores/debug.keystore"
export/android/debug_keystore_user = "androiddebugkey"
export/android/debug_keystore_pass = "android"
export/android/java_sdk_path = "/usr/lib/jvm/java-17-openjdk-amd64"
export/android/android_sdk_path = "/opt/android-sdk"
```

All three keystore fields must be set together or Godot silently fails.

### Verify

```bash
java -version                    # 17.x
/opt/android-sdk/platform-tools/adb --version
ls ~/.local/share/godot/export_templates/*/android_debug.apk
```

## API Keys

Set in environment:

- `GOOGLE_API_KEY` — Gemini image generation (references, characters, precise work) and the Codex Bevy post-task visual gate
- `XAI_API_KEY` — xAI Grok image/video generation (textures, simple objects)
- `TRIPO3D_API_KEY` — image-to-3D conversion (3D games only)

## Codex Bevy Post-Task Gate

`codex_bevy/publish.sh` installs a Codex `Stop` hook that verifies the latest `screenshots/result/{N}/` bundle with Gemini. The hook runs `.codex/hooks/verify_result.py` in the host Python environment and needs:

```bash
pip install google-genai pydantic
```

`ffprobe` (bundled with `ffmpeg`, already listed above) must be on `PATH` — the hook reads video fps and duration through it. `GOOGLE_API_KEY` is required at hook runtime.

## Notifications (optional)

[tg-push](https://github.com/htdt/tg-push) is a single-shot CLI that sends text plus an optional image or video to Telegram. The agent uses it to report progress, QA verdicts, and the final video — especially useful when a run executes on a remote server.

```bash
pipx install tg-push
```

Set `TG_BOT_TOKEN` (from [@BotFather](https://t.me/BotFather)) and `TG_CHAT_ID` in the environment.

## Verify All

```bash
dotnet --version                 # 9.0.x
godot --version                  # 4.x.x.stable.mono
nvidia-smi                       # GPU available
python3 -c "import rembg; print('rembg ok')"
```

Verify rendering pipeline (GPU + xvfb):

```bash
# NVIDIA Vulkan driver
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json vulkaninfo --summary 2>&1 | grep "deviceName"

# xvfb + Godot (headless rendering — the actual capture path)
xvfb-run -a godot --headless --quit
```
