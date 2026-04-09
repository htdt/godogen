# Asset Generator

Generate PNG images (Gemini, xAI Grok, or OpenRouter) and GLB 3D models (Tripo3D) from text prompts.

## Models

| Model | Flag | Cost | Best for |
|-------|------|------|----------|
| `gemini-3.1-flash-image-preview` | `--model gemini` | 5-15¢ (by size) | Precise prompt following — references, characters, backgrounds, 3D refs |
| `grok-imagine-image` | `--model grok` | 2¢ | High-quality but imprecise — textures, simple objects, item kits |
| OpenRouter (configurable) | `--model openrouter` | ~5¢ (varies by model, auto-detected) | Flexible — any OpenRouter image model. Default: openai/gpt-5-image-mini |

**When to use which:**
- **Gemini** — reference images, character design, 3D model references, animated sprite refs/poses, backgrounds with precise layout. Gemini costs more but reliably produces what you described.
- **Grok** — textures, simple objects, item kits, props, simple scenic backgrounds (sky, clouds, abstract). Produces high-quality (even photographic) output but often defaults to common interpretations instead of following specific instructions. Great when exact prompt adherence doesn't matter.
- **OpenRouter** — flexible alternative when you have an OpenRouter API key. Supports many image models via `--openrouter-model`. Good option when you don't have Gemini or xAI API keys, or want to try different models.

Default is `grok`. Switch to `gemini` when precision matters.

### Gemini sizes and costs

| Size | Cost |
|------|------|
| `512` | 5¢ |
| `1K` | 7¢ |
| `2K` | 10¢ |
| `4K` | 15¢ |

## CLI Reference

Tools live at `${CLAUDE_SKILL_DIR}/tools/`. Run from the project root.

### Generate image (2-15 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

`--model` (default `grok`): `grok` (2¢), `gemini` (5-15¢ by size), `openrouter` (~5¢, configurable model)
`--openrouter-model` (default `openai/gpt-5-image-mini`): OpenRouter model ID. Only used with `--model openrouter`.
`--size` (default `1K`): Grok: `1K`, `2K`. Gemini/OpenRouter: `512`, `1K`, `2K`, `4K`.
`--aspect-ratio` (default `1:1`): varies by backend — both support `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`

Typical combos:
- `--model gemini --size 1K` — reference images, character sprites, 3D refs (7¢)
- `--model gemini --size 2K --aspect-ratio 16:9` — backgrounds, title screens (10¢)
- `--model grok` — textures, simple objects, item kits (2¢)
- `--model openrouter` — flexible alternative with default model (~5¢)
- `--model openrouter --openrouter-model google/gemini-2.5-flash-image` — use a specific OpenRouter model

### Remove background

Read `${CLAUDE_SKILL_DIR}/rembg.md` for full guide: CLI, prompting strategy, troubleshooting, batch mode.

### Generate animated sprite (7¢ ref + 7¢/pose + 5¢/sec video)

Workflow: reference → pose frame → video → slice → loop trim → rembg.

**Step 1: Reference image (7¢ — Gemini)**

Gemini 1K, 1:1, neutral pose, solid BG — same color strategy as for rembg. Review carefully: this image anchors all subsequent poses and videos.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --model gemini --size 1K \
  --prompt "knight in armor, neutral standing pose, facing right, solid dark-green background" \
  --aspect-ratio 1:1 -o assets/img/knight_ref.png
```

**Step 2: Pose frame (7¢ — Gemini)**

Image-to-image edit: feed the reference, prompt only for the action/pose. Gemini is preferred here — the pose must match the prompt precisely since it anchors the video.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --model gemini \
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

For walk/run/idle cycles, find the best loop point. Picks top similarity candidates, deduplicates nearby frames, then chooses the latest (longest clip). Uses 7-frame window to avoid half-cycle cuts, falls back to 1-frame, then whole clip. Skip for one-shot animations (attack, death, jump).

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/find_loop_frame.py assets/video/knight_walk_frames/
```

Output: `{"loop_frame": 54, "similarity": 0.9983, "window": 7, "total_frames": 73}`

`window: 0` means no good loop point — use the whole clip. Then delete frames after the loop point, or note the range for the next step.

**Step 6: Batch background removal** (see `rembg.md` for full guide)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/rembg_matting.py \
  --batch assets/video/knight_walk_frames/ \
  -o assets/img/knight_walk/
```

**Step 7: Additional animations**

Repeat from step 2 using the same reference image. Each new animation costs 7¢ (Gemini pose) + video duration × 5¢.

### Convert image to GLB (40-50 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py glb \
  --image assets/img/car.png -o assets/glb/car.glb
```

`--quality`: `default` (P1, 50¢) or `high` (v3.1 + HD textures, 40¢)

