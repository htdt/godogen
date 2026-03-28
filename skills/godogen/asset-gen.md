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

### Generate animated sprite (2¢ ref + 2¢/pose + 5¢/sec video)

Workflow: reference → pose frame → video → slice → loop trim → rembg.

**Step 1: Reference image (2¢)**

Standard model, 1:1, neutral pose, solid BG — same color strategy as for rembg. Review carefully: this image anchors all subsequent poses and videos.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "knight in armor, neutral standing pose, facing right, solid dark-green background" \
  --aspect-ratio 1:1 -o assets/img/knight_ref.png
```

**Step 2: Pose frame (2¢)**

Image-to-image edit: feed the reference, prompt only for the action/pose.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "walking to the right, mid-stride pose, side view, solid dark-green background" \
  --image assets/img/knight_ref.png \
  --aspect-ratio 1:1 -o assets/img/knight_walk_pose.png
```

**Step 3: Generate video**

Feed the pose frame (not the reference) as the starting image. Prompt focuses on the motion, not appearance. Choose duration to fit the action — 2s for walk/run cycles, longer for complex actions.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py video \
  --prompt "walking to the right, smooth walk cycle, solid dark-green background" \
  --image assets/img/knight_walk_pose.png \
  --duration 2 -o assets/video/knight_walk.mp4
```

`--duration` (1-15 seconds), `--resolution` (default `720p`): `720p`, `480p`

Same cost per second at both resolutions — always use `720p`. Fall back to `480p` only if 720p fails (e.g. timeout or API error).

**Step 4: Extract frames**

```bash
mkdir -p assets/video/knight_walk_frames
ffmpeg -i assets/video/knight_walk.mp4 -vsync 0 assets/video/knight_walk_frames/%04d.png
```

**Step 5: Loop trim (looping animations only)**

For walk/run/idle cycles, find the frame most similar to frame 1 and trim there. Skip for one-shot animations (attack, death, jump).

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/find_loop_frame.py assets/video/knight_walk_frames/
```

Output: `{"loop_frame": 27, "similarity": 0.9997, "total_frames": 73}`

Then delete frames after the loop point, or note the range for the next step.

**Step 6: Batch background removal** (see `rembg.md` for full guide)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/rembg_matting.py \
  --batch assets/video/knight_walk_frames/ \
  -o assets/img/knight_walk/
```

**Step 7: Additional animations**

Repeat from step 2 using the same reference image. Each new animation costs 2¢ (pose) + video duration × 5¢.

### Convert image to GLB (30-60 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### Generate audio (3 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py audio \
  --prompt "metallic sword clash, short impact" -o assets/audio/sfx/sword_hit.ogg
```

`--duration` (default `2.0`): target duration in seconds

Output is always `.ogg` (OGG Vorbis) — the standard format for Godot audio. The Gemini backend produces raw audio which ffmpeg converts automatically.

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
| Video | --duration N | 5¢ × N seconds | Pose frame (2¢) as starting image |
| Audio | gemini | 3 cents | OGG output via ffmpeg conversion |

A full 3D asset (image + GLB) costs 32 cents at medium quality. A texture is 2 cents. A pro background is 7 cents. A 3-second animation costs 19 cents (2¢ ref + 2¢ pose + 15¢ video); additional animations from the same ref cost 2¢ pose + video.

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

**Variant from reference** (uses `--image`; see Tips for prompting guidance):
```
{what to change: different angle, pose, color, etc.}
```
`image --prompt "..." --image path_ref.png -o path_variant.png`

### Item kit (2c for 4 items)

Generate multiple objects in one image, then slice. Cheaper than generating individually (2¢ total vs 2¢ each).

```
{item1}, {item2}, {item3}, {item4}. 2x2 grid layout, each item centered in its cell, solid {bg_color} background. {art style}.
```
`image --prompt "..." -o path_grid.png`

To match an existing style, pass a reference — the model sees it, so just describe the items:
`image --prompt "..." --image path_style_ref.png -o path_grid.png`

Slice into individual PNGs:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/grid_slice.py path_grid.png \
  -o assets/img/items/ --grid 2x2 --names "sword,shield,potion,helm"
```

Then rembg each item if transparency is needed. Supports any grid: `2x2`, `3x3`, `2x4`, etc.

### 3D model reference (2c) + GLB (30-60c)

```
3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

### Animated sprite

Full workflow (ref → pose → video → frames → loop trim → rembg) is in CLI Reference above. Prompt templates:

**Reference:** `{name}, {description}. Neutral standing pose, facing right, centered on a solid {bg_color} background. Clean silhouette.`

**Pose (per action):** `{action pose description}, side view, solid {bg_color} background.`

**Video (per action):** `{action}, smooth animation. Solid {bg_color} background.`

## Tips

- **Image-to-image prompting**: when `--image` is provided, the model sees the reference. Don't re-describe the character/object — focus the prompt on what's different (the action, angle, or change). Re-describing appearance competes with the visual reference and dilutes consistency.
- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
