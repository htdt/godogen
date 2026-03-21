# Godogen Improvements Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add macOS capture support, harden GDScript/scene builder reliability, add audio generation, and add C# as an alternative scripting language.

**Architecture:** Godogen uses two Claude Code skills — `godogen` (orchestrator) and `godot-task` (executor). Changes are to skill definition files (`.md`), one Python tool (`asset_gen.py`), and one new GDScript template. No application code — these are LLM instructions that guide game generation.

**Tech Stack:** Markdown skill definitions, Python 3 (asset_gen.py), GDScript (verify_scene template), Godot 4 Engine, Gemini API, ffmpeg

**Spec:** `docs/superpowers/specs/2026-03-21-godogen-improvements-design.md`

---

## Chunk 1: Phase 1 — macOS Capture Support

### Task 1: Rewrite capture.md with platform-aware capture

**Files:**
- Modify: `skills/godot-task/capture.md` (full rewrite)

- [ ] **Step 1: Read current capture.md**

Read `skills/godot-task/capture.md` to confirm current content matches expectations.

- [ ] **Step 2: Rewrite capture.md with platform detection**

Replace the entire file with the platform-aware version. Key changes:

1. Add a new `## Platform Detection` section before GPU Detection:

```markdown
## Platform Detection

Run once per session to set platform-specific variables:
```bash
PLATFORM=$(uname -s)  # Darwin or Linux

# Timeout command — GNU timeout not available on macOS by default
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout"
else
    # POSIX fallback for macOS without coreutils
    timeout_fallback() { perl -e "alarm $1; exec @ARGV[1..$#ARGV]" -- "$@"; }
    TIMEOUT_CMD="timeout_fallback"
fi
```
```

2. Rename `## GPU Detection` to `## GPU Detection (Linux only)` and wrap it in a platform guard:

```markdown
## GPU Detection (Linux only)

Skip on macOS — Metal rendering is always available natively.

```bash
GPU_DISPLAY=""
if [[ "$PLATFORM" == "Linux" ]]; then
    for lock in /tmp/.X*-lock; do
      d=":${lock##/tmp/.X}"; d="${d%-lock}"
      if DISPLAY=$d $TIMEOUT_CMD 2 glxinfo 2>/dev/null | grep -qi nvidia; then
        GPU_DISPLAY=$d; break
      fi
    done
fi
```
```

3. Rewrite `## Screenshot Capture` with three paths — macOS, Linux GPU, Linux software:

```markdown
## Screenshot Capture

```bash
MOVIE=screenshots/{task_folder}
rm -rf $MOVIE && mkdir -p $MOVIE
touch screenshots/.gdignore
if [[ "$PLATFORM" == "Darwin" ]]; then
    # macOS — Metal rendering, no display server needed
    $TIMEOUT_CMD 30 godot --rendering-method forward_plus \
        --write-movie $MOVIE/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
elif [[ -n "$GPU_DISPLAY" ]]; then
    # Linux with GPU
    $TIMEOUT_CMD 30 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
        --write-movie $MOVIE/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
else
    # Linux software rendering (lavapipe)
    $TIMEOUT_CMD 30 xvfb-run -a -s '-screen 0 1280x720x24' godot --rendering-driver vulkan \
        --write-movie $MOVIE/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
fi
```
```

4. Rewrite `## Video Capture` with platform-aware gate:

```markdown
## Video Capture

Video capture requires hardware rendering — macOS (Metal) or Linux with GPU. Software rendering is too slow.

```bash
if [[ "$PLATFORM" == "Darwin" ]] || [[ -n "$GPU_DISPLAY" ]]; then
    VIDEO=screenshots/presentation
    rm -rf $VIDEO && mkdir -p $VIDEO
    touch screenshots/.gdignore
    if [[ "$PLATFORM" == "Darwin" ]]; then
        $TIMEOUT_CMD 60 godot --rendering-method forward_plus \
            --write-movie $VIDEO/output.avi \
            --fixed-fps 30 --quit-after 900 \
            --script test/presentation.gd 2>&1
    else
        $TIMEOUT_CMD 60 DISPLAY=$GPU_DISPLAY godot --rendering-method forward_plus \
            --write-movie $VIDEO/output.avi \
            --fixed-fps 30 --quit-after 900 \
            --script test/presentation.gd 2>&1
    fi
    # Convert AVI (MJPEG) to MP4 (H.264)
    ffmpeg -i $VIDEO/output.avi \
        -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow \
        -vf "scale='min(1280,iw)':-2" \
        -movflags +faststart \
        $VIDEO/gameplay.mp4 2>&1
else
    echo "No GPU available — skipping video capture"
fi
```
```

5. Keep the `### Frame Rate and Duration` section and the `**AVI to MP4:**` note unchanged.

- [ ] **Step 3: Verify the rewrite**

Read the rewritten file end-to-end. Confirm:
- Platform detection section exists at the top
- GPU detection is Linux-only
- Screenshot capture has macOS/Linux-GPU/Linux-software paths
- Video capture uses platform-aware gate, not just `$GPU_DISPLAY`
- Frame rate and AVI-to-MP4 sections preserved
- `$TIMEOUT_CMD` used everywhere instead of bare `timeout`

- [ ] **Step 4: Commit**

```bash
git add skills/godot-task/capture.md
git commit -m "feat: platform-aware capture with macOS Metal support"
```

### Task 2: Update README.md for macOS support

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current README.md**

