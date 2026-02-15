---
name: asset-gen
description: |
  Generate game assets (PNG images and GLB 3D models) using Gemini and Tripo3D.
  Provides CLI tools for image generation and 3D model conversion.

  **When to use:** When you need to generate visual assets for a Godot game — textures, 3D model reference images, or GLB models.
---

# Asset Generator

Generate PNG images (Gemini) and GLB 3D models (Tripo3D) from text prompts.

## CLI Reference

The tool lives at `.agents/skills/asset-gen/tools/asset_gen.py`. Run from the project root.

### Generate image (4 cents)

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

### Convert image to GLB (30-60 cents)

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### Output format

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 4}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress goes to stderr.

## Cost Table

| Operation | Preset | Cost | Notes |
|-----------|--------|------|-------|
| Image | — | 4 cents | Gemini Flash |
| GLB | medium | 30 cents | 20k faces, good default |
| GLB | lowpoly | 40 cents | 5k faces, smart topology |
| GLB | high | 40 cents | Adaptive faces, detailed textures (+10¢) |
| GLB | ultra | 60 cents | Detailed textures + geometry (+10¢ +20¢) |

A full 3D asset (image + GLB) costs 34 cents at medium quality. A texture is 4 cents (no GLB needed).

## Prompt Construction

You build the full prompt and pass it via `--prompt`. Use the templates below as a starting point — adapt as needed for the specific game.

### 3D model images

Recommended prompt template:
```
{style}, 3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```

Key principles for Tripo3D-friendly images:
- 3/4 front elevated angle — gives the reconstructor enough geometry info
- Solid white/gray background — clean separation from subject
- Matte finish, no reflections — specular highlights confuse depth estimation
- Opaque glass/windows — translucency creates holes in the mesh
- Single centered subject — multi-object scenes produce bad geometry

### Textures

Recommended prompt template:
```
{style}, {name}, {description}. Top-down view, uniform lighting, no shadows, seamless tileable texture, suitable for game engine tiling, clean edges.
```

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
