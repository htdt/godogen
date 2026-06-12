/// <reference types="node" />
import { createReadStream, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { defineConfig, type Plugin } from "vite";

// QA images the agent generates at the project root (outside src/ and public/)
// so they can be shown to the user by URL without polluting runtime asset paths.
const ROOT_IMAGE = /^\/(reference[\w.-]*\.png)$/;

function godogenBabylonDev(): Plugin {
  return {
    name: "godogen-babylon-dev",
    apply: "serve",

    configureServer(server) {
      // Serve project-root QA images (e.g. /reference.png) so the agent can
      // show the user the reference in the browser.
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split("?")[0] ?? "";
        const match = ROOT_IMAGE.exec(url);
        if (!match) return next();

        const file = resolve(join(server.config.root, match[1]));
        if (!file.startsWith(server.config.root) || !existsSync(file)) {
          // 404 instead of falling through to the SPA fallback, so a link to a
          // not-yet-generated image fails loudly rather than serving the game page.
          res.statusCode = 404;
          res.setHeader("Content-Type", "text/plain");
          res.end(`No ${match[1]} at the project root`);
          return;
        }

        res.setHeader("Content-Type", "image/png");
        res.setHeader("Cache-Control", "no-cache");
        createReadStream(file).pipe(res);
      });
    },

    // Manual-reload model: a save never auto-reloads the page. Returning an
    // empty array tells Vite the update is fully handled, suppressing the
    // default HMR / full reload. Refresh the browser to apply edits — the dev
    // server always serves the current source, and game state survives until
    // you choose to reset it. (State-preserving HMR — swapping only what
    // changed while keeping state — is intentionally not implemented yet.)
    hotUpdate() {
      if (this.environment.name !== "client") return;
      return [];
    }
  };
}

export default defineConfig({
  plugins: [godogenBabylonDev()],

  assetsInclude: [
    "**/*.glb",
    "**/*.gltf",
    "**/*.hdr",
    "**/*.env",
    "**/*.ktx2",
    "**/*.basis",
    "**/*.wasm"
  ],

  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    forwardConsole: {
      unhandledErrors: true,
      logLevels: ["warn", "error"]
    }
  },

  preview: {
    host: "0.0.0.0",
    port: 4173,
    strictPort: true
  },

  build: {
    target: "es2022",
    outDir: "dist",
    assetsDir: "assets",
    assetsInlineLimit: 0,
    modulePreload: {
      polyfill: false
    },
    sourcemap: true
  }
});
