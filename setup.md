# Workstation Setup

Shared workstation setup for the consolidated Godogen source repo.

## Bevy Docs Cache

If you work on the Bevy source in this repo, choose a shared docs folder and populate it once after clone:

```bash
./setup_bevy_docs.sh /absolute/or/user/path/to/bevy-docs
```

This script:

- links `bevy/skills/bevy-help/docs/` to one shared docs cache
- clones or updates `bevy` and `bevy-website`
- builds local rustdoc for the current stable Bevy release

No default path is assumed. Pick a writable folder on your machine. Published Bevy game repos reuse the source repo's configured docs symlinks.

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

## System Packages

```bash
sudo apt-get install vulkan-tools xvfb ffmpeg imagemagick
```

- **vulkan-tools** — `vulkaninfo` for GPU validation
- **xvfb** — virtual X11 display for headless Godot/Bevy smoke tests
- **ffmpeg** — MP4 encoding and `ffprobe` for hook validation
- **imagemagick** — image resize, flip, crop for sprite pipelines

On macOS:

```bash
brew install coreutils ffmpeg dotnet@9
```

## Python

Requires Python 3.10+.

```bash
python3 --version
pip install -r shared/skills/godogen/tools/requirements.txt
pip install google-genai
```

In a published game repo, the same asset-generation requirements file lives at:

- `.claude/skills/godogen/tools/requirements.txt` for Claude Code
- `.agents/skills/godogen/tools/requirements.txt` for Codex

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

## Godot Android Export

Godot Android export is only needed when a Godot runtime task asks for an APK.

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

Generate once:

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
java -version
/opt/android-sdk/platform-tools/adb --version
ls ~/.local/share/godot/export_templates/*/android_debug.apk
```

## API Keys

Set in environment:

- `GOOGLE_API_KEY` — Gemini image generation
- `XAI_API_KEY` — xAI Grok image/video generation
- `TRIPO3D_API_KEY` — image-to-3D conversion

## Post-Task Telegram Push (optional)

Published repos install a `Stop` hook that pushes the latest `screenshots/result/{N}/video.mp4` to Telegram. The hook is best-effort: it no-ops unless [tg-push](https://github.com/htdt/tg-push) is on `PATH` and both `TG_BOT_TOKEN` and `TG_CHAT_ID` are set.

```bash
pipx install tg-push
```

Set `TG_BOT_TOKEN` and `TG_CHAT_ID` in the environment.

## Verify Rendering

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json vulkaninfo --summary 2>&1 | grep "deviceName"
xvfb-run -a godot --headless --quit
```
