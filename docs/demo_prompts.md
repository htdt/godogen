# Demo Prompts

## CartoRally

```text
Top-down racing game with a stylized topographic map aesthetic. Terrain rendered with visible contour lines following elevation changes, spaced tighter on steep slopes and wider on flat areas. Muted earthy color palette: cream/parchment base, sage green for lowlands, tan/brown for mid-elevation, grey-white for peaks. The racing track is a bold saturated line (burnt orange or red) cutting through the terrain, with subtle road markings. Trees represented as simplified symbolic markers — small clustered circles in dark green, like map legend symbols. Mountain border walls rendered as dense contour bundles with hatch shading. Subtle paper texture overlay across the entire scene. Elevation communicated through both 3D geometry and contour line density. Clean, minimal, highly readable. Visual references: topographic hiking maps, ordnance survey maps, vintage cartography with a modern minimal twist.
Terrain is a heightmap with distinct elevation changes — rolling hills create natural ramps where the car launches into the air and lands with impact. Track conforms to the terrain surface, following contours over hills and through valleys. Car physics emphasize verticality: visible airtime on crests, shadow separation from ground during jumps, suspension compression on landing. High mountain walls enclose the scene as natural borders. Closed-loop circuit with a natural winding layout through varied elevation.
```

## Ultra Realistic Nature Scene

```text
Generate a serene riverbank nature scene combining HQ 3D models with procedural shaders.
Scene elements:
River with shader-based water (reflection, refraction, flow, edge foam)
Riverbank with shader-blended ground (grass/dirt/mud transition)
Procedural grass with wind-animated vertex shaders
One tree — modeled trunk/branches, shader-driven leaf cards with wind sway and translucency
Forest backdrop behind the river (simple tree silhouettes or billboard impostors)
Old small wooden boat (3D model, weathered look)
Fallen log on the bank (3D model)
Technical split:
Models: boat, log, tree trunk/branches, rocks
Shaders: water surface, grass, leaves, ground blending, wind animation
Visual targets: Natural lighting (directional sun + ambient), soft shadows, subtle fog/atmosphere for depth.
```

## Amsterdam Cyclist

```text
A 2D side-scrolling cyclist game, left to right, with lane switching, slow and relaxed in pace. You ride through Amsterdam on a red bike lane — 4 horizontal lanes stacked vertically: two bottom lanes for your direction, two top lanes with oncoming traffic. Tourists jump onto the bike lane from gray sidewalks (top and bottom edges) as obstacles; three caricature types: the Selfie Walker (phone up, completely oblivious), the Lost Map Reader (spinning confused, giant map unfolded), and the Tulip Hauler (struggling to see past a comically huge bouquet of tulips, drifting blindly). You dodge by switching lanes vertically; moving into oncoming lanes risks hitting approaching cyclists — the core risk/reward. Lane switching is discrete with smooth lerp, max speed caps at 25 km/h — the vibe is chill Amsterdam cruising that slowly gets chaotic.
Three-layer parallax: canal water at the bottom scrolls fastest, road/bike lanes at medium speed, townhouse facades along the top slowest. The canal is visually rich — animated dark water with ripple highlights, and varied boats drifting past: classic sloepen with passengers, houseboats with rooftop plants, tourist canal boats, an occasional rower. Boats vary in size and speed, some overlapping — pure eye candy, no interaction. Road markings (dashed center line, bike symbols, arrows) are baked into the road tile texture, not separate objects. Sidewalks have a subtle brick pattern. All sprites stay small (~250px) with bold simple shapes, thick outlines, flat filled colors — chunky and iconic, readable at a glance.
The cyclist has a pedaling animation loop. Each tourist type has a distinct animation: Selfie Walker shuffling with phone raised, Map Reader spinning in place, Tulip Hauler swaying with the bouquet bobbing. Art style: flat colored sprite illustrations, clean and cartoony. HUD shows distance and speed; game over screen with final score and restart. Controls: W/S or Up/Down to switch lanes. No coins or power-ups — just survival as tourist density gradually increases.
```

## 3D Alpine Snowboard Simulator

```text
A downhill snowboarding game set in an Alpine ski resort.
World: A long slope descending with gentle undulations. A curvy groomed track winds down the center, flanked by powder snow zones on both sides — visually distinct, and entering them heavily dampens speed. Scattered along the track are ramp-shaped kickers that launch the rider airborne when hit with speed.
Obstacles: Slow-moving skiers (simple figures) drift downhill on the track. Snowy pine trees with white snow caps line the edges and occasionally encroach onto the track. Collision with either means crash and game over with restart option.
Snowboard physics — the core feel: The rider stands sideways on a board. Left/Right input carves by tilting onto the heel edge or toe edge — lean the whole model into the turn and gradually arc the heading. Turns should feel carved with angular momentum, not instant snaps. Sharper carves scrub more speed. No input means neutral glide with gravity acceleration. Airborne means preserve momentum plus gravity.
Snow spray: Sharp carves spawn a burst of white particles fanning out from the board's outside edge, rising slightly and fading quickly. Harder carve means bigger spray. This should feel satisfying and punchy.
Camera: Third-person chase cam behind and above the rider, smooth-following with slight lag, gently swinging on turns.
Scenery: Panorama image. At the bottom of the slope, a charming Alpine village — clustered wooden chalets with snowy roofs, a small church steeple. Behind it, jagged snow-capped mountain peaks on the horizon. Clear winter blue sky with warm sun glow on one side. Directional sunlight with soft shadows.
HUD: Speed, run timer. Minimal, not intrusive.
```
