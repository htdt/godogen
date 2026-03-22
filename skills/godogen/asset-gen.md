# Asset Generator

Generate PNG images (Gemini) and GLB 3D models (Tripo3D) from text prompts.

## CLI Reference

Tools live at `${CLAUDE_SKILL_DIR}/tools/`. Run from the project root.

### Generate image (5-10 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

`--size` (default `1K`): `512` (5c), `1K` (7c), `2K` (10c)
`--aspect-ratio` (default `1:1`): `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`

Typical combos: `--size 2K --aspect-ratio 16:9` (landscape bg), `--size 2K --aspect-ratio 9:16` (portrait), `--size 1K` (textures, sprites, 3D refs).

### Remove background

Read `${CLAUDE_SKILL_DIR}/rembg.md` for full guide: CLI, prompting strategy, troubleshooting, batch mode.

### Generate sprite sheet (10 cents)

4x4 grid = 16 cells, always 2K (512px/cell). Two modes:

**With reference** (recommended for characters/animations): generate a 512px reference image first, then pass it with `--reference`. Cell 1 gets the reference, cells 2-16 get per-frame content. Gemini matches the character across all frames.

```bash
# 1. Reference image (5¢) — neutral pose, solid BG
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --size 512 --prompt "knight in armor, neutral standing pose, facing right, solid #4A6741 background" \
  -o assets/img/knight_ref.png

# 2. Sprite sheet (10¢ at 2K) — per-frame descriptions
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py spritesheet \
  --reference assets/img/knight_ref.png \
  --prompt "Walk cycle: 2: right foot stepping forward 3: mid-stride right leg ahead 4: right foot planted ... 16: returning to neutral" \
  --bg "#4A6741" -o assets/img/knight_walk_raw.png
```

**Without reference** (items, collections): all 16 cells described in the prompt.

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py spritesheet \
  --prompt "Items: 1: red apple 2: banana 3: orange ..." \
  --bg "#4A6741" -o assets/img/items_raw.png
```

`--reference`: reference image path — embedded in cell 1
`--bg`: background color hex (default: `#00FF00`). See BG color strategy in `${CLAUDE_SKILL_DIR}/rembg.md`.

**Multiple spritesheets per character**: same reference, different prompts. Reference paid once (5¢), each sheet 10¢.

```bash
# Attack sheet — same ref, different action
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py spritesheet \
  --reference assets/img/knight_ref.png \
  --prompt "Sword attack: 2: raising sword overhead 3: sword at peak ..." \
  --bg "#4A6741" -o assets/img/knight_attack_raw.png
```

### Process sprite sheet

Crops grid lines, auto-scales margin for 1K/2K sheets. Cell 1 (reference) is dropped by default — use `--keep-first` for item kits where all 16 cells are content.

**Animation keyframes** → split into individual PNGs (then RIFE interpolate):
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/spritesheet_slice.py split-bg \
  assets/img/knight_walk_raw.png -o assets/img/knight_walk_keyframes/
```

**Collection of distinct objects** (items, icons, props) → split into 16 individual PNGs:
```bash
# All 16 cells are content — keep cell 1
python3 ${CLAUDE_SKILL_DIR}/tools/spritesheet_slice.py split-bg --keep-first \
  assets/img/items_raw.png -o assets/img/items/

# With background removed — uses batch rembg
python3 ${CLAUDE_SKILL_DIR}/tools/spritesheet_slice.py split-clean --keep-first \
  assets/img/items_raw.png -o assets/img/items/ \
  --names "apple,banana,orange,grape,cherry,lemon,pear,plum,peach,melon,kiwi,mango,berry,fig,lime,coconut"
