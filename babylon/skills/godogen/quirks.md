# Babylon And Browser Gotchas

- Import Babylon symbols from `src/app/babylon.ts` unless you are deliberately adding a new export there.
- Import loaders explicitly. GLB/GLTF loading needs `import "@babylonjs/loaders/glTF";`.
- Vite asset imports should use `?url` for files that Babylon loads by URL.
- Do not put runtime-loaded source assets in `public/**` unless they need stable direct URLs. Prefer `src/assets/**`.
- `createScene(app)` must return a new `Scene`; `BabylonApp.load` disposes the previous scene after the replacement is ready (it runs on page load and when switching the `?scene=` route).
- Scenes live in `src/game/scenes/` and are addressed by `?scene=<name>` through `registry.ts`. Build in `main`; add a route only for on-demand isolation. An unknown `?scene=` name silently falls back to `main`; a registry entry whose module file is missing throws at page load.
- Window, document, pointer-lock, and gamepad listeners are not disposed by Babylon scene disposal. Own and remove them explicitly.
- `scene.onBeforeRenderObservable.add(...)` observers attached to the scene are cleaned up when the scene is disposed.
- Browser audio usually needs a user gesture before playback. Design menus or first input to unlock audio when needed.
- Vite dev server port is strict. If `5173` is occupied, stop the stale server instead of silently switching URLs, unless the user asks for another port.
- Browser console errors are runtime failures. Vite forwards warnings/errors to the server terminal; read them.
- Background tabs throttle `requestAnimationFrame`, so the first frame after the user tabs back arrives with one huge delta. Clamp the delta you feed gameplay (e.g. `Math.min(delta, 0.1)`) so a refocused tab doesn't teleport physics and animations.
