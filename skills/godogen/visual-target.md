# Visual Target

Generate a reference image of what the finished game looks like. Anchors art direction for scaffold, asset planner, and task agents.

## CLI

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "{prompt}" \
  --size 1K --aspect-ratio 16:9 -o reference.png
```

## Prompt

Must look like an in-game screenshot, not concept art. The purpose of this image is to demonstrate **composition, camera position, object placement, visual effects, and spatial relationships** — everything downstream agents must replicate. A beautiful photo of the game's theme is worthless; a screenshot showing the actual game layout is invaluable.

### Prompt rules

- **Describe what's on screen**, not the genre. Name the specific objects, their positions, sizes relative to screen, the camera angle and distance.
- **Reflect real technical constraints.** If you plan tiling backgrounds, prompt a tiling-friendly composition. If sprites are separate layers, show them as distinct objects against the background, not composited photorealism.
- **Don't prompt downgraded quality** ("lowpoly", "pixel art", "retro"). It doesn't help — the generator produces worse output without making it more game-like. Prompt clean, sharp rendering with the actual composition you need.
- **Focus on the most important gameplay moment** — the frame that best shows spatial layout, core mechanic, and camera perspective the player will see most.

```
Screenshot of a {2D/3D} video game. {Camera: angle, distance, perspective}. {Specific objects visible and their placement — foreground, midground, background}. {Environment structure — what tiles, what scrolls, what's static}. {Art style}. {Visual effects — lighting, particles, weather}. Clean digital rendering, game engine output, HUD visible.
```

This image becomes the visual QA target — every spatial and stylistic choice you bake in here becomes a requirement downstream.

## Output

`reference.png` — 1K 16:9 image.

Write the art direction into `ASSETS.md` — the asset planner uses it as context when crafting individual asset prompts (not as a literal prefix):

```markdown
# Assets

**Art direction:** <the art style description>
```
