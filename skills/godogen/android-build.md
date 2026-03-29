# Android Build

Export a Godot project as a debug APK for Android.

## Prerequisites

- OpenJDK 17, Android SDK, export templates, debug keystore — see `setup.md` Android section
- Editor settings configured with Java/SDK/keystore paths

## Steps

### 1. Enable ETC2/ASTC texture compression

Add to `project.godot` under `[rendering]`:

```ini
[rendering]

textures/vram_compression/import_etc2_astc=true
```

Without this, Android export silently fails with a blank configuration error.

### 2. Create `export_presets.cfg`

Place in the project root. Minimal working preset:

```ini
[preset.0]

name="Android"
platform="Android"
runnable=true
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path=""
patches=[]
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

custom_template/debug=""
custom_template/release=""
gradle_build/use_gradle_build=false
gradle_build/gradle_build_directory=""
gradle_build/android_source_template=""
gradle_build/export_format=0
architectures/armeabi-v7a=false
architectures/arm64-v8a=true
architectures/x86=false
architectures/x86_64=false
keystore/debug=""
keystore/debug_user=""
keystore/debug_password=""
keystore/release=""
keystore/release_user=""
keystore/release_password=""
version/code=1
version/name="1.0"
package/unique_name="com.godogen.PROJECTNAME"
package/name=""
package/signed=true
package/app_category=2
package/retain_data_on_uninstall=false
package/exclude_from_recents=false
package/show_in_android_tv=false
package/show_in_app_library=true
package/show_as_launcher_app=false
launcher_icons/main_192x192=""
launcher_icons/adaptive_foreground_432x432=""
launcher_icons/adaptive_background_432x432=""
launcher_icons/adaptive_monochrome_432x432=""
graphics/opengl_debug=false
xr_features/xr_mode=0
screen/immersive_mode=true
screen/support_small=true
screen/support_normal=true
screen/support_large=true
screen/support_xlarge=true
user_data_backup/allow=false
command_line/extra_args=""
apk_expansion/enable=false
apk_expansion/SALT=""
apk_expansion/public_key=""
permissions/custom_permissions=PackedStringArray()
permissions/internet=false
```

Replace `PROJECTNAME` in `package/unique_name` with the actual project name (lowercase, no spaces).

Empty `keystore/*` fields fall back to the debug keystore in editor settings — this is correct for debug builds.

Do NOT set `gradle_build/min_sdk`, `gradle_build/target_sdk`, or `gradle_build/compress_native_libraries` when `use_gradle_build=false` — Godot rejects them.

### 3. Export

```bash
mkdir -p build
godot --headless --export-debug "Android" build/game.apk
```

The preset name (`"Android"`) must match `name=` in `export_presets.cfg`.

## Gotchas

- **Blank config error** — missing `textures/vram_compression/import_etc2_astc=true` in project.godot
- **Keystore error** — all three editor settings (`debug_keystore`, `debug_keystore_user`, `debug_keystore_pass`) must be set together or none
- **`cannot connect to daemon`** — benign, just means no adb server is running (no device connected)
- **gradle-only fields** — `min_sdk`, `target_sdk`, `compress_native_libraries` cause errors when gradle build is disabled
