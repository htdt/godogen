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

Read `${CLAUDE_SKILL_DIR}/rembg.md` for full guide: CLI, prompting strategy, troubleshooting, batch mode.

### Generate animated sprite video (5¢/sec)

Full workflow: reference image → video → extract frames → batch rembg → sprite frames.

**Step 1: Reference image (7¢)**

Pro model, 1:1, neutral pose, solid BG — same color strategy as static sprites. This image becomes the video's starting frame. Review it carefully: a bad reference wastes 5¢/sec on every video generated from it.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --model pro --prompt "knight in armor, neutral standing pose, facing right, solid #4A6741 background" \
  --aspect-ratio 1:1 -o assets/img/knight_ref.png
```

**Step 2: Generate video**

The reference image is auto-resized to match video resolution (480p = 480×480 for 1:1).

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py video \
  --prompt "knight walking forward, side view, smooth walk cycle" \
  --image assets/img/knight_ref.png \
  --duration 3 -o assets/video/knight_walk.mp4
```

`--duration` (1-15 seconds), `--resolution` (default `480p`): `480p`, `720p`

**Step 3: Extract frames**

```bash
mkdir -p assets/video/knight_walk_frames
ffmpeg -i assets/video/knight_walk.mp4 -vsync 0 assets/video/knight_walk_frames/%04d.png
```

**Step 4: Batch background removal** (see `rembg.md` for full guide)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/rembg_matting.py \
  --batch assets/video/knight_walk_frames/ \
  -o assets/img/knight_walk/
```

Multiple animations for one character share the same reference image (paid once). Generate videos in parallel.

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
| Video | --duration N | 5¢ × N seconds | Reference image (pro, 7¢) paid once per character |

A full 3D asset (image + GLB) costs 32 cents at medium quality. A texture is 2 cents. A pro background is 7 cents. A 3-second animation costs 22 cents (7¢ ref + 15¢ video); additional animations from the same ref cost only the video.

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

For any asset needing transparency, read `${CLAUDE_SKILL_DIR}/rembg.md` first — covers BG color strategy, CLI, and troubleshooting.

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

**Transparent** (characters, props, icons, UI elements) — prompt with solid BG color, then rembg (see `rembg.md`):
```
{name}, {description}. Centered on a solid {bg_color} background.
```

### 3D model reference (2c) + GLB (30-60c)

```
3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

### Animated sprite — reference image (7c pro) + videos (5c/sec each)

**Reference image:**
```
{name}, {description}. Neutral standing pose, facing right, centered on a solid {bg_color} background. Clean silhouette.
```
`image --model pro --prompt "..." -o path_ref.png`

Then rembg the reference to check quality before committing to videos.

**Video prompt (per action):**
```
{name} performing {action}, side view, smooth {action} animation. Solid {bg_color} background maintained.
```
`video --prompt "..." --image path_ref.png --duration N -o path.mp4`

Then: ffmpeg frame extraction → batch rembg → clean RGBA frames. See `rembg.md` for CLI and batch details.

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