```

For split modes, `-o` is the output **directory**. `--names` provides filenames (without `.png`). Without `--names`, files are numbered `01.png`..`N.png`.

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

JSON to stdout: `{"ok": true, "path": "assets/img/car.png", "cost_cents": 7}`

On failure: `{"ok": false, "error": "...", "cost_cents": 0}`

Progress goes to stderr.

## Cost Table

| Operation | Preset | Cost | Notes |
|-----------|--------|------|-------|
| Image | --size 512 | 5 cents | References, quick tests |
| Image | --size 1K | 7 cents | Default. Textures, sprites, 3D refs |
| Image | --size 2K | 10 cents | HQ backgrounds, title screens |
| Image | --size 4K | 15 cents | Large game maps, panoramic backgrounds |
| Sprite sheet | — | 10 cents | 2K, 512px/cell |
| Sprite ref | --size 512 | 5 cents | Paid once per character |
| GLB | medium | 30 cents | 20k faces, good default |
| GLB | lowpoly | 40 cents | 5k faces, smart topology |
| GLB | high | 40 cents | Adaptive faces, detailed textures (+10c) |
| GLB | ultra | 60 cents | Detailed textures + geometry (+10c +20c) |

A full 3D asset (image + GLB) costs 37 cents at medium quality. A character with 3 animation sheets costs 35 cents (5¢ ref + 3×10¢ sheets) — each sheet produces 61+ smooth frames after RIFE interpolation. An item kit is 10 cents for 16 objects.

## Image Resolution

Use the full generation resolution — don't downscale for aesthetic reasons.
- `512`: reference images for spritesheets, quick tests
- Default (`1K`): textures, sprites, 3D references
- `2K`: HQ objects/textures, backgrounds, title screens
- `4K`: large game maps (zoom into regions instead of multiple smaller images), panoramic backgrounds
- Sprite sheets: 2048x2048 total → **512x512 per cell** (after grid crop ~496x496)

### Small sprites problem

Minimum generation resolution is 1K. A 1024px image downscaled to 64px or even 128px loses all fine detail and looks muddy. Mitigations:

1. **Avoid tiny display sizes.** Design game elements at 128px+ where possible. If a sprite must be small in-game, question whether it needs to be a generated image at all (a colored rectangle or simple shape drawn in code may read better at that size).
2. **Generate a kit image** — put multiple objects on one 1K image (e.g. 4 items in a 2x2 layout, each occupying ~512px) and crop the regions you need. More pixels per object = cleaner downscale.
3. **Prompt for bold, simple forms.** When the target display size is small, explicitly ask for: thick outlines, flat colors, minimal fine detail, exaggerated proportions. These survive downscaling; intricate textures don't.

## What to Generate — Cheatsheet

For any asset needing transparency, read `${CLAUDE_SKILL_DIR}/rembg.md` first — covers BG color strategy, CLI, and troubleshooting.

### Background / large scenic image (10c)

Title screens, sky panoramas, parallax layers, environmental art. Best place for art direction language.

```
{description in the art style}. {composition instructions}.
```
`image --prompt "..." --size 2K --aspect-ratio 16:9 -o path.png`

No post-processing — use as-is.

### Texture (7c)

Tileable surfaces: ground, walls, floors, UI panels.

```
{name}, {description}. Top-down view, uniform lighting, no shadows, seamless tileable texture, suitable for game engine tiling, clean edges.
```
`image --prompt "..." -o path.png`

No background removal — the entire image IS the texture.

### Single object / sprite (7c)

**With background** (object on a known scene background):
```
{name}, {description}.
```

**Transparent** (characters, props, icons, UI elements) — prompt with solid BG color, then rembg (see `rembg.md`):
```
{name}, {description}. Centered on a solid {bg_color} background.
```

### 3D model reference (7c) + GLB (30-60c)

```
3D model reference of {name}. {description}. 3/4 front elevated camera angle, solid white background, soft diffused studio lighting, matte material finish, single centered subject, no shadows on background. Any windows or glass should be solid tinted (opaque).
```
Then: `glb --image ... -o ...` — do NOT remove the background; Tripo3D needs the solid white bg for clean separation.

Key: 3/4 front elevated angle, solid white/gray bg, matte finish (no reflections), opaque glass, single centered subject.

### Animation → Reference + Spritesheet + Interpolation (5¢ + 10¢ per action)

Full pipeline: reference image → spritesheet (15 animation keyframes) → slice (drop reference cell) → RIFE interpolation → smooth animation.

Cell 1 = character reference for Gemini (visual identity only). Animation frames are cells 2-16. After slicing with `--drop-first`, you get 15 keyframes.

**Step 1: Reference image** (5¢, once per character):
```
{name}, {description}. Neutral standing pose, facing right, centered on a solid {bg_color} background. Clean silhouette.
```
`image --size 512 --prompt "..." -o ref.png`

Review the reference before proceeding. A bad reference wastes 10¢ per sheet.

**Step 2: Spritesheet per action** (10¢ each):
```
{action} animation, side view, full body visible in every frame: 2: {frame 2} 3: {frame 3} ... 16: {frame 16}
```
`spritesheet --reference ref.png --prompt "..." --bg "{bg_color}" -o action_raw.png`

Describe cells 2-16 (15 animation frames). Multiple animations per character share one reference — generate sheets in parallel.

**Step 3: Slice into keyframes** (cell 1 dropped by default):
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/spritesheet_slice.py split-bg \
  action_raw.png -o keyframes/
```