Read `README.md` to find the prerequisites section and the macOS caveat.

- [ ] **Step 2: Update prerequisites**

In the `### Prerequisites` section, after the existing bullet list, add macOS-specific notes:

```markdown
- **macOS additional:**
  - `brew install coreutils` (provides `gtimeout`) — or the capture script uses a perl-based fallback
  - `brew install ffmpeg` — needed for AVI-to-MP4 video conversion
  - Godot 4 must be on `PATH` (symlink from `Godot.app/Contents/MacOS/Godot` or install via Homebrew)
```

- [ ] **Step 3: Remove macOS untested caveat**

Replace the line:
```
- Tested on Ubuntu and Debian. macOS is untested — screenshot capture depends on X11/xvfb/Vulkan and will need a native capture path to work.
```

With:
```
- Tested on Ubuntu, Debian, and macOS. Linux uses X11/xvfb/Vulkan; macOS uses Metal natively.
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add macOS support to prerequisites, remove untested caveat"
```

---

## Chunk 2: Phase 2 — Reliability Hardening (GDScript)

### Task 3: Add pre-validation gate and structured error recovery to godot-task SKILL.md

**Files:**
- Modify: `skills/godot-task/SKILL.md`

- [ ] **Step 1: Read current SKILL.md**

Read `skills/godot-task/SKILL.md` to find the workflow section.

- [ ] **Step 2: Add pre-validation step to workflow**

In the `## Workflow` section, between step 4 ("Generate script(s)") and step 5 ("Validate"), insert a new step:

```markdown
5. **Pre-validate scripts** — for each newly written or modified `.gd` file, run `timeout 30 godot --headless --quit 2>&1` and filter the output for errors mentioning that file's path. This catches compilation errors in isolation before scene building or full project validation muddies the signal.
```

Renumber subsequent steps (old 5 becomes 6, etc.). Also update the `## Iteration Tracking` section's step range from "Steps 3-10" to "Steps 3-11" to account for the inserted step.

- [ ] **Step 3: Add structured error recovery section**

After the `**Error handling:**` block in the `## Commands` section, add:

```markdown
**Structured error recovery:** When a compilation error is caught:
1. Parse the error — extract the file path, line number, and error type from Godot's output
2. Look up the class — if the error mentions an unknown method or property, read `doc_api/{ClassName}.md` for the class involved
3. Check quirks — cross-reference against `quirks.md` for known patterns (`:=` with `instantiate()`, polymorphic math functions, Camera2D `current`, etc.)
4. Fix and re-validate — edit the specific file, then re-run the pre-validation step on that file only before proceeding
```

- [ ] **Step 4: Verify changes**

Read the modified file. Confirm the new step is correctly numbered and the error recovery section is in the right place.

- [ ] **Step 5: Commit**

```bash
git add skills/godot-task/SKILL.md
git commit -m "feat: add pre-validation gate and structured error recovery to task executor"
```

### Task 4: Add scene verification template and ownership validation to scene-generation.md

**Files:**
- Modify: `skills/godot-task/scene-generation.md`

- [ ] **Step 1: Read current scene-generation.md**

Read `skills/godot-task/scene-generation.md` to find the Scene Template section and the ownership chain section.

- [ ] **Step 2: Add node count emission to the scene template**

In the `## Scene Template` section, before the `quit(0)` line in the template, add:

```gdscript
    # Count nodes for verification
    var count := _count_nodes(root)
    print("BUILT: %d nodes" % count)
    print("Saved: res://{output_path}.tscn")
    quit(0)

func _count_nodes(node: Node) -> int:
    var total := 1
    for child in node.get_children():
        total += _count_nodes(child)
    return total
```

- [ ] **Step 3: Add post-save verification section**

After the `## Scene Template` section, add a new section:

```markdown
## Post-Save Verification

After running a scene builder, verify the saved `.tscn` by writing and running a verification script. The builder's stdout includes `BUILT: N nodes` — use this expected count.

Write `scenes/verify_scene.gd` into the project:

```gdscript
extends SceneTree

func _initialize() -> void:
    var args := OS.get_cmdline_user_args()
    if args.size() < 2:
        push_error("Usage: verify_scene.gd -- <scene_path> <expected_nodes>")
        quit(1)
        return

    var scene_path: String = args[0]
    var expected_nodes: int = int(args[1])

    var packed = load(scene_path)
    if packed == null:
        print("VERIFY FAIL: could not load %s" % scene_path)
        quit(1)
        return

    var instance = packed.instantiate()
    if instance == null:
        print("VERIFY FAIL: could not instantiate %s" % scene_path)
        quit(1)
        return

    var actual_nodes := _count_nodes(instance)
    instance.free()

    # Check file size for GLB inlining
    var file := FileAccess.open(scene_path.replace("res://", ""), FileAccess.READ)
    var file_size_mb := 0.0
    if file:
        file_size_mb = file.get_length() / 1048576.0
        file.close()

    var size_threshold := 5.0  # MB — adjust to 1.0 for 2D scenes
    if file_size_mb > size_threshold:
        print("VERIFY WARN: %s is %.1f MB — possible GLB inlining" % [scene_path, file_size_mb])

    if actual_nodes < expected_nodes:
        print("VERIFY FAIL: expected %d nodes, got %d in %s" % [expected_nodes, actual_nodes, scene_path])
        quit(1)
        return

    print("VERIFY PASS: %d nodes in %s (%.1f MB)" % [actual_nodes, scene_path, file_size_mb])
    quit(0)

