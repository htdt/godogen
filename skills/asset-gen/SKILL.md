---
name: asset-gen
description: |
  This skill should be used when the user asks to "generate assets", "create textures", "make 3D models", or needs to generate PNG images or GLB models for a Godot game. Provides CLI tools for image generation (Gemini) and 3D model conversion (Tripo3D).
---

# Asset Generator

Generate PNG images (Gemini) and GLB 3D models (Tripo3D) from text prompts.

## CLI Reference

Tools live at `.claude/skills/asset-gen/tools/`. Run from the project root.

### Generate image (4 cents)

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

### Remove background

Uses rembg mask + alpha matting. Handles semi-transparent objects, fine edges, hair, glass, particles. Auto-detects the background color from corner pixels. Dependencies in `.claude/skills/asset-gen/tools/requirements.txt`.

```bash
python3 .claude/skills/asset-gen/tools/rembg_matting.py \
  assets/img/car.png -o assets/img/car_nobg.png
```

### Generate sprite sheet (14 cents)

Always 4x4 = exactly 16 cells. All 16 must be used — no more, no less. Template and grid instructions are injected automatically; you provide only the subject and BG color.

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py spritesheet \
  --prompt "Animation: a knight swinging a sword" \
  --bg "#4A6741" -o assets/img/knight_swing_raw.png
```

- `--prompt` — subject only. Don't specify frame count (system prompt handles it). For animations describe the action; for collections number each item 1-16.
- `--bg` — background color hex (default: `#00FF00`). See BG strategy in Prompt Construction below.

### Clean sprite sheet

Crops red grid lines. Two modes: `keep-bg` keeps the background, `clean-bg` also removes background per frame via rembg and reassembles. Output: single PNG for `Sprite2D` (`hframes=4, vframes=4`).

```bash
# Keep background (textures, solid-color game BG)
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py keep-bg \
  assets/img/knight_raw.png -o assets/img/knight.png

# Remove background (sprites, characters, items — preferred)
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py clean-bg \
  assets/img/knight_raw.png -o assets/img/knight.png
```

### Convert image to GLB (30-60 cents)

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### Set budget

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py set_budget 500
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

## Style

Before generating any assets, choose an interesting visual style for the game. Bake the style into every prompt to keep all assets visually consistent. Include `{style}` as the first element in all prompts.

## Image Resolution

Use the full generation resolution — don't downscale for aesthetic reasons.
- Single images / textures / 3D references: **1024x1024**
- Sprite sheets: 2048x2048 total → **512x512 per cell** (after grid crop ~500x500)

## Prompt Construction

You build the full prompt and pass it via `--prompt`. Use the templates below as a starting point — adapt as needed for the specific game.

**Never ask the generator to produce a "transparent background"** — it will draw a checkerboard pattern imitating transparency, which is useless. Always generate with a solid background color and remove it with `rembg_matting.py` afterwards.

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

Textures are the one case where background removal does NOT apply — keep the background as-is.

### Sprite sheets

Prompt examples (don't specify frame count — system prompt handles it):
```
Animation: a slime bouncing
Items in flat vector style: 1: red apple 2: banana 3: orange 4: grape ...
```

**BG strategy:** Choose a `--bg` color that is (1) distinct from the subject so rembg can separate cleanly, and (2) close to the expected in-game environment background so any residual fringe blends naturally. Examples: forest game → muted green `#4A6741`; sky/water → muted blue `#4A6B8A`; dungeon → dark gray `#2A2A2A`. Avoid pure chromakey colors like `#00FF00` — they create unnatural fringing.

Prefer `clean-bg` — keeping the background almost always looks bad in-game (padding around the object).

### Single images (sprites, UI, items)

For non-texture single images, prefer to remove the background. Generate with a background color that contrasts with the subject but is close to the expected environment, then run `rembg_matting.py`.

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
