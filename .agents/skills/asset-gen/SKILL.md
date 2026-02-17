---
name: asset-gen
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

The tool lives at `.agents/skills/asset-gen/tools/asset_gen.py`. Run from the project root.

### Generate image (4 cents)

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

### Generate sprite sheet (14 cents)

Always 4x4 = exactly 16 cells. All 16 must be used — no more, no less. Template and grid instructions are injected automatically; you provide only the subject and BG color.

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py spritesheet \
  --prompt "Animation: a knight swinging a sword" \
  --bg "#FF00FF" -o assets/img/knight_swing_raw.png
```

- `--prompt` — subject only. Don't specify frame count (system prompt handles it). For animations describe the action; for collections number each item 1-16.
- `--bg` — background color hex (default: `#00FF00`). See BG strategy in Prompt Construction below.

### Clean sprite sheet

Crops red grid lines. Optionally removes BG color via color-key. Output: single PNG for `Sprite2D` (`hframes=4, vframes=4`, frames 0-15).

```bash
# Keep BG
python3 .agents/skills/asset-gen/tools/spritesheet_slice.py \
  assets/img/knight_raw.png -o assets/img/knight.png

# Remove BG → transparent
python3 .agents/skills/asset-gen/tools/spritesheet_slice.py \
  assets/img/knight_raw.png -o assets/img/knight.png --remove-bg "#FF00FF"
```

Optional: `--gif preview.gif --fps 10` for preview, `--frames dir/` for individual PNGs.

### Convert image to GLB (30-60 cents)

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### Set budget

```bash
python3 .agents/skills/asset-gen/tools/asset_gen.py set_budget 500
```

Sets the generation budget to 500 cents. All subsequent generations check remaining budget and reject if insufficient. CRITICAL: only call once at the start, and only when the user explicitly provides a budget.

### Output format

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 4}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress goes to stderr.

## Cost Table

| Operation | Preset | Cost | Notes |
|-----------|--------|------|-------|
| Image | — | 4 cents | Gemini 2.5 Flash |
| Sprite sheet | — | 14 cents | Gemini 3 Pro, 4x4 grid (16 cells) |
| GLB | medium | 30 cents | 20k faces, good default |
| GLB | lowpoly | 40 cents | 5k faces, smart topology |
| GLB | high | 40 cents | Adaptive faces, detailed textures (+10¢) |
| GLB | ultra | 60 cents | Detailed textures + geometry (+10¢ +20¢) |

A full 3D asset (image + GLB) costs 34 cents at medium quality. A texture is 4 cents. A sprite sheet is 14 cents for 16 frames/items.

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

### Sprite sheets

Prompt examples (don't specify frame count — system prompt handles it):
```
Animation: a slime bouncing
Items in flat vector style: 1: red apple 2: banana 3: orange 4: grape ...
```

**BG strategy — two scenarios:**

**1. Opaque BG (easy, stable):** The game has a solid-color background (white, black, sky blue, etc.). Use that color as `--bg`, generate, clean grid lines only (no `--remove-bg`). The BG stays and matches the game. No artifacts, no hassle.

**2. Transparent BG (fragile):** Pick a `--bg` color absent from the subject, then clean with `--remove-bg`. Color-key removal has limitations: it can clip subject pixels that happen to match the BG color, and often leaves a faint contour tinted with the BG color around sprites. Creative workaround: use green (`#00FF00`) as BG and place the sprites on grass or a green surface in-game — the green contour blends naturally instead of looking like an artifact. Same idea applies to other colors (blue BG → water/sky scene, etc.).

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
