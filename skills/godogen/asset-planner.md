# Asset Planner

Analyze a game, decide what assets it needs, and generate them within a budget.

## Input

The caller provides:
- `budget_cents` — total budget (or remaining budget for iterations)
- For iterations: a specific task description (e.g. "regenerate car model" or "add missing explosion sprite")

The game description is in `PLAN.md` under **Game Description**.

## Setup

Read `${CLAUDE_SKILL_DIR}/asset-gen.md` for CLI reference and prompt templates.

## Workflow

### 1. Analyze inputs → identify visual elements

Read `reference.png` — understand the visual composition: what objects are visible, their proportions, the environment, foreground vs background layers. Use this to inform what assets to generate and at what scale.

Read `STRUCTURE.md` (especially **Asset Hints**) and `PLAN.md` (especially **Assets needed** per task). Cross-reference both with the reference image to build the complete asset list:
- **3D models**: characters, vehicles, key props, buildings — anything that needs geometry
- **Textures**: ground surfaces, walls, UI backgrounds — flat materials that tile
- **Backgrounds**: sky panoramas, parallax layers, title screens, large scenic images — use `--model pro --size 2K` and an appropriate `--aspect-ratio`
- **Animated sprites**: characters or objects with multiple actions (walk, attack, idle) — plan the motion graph before generating
- **Audio**: sound effects for gameplay events, background music loops, ambient sounds — determine what sounds are needed for game feel

The scaffold's Asset Hints describe what the architecture needs. The decomposer's Assets needed fields describe what each task needs. Reconcile both — they may overlap or one may mention assets the other missed.

### 2. Prioritize and budget

Each asset costs:
- Texture / sprite / 3D ref: 2 cents (standard model)
- HQ background / title screen: 7 cents (pro model with `--size 2K`)
- 3D model: 32 cents (2 cent image + 30 cent GLB at medium quality)
- Audio SFX: 3 cents (Gemini)

