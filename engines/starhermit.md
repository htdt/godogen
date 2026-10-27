# StarHermit engine guide

Stack: **TypeScript**, the prebuilt **StarHermit runtime**, built-in `starhermit:*` host modules. One script-game package plays in browsers and natively in the StarHermit client.

## Runtime and API lookup

Get a current, non-revoked release from [engine releases](https://wiki.starhermit.com/docs/engine-releases.html) ([versions.json](https://wiki.starhermit.com/engine/versions.json)); download the Windows or Linux runtime and verify its archive against `native.json`. Keep its executable, `release.json` and `web-manifest.json` together, outside the game repo, with `starhermit` on `PATH`. Linux needs glibc 2.35+; windowed play needs X11/Wayland and graphics/audio drivers. Headless checks and packaging need no display.

[Standalone developer tools](https://wiki.starhermit.com/engine/tools/README.html) provide `starhermit-tools` for checking and web packaging on macOS, Linux and Windows. Their `check` validates files but does **not execute gameplay**; macOS playtests use the browser.

Read the generated `.starhermit/starhermit.d.ts` for exact modules, supported methods, units and limits. `starhermit:scene` resembles three.js, but implements its own supported surface. Use those declarations rather than npm three.js types or remembered browser APIs. The [tutorial](https://wiki.starhermit.com/docs/tutorials/starhermit-engine.html) covers the full workflow.

## Project shape

`starhermit new <new-directory> --title "Game Title"` creates `starhermit.txt`, `src/main.ts`, `tsconfig.json`, and the declarations. In an already-published Godogen repo, scaffold into a temporary sibling and copy those files in. Refresh declarations with `starhermit types .` after changing runtimes.

- `starhermit.txt` pins `engine.api`, `engine.minor`, `engine.version`, and `engine.entry=src/main.ts`; retain `launch=index.html` for web play. The release version and host API minor are separate numbers: preserve the scaffold's values and test before re-pinning.
- Keep generated assets in `assets/`, addressed by package-relative paths such as `assets/hero.glb`. Load models through the host's `GLTFLoader` from `starhermit:scene`; check its declarations for animation and supported extensions.
- Register lifecycle hooks through `starhermit:engine`: fixed-step rules in `onFixedUpdate`, interpolated scene state in `onRender`. Assign `renderer.camera` and add nodes to `scene`. `starhermit:draw` and `starhermit:ui` provide HUD and menus.
- Declare actions with `control.<action>` and optional `engine.gamepad.<action>`; read them through `starhermit:input`. F1 belongs to the runtime's options menu. Declare capabilities such as `platform,storage` when used; account, settings and saves go through the corresponding host modules.

## Run, package and show

```bash
npx --package typescript tsc -p .
starhermit check .
starhermit . --dev
starhermit package --web . --out ../game-upload
python3 -m http.server 5173 --bind 0.0.0.0 --directory ../game-upload
```

TypeScript checks types; the native `check` executes 120 headless frames and catches module/startup errors. Share `http://<host>:5173` for browser play. Repackage after edits and refresh. With standalone tools, substitute `starhermit-tools` for the check/package commands and test execution in the browser.

## Traps and capture

- Games run in a sandbox, including in a browser worker: use host file, input, UI, audio and platform APIs. There is no game DOM, arbitrary network access, or Node.js environment. For large entity counts, use `starhermit:world` tables, kernels and bindings to keep per-entity work native.
- Check `GLTFLoader`'s supported features before generating assets. In runtime 1.17.1 it imports static geometry and PNG/WebP textures, leaving out JPEG textures, skins, animation clips and morph targets. Inspect its warnings and `ignored` result; use supported textures and animate separate scene nodes for articulated models.
- Packaging writes `index.html` and the hash-indexed `starhermit-files.json`. Let it generate the loader; regenerate the upload after any source/asset change. `--out` must be outside the game directory. Exclude Godogen docs (`AGENTS.md`, `CLAUDE.md`, `starhermit.md`, `README.md`) and captures with `.starhermitignore`; `.gitignore` does not control packaging.
- Upload size defaults to 50 MiB. For larger assets, follow the release's remote-file packaging workflow. The distributable is `../game-upload/`; publishing to StarHermit uses the standalone tools' documented `publish` command and deployment credentials.
- Capture the packaged browser URL with Playwright/Chrome, using hardware rendering. Wait for visible gameplay and assets, exercise actions, and inspect console/page errors. Record 15–20s through Playwright video or timed screenshots encoded with ffmpeg. The native headless check alone is no visual proof.
