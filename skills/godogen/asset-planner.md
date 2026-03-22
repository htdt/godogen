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

The scaffold's Asset Hints describe what the architecture needs. The decomposer's Assets needed fields describe what each task needs. Reconcile both — they may overlap or one may mention assets the other missed.

### 2. Prioritize and budget

Each asset costs:
- Texture / sprite / 3D ref: 2 cents (standard model)
- HQ background / title screen: 7 cents (pro model with `--size 2K`)
- 3D model: 32 cents (2 cent image + 30 cent GLB at medium quality)

Prioritize by visual impact — what makes the game recognizable. Cut low-impact assets first if budget is tight. Reserve ~10% of budget for retries.

### 3. Understand art direction

Read the **Art direction** from `ASSETS.md` (written by visual-target). Use it as context when crafting each asset prompt — but do NOT mechanically prepend it. Different asset types need different prompting:
- **Textures** often need no style language at all — describe the material and tiling properties
- **3D model references** need clean studio lighting and neutral presentation; style cues can hurt mesh quality
- **Backgrounds/panoramas** benefit most from art direction language
- **Sprites** may need some style cues but adapted to the subject

Craft each prompt for its specific goal. The art direction tells you the visual identity; translate it appropriately per asset type.

### 4. Generate images, review, convert to GLBs

Use the asset-gen instructions for prompt templates, CLI commands, and review guidance. Generate all images in parallel, review each PNG, regenerate bad ones (max 1 retry each), then convert approved 3D images to GLBs in parallel.

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
| knight | armored knight walk cycle | 128x128 px per frame | assets/img/knight.png |
```

### 6. Update PLAN.md with asset assignments

After generating assets, read PLAN.md and add concrete asset assignments to each task that needs them. For tasks with an **Assets needed** field, replace or augment it with an **Assets:** field listing the actual generated files:

```markdown
- **Assets:**
  - `car` GLB model (`assets/glb/car.glb`) — scale to 4m long
  - `grass` texture (`assets/img/grass.png`) — tile every 2m via UV scale
```

This ensures no asset is lost in the process — every generated file is assigned to the task that uses it. An asset may appear in multiple tasks.
