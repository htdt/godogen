# Task Execution

Implementation workflow for Babylon.js feature work after scaffold is in place.

## Planning Each Task

- Read `STRUCTURE.md`, `package.json`, `src/game/scenes/main.ts`, `architecture.md`, `scene-generation.md`, and `quirks.md` before touching code.
- Use `babylon-help` for Babylon APIs, loaders, exact import paths, Vite behavior, browser capture, and rendering setup.
- Decide the concrete scope: state owner, modules/files, runtime assets, verification commands, and browser evidence.
- Preserve dependency versions unless the task is an engine/tool migration.
- Keep `npm run dev` running at `http://127.0.0.1:5173` when possible.

## Default Loop

1. Start or reuse `npm run dev`.
2. Implement the next visible/playable slice.
3. Refresh the browser to see the edit; tell the user to refresh when you want them to see it.
4. Capture an ad hoc screenshot when the change is visual:
   ```bash
   node scripts/capture.mjs still screenshots/{task}/still.png
   ```
5. Run `npm run check`.
6. Fix TypeScript and runtime console errors before tuning.
7. Run `npm run build` once the slice is clean.
8. Update `STRUCTURE.md` if module ownership, state, asset contracts, or verification changed.

For long-running visible work, capture several frames:

```bash
node scripts/capture.mjs frames screenshots/{task} 30
```

## Browser Runtime Standard

The browser path is the runtime. Do not treat a TypeScript build as sufficient proof.

Required for browser validation:

- Chrome/Chromium executable is available or `CHROME_BIN` points to one.
- WebGL2 is available on the game canvas.
- Hardware GPU acceleration is preferred — `capture.md` covers reading the software-renderer warning.
- Vite browser console forwarding stays enabled so runtime errors appear in the terminal.

## Assets

Time asset generation to where the work is. When the substance is logic, build on placeholders — primitives, flat colors, procedural stand-ins — until the design that needs a real asset is settled, then generate it and swap it in. When the substance is the art, generate the real assets early and build around them; a placeholder would tell you nothing. See `interactive.md` for asset timing and budget confirmation.

Use Vite asset URLs:

```ts
import heroUrl from "../assets/models/hero.glb?url";
```

Then load with Babylon:

```ts
import "@babylonjs/loaders/glTF";
import { SceneLoader } from "../app/babylon";

await SceneLoader.ImportMeshAsync("", "", heroUrl, scene);
```

Use `public/**` only for files that need stable direct URLs. Imported runtime assets should normally live under `src/assets/**`. Generation intermediates (source videos, raw frame dumps, QA previews) are not runtime assets — keep them out of `src/assets/**` and delete them once the final files are in place.

## Delivery

The deliverable is the live URL. Surface it as soon as something is showable and keep `npm run dev` alive so the user sees every change.

- Default scene: `http://127.0.0.1:5173/` (builds `?scene=main`).
- Isolated review scene (on demand only): `http://127.0.0.1:5173/?scene=<name>` — add the route in `src/game/scenes/registry.ts`, fold it back into `main` once accepted.
- Remote user: the dev server binds `0.0.0.0`, so the machine's LAN address works directly; use a tunnel for a public link — see `interactive.md`.

## Stop Conditions

- `npm run check` passes.
- `npm run build` passes (compile gate).
- The Vite dev server runs and the user has the live URL.
- Browser validation confirms WebGL2 hardware rendering.
- Visual requirements verified from your own screenshots and confirmed live by the user.
- `STRUCTURE.md` matches the shipped runtime shape.