**Step 4: RIFE interpolation** — generates smooth in-between frames:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/interpolate.py \
  keyframes/ -o smooth_frames/ --mid 3
```

`--mid N`: interpolated frames between each keyframe pair (default 3). With 15 keyframes and `--mid 3`: 15 + 14×3 = 57 total frames.
`--gif path.gif --fps 18`: optional preview GIF.

#### Loop vs one-shot animations

**Looping** (walk, run, idle breathing): frame 2 and frame 16 must be the **same pose** — this is the loop point. Don't use the neutral/idle pose; use a pose natural to the action (e.g. mid-stride for walk). The game engine handles transitions between animation states.

**One-shot** (punch, jump, hurt, death): frame 2 = start pose, frame 16 = end pose. These don't need to match each other. They should be a resting pose compatible with whatever animation the engine blends into next (typically idle or combat-ready).

#### How to prompt frames for smooth interpolation

RIFE interpolates pixel motion between consecutive frames. It works when frames differ by small, continuous changes. It fails on large jumps, teleporting limbs, or drastically different poses.

**Rules:**
- **Small incremental changes** between consecutive frames. Each frame should be a slight progression from the previous one. If you can't imagine a smooth morph between two adjacent frames, add detail between them.
- **Describe body state, not action verbs.** "right arm at 45 degrees, fist at shoulder height" is interpolatable. "swinging sword" is not — RIFE doesn't know what that means between frames.
- **Keep the full body in every frame.** Don't let limbs exit the cell or get cropped. Consistent framing = consistent interpolation.
- **Avoid sudden appearance/disappearance.** Don't introduce effects in one frame and remove them the next. Fade over 2-3 frames.
- **Use all 15 frames.** Spread the motion evenly. Don't cluster action at the start and pad the end with idle.

**Good prompt** (one-shot punch — small steps, positional descriptions):
```
Punch, side view, full body: 2: weight shifting back, right arm drawing behind torso
3: right arm fully cocked, torso twisting away, knees bent 4: torso rotating forward,
right arm starting to extend 5: arm at half extension, weight moving forward
6: arm fully extended, fist at peak reach 7: slight overextension, energy at fist
8: arm still out, beginning to retract 9: arm halfway back, torso rotating to neutral
10: arm nearly retracted, weight recentering 11: settling into stance, knees absorbing
12: arms lowering 13: body straightening 14: upright, arms at sides
15: combat-ready stance 16: combat-ready stance, still
```

**Good prompt** (looping walk — frame 2 = frame 16):
```
Walk cycle, side view, full body: 2: left foot forward, right foot back, arms swinging
3: weight on left foot, right leg lifting 4: right knee rising, left arm forward
5: right leg swinging forward 6: right foot reaching forward, left pushing off
7: both feet on ground, weight centered 8: weight shifting to right foot, left leg lifting
9: left knee rising, right arm forward 10: left leg swinging forward
11: left foot reaching forward, right pushing off 12: both feet on ground, weight centered
13: weight on left, right beginning to lift 14: right leg swinging through
15: approaching left-foot-forward position 16: left foot forward, right foot back, matching frame 2
```

**Bad prompt** (vague, large jumps):
```
2: standing 3: punching 4: standing again
```

### Asset kit (16 objects, consistent style) → Spritesheet (10c)

Generate 16 small objects that share the same visual style (items, icons, props, tiles). Cheaper and more consistent than 16 individual calls (10c vs 112c).

```
Items: 1: red apple 2: banana 3: orange 4: grape 5: cherry ...
```

Number every item 1-16. Don't specify grid layout — system prompt handles it. No `--reference` needed.

Post-processing — split into individual images (use `--keep-first` since all 16 cells are content):
- **Transparent** (preferred): `split-clean --keep-first -o dir/ --names "apple,banana,..."`
- **With background:** `split-bg --keep-first -o dir/ --names "apple,banana,..."`

## Tips

- Generate multiple images in parallel via multiple Bash calls in one message.
- Always review generated PNGs before GLB conversion — read each image and check: centered? complete? clean background? Regenerate bad ones first; a bad image wastes 30+ cents on GLB.
- Convert approved images to GLBs in parallel.