func _count_nodes(node: Node) -> int:
    var total := 1
    for child in node.get_children():
        total += _count_nodes(child)
    return total
```

Run after each scene builder:
```bash
timeout 30 godot --headless --script scenes/verify_scene.gd -- res://scenes/{name}.tscn {expected_count}
```

Parse `BUILT: N nodes` from the scene builder's stdout to get `{expected_count}`.
```

- [ ] **Step 4: Add ownership chain validation function**

In the `## Owner Chain (CRITICAL)` section, after the existing `set_owner_on_new_nodes` function, add:

```markdown
### Post-Pack Validation

Call after `packed.pack(root)` to verify no nodes were silently dropped:

```gdscript
func validate_packed_scene(packed: PackedScene, expected_count: int, scene_path: String) -> bool:
    var test_instance = packed.instantiate()
    var actual := _count_nodes(test_instance)
    test_instance.free()
    if actual < expected_count:
        push_error("Pack validation failed for %s: expected %d nodes, got %d — nodes were dropped during serialization" % [scene_path, expected_count, actual])
        return false
    return true
```

Use in the scene template between `packed.pack(root)` and `ResourceSaver.save()`. **Gate the save on the validation result:**
```gdscript
    var count := _count_nodes(root)
    var err := packed.pack(root)
    if err != OK:
        push_error("Pack failed: " + str(err))
        quit(1)
        return
    if not validate_packed_scene(packed, count, "res://{output_path}.tscn"):
        quit(1)
        return
```
```

- [ ] **Step 5: Verify changes**

Read the modified file. Confirm:
- Scene template emits `BUILT: N nodes`
- Post-save verification section has complete `verify_scene.gd` template
- Ownership validation function exists and is wired into the template

- [ ] **Step 6: Commit**

```bash
git add skills/godot-task/scene-generation.md
git commit -m "feat: add scene verification template and ownership chain validation"
```

### Task 4b: Expand quirks.md with common failure patterns

**Files:**
- Modify: `skills/godot-task/quirks.md`

- [ ] **Step 1: Read current quirks.md**

Read `skills/godot-task/quirks.md` to understand existing entries and format.

- [ ] **Step 2: Add new quirk entries**

Add the following entries to the end of the file (before any closing sections), following the existing format of `- **title** — description`:

```markdown
## Feedback Loop

Quirks are curated manually in this file (skill source repo). When the task executor discovers a workaround during a game build, it writes to `MEMORY.md` (project-level). The skill maintainer periodically reviews `MEMORY.md` entries across projects and promotes recurring patterns here. This is a manual curation step — do not modify this file from within a game project.
```

Review the existing quirks and ensure no duplicates. Add any additional patterns discovered from recent pipeline runs.

- [ ] **Step 3: Commit**

```bash
git add skills/godot-task/quirks.md
git commit -m "feat: expand quirks.md and document feedback loop from MEMORY.md"
```

### Task 5: Add build order to scaffold.md

**Files:**
- Modify: `skills/godogen/scaffold.md`

- [ ] **Step 1: Read current scaffold.md**

Read `skills/godogen/scaffold.md` to find the STRUCTURE.md output section.

- [ ] **Step 2: Add Build Order section to STRUCTURE.md template**

In the `### 2. STRUCTURE.md` section, after the `## Asset Hints` example, add:

```markdown
## Build Order

Emit an explicit build order based on scene dependency analysis. Leaf scenes (no child scene references) first, parents after:

```markdown
## Build Order
1. scenes/build_player.gd → scenes/player.tscn
2. scenes/build_enemy.gd → scenes/enemy.tscn
3. scenes/build_main.gd → scenes/main.tscn (depends: player.tscn, enemy.tscn)
```

The task executor follows this order mechanically. Do not rely on the executor to infer dependencies.
```

- [ ] **Step 3: Update the existing build order note in scene builder stubs**

In the `### 5. Scene builder stubs` section, replace the existing `**CRITICAL: Build order matters.**` paragraph with:

```markdown
**CRITICAL: Build order is specified in STRUCTURE.md.** The `## Build Order` section lists the exact sequence. Follow it mechanically — do not infer or reorder.
```

- [ ] **Step 4: Commit**

```bash
git add skills/godogen/scaffold.md
git commit -m "feat: emit explicit build order in STRUCTURE.md from scaffold"
```

### Task 6: Update coordination.md to reference build order

**Files:**
- Modify: `skills/godot-task/coordination.md`

- [ ] **Step 1: Read current coordination.md**

Read `skills/godot-task/coordination.md`.

- [ ] **Step 2: Add build order reference**

After the existing step 1 ("Generate scenes first"), add:

```markdown
1b. **Follow the build order** — `STRUCTURE.md` contains a `## Build Order` section listing the exact sequence of scene builder executions. Follow this order mechanically instead of inferring dependencies from scene references.
```

- [ ] **Step 3: Commit**

```bash
git add skills/godot-task/coordination.md
git commit -m "feat: reference STRUCTURE.md build order in coordination guide"
```

---

## Chunk 3: Phase 3a — Audio Support

### Task 7: Add audio subcommand to asset_gen.py

**Files:**
- Modify: `skills/godogen/tools/asset_gen.py`
- Modify: `skills/godogen/tools/requirements.txt`

- [ ] **Step 1: Read current asset_gen.py**

Read the full `skills/godogen/tools/asset_gen.py` to understand the existing subcommand pattern (image, spritesheet, glb, set_budget).

- [ ] **Step 2: Add audio generation function**

Add a new function `cmd_audio(args)` following the same pattern as `cmd_image`. Start with Gemini as the primary backend:

```python
def cmd_audio(args):
    """Generate audio from a text prompt via configured backend."""
    if args.backend != "gemini":
        result_json(False, error=f"Backend '{args.backend}' not yet implemented. Only 'gemini' is currently supported.")
        sys.exit(1)

    cost = 3  # cents for Gemini audio
    check_budget(cost)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Include duration hint in the prompt
    prompt = f"{args.prompt}. Duration: approximately {args.duration} seconds."

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
        ),
    )

    # Null-check response (mirrors cmd_image pattern)
    if not response.candidates or not response.candidates[0].content.parts:
        reason = getattr(response.candidates[0], "finish_reason", "unknown") if response.candidates else "no candidates"
        result_json(False, error=f"Audio generation failed: {reason}")
        sys.exit(1)

    # Extract audio data from response
    audio_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
            audio_data = part.inline_data.data
            break

    if audio_data is None:
        result_json(False, error="No audio data in response")
        sys.exit(1)

    # Write raw audio, then convert to OGG via ffmpeg
    tmp_path = output.with_suffix(".tmp.wav")
    tmp_path.write_bytes(audio_data)

    import subprocess
    ret = subprocess.run(
        ["ffmpeg", "-y", "-i", str(tmp_path), "-c:a", "libvorbis", "-q:a", "4", str(output)],
        capture_output=True, text=True,
    )
    tmp_path.unlink(missing_ok=True)

    if ret.returncode != 0:
        result_json(False, error=f"ffmpeg conversion failed: {ret.stderr[:200]}")
        sys.exit(1)

    record_spend(cost, "gemini_audio")
    result_json(True, path=str(output), cost_cents=cost)
```

- [ ] **Step 3: Add audio subparser to argparse**

In the argument parser setup, add:

```python
p_audio = sub.add_parser("audio", help="Generate audio from prompt")
p_audio.add_argument("--prompt", required=True)
p_audio.add_argument("--backend", default="gemini", choices=["gemini", "local", "elevenlabs", "suno"])
p_audio.add_argument("--duration", type=float, default=2.0, help="Target duration in seconds")
p_audio.add_argument("-o", "--output", required=True)
p_audio.set_defaults(func=cmd_audio)
```

- [ ] **Step 4: Update requirements.txt**

Read `skills/godogen/tools/requirements.txt`, then add `pydub` if not already present (needed for local backend in future iterations).

- [ ] **Step 5: Verify the changes compile**

Read the modified `asset_gen.py` end-to-end. Confirm:
- `cmd_audio` function exists with Gemini backend
- Audio subparser is registered
- OGG conversion via ffmpeg is present
- Budget check and record_spend are called

- [ ] **Step 6: Commit**

```bash
git add skills/godogen/tools/asset_gen.py skills/godogen/tools/requirements.txt
git commit -m "feat: add audio generation subcommand to asset_gen.py (Gemini backend)"
```

### Task 8: Add audio to asset-gen.md CLI reference

**Files:**
- Modify: `skills/godogen/asset-gen.md`

- [ ] **Step 1: Read current asset-gen.md**

Read `skills/godogen/asset-gen.md` to find the CLI Reference and Cost Table sections.

- [ ] **Step 2: Add audio CLI section**

After the `### Convert image to GLB` section, add:

```markdown
### Generate audio (3-10 cents)

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py audio \
  --prompt "metallic sword clash, short impact" \
  --backend gemini -o assets/audio/sfx/sword_hit.ogg
```

`--backend` (default `gemini`): `gemini` (3c), `local` (0c, basic synthesis), `elevenlabs` (5c), `suno` (10c, music)
`--duration` (default `2.0`): target duration in seconds

Output is always `.ogg` (OGG Vorbis) — the standard format for Godot audio. If the backend produces a different format, ffmpeg converts automatically.

**Backend selection:** Start with `gemini` (cheapest API integration, already connected). Use `local` for zero-cost basic effects (tones, noise). Use `elevenlabs` or `suno` for premium quality when budget allows.
```

- [ ] **Step 3: Add audio rows to cost table**

In the `## Cost Table`, add:

```markdown
| Audio SFX | gemini | 3 cents | OGG output, good quality |
| Audio SFX | elevenlabs | 5 cents | High quality |
| Audio SFX | local | 0 cents | Procedural synthesis, basic |
| Audio music | suno | 10 cents | 30s loop, high quality |
| Audio music | local (MusicGen) | 0 cents | Requires GPU |
```

- [ ] **Step 4: Commit**

```bash
git add skills/godogen/asset-gen.md
git commit -m "docs: add audio CLI reference and cost table to asset-gen.md"
```

### Task 9: Add audio planning to asset-planner.md and decomposer.md

**Files:**
- Modify: `skills/godogen/asset-planner.md`
- Modify: `skills/godogen/decomposer.md`

- [ ] **Step 1: Read current asset-planner.md**

Read `skills/godogen/asset-planner.md` to find the ASSETS.md output format section.

- [ ] **Step 2: Add audio planning workflow**

In the `### 1. Analyze inputs` section, add to the bullet list:

