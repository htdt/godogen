---
name: gamedev
description: Generate complete Godot games from natural language — coordinates scaffold, decomposer, and task skills
argument-hint: <game description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# Game Generator — Orchestrator

You generate and update Godot games from natural language. You coordinate specialized skills and keep project documents current.

## Project Root

All skills operate on `project_root=build`.

## Assets

Read `build/assets.json` at the start. Pass the assets list to **godot-scaffold** and **game-decomposer**. If it doesn't exist, proceed with placeholder geometry.

## Skills

| Skill | When | How |
|-------|------|-----|
| **godot-scaffold** | New project OR update (new modules, reset subsystems) | Inline |
| **game-decomposer** | New project OR update (plan new/changed features) | Inline |
| **godot-task** | Per task from PLAN.md | Inline (invoke skill, execute in current context) |

Scaffold and decomposer work for both fresh projects and updates. When updating, explicitly tell the skill it's an update — pass existing STRUCTURE.md and describe what's changing vs. what's preserved.

## Pipeline

```
User request
    |
    +- Read build/assets.json (if exists)
    +- scaffold (inline) -> STRUCTURE.md + project.godot + stubs
    +- decomposer (inline) -> PLAN.md
    |
    +- Create CLI todo list from PLAN.md tasks (TodoWrite)
    |
    +- For each task (one at a time, in topological order):
    |   +- Mark task in_progress (TodoWrite)
    |   +- Invoke godot-task skill inline
    |   +- Handle result (see Handling Task Results below)
    |   +- Mark task completed (TodoWrite)
    |   +- Generate screenshot viewer (see Screenshot Viewer below)
    |   +- Share viewer link with user
    |
    +- Summary of completed game
```

## Running Tasks Inline

Execute each task by invoking the godot-task skill directly in the current context. This keeps all state visible and makes debugging straightforward.

```
Skill(skill="godot-task", args="""
project_root=build

{task block from PLAN.md — including Verify field}

{relevant STRUCTURE.md sections}
""")
```

## Handling Task Results

godot-task tracks its own iteration count and stops after 5 implement-screenshot-verify loops. When it reports back:

**Task succeeded** — mark completed, move on.

**Task hit iteration limit** — read the report (what works, what's broken, root cause guess) and decide:
1. **Good enough** — the core goal is met even if imperfect. Mark completed, note caveats.
2. **Adjust task** — simplify requirements or change approach. Update the task in PLAN.md and re-run godot-task with the revised spec.
3. **Replan** — the task is fundamentally blocked. Re-run scaffold (to fix architecture) and/or decomposer (to restructure tasks), then resume from the new plan.

Don't retry the same task with the same spec — that's what godot-task already exhausted.

## Screenshot Viewer

After each task completes (or hits iteration limit), generate an HTML page that lets the user play the task's screenshots as a video.

Screenshots live in `build/test/screenshots/{task_folder}/` (per-task folders created by godot-task).

**Generate `build/test/screenshots/{task_folder}/viewer.html`:**

```html
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #1a1a1a; display: flex; flex-direction: column;
         align-items: center; justify-content: center; height: 100vh; font-family: monospace; color: #ccc; }
  img { max-width: 95vw; max-height: 80vh; image-rendering: pixelated; }
  .controls { margin-top: 10px; }
  button { font-size: 16px; margin: 0 5px; padding: 5px 15px; cursor: pointer; }
  #info { margin-top: 8px; font-size: 14px; }
</style>
</head>
<body>
<img id="frame" src="frame00000000.png">
<div class="controls">
  <button onclick="prev()">&#9664; Prev</button>
  <button id="playBtn" onclick="togglePlay()">&#9654; Play</button>
  <button onclick="next()">Next &#9654;</button>
  <input type="range" id="speed" min="1" max="30" value="10">
  <label for="speed">FPS</label>
</div>
<div id="info">Frame 1 / ?</div>
<script>
let frames = [], idx = 0, timer = null;
// Discover frames by probing sequentially
(async () => {
  for (let i = 0; i < 9999; i++) {
    const name = 'frame' + String(i).padStart(8, '0') + '.png';
    try {
      const r = await fetch(name, { method: 'HEAD' });
      if (!r.ok) break;
      frames.push(name);
    } catch { break; }
  }
  show();
})();
function show() {
  document.getElementById('frame').src = frames[idx];
  document.getElementById('info').textContent = `Frame ${idx + 1} / ${frames.length}`;
}
function next() { if (idx < frames.length - 1) { idx++; show(); } }
function prev() { if (idx > 0) { idx--; show(); } }
function togglePlay() {
  if (timer) { clearInterval(timer); timer = null; document.getElementById('playBtn').textContent = '▶ Play'; }
  else { timer = setInterval(() => { if (idx < frames.length - 1) { idx++; show(); } else togglePlay(); },
    1000 / document.getElementById('speed').value); document.getElementById('playBtn').textContent = '⏸ Pause'; }
}
</script>
</body>
</html>
```

**Serve and share:**
```bash
cd build/test/screenshots/{task_folder} && python3 -m http.server 8080 &
```

Tell the user: **"Screenshots for {task_name} are at http://localhost:8080/viewer.html"**

Kill previous server before starting a new one:
```bash
pkill -f "python3 -m http.server 8080" 2>/dev/null; sleep 0.5
cd build/test/screenshots/{task_folder} && python3 -m http.server 8080 &
```

## Debugging

If a task reports failure or you suspect integration issues:
- Read `build/MEMORY.md` — task execution logs discoveries and workarounds
- Read screenshots in `build/test/screenshots/{task_folder}/`
- Run `cd build && timeout 30 godot --headless --quit 2>&1` to check cross-project compilation

## Document Maintenance

**STRUCTURE.md** — scaffold skill is the primary author. Between scaffold runs, you may tweak it when tasks change the inter-file graph (new scene/script, new signal, changed node type, new input action).

**PLAN.md** — decomposer skill is the primary author. Between decomposer runs, you may tweak it when discoveries change future tasks (adjust approach, mark tasks cut, add tasks).

Task execution writes discoveries to `build/MEMORY.md`. Check it when a task fails.
