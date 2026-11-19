---
name: engine-guide
description: |
  Building on Godot 4 (C# or GDScript), Bevy, Babylon.js, three.js or HTML: which to choose, installing its toolchain, the project sketch, build commands, headless capture to screenshots and video, and the traps that fail silently. Use when starting or working on a game, a video made in an engine (presentation, explainer, trailer, product showcase), an interactive 3D or 2D page, or anything else built on one of these engines.
---

# Engine guide

One guide per engine sits next to this file: the stack, a project sketch, build commands, headless capture, and the traps that pass a build and break at runtime. Read the chosen engine's guide before writing the project. On an existing project, the engine is already chosen. `setup.md` installs what the engine needs, at current versions.

| Guide | Stack | Pick it for |
|---|---|---|
| `godot.md` | Godot 4, C# | desktop 2D or 3D; the fewest runtime surprises in long unattended runs |
| `godot-gdscript.md` | Godot 4, GDScript | a Godot project the user will keep developing in the editor |
| `bevy.md` | Bevy, Rust | a Rust codebase: ECS, no editor, many entities |
| `babylon.md` | Babylon.js, TypeScript | a browser game that leans on engine systems: physics, GUI, particles, animation |
| `threejs.md` | three.js, TypeScript | a browser piece that leans on its look: custom shaders, stylized rendering, a light page |
| `html.md` | DOM + canvas and three.js, TypeScript | 2D that is mostly text and UI: interactive fiction, cards, grid roguelikes, puzzles, management |

## Choosing

Every engine gets the same loop (build, generate assets, capture), so the choice comes down to what the user holds at the end and how they watch along the way. When the brief leaves it open, it is the user's call as much as yours: it decides what they get, and a switch later is a rewrite. What's already installed can tip a close call: `godot --version` (`mono` in it means the .NET build), `dotnet --version`, `cargo --version`, `node --version`.

- **How the user watches.** On a remote box or steering from a phone, a browser engine wins: the dev server is a URL they refresh while you edit. Godot and Bevy run as desktop apps; from a headless server the user sees them in a recorded video, or pulls the repo and runs it. On the user's own desktop the engines are even.
- **2D.** Godot has a dedicated 2D engine (pixel-space nodes, tilemaps, 2D physics). Bevy handles 2D well. Babylon.js and three.js are 3D-first and draw 2D as sprites and planes. For 2D that is mostly text, panels and buttons, `html` builds on the DOM: type and CSS are the art, with canvas and three.js for motion, effects and 3D moments.
- **Godot: C# or GDScript.** Same engine, scenes and capture. C# compiles: `dotnet build` type-checks the whole project before anything runs, so mistakes surface early; it needs the .NET build of Godot and the .NET SDK. GDScript is Godot's native language, used by most tutorials, addons and Asset Library entries, and runs on any Godot build; whatever the parser can't type fails only at runtime, on the path that runs. GDScript exports everywhere Godot does; check current C# platform support before a web export.
- **Babylon.js or three.js.** Babylon.js is a full engine: Havok physics, GUI, particles, animation groups and an inspector come in the box, so there are fewer seams to wire, at the cost of a heavier bundle. three.js is a renderer: you pick and wire physics (Rapier), UI (HTML over the canvas) and audio, and get the deepest pool of web 3D examples, the most control over the look (custom shaders, postprocessing, WebGPU and TSL node materials) and a small bundle.
- **Bevy** is for a project that should be Rust: code only, ECS, compile-time guarantees, headroom for many entities. It compiles slowest, and its API moves between releases faster than training data catches up, so its guide reads the installed source.
- **No strong preference:** `babylon` for a user who watches and steers from anywhere; `godot` for a desktop game they'll receive as a video or run themselves.

## Beyond games

Godot's movie writer, Bevy's offscreen binary and three.js's stepped capture advance a fixed timestep per saved frame: render cost never shows in the result, and every frame lands exactly where it was scheduled. That makes an engine a studio for more than games. The guides say "the game"; read it as whatever is being built.

- **Video**: a presentation, explainer, trailer, product showcase, data story, music visualization. The capture is the deliverable. Script camera, animation and text on one timeline, place generated voice-over and music (the asset-gen skill) on the same timeline, and mux with ffmpeg. Godot is the strongest pick: deterministic `--write-movie` is built in, it records the scene's own audio in sync, and 3D, 2D, text, particles and tweens are one toolset. three.js when the look is shader-driven or the piece should also live on the web.
- **Interactive pages**: a product configurator, an interactive explainer or data visualization, a 3D landing scene. three.js or Babylon.js, or `html` when it is mostly text and UI.