```markdown
- **Audio**: sound effects for gameplay events, background music loops, ambient sounds — determine what sounds are needed for game feel
```

In the `### 2. Prioritize and budget` section, add audio to the cost list:

```markdown
- Audio SFX: 3 cents (Gemini) or 0 cents (local synthesis)
- Audio music loop: 10 cents (Suno) or 0 cents (local MusicGen, requires GPU)
```

- [ ] **Step 3: Add audio tables to ASSETS.md template**

In the `### 5. Write ASSETS.md` section, after the `## Sprites` table, add:

```markdown
## Sound Effects

| Name | Description | Duration | File |
|------|-------------|----------|------|
| jump | springy jump launch | 0.3s | assets/audio/sfx/jump.ogg |
| hit | blunt impact | 0.2s | assets/audio/sfx/hit.ogg |

## Music

| Name | Description | Duration | Loop | File |
|------|-------------|----------|------|------|
| gameplay_loop | upbeat chiptune loop | 30s | yes | assets/audio/music/gameplay.ogg |
```

- [ ] **Step 4: Add Audio needed field to decomposer.md**

Read `skills/godogen/decomposer.md`. In the `## Output Format` section, add `**Audio needed:**` to the task template:

```markdown
- **Audio needed:** {What sounds this task needs — SFX triggers, music, ambient. Omit if task needs no audio.}
```

Add it after the `**Assets needed:**` field. Also add a note to `### Task Fields`:

```markdown
- **Audio needed** — sound effects and music this task requires, described by trigger event and character. Omit for tasks that don't involve audio. The asset planner reads these and generates the actual files.
```

- [ ] **Step 5: Commit**

```bash
git add skills/godogen/asset-planner.md skills/godogen/decomposer.md
git commit -m "feat: add audio planning to asset planner and decomposer"
```

### Task 10: Add audio patterns to script-generation.md and scene-generation.md

**Files:**
- Modify: `skills/godot-task/script-generation.md`
- Modify: `skills/godot-task/scene-generation.md`

- [ ] **Step 1: Read current script-generation.md**

Read `skills/godot-task/script-generation.md`.

- [ ] **Step 2: Add audio patterns to script-generation.md**

After the `## VehicleBody3D` section, add:

```markdown
## Audio Playback

**SFX (one-shot):**
```gdscript
# AudioStreamPlayer as child of the emitting node
@onready var sfx_jump: AudioStreamPlayer = $SfxJump

func _on_jumped() -> void:
    sfx_jump.play()
```

**Music (looping):**
```gdscript
# AudioStreamPlayer for background music — typically on main scene or autoload
@onready var music: AudioStreamPlayer = $Music

func _ready() -> void:
    music.play()

# Crossfade between tracks:
func crossfade_to(stream: AudioStream, duration: float = 1.0) -> void:
    var tween := create_tween()
    tween.tween_property(music, ^"volume_db", -40.0, duration * 0.5)
    tween.tween_callback(func():
        music.stream = stream
        music.play()
    )
    tween.tween_property(music, ^"volume_db", 0.0, duration * 0.5)
```

**Spatial audio (3D):**
```gdscript
# AudioStreamPlayer3D positioned on the sound source
@onready var engine_sound: AudioStreamPlayer3D = $EngineSound

func _physics_process(delta: float) -> void:
    # Pitch based on speed
    var pitch: float = clampf(speed / max_speed * 1.5 + 0.5, 0.5, 2.0)
    engine_sound.pitch_scale = pitch
```
```

- [ ] **Step 3: Add audio node patterns to scene-generation.md**

Read `skills/godot-task/scene-generation.md`. After the `## CSG for Rapid Prototyping` section, add:

```markdown
## Audio Nodes

**SFX player (attach to emitting node):**
```gdscript
var sfx := AudioStreamPlayer.new()
sfx.name = "SfxJump"
sfx.stream = load("res://assets/audio/sfx/jump.ogg")
sfx.bus = &"SFX"  # Optional: route to SFX bus
player.add_child(sfx)
```

**Music player (on main scene):**
```gdscript
var music := AudioStreamPlayer.new()
music.name = "Music"
music.stream = load("res://assets/audio/music/gameplay.ogg")
music.autoplay = true
# Set looping via the stream resource (safe cast):
var stream := music.stream as AudioStreamOGGVorbis
if stream:
    stream.loop = true
root.add_child(music)
```

**3D spatial audio:**
```gdscript
var engine := AudioStreamPlayer3D.new()
engine.name = "EngineSound"
engine.stream = load("res://assets/audio/sfx/engine.ogg")
engine.max_distance = 50.0
engine.autoplay = true
vehicle.add_child(engine)
```
```

- [ ] **Step 4: Commit**

```bash
git add skills/godot-task/script-generation.md skills/godot-task/scene-generation.md
git commit -m "feat: add audio playback and audio node patterns to task executor"
```

### Task 11: Add AudioManager autoload pattern to scaffold.md

**Files:**
- Modify: `skills/godogen/scaffold.md`

- [ ] **Step 1: Read current scaffold.md**

Read `skills/godogen/scaffold.md` to find the autoload section in the project.godot template.

- [ ] **Step 2: Add AudioManager pattern**

After the `## UI Overlay Architecture` section, add:

