# Visual Target

Generate a reference image of what the finished game looks like. Anchors art direction for scaffold, asset planner, and task agents.

## CLI

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "{prompt}" \
  --size 1K --aspect-ratio 16:9 -o reference.png
```

## Prompt

Must look like an in-game screenshot, not concept art:

```
Screenshot of a {genre} {2D/3D} video game. {Key gameplay moment — peak action, not a menu}. {Environment details}. {Art style — be specific and bold}. In-game camera perspective, HUD visible. Clean digital rendering, game engine output.
```

Camera perspective should match the genre. This image becomes the visual QA target — every stylistic choice you bake in here becomes a requirement downstream agents must deliver. Don't invent complexity the user didn't ask for; pick a style that serves the game, not one that looks impressive as concept art.

## Output

`reference.png` — 1K 16:9 image.

Write the art direction into `ASSETS.md` — the asset planner uses it as context when crafting individual asset prompts (not as a literal prefix):

```markdown
# Assets

**Art direction:** <the art style description>
```
