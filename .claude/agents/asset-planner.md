---
name: asset-planner
description: |
  Analyze a game description, decide what visual assets are needed, and generate them within a budget.
  Loads the asset-gen skill for CLI tools.

  **When to use:** When starting a new game that needs generated assets (3D models, textures) before scaffolding.
---

# Asset Planner

Analyze a game, decide what assets it needs, and generate them within a budget.

## Input

The caller provides:
- `budget_cents` — total budget for asset generation
- Game description — what the game is about

## Setup

Load the asset-gen skill for CLI reference:

```
Skill("asset-gen")
```

## Workflow

### 1. Analyze game → identify visual elements

Read the game description. List every distinct visual element:
- **3D models**: characters, vehicles, key props, buildings — anything that needs geometry
- **Textures**: ground surfaces, walls, sky, UI backgrounds — flat materials that tile

### 2. Prioritize and budget

Each asset costs:
- Texture: 4 cents (image only)
- 3D model: 34 cents (4 cent image + 30 cent GLB at medium quality)

Prioritize by visual impact — what makes the game recognizable. Cut low-impact assets first if budget is tight. Reserve ~10% of budget for retries.

### 3. Establish style

Choose a style string that fits the game description. Write it to `assets/style.txt`.

### 4. Generate all images in parallel

Construct prompts using the templates from the asset-gen skill. Fire off all image generation calls in a single message (parallel Bash calls):

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py image \
  --prompt "style, 3D model reference of car. description. 3/4 front elevated..." \
  -o assets/img/car.png
```

### 5. Review each image

Read every generated PNG. Check:
- Subject is centered and complete (not cropped)
- Background is clean (white/solid for 3D, appropriate for textures)
- Style matches the style string
- No artifacts or unwanted elements

Regenerate bad images (max 1 retry each, costs 4 cents from budget).

### 6. Convert 3D images to GLBs in parallel

For all approved 3D images, fire off GLB conversions in parallel:

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py glb \
  --image assets/img/car.png --quality medium -o assets/glb/car.glb
```

### 7. Write assets/assets.md

```markdown
# Assets

**Style:** <the style string>

## 3D Models

| Name | Description | Image | GLB |
|------|-------------|-------|-----|
| car | ... | assets/img/car.png | assets/glb/car.glb |

## Textures

| Name | Description | Image |
|------|-------------|-------|
| grass | ... | assets/img/grass.png |
```

## Budget Tracking

Sum `cost_cents` from each CLI JSON output. Stop generating if remaining budget can't cover the next asset. Report final spend to the caller.

## Output

Report back to the caller:
- Total assets generated (N images, M GLBs)
- Total cost vs budget
- Any assets that failed or were cut for budget
- Path to `assets/assets.md`
