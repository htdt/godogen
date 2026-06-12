---
name: babylon-help
display_name: Babylon Help
short_description: Babylon.js APIs, loaders, Vite patterns, and browser runtime help
default_prompt: "Use ${BABYLON_HELP_COMMAND} for Babylon.js, Vite, WebGL, loader, or browser-capture questions."
allow_implicit_invocation: false
description: |
  Look up Babylon.js APIs, import paths, examples, loaders, Vite integration, and browser runtime behavior. Use for Babylon-specific API lookup, feature design, rendering setup, asset loading, and capture issues.
---

# Babylon Help

Use this skill for Babylon.js API questions, exact import paths, loader behavior, rendering setup, Vite/HMR integration, WebGL/browser runtime questions, and browser capture problems.

Single-version policy:

- Resolve the target version from the project's `package.json` and `package-lock.json`.
- Use the installed npm package for the current project version as the primary local reference.
- Do not blend examples from older Babylon versions unless the caller explicitly asks for migration help.

Primary local sources after `npm install`:

```text
node_modules/@babylonjs/core/
node_modules/@babylonjs/loaders/
node_modules/vite/
```

Lookup order:

1. Project `package.json` and lockfile for exact versions.
2. Installed `node_modules/@babylonjs/core` and `node_modules/@babylonjs/loaders` source/types.
3. Installed `node_modules/vite` docs/types for Vite-specific behavior.
4. Official Babylon documentation at `https://doc.babylonjs.com/`.
5. Official npm package pages for package metadata.
6. Official Vite docs for HMR/server behavior.

If `node_modules/` is missing in a scaffolded project, run `npm install` before lookup. If the project is not scaffolded yet, use official docs and say which package version you are targeting.

Useful searches:

```bash
rg "class ArcRotateCamera" node_modules/@babylonjs/core
rg "ImportMeshAsync" node_modules/@babylonjs/core node_modules/@babylonjs/loaders
rg "hotUpdate" node_modules/vite
```

When answering:

- Start with the concrete recommendation.
- Name the files or official pages checked.
- Separate documented facts from inference.
- Give import paths that match the installed package.
- Mention browser/GPU constraints when they affect the answer.
