# Visual Target

Generate a reference image of what the finished game looks like. Anchors art direction for scaffold, asset planner, and task agents.

## CLI

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --model gemini --prompt "{prompt}" \
  --size 1K --aspect-ratio 16:9 -o reference.png
```

## Prompt

Must look like an in-game screenshot, not concept art. Every distinct object visible here becomes an asset requirement — downstream agents must generate and place it. Prompt only elements you will actually build. A beautiful atmospheric scene wastes budget when the asset planner tries to reproduce effects the game won't have; a clean screenshot showing every game object at correct scale and position is what drives the pipeline.

### Prompt rules

- **Enumerate every game object** — player character, each enemy type, obstacles, collectibles, projectiles, platforms, props. Name each with position and approximate size relative to screen. Every object here becomes an asset to generate; objects absent from the reference get forgotten downstream.
- **Reflect real technical constraints.** If you plan tiling backgrounds, prompt a tiling-friendly composition. If sprites are separate layers, show them as distinct objects against the background, not composited photorealism.
- **Don't prompt downgraded quality** ("lowpoly", "pixel art", "retro"). It doesn't help — the generator produces worse output without making it more game-like. Prompt clean, sharp rendering with the actual composition you need.
- **Focus on the most important gameplay moment** — the frame that best shows spatial layout, core mechanic, and camera perspective the player will see most.
- **Exclude what you won't build.** Volumetric lighting, motion blur, depth of field, atmospheric fog, complex reflections, lens flares, detailed cast shadows — skip unless the game actually implements them. They create asset requirements nobody can fulfill.
- **Show HUD/UI elements.** Health bar, score counter, minimap, inventory slots — include every UI element with its screen position. These are implementation requirements too.

```
Screenshot of a {2D/3D} video game. {Camera: angle, distance, perspective}.
Game objects: {player — appearance, position, size vs screen}. {enemies/NPCs — each type, position}. {obstacles}. {collectibles/pickups}. {projectiles if any}.
Environment: {background layers — sky, distant, mid}. {playfield surface — material, tiling}. {foreground elements}. {boundaries/edges}.
HUD: {each UI element — type and screen position}.
{Art style, color palette}. Clean sharp digital rendering, game engine output.
```

This image becomes the visual QA target — every spatial and stylistic choice you bake in here becomes a requirement downstream.

## Output

`reference.png` — 1K 16:9 image.

Write the art direction into `ASSETS.md` — the asset planner uses it as context when crafting individual asset prompts (not as a literal prefix):

```markdown
# Assets

**Art direction:** <the art style description>
```
