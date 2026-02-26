---
name: visual-target
description: |
  This skill should be used when starting a new game to generate a visual reference image before scaffold and asset planning. Produces a "target screenshot" that anchors art direction, camera angle, and composition for all downstream agents.
---

# Visual Target

Generate a reference image of what the finished game looks like. Anchors art direction for scaffold, asset planner, and task agents.

## CLI

```bash
python3 .claude/skills/asset-gen/tools/asset_gen.py image \
  --prompt "{prompt}" \
  --size 2K --aspect-ratio 16:9 -o reference.png
```

## Prompt

Must look like an in-game screenshot, not concept art:

```
Screenshot of a {genre} {2D/3D} video game. {Key gameplay moment — peak action, not a menu}. {Environment details}. {Art style — be specific and bold}. In-game camera perspective, HUD visible. Clean digital rendering, game engine output.
```

Camera perspective should match the genre. This image becomes the visual QA target — every stylistic choice you bake in here becomes a requirement downstream agents must deliver. Don't invent complexity the user didn't ask for; pick a style that serves the game, not one that looks impressive as concept art.

## Output

`reference.png` — 2K 16:9 image.

Write the style string (art style portion of the prompt) into `ASSETS.md` — the asset planner will prepend it to every asset prompt, so this single string defines the visual identity of the entire game:

```markdown
# Assets

**Style:** <the style string>
```
