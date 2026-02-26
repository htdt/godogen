---
name: asset-gen
description: |
  This skill should be used when the user asks to "generate assets", "create textures", "make 3D models", or needs to generate PNG images or GLB models for a Godot game. Provides CLI tools for image generation (Gemini) and 3D model conversion (Tripo3D).
---

# Asset Generator

Generate PNG images (Gemini) and GLB 3D models (Tripo3D) from text prompts.

## CLI Reference

Tools live at `.claude/skills/asset-gen/tools/`. Run from the project root.

### Generate image (5-10 cents)

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

`--size` (default `1K`): `512` (5¢), `1K` (7¢), `2K` (10¢)
`--aspect-ratio` (default `1:1`): `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`

Typical combos: `--size 2K --aspect-ratio 16:9` (landscape bg), `--size 2K --aspect-ratio 9:16` (portrait), `--size 1K` (textures, sprites, 3D refs).

### Remove background

Uses rembg mask + alpha matting. Handles semi-transparent objects, fine edges, hair, glass, particles. Auto-detects the background color from corner pixels. Dependencies in `.claude/skills/asset-gen/tools/requirements.txt`.

If rembg is not installed:
```bash
pip install rembg[gpu,cli]   # use rembg[cpu,cli] if no GPU
rembg d isnet-anime          # download model
```

```bash
python3 .claude/skills/asset-gen/tools/rembg_matting.py \
  assets/img/car.png -o assets/img/car_nobg.png
```

### Generate sprite sheet (7 cents)

Always 4x4 = exactly 16 cells. All 16 must be used — no more, no less. Template and grid instructions are injected automatically; you provide only the subject and BG color.

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py spritesheet \
  --prompt "Animation: a knight swinging a sword" \
  --bg "#4A6741" -o assets/img/knight_swing_raw.png
```

- `--prompt` — subject only. Don't specify frame count (system prompt handles it). For animations describe the action; for collections number each item 1-16.
- `--bg` — background color hex (default: `#00FF00`). See BG color strategy below.

### Process sprite sheet

Crops red grid lines. Choose mode based on use case:

**Animation frames** → output single sheet for `Sprite2D` (`hframes=4, vframes=4`):
```bash
# Keep background (textures, solid-color game BG)
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py keep-bg \
  assets/img/knight_raw.png -o assets/img/knight.png

# Remove background (sprites, characters — preferred)
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py clean-bg \
  assets/img/knight_raw.png -o assets/img/knight.png
```

**Collection of distinct objects** (items, icons, props) → split into 16 individual PNGs:
```bash
# Split with background kept
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py split-bg \
  assets/img/items_raw.png -o assets/img/items/

# Split with background removed (preferred for in-game objects)
python3 .claude/skills/asset-gen/tools/spritesheet_slice.py split-clean \
  assets/img/items_raw.png -o assets/img/items/ \
  --names "apple,banana,orange,grape,cherry,lemon,pear,plum,peach,melon,kiwi,mango,berry,fig,lime,coconut"
```

For split modes, `-o` is the output **directory**. `--names` provides filenames (without `.png`) for each cell left-to-right, top-to-bottom. Without `--names`, files are numbered `01.png`..`16.png`.

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

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 7}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress goes to stderr.

## Cost Table

| Operation | Preset | Cost | Notes |
|-----------|--------|------|-------|
| Image | --size 512 | 5 cents | 704x384 (aspect ratio ignored) |
| Image | --size 1K | 7 cents | Default. Configurable aspect ratio |
| Image | --size 2K | 10 cents | Configurable aspect ratio |
| Sprite sheet | — | 7 cents | 1K, 4x4 grid (16 cells, 256x256 each) |
| GLB | medium | 30 cents | 20k faces, good default |
| GLB | lowpoly | 40 cents | 5k faces, smart topology |
| GLB | high | 40 cents | Adaptive faces, detailed textures (+10¢) |
| GLB | ultra | 60 cents | Detailed textures + geometry (+10¢ +20¢) |

A full 3D asset (image + GLB) costs 37 cents at medium quality. A texture is 7 cents. A sprite sheet is 7 cents for 16 frames/items. A high-res background is 10 cents.

## Style

Before generating any assets, choose an interesting visual style for the game. Bake the style into every prompt to keep all assets visually consistent. Include `{style}` as the first element in all prompts.

## Image Resolution

Use the full generation resolution — don't downscale for aesthetic reasons.
- Default (`1K`): textures, sprites, 3D references
- `2K`: backgrounds, title screens, large scenic art
- `512`: quick tests only (704x384, aspect ratio ignored)
- Sprite sheets: 1024x1024 total → **256x256 per cell** (after grid crop ~248x248)

## What to Generate — Cheatsheet

**CRITICAL: Never prompt for "transparent background" — the generator draws a checkerboard. Always use a solid color background, then remove with `rembg_matting.py`.**

Include `{style}` as the first element in all prompts. Adapt templates as needed.

### Background / large scenic image (10¢)

Title screens, sky panoramas, parallax layers, environmental art.

```
{style}, {description}. {composition instructions}.
```
`image --prompt "..." --size 2K --aspect-ratio 16:9 -o path.png`

No post-processing — use as-is.

### Texture (7¢)

Tileable surfaces: ground, walls, floors, UI panels.

```
{style}, {name}, {description}. Top-down view, uniform lighting, no shadows, seamless tileable texture, suitable for game engine tiling, clean edges.
```
`image --prompt "..." -o path.png`

No background removal — the entire image IS the texture.

### Single object / sprite (7¢)

**With background** (object on a known scene background):
```
{style}, {name}, {description}.
```

**Transparent** (characters, props, icons, UI elements) — **CRITICAL: prompt must include a solid flat background color.** Without it, the generator draws a detailed/noisy background that rembg cannot cleanly separate:
```
{style}, {name}, {description}. Centered on a solid {bg_color} background.
```
Then: `rembg_matting.py input.png -o output.png`

### 3D model reference (7¢) + GLB (30-60¢)

```
{style}, 3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

### Animation → Spritesheet (7¢)

16 cells in a 4×4 grid. Flexible layouts:
- 16 frames of one subject (walk cycle, attack, bounce)
- 4 objects × 4 frames each (4 enemies × 4 walk frames)
- 2 objects × 8 frames (split across rows)

The longer/more complex the animation, the more likely it breaks — keep motions simple.

```
Animation: a slime bouncing
```

Post-processing:
- **Transparent sprites** (preferred): `clean-bg` → single sheet for `Sprite2D` (`hframes=4, vframes=4`)
- **With background:** `keep-bg` → single sheet

### Asset kit (16 objects, consistent style) → Spritesheet (7¢)

Generate 16 small objects that share the same visual style (items, icons, props, tiles). Cheaper and more consistent than 16 individual calls (7¢ vs 112¢).

```
Items: 1: red apple 2: banana 3: orange 4: grape 5: cherry ...
```

Number every item 1-16. Don't specify grid layout — system prompt handles it.

Post-processing — split into individual images:
- **Transparent** (preferred): `split-clean -o dir/ --names "apple,banana,..."`
- **With background:** `split-bg -o dir/ --names "apple,banana,..."`

---

### BG color strategy (applies to all transparent assets)

Pick a `--bg` / prompt bg color that is (1) **distinct from the subject** so rembg separates cleanly, and (2) **close to the expected in-game environment** so residual fringe blends naturally.

Examples: forest game → `#4A6741`; sky/water → `#4A6B8A`; dungeon → `#2A2A2A`; generic → `#808080`.

Avoid pure chromakey colors like `#00FF00` — they create unnatural green fringing.

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