```markdown
## Audio Architecture

When the game needs audio, add an AudioManager autoload:

**In `project.godot`:**
```ini
[autoload]
AudioManager="*res://scripts/audio_manager.gd"
```

**Script stub `scripts/audio_manager.gd`:**
```gdscript
extends Node
## Singleton: manages music playback and SFX pooling

var _music_player: AudioStreamPlayer
var _sfx_pool: Array[AudioStreamPlayer] = []
const SFX_POOL_SIZE := 8

func _ready() -> void:
    _music_player = AudioStreamPlayer.new()
    _music_player.bus = &"Music"
    add_child(_music_player)
    for i in range(SFX_POOL_SIZE):
        var p := AudioStreamPlayer.new()
        p.bus = &"SFX"
        add_child(p)
        _sfx_pool.append(p)

func play_music(stream: AudioStream, loop: bool = true) -> void:
    _music_player.stream = stream
    if stream is AudioStreamOGGVorbis:
        stream.loop = loop
    _music_player.play()

func play_sfx(stream: AudioStream) -> void:
    for p in _sfx_pool:
        if not p.playing:
            p.stream = stream
            p.play()
            return
```

The scaffold also creates audio directories and audio buses. Add to the scaffold workflow after step 7 ("Write script stubs"):

```markdown
7b. **Create audio directories** (when game needs audio):
    ```bash
    mkdir -p assets/audio/sfx assets/audio/music
    ```
```

**Audio bus note:** The `&"SFX"` and `&"Music"` buses referenced in AudioManager are optional. Godot falls back to "Master" if they don't exist. If per-bus volume control is needed, the scaffold creates a `default_bus_layout.tres` — but for most projects, the Master bus suffices and bus creation can be skipped.
```

- [ ] **Step 3: Add audio to STRUCTURE.md template**

In the `### 2. STRUCTURE.md` section, add an example audio entry in the Scripts section:

```markdown
### AudioManager
- **File:** res://scripts/audio_manager.gd
- **Extends:** Node
- **Autoload:** yes
- **Purpose:** Music playback, SFX pooling
```

- [ ] **Step 4: Commit**

```bash
git add skills/godogen/scaffold.md
git commit -m "feat: add AudioManager autoload pattern and audio directory creation to scaffold"
```

---

## Chunk 4: Phase 3b — C# Support

### Task 11b: Proof-of-concept — set_script() with .cs paths from GDScript builder

**Files:**
- None (manual validation task)

This is a **prerequisite gate** for the rest of Chunk 4. The result determines the script attachment strategy.

- [ ] **Step 1: Create a minimal test project**

In a temporary directory, create a minimal Godot .NET project:
- `project.godot` with basic config
- `scripts/TestScript.cs` — a simple `public partial class TestScript : Node { public override void _Ready() { GD.Print("C# script attached"); } }`
- Run `godot --headless --quit` to generate `.csproj`/`.sln`
- Run `dotnet build`

- [ ] **Step 2: Write a GDScript scene builder that attaches the C# script**

```gdscript
extends SceneTree
func _initialize() -> void:
    var root := Node.new()
    root.name = "TestRoot"
    root.set_script(load("res://scripts/TestScript.cs"))
    var packed := PackedScene.new()
    packed.pack(root)
    ResourceSaver.save(packed, "res://scenes/test.tscn")
    quit(0)
```

Run: `godot --headless --script scenes/build_test.gd`

- [ ] **Step 3: Evaluate result**

- **If it works:** `set_script(load("res://scripts/Foo.cs"))` is the strategy. Proceed with Tasks 12-16 as written.
- **If it fails:** Adopt Fallback A from the spec — scene builders save `.tscn` without script attachments, and a post-build text replacement step patches `.tscn` files to add `[ext_resource type="Script" path="res://scripts/Foo.cs"]` references. Document this in `scene-generation.md`.

- [ ] **Step 4: Document the result**

Add a note to the top of `skills/godot-task/scene-generation.md` under a new `## C# Script Attachment` section documenting which strategy works and how to use it.

- [ ] **Step 5: Commit**

```bash
git add skills/godot-task/scene-generation.md
git commit -m "feat: document C# script attachment strategy (PoC validated)"
```

### Task 12: Write csharp.md reference

**Files:**
- Create: `skills/godot-task/csharp.md`

- [ ] **Step 1: Write the C# + Godot .NET reference**

Create `skills/godot-task/csharp.md` covering:

1. **GDScript → C# mapping** — the essential translations:
   - `extends Node` → `public partial class MyClass : Node`
   - `@export var` → `[Export] public type Name { get; set; }`
   - `@onready var x = $Node` → `private Type _x; public override void _Ready() { _x = GetNode<Type>("Node"); }`
   - `signal my_signal` → `[Signal] public delegate void MySignalEventHandler();`
   - `my_signal.emit()` → `EmitSignal(SignalName.MySignal);`
   - `func _process(delta)` → `public override void _Process(double delta)`
   - `func _physics_process(delta)` → `public override void _PhysicsProcess(double delta)`

2. **Lifecycle methods** — `_Ready()`, `_Process()`, `_PhysicsProcess()`, `_Input()`, `_EnterTree()`, `_ExitTree()`

3. **Node references** — `GetNode<T>()`, `GetNodeOrNull<T>()`, `GetParent<T>()`, `GetTree()`

4. **Signal connections:**
```csharp
button.Pressed += OnButtonPressed;
// or
button.Connect("pressed", new Callable(this, nameof(OnButtonPressed)));
```