### Set budget

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py set_budget 500
```

Sets the generation budget to 500 cents. All subsequent generations check remaining budget and reject if insufficient. CRITICAL: only call once at the start, and only when the user explicitly provides a budget.

### Output format

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 7}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress and API client output goes to stderr. **Redirect stderr to a temp file** to keep context clean — read it only on failure:
```bash
_log=$(mktemp)
result=$(python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image --prompt "..." -o path.png 2>"$_log") || tail -20 "$_log"
```

## Cost Table

| Operation | Options | Cost | Notes |
|-----------|---------|------|-------|
| Image | --model grok | 2 cents | Fast, simple images |
| Image | --model gemini --size 512 | 5 cents | Small refs, quick tests |
| Image | --model gemini --size 1K | 7 cents | References, characters, 3D refs |
| Image | --model gemini --size 2K | 10 cents | Backgrounds, title screens |
| Image | --model gemini --size 4K | 15 cents | Large maps, panoramas |
| Image | --model openrouter | ~5 cents (auto-detected from model pricing) | Flexible model, configurable via --openrouter-model |
| GLB | default | 50 cents | P1 model, fast, game-optimized topology |
| GLB | high | 40 cents | v3.1, HD textures |
| Video | --duration N | 5¢ × N seconds | Pose frame as starting image |

A full 3D asset (Gemini 1K image + GLB) costs 47 cents at high quality. A texture (Grok) is 2 cents. A background is 2¢ (Grok, simple) or 10¢ (Gemini 2K, precise layout). A 3-second animation costs 24 cents (7¢ Gemini ref + 7¢ Gemini pose + 10¢ video); additional animations from the same ref cost 7¢ pose + video.

## Image Resolution

Use the full generation resolution — don't downscale for aesthetic reasons.
- Default (`1K`): textures, sprites, 3D references, character refs
- `512` (Gemini only): quick tests
- `2K`: HQ objects/textures, backgrounds, title screens
- `4K` (Gemini only): large game maps, panoramic backgrounds

### Small sprites problem

Minimum generation resolution is 1K. A 1024px image downscaled to 64px or even 128px loses all fine detail and looks muddy. Mitigations:

1. **Avoid tiny display sizes.** Design game elements at 128px+ where possible. If a sprite must be small in-game, question whether it needs to be a generated image at all (a colored rectangle or simple shape drawn in code may read better at that size).
2. **Generate a kit image** — put multiple objects on one 1K image (e.g. 4 items in a 2x2 layout, each occupying ~512px) and crop the regions you need. More pixels per object = cleaner downscale.
3. **Prompt for bold, simple forms.** When the target display size is small, explicitly ask for: thick outlines, flat colors, minimal fine detail, exaggerated proportions. These survive downscaling; intricate textures don't.

## What to Generate — Cheatsheet

For any asset needing transparency, read `${CLAUDE_SKILL_DIR}/rembg.md` first — covers BG color strategy, CLI, and troubleshooting.

### Background / large scenic image (2c Grok or 10c Gemini)

Title screens, sky panoramas, parallax layers, environmental art. Best place for art direction language.

Grok works well for simple scenic backgrounds (sky, clouds, abstract environments) — 2¢. Use Gemini when layout and composition must match the prompt precisely (specific object placement, layered parallax with exact structure) — 10¢.

```
{description in the art style}. {composition instructions}.
```
`image --prompt "..." --size 2K --aspect-ratio 16:9 -o path.png` (Grok default, add `--model gemini` for precise layout)

No post-processing — use as-is.

### Texture (2c Grok)

Tileable surfaces: ground, walls, floors, UI panels. Grok handles these well — exact prompt adherence isn't critical for textures.

```
{name}, {description}. Top-down view, uniform lighting, no shadows, seamless tileable texture, suitable for game engine tiling, clean edges.
```
`image --prompt "..." -o path.png`

No background removal — the entire image IS the texture.

### Single object / sprite

**Simple objects** (2c Grok) — props, items, icons where exact appearance isn't critical:
```
{name}, {description}. Centered on a solid {bg_color} background.
```
`image --prompt "..." -o path.png`

**Character design** (7c Gemini 1K) — player characters, enemies, NPCs where the design must match the prompt:
```
{name}, {description}. Centered on a solid {bg_color} background.
```
`image --model gemini --prompt "..." -o path.png`

**Variant from reference** (uses `--image`; see Tips for prompting guidance):
```
{what to change: different angle, pose, color, etc.}
```
`image --prompt "..." --image path_ref.png -o path_variant.png`

### Item kit (2c Grok for 4 items)

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

### 3D model reference (7c Gemini 1K) + GLB (40-50c)

Use Gemini — clean composition and precise prompt following are critical for 3D conversion.

```
3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
`image --model gemini --prompt "..." -o path.png`

Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

### Animated sprite

Full workflow (ref → pose → video → frames → loop trim → rembg) is in CLI Reference above. Prompt templates:

**Reference (Gemini 1K):** `{name}, {description}. Neutral standing pose, facing right, centered on a solid {bg_color} background. Clean silhouette.`

**Pose (per action):** `{action pose description}, side view, solid {bg_color} background.`

**Video (per action):** `{action}, smooth animation. Solid {bg_color} background.`

## Visual Pitfalls

Image generators and vision validators have poor spatial understanding. These issues are invisible to the agent but degrade quality significantly. Verify carefully.

### Direction and orientation

Generators cannot reliably distinguish left vs right facing, or produce correct rotations. Prompting for "NE facing" vs "NW facing" often produces identical output.

**Solution:** Generate one direction only (sprites are typically left-facing), flip horizontally for the opposite direction (`sprite.flip_h = true`). Use visual-qa question mode to verify orientation when it matters — don't trust the generator got it right.

### Video size consistency

When mixing image-generated assets (1024px) with video-extracted frames (~720px), resize everything to the smallest source size. Downscale the 1024px images to match video frame resolution — upscaling is rarely needed. Do this before background removal.

Use ImageMagick:
```bash
magick identify input.png                                      # check size
magick input.png -resize 720x720 -filter Lanczos output.png   # resize
magick input.png -flop output.png                              # horizontal flip
```

### Animation playback

Video-extracted animations look choppy when played back at the wrong frame rate. Source videos are typically 24fps — set frame duration to `1.0/24 = 0.042s`. Don't reset the animation frame counter between movement tiles; let it run continuously across boundaries.

## Tips

- **Image-to-image prompting**: when `--image` is provided, the model sees the reference. Don't re-describe the character/object — focus the prompt on what's different (the action, angle, or change). Re-describing appearance competes with the visual reference and dilutes consistency.
- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
