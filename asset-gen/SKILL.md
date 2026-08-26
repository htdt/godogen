---
name: asset-gen
display_name: Asset Generator
short_description: Generate game images, GLB 3D models, and animated sprites
default_prompt: "Use ${ASSET_SKILL_COMMAND} to generate images, 3D models, or animated sprites for this game."
allow_implicit_invocation: true
description: |
  Generate visual assets from text prompts: PNG images and videos with Alibaba Cloud Wan, GLB 3D models with Tencent Hunyuan 3D, and frame-by-frame animated sprites with local extraction and background removal. Use whenever a game needs generated art.
---

# Asset Generator

This skill uses China mainland cloud services: Alibaba Cloud Wan for PNG images and image-to-video, and Tencent Hunyuan 3D for image-to-GLB. Every generation is billable; confirm with the user before making a request. Tools live at `${ASSET_GEN_SKILL_DIR}/tools/`; keep runtime-loaded outputs under `${RUNTIME_ASSET_DIR}/`.

## Images

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" --size 1K --aspect-ratio 1:1 \
  -o ${RUNTIME_ASSET_DIR}/img/car.png
```

Use `--image ref.png` for image-to-image generation. Prompt only for what changes when making a style family or a pose variant. Valid sizes are `1K`, `2K`, and `4K`; valid aspect ratios are `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, and `2:3`.

Review every PNG before using it as a 3D reference. For tiny sprites, generate a kit at 1K and slice it with `tools/grid_slice.py`, or use bold, flat forms that survive downscaling.

### Background removal

Read `${ASSET_GEN_SKILL_DIR}/rembg.md`. Never prompt for a transparent background: generate against a solid color, then matte it locally.

## Animated sprites

Recipe: **reference → pose → video → extract frames → loop-trim → rembg.**

1. Generate a neutral reference with `image`; review it before reuse.
2. Generate each action pose with `image --image ref.png`.
3. Generate a 5s or 10s clip: `asset_gen.py video --image pose.png --duration 5 -o walk.mp4`.
4. Extract frames: `ffmpeg -i walk.mp4 -vsync 0 frames/%04d.png`.
5. For loops, run `tools/find_loop_frame.py frames/` and trim frames after the reported frame.
6. Matte frames: `tools/rembg_matting.py --batch frames/ -o clean/`.

Reuse one reference for a character's actions. Chain at most two actions; longer chains drift.

## 3D models

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py glb --image ref.png -o model.glb
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py glb --image ref.png --quality hd -o model.glb
```

Use a 3/4 elevated image with a solid white or gray background, matte materials, opaque glass, and one centered subject. Do not remove its background before passing it to Hunyuan 3D. `--quality hd` requests the provider's high-quality mode; `--no-pbr` disables PBR when the imported material renders poorly.

Hunyuan 3D generation is asynchronous. The submitted job ID is stored in `<output>.hunyuan.json`; do not submit a second job after a timeout. Resume the existing one instead:

```bash
python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py resume -o model.glb
```

The former Tripo biped rigging and preset-animation retarget workflow is not exposed by this skill because Hunyuan 3D uses separate auto-rigging and text-motion workflows. Add that pipeline only after choosing the desired character and animation contract.

## Output and logging

Each command prints JSON to stdout: `{"ok": true, "path": "...", "cost_cents": 0}`. The cost field is intentionally `0`: Wan and Hunyuan billing varies by account, region, and selected model, so check the respective cloud console before confirming spend.

```bash
_log=$(mktemp)
result=$(python3 ${ASSET_GEN_SKILL_DIR}/tools/asset_gen.py image --prompt "..." -o p.png 2>"$_log") || tail -20 "$_log"
```

Generate independent images in parallel.

## Asset manifest (in README.md)

Track every generated asset in `README.md` with an **in-game Size** column:

- 3D models: meters, e.g. `4m long`, `1.8m tall`, `0.3m`
- Textures: tile size, e.g. `2m tile`
- Backgrounds: pixel size + behavior, e.g. `1920x1080, fullscreen`
- Sprites: display pixels, e.g. `128x128 px`
