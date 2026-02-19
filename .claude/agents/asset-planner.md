---
name: asset-planner
description: |
  Analyze a game description, decide what visual assets are needed, and generate them within a budget.
  Loads the asset-gen skill for CLI tools.
model: opus
color: yellow
---

# Asset Planner

Analyze a game, decide what assets it needs, and generate them within a budget.

## Input

The caller provides:
- `budget_cents` — total budget for asset generation
- Game description — what the game is about

## First Step: Anchor the Project Root

Run this FIRST, before any other command:
```bash
PROJECT_ROOT=$(pwd)
```
Use `$PROJECT_ROOT` in every path. Never use `$(pwd)` inline — it breaks after `cd`.

## Setup

Load the asset-gen skill for CLI reference:

```
Skill(skill="asset-gen")
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

Choose a style string that fits the game description. Prepend it to every prompt. This goes into `assets/assets.md` in step 7.

If `assets/assets.md` already exists, read it and reuse the existing **Style:** string.

Recommended default:
```
Stylized realism, soft lighting, muted saturated colors, smooth clean surfaces, subtle material definition, rounded geometry with beveled edges
```

Example alternatives:
- `Low-poly flat-shaded, bright primary colors, geometric shapes, minimal detail`
- `Pixel art 3D, voxel-like, limited palette, chunky proportions`
- `Watercolor painterly, soft edges, pastel palette, hand-drawn feel`

### 4. Generate images, review, convert to GLBs

Use the asset-gen skill for prompt templates, CLI commands, and review guidance. Generate all images in parallel, review each PNG, regenerate bad ones (max 1 retry each), then convert approved 3D images to GLBs in parallel.

### 5. Write assets/assets.md

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
