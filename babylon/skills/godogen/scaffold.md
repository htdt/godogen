# Babylon Scaffold

Create or refresh a Babylon.js + TypeScript + Vite project shell. This defines the runtime entrypoints and reload model; gameplay generation fills in `src/game/**`.

## Workflow

1. Check `node --version` and `npm --version`.
2. Fresh project: use the published scaffold files already present in the repo root, or recreate the same file set if the directory was wiped.
3. Existing Babylon project: preserve package name and dependency versions unless the user asked for a migration. Preserve `package-lock.json` when it already matches the manifest.
4. Keep the baseline contract:
   - `index.html` contains `canvas#game-canvas` and `div#hud`.
   - `src/main.ts` creates one `BabylonApp`, resolves the active scene from `?scene=` via the registry, and loads it.
   - `src/app/BabylonApp.ts` owns the Babylon `Engine` lifecycle.
   - `src/app/babylon.ts` is the project import surface for Babylon symbols.
   - `src/game/scenes/main.ts` exports `createScene(app)`; `src/game/scenes/registry.ts` maps scene names to modules (`main` is the default).
   - `src/game/assets.ts`, `input.ts`, and `state.ts` are small helpers, not mandatory frameworks.
   - `scripts/capture.mjs` captures browser screenshots through Chrome/Chromium.
5. Run `npm install` if `node_modules/` is missing or `package-lock.json` is stale.
6. Run `npm run check`.
7. Run `npm run build`.
8. Start `npm run dev` and keep it running when possible.
9. Verify the browser at `http://127.0.0.1:5173` with `node scripts/capture.mjs still screenshots/scaffold.png`.

If Chrome/Chromium or WebGL2 is unavailable, stop and report the missing dependency. Hardware GPU is preferred; `capture.md` covers reading the software-renderer warning.

## Baseline Files

```text
index.html
package.json
tsconfig.json
vite.config.ts
scripts/capture.mjs
src/main.ts
src/style.css
src/app/BabylonApp.ts
src/app/babylon.ts
src/game/scenes/main.ts
src/game/scenes/registry.ts
src/game/assets.ts
src/game/input.ts
src/game/state.ts
src/assets/models/
src/assets/textures/
src/assets/audio/
src/assets/shaders/
public/
```

The current baseline package versions are:

```json
{
  "@babylonjs/core": "^9.8.0",
  "@babylonjs/loaders": "^9.8.0",
  "playwright-core": "^1.60.0",
  "typescript": "^6.0.3",
  "vite": "^8.0.13"
}
```

These versions were checked against npm during the Babylon source update. For a new project, use the current source scaffold. For an existing project, avoid opportunistic dependency churn.

## Reload Model

`vite.config.ts` installs the `godogen-babylon-dev` plugin, which serves project-root QA images (`/reference.png`) and disables auto-reload — edits apply on the next browser refresh, a clean full load (fresh `Engine`, `Scene`, and WebGL context). The dev server always serves current source, so a refresh never shows stale code.

`createScene(app)` must create a fresh `Scene` every call. `BabylonApp.load` disposes the previous scene after the new one is ready, so switching the `?scene=` route never leaks the old scene.

## STRUCTURE.md

Write `STRUCTURE.md` in full. Start with this shape:

````markdown
# {Project Name}

## Runtime

- Babylon.js {version from package.json}
- TypeScript + Vite
- Browser URL: `http://127.0.0.1:5173`
- Dimension: 3D

## App Entry

- `index.html` -> `src/main.ts`
- `src/main.ts` -> creates `BabylonApp`, resolves the `?scene=` route via the registry, loads it, starts the render loop
- `src/app/BabylonApp.ts` -> owns `Engine`, active `Scene`, resize, disposal
- `src/app/babylon.ts` -> Babylon import barrel

## Game Entry

- `src/game/scenes/main.ts` -> default scene, exports `createScene(app)`
- `src/game/scenes/registry.ts` -> scene name -> module map; `?scene=<name>` selects it (`main` default)
- `src/game/assets.ts` -> imported asset URLs
- `src/game/input.ts` -> optional input helper
- `src/game/state.ts` -> optional state helper

## Planned Modules

- `GameWorld` -> active actors, spawning, high-level rules
- `CameraController` -> camera behavior
- `UIController` -> HUD and menus through DOM or Babylon GUI

## Assets

- Runtime imports: `src/assets/**`
- Stable direct URLs: `public/**`

## Verification

- `npm run check`
- `npm run build`
- `npm run dev`
- browser screenshot self-check through `scripts/capture.mjs`
- user confirms the playable result live at the URL
````

Keep `STRUCTURE.md` structural. Do not turn it into a task log.