5. **Input handling:**
```csharp
Input.IsActionPressed("move_forward")
Input.GetAxis("move_left", "move_right")
Input.GetVector("left", "right", "up", "down")
```

6. **Common patterns** — timers, tweens, scene instantiation, groups

7. **Key differences from GDScript:**
   - `partial class` is mandatory for all Godot classes
   - `GD.Print()` for Godot console, not `Console.WriteLine()`
   - Properties use PascalCase (`Position`, `Rotation`, `Velocity`)
   - Methods use PascalCase (`MoveAndSlide()`, `LookAt()`)
   - Enums accessed via class: `CharacterBody3D.MotionModeEnum.Floating`

- [ ] **Step 2: Verify completeness**

Read the written file. Confirm it covers all the patterns from `gdscript.md` that have C# equivalents.

- [ ] **Step 3: Commit**

```bash
git add skills/godot-task/csharp.md
git commit -m "feat: add C# + Godot .NET reference for task executor"
```

### Task 13: Write script-generation-csharp.md

**Files:**
- Create: `skills/godot-task/script-generation-csharp.md`

- [ ] **Step 1: Write the C# script generation guide**

Create `skills/godot-task/script-generation-csharp.md` mirroring the structure of `script-generation.md` but for C#:

```markdown
# C# Script Generation

Runtime scripts in C# define node behavior. They attach to nodes in scenes and run when the game plays.

## Script Output Requirements

Generate a `.cs` file that:
1. `public partial class ClassName : NodeType` matching the node it attaches to
2. Uses proper Godot lifecycle methods (`_Ready`, `_Process`, `_PhysicsProcess`)
3. References sibling/child nodes via `GetNode<T>()` in `_Ready()`
4. Defines signals with `[Signal]` delegate pattern

## Script Template

```csharp
using Godot;

public partial class PlayerController : CharacterBody3D
{
    // Signals
    [Signal] public delegate void HealthChangedEventHandler(int newValue);
    [Signal] public delegate void DiedEventHandler();

    // Exports
    [Export] public float Speed { get; set; } = 100.0f;
    [Export(PropertyHint.Range, "0,100")] public int Health { get; set; } = 100;

    // Node references (resolved in _Ready)
    private MeshInstance3D _mesh;
    private CollisionShape3D _collision;

    // State
    private int _currentHealth;

    public override void _Ready()
    {
        _mesh = GetNode<MeshInstance3D>("MeshInstance3D");
        _collision = GetNode<CollisionShape3D>("CollisionShape3D");
        _currentHealth = Health;
    }

    public override void _PhysicsProcess(double delta)
    {
    }
}
```

## Script Constraints

- `partial class` is MANDATORY for all Godot C# classes
- `extends` equivalent is `: BaseType` — must match the node type
- Use `GetNode<T>()` in `_Ready()`, NOT field initializers
- Connect signals in `_Ready()`, not in scene builders
- Use `GD.Print()` for Godot console output, NOT `Console.WriteLine()`
- All Godot API methods and properties use PascalCase
- Validate via `dotnet build` — MSBuild errors are more structured than Godot GDScript errors
```

- [ ] **Step 2: Commit**

```bash
git add skills/godot-task/script-generation-csharp.md
git commit -m "feat: add C# script generation guide for task executor"
```

### Task 14: Write quirks-csharp.md

**Files:**
- Create: `skills/godot-task/quirks-csharp.md`

- [ ] **Step 1: Write the C#-specific quirks file**

Create `skills/godot-task/quirks-csharp.md`:

```markdown
# C# Quirks (Godot .NET)

- **`partial class` is mandatory** — every class that extends a Godot type MUST be `partial`. Without it, signal delegates and export properties fail silently or produce cryptic build errors.
- **`GD.Print()` not `Console.WriteLine()`** — `Console.WriteLine()` writes to the system console, not Godot's output panel. Use `GD.Print()` for all game output.
- **PascalCase for all Godot API** — `Position` not `position`, `MoveAndSlide()` not `move_and_slide()`, `GlobalPosition` not `global_position`. This applies to properties, methods, signals, and enums.
- **Signal delegate naming** — must end with `EventHandler`. `[Signal] public delegate void DiedEventHandler();` creates a signal named `Died`. Emit with `EmitSignal(SignalName.Died)`.
- **`dotnet build` before Godot recognizes scripts** — C# scripts exist as compiled DLLs, not interpreted files. After writing or modifying `.cs` files, run `dotnet build` before `godot --headless --quit` or Godot won't see the new scripts.
- **Export property serialization** — `[Export]` properties must have public getters and setters. Auto-properties (`{ get; set; }`) work. Private setters cause silent serialization failures.
- **Nullable reference type warnings** — Godot's generated code triggers NRT warnings. Add `<Nullable>disable</Nullable>` to `.csproj` or use `= null!` for node references resolved in `_Ready()`.
- **`_Ready()` timing with `GetNode()`** — same as GDScript: `GetNode<T>()` fails if called before the node enters the tree. Always use in `_Ready()`, never in constructors or field initializers.
- **Enum access** — Godot enums are nested in their class: `CharacterBody3D.MotionModeEnum.Floating`, not bare `MOTION_MODE_FLOATING`.
- **`Callable` construction** — `new Callable(this, MethodName.MyMethod)` or `new Callable(this, nameof(MyMethod))`. Lambda-based callables: `Callable.From(() => MyMethod())`.
```

- [ ] **Step 2: Commit**

