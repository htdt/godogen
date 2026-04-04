# Workstation Setup

## .NET 8 SDK

Required for C# Godot projects. Install before Godot.

### Linux (Ubuntu/Debian)

```bash
# Microsoft package repo (recommended — apt dotnet-sdk-8.0 may not exist on all distros)
wget https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh
chmod +x /tmp/dotnet-install.sh
/tmp/dotnet-install.sh --channel 8.0 --install-dir /usr/local/share/dotnet
sudo ln -sf /usr/local/share/dotnet/dotnet /usr/local/bin/dotnet
```

Or if your distro has it:
```bash
sudo apt-get install -y dotnet-sdk-8.0
```

### macOS

```bash
brew install dotnet@8
```

### Verify and PATH

`dotnet` must be on PATH for both the user and any shell Claude Code spawns:

```bash
dotnet --version   # 8.0.x
which dotnet       # should resolve
```

If installed via the script to `/usr/local/share/dotnet`, the symlink above handles PATH. If installed elsewhere, add to `~/.bashrc` or `~/.zshrc`:
```bash
export DOTNET_ROOT=/path/to/dotnet
export PATH="$DOTNET_ROOT:$PATH"
```

## System Packages

```bash
sudo apt-get install mesa-utils ffmpeg imagemagick

# ImageMagick 7 (provides `magick` CLI — apt only has v6)
wget https://imagemagick.org/archive/binaries/magick
chmod +x magick
sudo mv magick /usr/local/bin/
```

- **mesa-utils** — provides `glxinfo` for GPU detection
- **ffmpeg** — AVI→MP4 conversion, video frame extraction
- **imagemagick** — image resize, flip, crop for sprite pipelines

No xvfb needed when a GPU is available.

## macOS

```bash
brew install coreutils ffmpeg dotnet@8
```

- **coreutils** — provides `gtimeout`; the capture script falls back to a perl-based timeout if missing
- **ffmpeg** — AVI→MP4 conversion
- macOS uses Metal natively — no xvfb or Vulkan setup needed.

## Python

Requires Python 3.10+.

```bash
python3 --version
pip install -r skills/godogen/tools/requirements.txt
```

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

- `GOOGLE_API_KEY` — Gemini image generation (references, characters, precise work)
- `XAI_API_KEY` — xAI Grok image/video generation (textures, simple objects)
- `TRIPO3D_API_KEY` — image-to-3D conversion (3D games only)

## Verify All

```bash
dotnet --version                 # 8.0.x
godot --version                  # 4.x.x.stable.mono
nvidia-smi                       # GPU available
python3 -c "import rembg; print('rembg ok')"
```

GPU detection needs X11 sockets in `/tmp/.X11-unix/`. Confirm with:

```bash
for sock in /tmp/.X11-unix/X*; do
  d=":${sock##*/X}"
  DISPLAY=$d glxinfo 2>/dev/null | grep -i "opengl renderer" && echo "GPU on $d"
done
```
