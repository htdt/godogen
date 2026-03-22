# Asset Generator

Generate PNG images (xAI Grok) and GLB 3D models (Tripo3D) from text prompts.

## Models

| Model | Flag | Cost | Rate limit | Best for |
|-------|------|------|------------|----------|
| `grok-imagine-image` | `--model standard` | 2¢ | 300 req/min | Textures, sprites, 3D refs — high-volume |
| `grok-imagine-image-pro` | `--model pro` | 7¢ | 30 req/min | Backgrounds, title screens, visual targets — quality matters |

Default is `standard`. Use `pro` when visual quality is the priority (backgrounds, hero images, reference.png).

## CLI Reference

Tools live at `${CLAUDE_SKILL_DIR}/tools/`. Run from the project root.

### Generate image (2-7 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

`--model` (default `standard`): `standard` (2¢), `pro` (7¢)
`--size` (default `1K`): `1K`, `2K`
`--aspect-ratio` (default `1:1`): `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `2:1`, `1:2`, `19.5:9`, `9:19.5`, `20:9`, `9:20`, `auto`

Typical combos: `--model pro --size 2K --aspect-ratio 16:9` (landscape bg), `--model standard --size 1K` (textures, sprites, 3D refs).

### Remove background

Auto-detects bg color from corners, auto-selects regime based on mask quality. Dependencies in `${CLAUDE_SKILL_DIR}/tools/requirements.txt`.

If rembg is not installed:
```bash
pip install rembg[gpu,cli]   # use rembg[cpu,cli] if no GPU
```

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/rembg_matting.py \
  assets/img/car.png -o assets/img/car_nobg.png
```

Always read `${CLAUDE_SKILL_DIR}/rembg.md` after running — it explains how to read the output and fix issues.

### Convert image to GLB (30-60 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### Set budget

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py set_budget 500
```

Sets the generation budget to 500 cents. All subsequent generations check remaining budget and reject if insufficient. CRITICAL: only call once at the start, and only when the user explicitly provides a budget.

### Output format

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 2}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress goes to stderr.

## Cost Table

| Operation | Options | Cost | Notes |
|-----------|---------|------|-------|
| Image | --model standard | 2 cents | Default. Fast, high-volume |
| Image | --model pro | 7 cents | Higher quality output |
| GLB | medium | 30 cents | 20k faces, good default |
| GLB | lowpoly | 40 cents | 5k faces, smart topology |
| GLB | high | 40 cents | Adaptive faces, detailed textures (+10c) |
| GLB | ultra | 60 cents | Detailed textures + geometry (+10c +20c) |

A full 3D asset (image + GLB) costs 32 cents at medium quality. A texture is 2 cents. A pro background is 7 cents.

## Image Resolution

Use the full generation resolution — don't downscale for aesthetic reasons.
- Default (`1K`): textures, sprites, 3D references
- `2K`: HQ objects/textures, backgrounds, title screens

### Small sprites problem

Minimum generation resolution is 1K. A 1024px image downscaled to 64px or even 128px loses all fine detail and looks muddy. Mitigations:

1. **Avoid tiny display sizes.** Design game elements at 128px+ where possible. If a sprite must be small in-game, question whether it needs to be a generated image at all (a colored rectangle or simple shape drawn in code may read better at that size).
2. **Generate a kit image** — put multiple objects on one 1K image (e.g. 4 items in a 2x2 layout, each occupying ~512px) and crop the regions you need. More pixels per object = cleaner downscale.
3. **Prompt for bold, simple forms.** When the target display size is small, explicitly ask for: thick outlines, flat colors, minimal fine detail, exaggerated proportions. These survive downscaling; intricate textures don't.

## What to Generate — Cheatsheet

**CRITICAL: Never prompt for "transparent background" — the generator draws a checkerboard. Always use a solid color background, then remove with `rembg_matting.py`.**

### Background / large scenic image (7c pro)

Title screens, sky panoramas, parallax layers, environmental art. Best place for art direction language.

```
{description in the art style}. {composition instructions}.
```
`image --model pro --prompt "..." --size 2K --aspect-ratio 16:9 -o path.png`

No post-processing — use as-is.

### Texture (2c)

Tileable surfaces: ground, walls, floors, UI panels.

```
{name}, {description}. Top-down view, uniform lighting, no shadows, seamless tileable texture, suitable for game engine tiling, clean edges.
```
`image --prompt "..." -o path.png`

No background removal — the entire image IS the texture.

### Single object / sprite (2c)

**With background** (object on a known scene background):
```
{name}, {description}.
```

**Transparent** (characters, props, icons, UI elements) — **CRITICAL: prompt must include a solid flat background color.** Without it, the generator draws a detailed/noisy background that rembg cannot cleanly separate:
```
{name}, {description}. Centered on a solid {bg_color} background.
```
Then: `rembg_matting.py input.png -o output.png`

### 3D model reference (2c) + GLB (30-60c)

```
3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

---

### BG color strategy (applies to all transparent assets)

Pick a prompt bg color that is (1) **distinct from the subject** so rembg separates cleanly, and (2) **close to the expected in-game environment** so residual fringe blends naturally.

Examples: forest game → `#4A6741`; sky/water → `#4A6B8A`; dungeon → `#2A2A2A`; generic → `#808080`.

Avoid pure chromakey colors like `#00FF00` — they create unnatural green fringing.

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
