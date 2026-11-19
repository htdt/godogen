# Babylon.js engine guide

Stack: **Babylon.js** (`@babylonjs/core` + `@babylonjs/loaders`), **Vite**, **TypeScript**, Node (current LTS).

## Project shape

A plain Vite + TS project is enough. Scaffold one (`npm create vite@latest . -- --template vanilla-ts`), add `@babylonjs/core` and `@babylonjs/loaders`, then:

- A fullscreen `<canvas>` in `index.html` and a render loop: create an `Engine`, build a `Scene`, call `engine.runRenderLoop(() => scene.render())`, and resize on `window`.
- Put gameplay in `src/` modules; keep generated assets under `src/assets/` and load them through Vite (`import url from './assets/x.glb?url'`).
- Drive gameplay off `scene.onBeforeRenderObservable` and the engine delta — don't assume a fixed frame rate.

Commands: `npm install` · `npm run dev` · `npm run build`.

**Bind the dev server to `0.0.0.0` on a fixed port** (`server: { host: true, port: 5173 }`) so `http://<host>:5173` is reachable from other machines on the LAN or through a tunnel.

## Imports

Import from `@babylonjs/core` subpaths (e.g. `@babylonjs/core/Meshes/meshBuilder`). Some features are registered by a **side-effect module** that tree-shaking drops — code compiles but throws at runtime with `"<Feature> needs to be imported before it can be used"`. When you hit that, add the named side-effect import it asks for (e.g. `import "@babylonjs/core/Meshes/instancedMesh"`, `import "@babylonjs/core/Culling/ray"`, `import "@babylonjs/loaders/glTF"`).

## Physics

Havok is available via `@babylonjs/havok`. Serve `HavokPhysics.wasm` from `public/` and load it with `HavokPhysics({ locateFile: () => "/HavokPhysics.wasm" })` — a `?url` import is blocked by the package `exports`. Enabling physics needs its side-effect module registered (per the rule above); then use `PhysicsAggregate`.

## Capture

Load the running dev URL in headless Chrome/Chromium (`playwright-core`, or `google-chrome --headless`) and screenshot.

- **Use a real GPU.** Headless Chrome silently falls back to SwiftShader/llvmpipe, which renders slowly or blank. On Linux, run under `xvfb-run` and request hardware (`--use-angle=vulkan`); read the WebGL `RENDERER` string and warn if it contains `swiftshader`/`llvmpipe`/`lavapipe`.
- **Wait before shooting.** Capture only after the scene has rendered a frame and textures/GLBs have loaded — gate on a ready flag the game sets, or settle a fixed delay after network idle. Screenshotting too early gives a misleading blank frame.
- **Video:** screenshot on an interval (~30fps) into a temp dir, then encode at ~720p: `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video.mp4`.

## Babylon API lookups

For exact import paths, loader behavior, or Vite specifics on the installed version, read the package sources under `node_modules/@babylonjs/core` and `node_modules/@babylonjs/loaders`; fall back to `https://doc.babylonjs.com/`.
