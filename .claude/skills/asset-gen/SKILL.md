---
triggers:
  - "generate assets"
  - "create assets"
  - "asset generation"
  - "make 3d models"
  - "generate textures"
description: |
  Generate game assets (PNG images and GLB 3D models) using Gemini and Tripo3D.
  Provides CLI tools for image generation and 3D model conversion.

  **When to use:** When you need to generate visual assets for a Godot game — textures, 3D model reference images, or GLB models.
---

# Asset Generator

Generate PNG images (Gemini) and GLB 3D models (Tripo3D) from text prompts.

## CLI Reference

The tool lives at `.claude/skills/asset-gen/tools/asset_gen.py`. Run from the project root.

### Generate image (4 cents)

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

### Convert image to GLB (30-80 cents)

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py glb \
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

Template:
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

Template:
```
{style}, seamless tileable texture of {name}. {description}. Top-down view, uniform lighting, no shadows, suitable for game engine tiling, clean edges.
```

### Writing good descriptions

Good: `"cartoon sedan with round headlights and chunky tires"`
Bad: `"a car"` (too vague) or `"3D render on white background at 3/4 angle"` (duplicates the template framing)

## Style Consistency

All assets in a game should share one style string. Establish it early, save to `assets/style.txt`, and prepend it to every prompt.

Recommended default:
```
Stylized realism, soft lighting, muted saturated colors, smooth clean surfaces, subtle material definition, rounded geometry with beveled edges
```

Example alternatives:
- `Low-poly flat-shaded, bright primary colors, geometric shapes, minimal detail`
- `Pixel art 3D, voxel-like, limited palette, chunky proportions`
- `Watercolor painterly, soft edges, pastel palette, hand-drawn feel`

## Workflow

### Single asset

1. Construct prompt using templates above + style from `assets/style.txt`
2. Generate: `asset_gen.py image --prompt "..." -o assets/img/X.png`
3. Read the PNG to review (centered? complete? clean bg? style match?)
4. If bad, adjust prompt and regenerate (costs another 4 cents)
5. If good and 3D: `asset_gen.py glb --image assets/img/X.png -o assets/glb/X.glb`
6. Update `assets/assets.md`

### Parallel generation

Generate multiple images in parallel by making multiple Bash calls in one message. Review all PNGs, then convert approved ones to GLBs in parallel.

## assets/assets.md

Track all generated assets. Read this file before generating to avoid duplicates.

```markdown
# Assets

**Style:** Low-poly flat-shaded, bright primary colors

## 3D Models

| Name | Description | Image | GLB |
|------|-------------|-------|-----|
| car | cartoon sedan with round headlights | assets/img/car.png | assets/glb/car.glb |

## Textures

| Name | Description | Image |
|------|-------------|-------|
| grass | green grass ground cover | assets/img/grass.png |
```

After generating assets, update this file.