Animated sprites cost more — budget carefully:
- Reference image: 2 cents (once per character — all animations share it)
- Root action (from ref): 2 cent pose + 5 cents × duration
- Chained action (from predecessor's last frame): 5 cents × duration only
- Example: knight with walk 3s, idle 2s (roots) + attack 2s (chained from walk)
  = 2 (ref) + 17 (walk) + 12 (idle) + 10 (attack) = 41 cents

Prioritize by visual impact — what makes the game recognizable. Cut low-impact assets first if budget is tight. Reserve ~10% of budget for retries.

### 3. Understand art direction

Read the **Art direction** from `ASSETS.md` (written by visual-target). Use it as context when crafting each asset prompt — but do NOT mechanically prepend it. Different asset types need different prompting:
- **Textures** often need no style language at all — describe the material and tiling properties
- **3D model references** need clean studio lighting and neutral presentation; style cues can hurt mesh quality
- **Backgrounds/panoramas** benefit most from art direction language
- **Sprites** may need some style cues but adapted to the subject

Craft each prompt for its specific goal. The art direction tells you the visual identity; translate it appropriately per asset type.

#### Using image references for consistency

Feed a generated image as `--image` input when subsequent assets need to match it. Identify which assets are **anchors** (generated first, reviewed) and which are **derivatives** (use the anchor as input). Common patterns:

- **Style family** — generate one hero asset, use it as input for the rest of the set (one enemy → all enemies, one tree → all vegetation, one weapon → full arsenal)
- **Multiple views** — front view as input → side, back, 3/4 angle for 3D references or sprite variants
- **Variants** — base object as input → recolors, damaged versions, size variants (red potion → blue, green)
- **Scene coherence** — use the background as input when generating foreground props that should feel part of the same world

Generate anchors first, review, then fan out derivatives in parallel. Budget 1 retry per anchor since derivatives amplify any problems in it.

### 4. Generate images, review, convert to GLBs

Use the asset-gen instructions for prompt templates, CLI commands, and review guidance. Generate all images in parallel, review each PNG, regenerate bad ones (max 1 retry each), then convert approved 3D images to GLBs in parallel.

For animated sprites, generate in dependency order per the Start From column in ASSETS.md — root actions first (parallel), extract frames and trim loops, then chained actions from their predecessors' last frames (parallel).

To prevent cost overruns, a JSON log is automatically maintained that tracks the cost of each request.

#### Common Mistakes

- **Detailed image shrunk to a tile** — minimum generation resolution is 1K. A 1024px image downscaled to 64px looks muddy. For small sprites: avoid tiny display sizes (128px+ preferred), generate a kit image with multiple objects sharing one 1K image and crop, or prompt for bold simple forms (thick outlines, flat colors, exaggerated proportions).
- **Tiling texture for a unique background** — don't tile a small repeating texture where the game needs a single scenic background. Use `--model pro` instead.
- **Image where procedural drawing works** — pure geometric primitives (solid-color rectangles for health bars, single-color circle for a ball, straight divider lines) should be drawn in code. But anything with texture, detail, or artistic style — characters, backgrounds, terrain, objects, icons — should use generated assets even if you *could* approximate it with code. Procedural vector art almost always looks worse than a generated image.
- **Stretching one texture over a large area** — a small texture stretched across a big surface looks blurry. Use a tileable texture or generate at higher resolution.

### 5. Write ASSETS.md

Every asset row **must** include a **Size** column — the intended in-game dimensions the coding agent should use when placing this asset. Without this, coders consistently scale backgrounds too small or sprites too tiny.

- **3D models:** target size in meters, e.g. `4m long` (car), `1.8m tall` (character), `0.3m` (coin)
- **Textures:** tile size in meters, e.g. `2m tile` (floor repeats every 2m via UV scale)
- **Backgrounds (pro model):** pixel dimensions to display at, e.g. `1920x1080` (fullscreen), `2560x720` (parallax layer). Mention if it should fill the viewport or scroll.
- **Sprites:** display size in pixels, e.g. `128x128 px` (player), `64x64 px` (item). This is the size in the game viewport, not the source resolution.

```markdown
# Assets

**Art direction:** <the art direction string>

## 3D Models

| Name | Description | Size | Image | GLB |
|------|-------------|------|-------|-----|
| car | sedan with spoiler | 4m long | assets/img/car.png | assets/glb/car.glb |

## Textures

| Name | Description | Size | Image |
|------|-------------|------|-------|
| grass | green meadow | 2m tile | assets/img/grass.png |

## Backgrounds

| Name | Description | Size | Image |
|------|-------------|------|-------|
| forest_bg | dense forest panorama | 1920x1080, fullscreen | assets/img/forest_bg.png |

## Sprites

| Name | Description | Size | Image |
|------|-------------|------|-------|
| coin | spinning gold coin | 64x64 px | assets/img/coin.png |

## Animated Sprites

### knight

**Reference:** `assets/img/knight_ref.png`
**Transitions:** idle ↔ walk, walk → attack → idle, walk → jump → land → idle

| Action | Type | Size | Duration | Start From | Frames Dir |
|--------|------|------|----------|------------|------------|
| idle | loop | 128x128 px | 2s | ref | assets/img/knight_idle/ |
| walk | loop | 128x128 px | 3s | ref | assets/img/knight_walk/ |
| attack | one-shot | 128x128 px | 2s | walk | assets/img/knight_attack/ |
| jump | one-shot | 128x128 px | 1s | ref | assets/img/knight_jump/ |
| land | one-shot | 128x128 px | 1s | jump | assets/img/knight_land/ |

## Sound Effects

| Name | Description | Duration | File |
|------|-------------|----------|------|
| jump | springy jump launch | 0.3s | assets/audio/sfx/jump.ogg |
| hit | blunt impact | 0.2s | assets/audio/sfx/hit.ogg |

## Music

| Name | Description | Duration | Loop | File |
|------|-------------|----------|------|------|
| gameplay_loop | upbeat chiptune loop | 30s | yes | assets/audio/music/gameplay.ogg |
```

One reference per character anchors all animations. **Loops** (idle, walk) repeat seamlessly — trimmed to loop point. **One-shots** (attack, death) play once.

**Chaining:** last extracted frame of action A → starting image for action B's video. Maintains visual continuity across transitions and skips the pose step for chained actions. Keep chains short (max 1-2 deep) — each link drifts further from the reference. Prefer ref → pose → video for most actions; only chain when the transition genuinely needs positional continuity (e.g., walk → attack where the stride pose matters).

**Start From column:** `ref` = generate pose from reference, then video from pose. Action name = use that action's last extracted frame as video input directly.

**Background removal:** almost always needed for sprites. Same rules as static sprites — prompt for solid background color, no cast shadows, no ground shadows, clean silhouette. This applies to the reference, every pose frame, and video prompts (the solid BG must persist through the whole animation).

**Small display size:** same as static sprites — if the character renders small in-game, prompt for bold simple forms, thick outlines, flat colors, exaggerated proportions. Fine detail disappears when 1K frames are downscaled to 64-128px.

**Generation order:** roots first (parallel) → extract frames + loop trim → chains (parallel) → extract → batch rembg all.

### 6. Update PLAN.md with asset assignments

After generating assets, read PLAN.md and add concrete asset assignments to each task that needs them. For tasks with an **Assets needed** field, replace or augment it with an **Assets:** field listing the actual generated files:

```markdown
- **Assets:**
  - `car` GLB model (`assets/glb/car.glb`) — scale to 4m long
  - `grass` texture (`assets/img/grass.png`) — tile every 2m via UV scale
```

This ensures no asset is lost in the process — every generated file is assigned to the task that uses it. An asset may appear in multiple tasks.
