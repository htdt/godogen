# HTML engine guide

Stack: **DOM + CSS + TypeScript**, **Vite**, Node (current LTS), with `<canvas>` and **three.js** wherever motion or a scene makes the game better. No UI framework: the page is the game. Made for 2D games built around text and UI — interactive fiction, card and board games, roguelikes on a character grid, puzzles, management and incremental games.

## Project shape

Scaffold a plain Vite + TS project (`npm create vite@latest . -- --template vanilla-ts`), then:

- One game-state object is the source of truth; rules are functions of state, and a `render()` brings the DOM up to date after every action.
- Fonts are self-hosted (`@fontsource/<name>`), the palette lives in CSS variables, and generated images (portraits, card art, backdrops) live under `src/assets/`, imported through Vite.
- Text and controls are DOM; animation and interactive elements can be canvas or three.js layered with it — don't limit the look to plain HTML.
- Build for the device the user plays on — the one the brief names, else a desktop browser — and make it look its best there: a rich page on that device beats a plain one that runs on any old phone.

Commands: `npm install` · `npm run dev` · `npm run build`.

**Bind the dev server to `0.0.0.0` on a fixed port** (`server: { host: true, port: 5173 }`) so `http://<host>:5173` is reachable from other machines on the LAN or through a tunnel.

## Quirks worth knowing (silent-failure)

- **Every edit reloads the page** and resets the game the user is in the middle of. Autosave state to `localStorage` after each action and restore on load. Version the save and discard a mismatched one — an old save loaded into a new state shape throws, and looks like a new bug. `?new` starts clean and `?seed=N` fixes the RNG.
- **Rewriting `innerHTML` destroys what lived there**: a text input's focus and caret, a log's scroll position, running transitions, listeners on children. Keep the command line and the scrolling log outside the re-rendered region (append to the log), and handle clicks by delegation on a stable parent.
- **Headless Chrome renders WebGL in software** (SwiftShader), slowly or blank, so a three.js layer can be missing from a capture and fine in a browser. On Linux run under `xvfb-run` with `--use-angle=vulkan`, and read the WebGL `RENDERER` string before trusting the shot.
- **Glyph fallback.** A character missing from the font is drawn from whatever system font has it, at its own width — a character grid drifts out of line, and a machine without an emoji font draws emoji as empty boxes. Pick a monospace font that covers the glyph set (box drawing, arrows, suits) and keep emoji out of grids.
- **Hidden tabs stall time.** `requestAnimationFrame` stops and timers drop to about once a second in a background tab. Compute idle and real-time progress from elapsed wall-clock time, not from tick counts.
- **Sound needs a gesture.** An `AudioContext` created before the first click or key stays suspended, and `play()` rejects, with only a console warning. Resume it in the first input handler.
