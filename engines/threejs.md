# three.js engine guide

Stack: **three.js** (`three`), **Vite**, **TypeScript**, Node 22+.

> three ships a release a month and deprecates as it goes, so the installed one is likely newer than this model's training data. When the console warns that something is deprecated, follow it; for exact shapes read `node_modules/three/src` (addons under `node_modules/three/examples/jsm`), not memory.

## Project shape

A plain Vite + TS project is enough. Scaffold one (`npm create vite@latest . -- --template vanilla-ts`), add `three` and `@types/three` on the same `0.N` release (three ships no types of its own), then:

- A fullscreen `<canvas>`, a `WebGLRenderer` driven by `renderer.setAnimationLoop`, and resize on `window`. Addons (loaders, controls, postprocessing, `SkeletonUtils`) import from `three/addons/...`.
- Put gameplay in `src/` modules; keep generated assets under `src/assets/` and load them through Vite (`import url from './assets/x.glb?url'`).
- three is a renderer, not an engine — physics, UI, and audio are yours to choose. For physics, `@dimforge/rapier3d-compat` inlines its wasm (`await RAPIER.init()` before use); the plain `@dimforge/rapier3d` imports `.wasm` as a module, which Vite doesn't handle without a plugin.

Commands: `npm install` · `npm run dev` · `npm run build` (use the build as a compile gate, but it is not proof the game runs — only the running page is).

**Bind the dev server to `0.0.0.0` on a fixed port** (`server: { host: true, port: 5173 }`) so the URL is shareable on the LAN or via a tunnel. This is how the user watches: keep `npm run dev` running and hand them `http://<host>:5173` — you edit, they refresh.

## Quirks worth knowing (silent-failure)

- **Color space.** Textures you load or build yourself default to `NoColorSpace`; set `colorSpace = SRGBColorSpace` on color maps (albedo, sprites, UI, sky) or they render washed out. The glTF loader tags its own.
- **Lights are physical.** Point and spot lights fall off with inverse-square (`decay = 2`) — intensities from older examples leave the scene near-black a few meters out. A directional light's shadow camera spans ±5 units: size `light.shadow.camera` to the play area and move it with the player, or shadows stop at its edge.
- **Rigged clones.** `clone()` on a skinned GLB keeps the copy bound to the original's bones, so it renders in the original's pose. Clone rigs with `SkeletonUtils.clone()`.
- **WebGPU falls back.** `WebGPURenderer` (`three/webgpu`, TSL node materials) runs on its WebGL2 backend when the browser has no WebGPU adapter, with only a console warning — check `renderer.backend.isWebGPUBackend` before trusting a capture of a WebGPU-only effect.

## Capture (self-verify + proof video)

Load the running dev URL in headless Chrome/Chromium (`playwright-core`, or `google-chrome --headless`) and screenshot. This is how you verify your own work and how you produce the proof video.

- **Use a real GPU.** Headless Chrome silently falls back to SwiftShader/llvmpipe, which renders slowly or blank. On Linux, run under `xvfb-run` and request hardware (`--use-angle=vulkan`); read the WebGL `RENDERER` string and warn if it contains `swiftshader`/`llvmpipe`/`lavapipe`.
- **Wait before shooting.** Capture only after the scene has rendered a frame and textures/GLBs have loaded — gate on a ready flag the game sets. Screenshotting too early gives a misleading blank frame.
- **Step time from the capture script.** A screenshot takes longer than a frame, so shooting the live loop on an interval gives a sped-up, stuttering clip. Give the game a capture mode (a query flag) that stops `setAnimationLoop` and exposes a hook advancing one fixed 1/30 s step and rendering; shoot after each call — 450 steps = 15 s. Reading pixels with `canvas.toDataURL()` returns blank unless it runs right after `render()` in the same task, or the renderer has `preserveDrawingBuffer: true`.
- **Proof video:** encode the frames at ~720p: `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p proof.mp4`.
