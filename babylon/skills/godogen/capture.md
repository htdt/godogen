# Browser Screenshots

Screenshots are for *your own* verification — confirm a visible change before showing the user, who judges motion and feel on the live URL. Keep the Vite dev server alive and capture from the already-running page.

Primary URL:

```text
http://127.0.0.1:5173
```

## Browser/GPU Requirements

Use Chrome or Chromium with WebGL2. Hardware GPU acceleration is strongly preferred. The capture script reads the WebGL2 vendor/renderer through the game canvas and logs a prominent `[capture] WARNING` when it sees a software renderer (SwiftShader, llvmpipe, lavapipe, softpipe, mesa offscreen) — the capture still completes so a GPU-less host can still self-check, just at reduced quality and speed.

If the host has a GPU and capture is still falling back to software, treat that as a misconfiguration and fix the browser GPU path (ANGLE backend, Vulkan ICD, drivers) so your screenshots match what the user sees in their own browser.

If Chrome/Chromium itself or WebGL2 is missing, capture cannot run — report the missing dependency clearly rather than improvising around it.

Useful checks:

```bash
node --version
npm --version
command -v google-chrome || command -v chromium || command -v chromium-browser
vulkaninfo --summary | sed -n '1,120p'
```

Set `CHROME_BIN=/path/to/chrome` if Chrome is installed outside the common paths.

## Ad Hoc Screenshot

With `npm run dev` already running:

```bash
node scripts/capture.mjs still screenshots/{task}/still.png
```

This is cheap. Use it frequently after visible changes.

## Short Frame Sequence

For animation checks:

```bash
node scripts/capture.mjs frames screenshots/{task} 60
```

This writes `frame00001.png`, `frame00002.png`, and so on. Use frames to debug motion you can't judge from a single still.

## Validation Standard

- `npm run check`
- `npm run build`
- Vite server responds at `http://127.0.0.1:5173`
- `node scripts/capture.mjs still screenshots/{task}/still.png` writes a real PNG
- the screenshot shows the change you intended, with no missing textures or placeholder materials

A compile-clean page is not proof of a playable game — the user confirms the playable result live.