```bash
git add skills/godot-task/quirks-csharp.md
git commit -m "feat: add C# quirks for Godot .NET"
```

### Task 15: Update SKILL.md, coordination.md, and test-harness.md for language awareness

**Files:**
- Modify: `skills/godot-task/SKILL.md`
- Modify: `skills/godot-task/coordination.md`
- Modify: `skills/godot-task/test-harness.md`

- [ ] **Step 1: Add language-aware file loading to SKILL.md**

In the file-loading table at the top of `skills/godot-task/SKILL.md`, add conditional entries:

```markdown
| `csharp.md` | C# + Godot .NET reference | Language is C# and before writing any code |
| `script-generation-csharp.md` | Writing C# runtime scripts | Language is C# and targets include `.cs` |
| `quirks-csharp.md` | C#-specific Godot pitfalls | Language is C# and before writing any code |
```

Add a note after the table:

```markdown
**Language detection:** Read `STRUCTURE.md` for the `## Language:` field. If `C#`, load C#-specific references instead of GDScript equivalents. If `GDScript` or absent, use the default GDScript references.
```

- [ ] **Step 2: Add C# validation to SKILL.md workflow**

In the Validate step, add a language-aware branch:

```markdown
- **GDScript:** `timeout 60 godot --headless --quit 2>&1`
- **C#:** `dotnet build 2>&1` — MSBuild errors are more structured. Parse for `error CS` lines.
```

- [ ] **Step 3: Add C# coordination note**

In `skills/godot-task/coordination.md`, add after the existing step 5:

```markdown
6. **C# projects: build before Godot validation** — after writing `.cs` scripts, run `dotnet build` before any `godot --headless` commands. Godot cannot see C# scripts until they are compiled into the DLL.
```

- [ ] **Step 4: Add test harness language note**

In `skills/godot-task/test-harness.md`, add near the top:

```markdown
**Language note:** Test harnesses are always GDScript (`extends SceneTree`) regardless of the project's scripting language. They are build/test-time tools, not shipped code.
```

- [ ] **Step 5: Commit**

```bash
git add skills/godot-task/SKILL.md skills/godot-task/coordination.md skills/godot-task/test-harness.md
git commit -m "feat: add language-aware loading, C# validation, and test harness note"
```

### Task 16: Update scaffold.md and orchestrator SKILL.md for C# projects

**Files:**
- Modify: `skills/godogen/scaffold.md`
- Modify: `skills/godogen/SKILL.md`
- Modify: `skills/godogen/decomposer.md`

- [ ] **Step 1: Add language field to STRUCTURE.md in scaffold.md**

In `skills/godogen/scaffold.md`, in the `### 2. STRUCTURE.md` template, add after the `## Dimension:` line:

```markdown
## Language: {GDScript or C#}
```

- [ ] **Step 2: Add C# scaffold workflow**

In the `## Workflow` section of `skills/godogen/scaffold.md`, after step 7 (Write script stubs), add:

```markdown
7b. **C# projects only:**
    - Write `.cs` script stubs to `scripts/` instead of `.gd`
    - Run `godot --headless --quit` to auto-generate `.csproj` and `.sln`
    - Run `dotnet restore` to pull NuGet packages
    - Run `dotnet build` to verify compilation
```

Add a C# script stub template:

```markdown
### C# Script Stubs

```csharp
using Godot;

public partial class PlayerController : CharacterBody3D
{
    [Signal] public delegate void DiedEventHandler();

    [Export] public float Speed { get; set; } = 7.0f;

    public override void _Ready()
    {
    }

    public override void _PhysicsProcess(double delta)
    {
    }
}
```
```

- [ ] **Step 3: Add language propagation to orchestrator SKILL.md**

In `skills/godogen/SKILL.md`, in the `## Pipeline` section, after the "Check if PLAN.md exists" block, add:

```markdown
    +- Detect language preference (from user prompt or CLAUDE.md)
    |   +- Default: GDScript
    |   +- If user specifies C#: propagate to all downstream stages
```

- [ ] **Step 4: Add language to decomposer task format**

In `skills/godogen/decomposer.md`, in the task template, the language is inherited from the project level (STRUCTURE.md), not per-task. Add a note:

```markdown
**Language:** Tasks inherit the project language from `STRUCTURE.md`. Do not specify language per-task.
```

- [ ] **Step 5: Update README.md with C# prerequisites**

Add to `README.md` in the prerequisites:

```markdown
- **C# projects additional:**
  - [Godot .NET variant](https://godotengine.org/download/) — the .NET build, not the standard build
  - [.NET SDK 8.0+](https://dotnet.microsoft.com/download) — required for compilation and validation
```

- [ ] **Step 6: Commit**

```bash
git add skills/godogen/scaffold.md skills/godogen/SKILL.md skills/godogen/decomposer.md README.md
git commit -m "feat: add C# project support to scaffold, orchestrator, and decomposer"
```

---

## Execution Notes

- **Phase ordering:** Task 1-2 (macOS) → Task 3-6 (reliability) → Tasks 7-11 and 12-16 (audio and C#, parallelizable)
- **No unit tests:** These are skill definition files (markdown + prompts). Verification is by reading the files and running the pipeline on a test game.
- **Scene builders stay GDScript:** Even for C# projects. The `set_script()` with `.cs` paths requires a proof-of-concept (see spec) before Tasks 12-16 can finalize the scene-generation.md changes.
