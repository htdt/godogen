# Godogen Improvements: macOS Support, Reliability, Audio, and C#

**Date:** 2026-03-21
**Status:** Draft
**Approach:** Platform Abstraction Layer (Approach 1)

## Summary

Improve Godogen across four areas, delivered in three independent phases: macOS screenshot capture support, GDScript/scene builder reliability hardening, audio asset generation, and C# as an alternative scripting language.

## Priorities (user-defined)

1. macOS support — unblock development on the platform the user is actually on
2. Reliability — reduce GDScript compilation errors and scene builder failures
3. Audio + C# — new capabilities as a second wave

---

## Phase 1: macOS Screenshot Capture

### Problem

`capture.md` hardcodes Linux-only GPU detection — scanning `/tmp/.X*-lock` for X11 displays and falling back to `xvfb-run`. On macOS, none of this exists. Godot uses Metal natively and needs no display server workarounds. This makes the entire pipeline Linux-only.

### Design

Replace the GPU detection block in `capture.md` with a platform-aware capture strategy.

**Platform detection:** A `uname -s` check at the top of the capture flow. `Darwin` = macOS, `Linux` = existing behavior.

**macOS capture path:** Godot runs directly — no `DISPLAY` variable, no `xvfb-run`, no `glxinfo`. **Note:** GNU `timeout` is not available by default on macOS. Use `gtimeout` (from `brew install coreutils`) or a POSIX-compatible alternative. The capture commands document both:

```bash
# macOS — gtimeout from coreutils preferred
if command -v gtimeout &>/dev/null; then
    gtimeout 30 godot --write-movie $MOVIE/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
else
    # POSIX fallback — perl alarm-based timeout
    perl -e 'alarm 30; exec @ARGV' -- godot --write-movie $MOVIE/frame.png \
        --fixed-fps 10 --quit-after {N} \
        --script test/test_task.gd 2>&1
fi
```

Metal rendering is the default on macOS Godot builds. `--rendering-method forward_plus` works natively.

**Linux capture path:** Existing GPU detection and xvfb fallback unchanged.

**Video capture:** Currently gated on `$GPU_DISPLAY`. The gate becomes platform-aware:

```bash
if [[ "$(uname -s)" == "Darwin" ]] || [[ -n "$GPU_DISPLAY" ]]; then
    # Video capture available — macOS has Metal, Linux has GPU
else
    # No video capture — software rendering too slow
fi
```

### Prerequisites (macOS-specific)

- `brew install coreutils` (provides `gtimeout`) — or the capture script uses a perl-based fallback
- `ffmpeg` must be installed (`brew install ffmpeg`) — needed for AVI-to-MP4 conversion
- Godot 4 must be on `PATH` (symlinked from `Godot.app/Contents/MacOS/Godot` or installed via Homebrew)

### Files changed

- `skills/godot-task/capture.md` — platform-aware capture commands
- `README.md` — update prerequisites to mention macOS support, remove "macOS is untested" caveat, add macOS-specific prerequisites

### Scope boundary

Only `capture.md` changes. The rest of the pipeline (test harness, visual QA, orchestrator) doesn't need to know which platform captured the screenshots.

---

## Phase 2: Reliability Hardening

### Problem: GDScript Compilation Errors

The task executor writes GDScript that fails to compile — wrong APIs, type inference errors, syntax issues. Errors are caught late (during scene building or full project validation) when the error context is muddled with other concerns.

### Design: Pre-validation Gate

Add a step to the `godot-task` workflow between "Generate script(s)" and "Validate." Before running scene builders or full project validation, validate each newly written `.gd` file individually using `godot --headless --quit`:

```bash
timeout 30 godot --headless --quit 2>&1 | grep -i "error"
```

**Note:** Godot 4.x does not have a `--check-only` flag. The validation uses the existing `--quit` approach but focuses on parsing stderr/stdout for errors specific to the newly written files. To isolate errors to a single file, temporarily comment out other scripts or use the error line/file paths in Godot's output to filter. This isolates compilation errors to the specific file that caused them.

### Design: Structured Error Recovery

Add an explicit error-fix protocol to `godot-task` SKILL.md. When a compilation error is caught:

1. Parse the error line number and error type from Godot's output
2. Read the relevant `doc_api/{ClassName}.md` for the class involved
3. Cross-reference against `quirks.md` (many errors match known quirks like `:=` with `instantiate()`)
4. Fix and re-validate the individual file before proceeding

Currently the workflow says "fix errors, re-run, repeat until clean" but doesn't encode how to diagnose.

### Design: Expanded Quirks

Add new entries to `quirks.md` for recurring failure patterns. **Feedback loop:** Quirks are curated manually in the skill source repo. When the task executor discovers a workaround during a game build, it writes to `MEMORY.md` (project-level). Periodically, the skill maintainer reviews `MEMORY.md` entries across projects and promotes recurring patterns to `quirks.md` in the source. This is a manual curation step, not automated.

### Problem: Scene Builder Failures

Scene builders fail subtly — nodes silently vanish from saved `.tscn` files due to ownership chain bugs, GLB inlining bloats files to 100MB+, and build-order mistakes cause load failures. These are caught late or not at all.

### Design: Post-save Scene Verification

After every scene builder saves a `.tscn`, run a verification pass:

```bash
timeout 30 godot --headless --script scenes/verify_scene.gd -- res://scenes/player.tscn 5
```

A reusable GDScript verification script. **Deployment:** The scene builder itself emits the expected node count as its last stdout line (e.g., `BUILT: 12 nodes`). The task executor then writes `verify_scene.gd` into the project (similar to how scene builders are written into `scenes/`) and invokes it with the scene path and expected count. The verification script:

1. Loads the saved `.tscn` as a `PackedScene`
2. Instantiates it and counts the node tree depth/count
3. Compares against the expected node count from the builder's output
4. Checks file size — if `.tscn` exceeds a threshold (1MB for 2D scenes, 5MB for 3D non-terrain scenes), flags likely GLB inlining
5. Prints `VERIFY PASS` or `VERIFY FAIL: expected 12 nodes, got 3` with details
6. Has explicit error handling for load failures with `quit(1)` in all error paths. Hang protection is external only (the `timeout` wrapper around the Godot invocation)

### Design: Build Order Enforcement

Enhance the scaffold stage to emit an explicit build order in `STRUCTURE.md`:

```markdown
## Build Order
1. scenes/build_player.gd → scenes/player.tscn
2. scenes/build_enemy.gd → scenes/enemy.tscn
3. scenes/build_main.gd → scenes/main.tscn (depends: player.tscn, enemy.tscn)
```

The task executor follows this order mechanically rather than inferring dependencies.

### Design: Ownership Chain Validation

Add a second safety function that runs after `pack()` — a `validate_packed_scene` that instantiates the packed result and verifies no nodes were silently dropped during serialization. If the count doesn't match, the builder reports the specific missing nodes before exiting with an error.

### Files changed

- `skills/godot-task/SKILL.md` — add pre-validation step and structured error recovery to workflow
- `skills/godot-task/quirks.md` — expanded entries
- `skills/godot-task/scene-generation.md` — post-save verification, ownership validation, verify_scene.gd template
- `skills/godot-task/coordination.md` — update ordering guidance to reference build order from STRUCTURE.md
- `skills/godogen/scaffold.md` — emit explicit build order in STRUCTURE.md

---

## Phase 3a: Audio Support

### Problem

Games ship with no sound — no SFX, no music, no ambient audio. Sound is a huge part of game feel and its absence makes Godogen output feel like tech demos.

### Design: Audio Asset Generation

Add a new asset type to the `asset-gen` pipeline with configurable backends:

**Free/open-source:** Local tools — `pydub` for basic SFX synthesis (tones, noise bursts, simple layering), or open-source models like AudioCraft/MusicGen running locally. Zero cost, works offline, lower quality.

**Budget tier:** Gemini audio generation or Replicate-hosted models. Low cost per clip, good quality for SFX.

**Premium tier:** ElevenLabs Sound Effects for SFX, Suno/Udio for music. Best quality, higher cost per asset.

The asset planner recommends a backend based on user preference and budget.

New CLI command in `asset_gen.py`:

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py audio \
  --prompt "metallic sword clash, short impact" \
  --backend local --duration 1.5 -o assets/audio/sfx/sword_hit.wav
```

`--backend` options: `local`, `gemini`, `elevenlabs`, `suno`.

**Implementation strategy:** Start with Gemini as the primary backend (already integrated for images, lowest integration effort). Add other backends iteratively based on quality/cost tradeoffs observed in practice.

### Design: Audio Format Standardization

All backends output `.ogg` (OGG Vorbis) as the standard format for Godot. If a backend produces `.wav` or `.mp3`, `asset_gen.py` converts to `.ogg` via `ffmpeg` before saving. Godot auto-imports `.ogg` files correctly with `AudioStreamOGGVorbis`.

For looping music, the pipeline sets the `loop` property on the imported `AudioStreamOGGVorbis` resource. This is configured in the scene builder when creating `AudioStreamPlayer` nodes, not embedded in the audio file.

### Design: Audio Import Step

After generating audio files, the existing `timeout 60 godot --headless --import` step (already in the pipeline for textures and GLBs) picks up the new `.ogg` files automatically. No separate import step needed — audio files go to `assets/audio/` which is under `res://`, and Godot's importer handles them. The scaffold stage creates `assets/audio/sfx/` and `assets/audio/music/` directories.

### Design: Audio Planning

Extend `asset-planner.md` to include audio in `ASSETS.md`:

```markdown
## Sound Effects
| Name | Description | Duration | File |
|------|-------------|----------|------|
| jump | springy jump launch | 0.3s | assets/audio/sfx/jump.ogg |

## Music
| Name | Description | Duration | Loop | File |
|------|-------------|----------|------|------|
| gameplay_loop | upbeat chiptune loop | 30s | yes | assets/audio/music/gameplay.ogg |
```

The decomposer's task descriptions gain an **Audio needed** field alongside **Assets needed**.

### Design: Audio Integration in Scripts

Add audio patterns to `script-generation.md`:

- **SFX:** `AudioStreamPlayer` child on the emitting node, triggered in signal handlers
- **Music:** `AudioStreamPlayer` as autoload or main scene child, looping
- **Spatial audio (3D):** `AudioStreamPlayer3D` positioned on the sound source

Add audio nodes to scene builder patterns in `scene-generation.md`.

The scaffold stage adds audio nodes to `STRUCTURE.md` and the scene hierarchy. An `AudioManager` autoload is the recommended pattern — a singleton handling music crossfades and SFX pooling.

### Design: Configurable Audio Backend

The audio generation step accepts a backend preference, configured at project setup or runtime:

- User states preference in prompt or `CLAUDE.md` (e.g., "use open-source tools only" or "budget: $2 including audio")
- The asset planner recommends backends per asset based on preference and remaining budget
- `asset_gen.py` routes to the appropriate API

### Design: Audio Cost Table

| Operation | Backend | Cost | Notes |
|-----------|---------|------|-------|
| SFX | local (numpy/scipy procedural synthesis) | 0 cents | Basic tones, noise bursts; pydub for post-processing |
| SFX | gemini | 3 cents | Good quality |
| SFX | elevenlabs | 5 cents | High quality |
| Music loop | local (MusicGen) | 0 cents | Requires GPU |
| Music loop | suno/udio | 10 cents | High quality, 30s |

### Files changed

- `skills/godogen/tools/asset_gen.py` — add `audio` subcommand with backend routing
- `skills/godogen/tools/requirements.txt` — add audio backend dependencies (`pydub`, etc.)
- `skills/godogen/asset-gen.md` — audio CLI reference and cost table
- `skills/godogen/asset-planner.md` — audio planning workflow and ASSETS.md schema
- `skills/godogen/decomposer.md` — **Audio needed** field in task format
- `skills/godot-task/script-generation.md` — audio playback patterns
- `skills/godot-task/scene-generation.md` — audio node composition patterns
- `skills/godogen/scaffold.md` — AudioManager autoload pattern, `assets/audio/` directory creation

---

## Phase 3b: C# Support

### Problem

GDScript is the primary source of compilation failures — thin LLM training data and Python-like-but-not-Python syntax traps. C# is a well-known language that LLMs write reliably, with strong typing that catches errors at compile time.

### Design: Language Selection

The user specifies preferred language when invoking `/godogen` — in the prompt or as a project-level setting in `CLAUDE.md`. Default remains GDScript. The choice propagates via a `## Language: GDScript|C#` field in `STRUCTURE.md`.

### Design: C# Reference Docs

- `csharp.md` — hand-written C# + Godot .NET reference covering: node lifecycle (`_Ready()`, `_Process()`, `_PhysicsProcess()`), `[Signal]` delegates, `GetNode<T>()` patterns, `[Export]` attributes, GodotObject lifecycle, and a GDScript → C# mapping guide.
- No full API doc mirror needed — LLMs know C# well and the Godot .NET API maps 1:1 from GDScript with PascalCase naming.

### Design: Script Generation Path

`script-generation-csharp.md` loaded when language is C#. Key differences from GDScript:

- Scripts are `.cs` files in `scripts/`
- `extends CharacterBody3D` → `public partial class PlayerController : CharacterBody3D`
- `@onready` → `GetNode<T>()` in `_Ready()`
- Signal connections use C# events or `Connect()`
- `.csproj` file generation handled by Godot's `dotnet` integration

### Design: Scene Builders Stay GDScript

Scene builders remain GDScript — they're build-time tools, not shipped code, and are well-tested.

**CRITICAL RISK: C# script attachment from GDScript builders.** The standard approach `set_script(load("res://scripts/Player.cs"))` may not work identically to GDScript loading because C# scripts are compiled into a DLL and resolved via the .NET assembly, not direct file load. **This must be validated with a proof-of-concept before committing to the design.** If `set_script()` with `.cs` paths does not work from headless GDScript:

- **Fallback A:** Scene builders save `.tscn` without script attachments. A post-build step (a small C# script or `dotnet` tool) patches the `.tscn` files to add script references.
- **Fallback B:** Scene builders write placeholder `.gd` stubs that the scaffold replaces with `.cs` references in the `.tscn` text after serialization.

The proof-of-concept is a Phase 3b prerequisite — it determines which script attachment strategy to use.

### Design: Prerequisites

C# support requires:
- **Godot .NET variant** — a separate download from the standard build. The .NET variant runs both GDScript and C#, so it replaces (not supplements) the standard binary. Scene builders in GDScript work fine on the .NET variant.
- **.NET SDK 8.0+** — required for `dotnet build` validation. Godot 4.3+ requires .NET 8.0.
- The scaffold stage runs `godot --headless --quit` on initial project creation to auto-generate the `.csproj` and `.sln` files, then `dotnet restore` to pull NuGet packages.

### Design: Validation

C# projects validate via `dotnet build` instead of `godot --headless --quit`. MSBuild output is more structured and easier to parse. The pre-validation gate from Phase 2 must be language-aware — if Phase 2 ships first with GDScript-only pre-validation, Phase 3b retrofits it to check the language field in `STRUCTURE.md` and route to `dotnet build` for C# projects.

### Design: C# Quirks

A `quirks-csharp.md` for C#-specific Godot pitfalls:

- Partial class requirements
- `GD.Print()` vs `Console.WriteLine()`
- Signal naming conventions
- Export property serialization differences
- C# scripts need a build before the editor recognizes them
- Nullable reference type warnings in Godot context

### Files changed

- `skills/godot-task/SKILL.md` — language-aware file loading (csharp.md vs gdscript.md), test harness stays GDScript
- `skills/godot-task/csharp.md` — new C# + Godot .NET reference
- `skills/godot-task/script-generation-csharp.md` — new C# script generation guide
- `skills/godot-task/quirks-csharp.md` — new C# quirks
- `skills/godot-task/scene-generation.md` — `.cs` script attachment when language is C# (pending PoC validation)
- `skills/godot-task/coordination.md` — C# build step before Godot recognizes scripts
- `skills/godot-task/test-harness.md` — note that test harnesses remain GDScript regardless of project language
- `skills/godogen/scaffold.md` — generate `.csproj`/`.sln`, emit `.cs` stubs, `dotnet restore`, language field in STRUCTURE.md
- `skills/godogen/decomposer.md` — language-aware task descriptions
- `skills/godogen/SKILL.md` — propagate language choice through pipeline
- `README.md` — document .NET Godot variant and .NET SDK 8.0+ as prerequisites for C# projects

---

## Phase Independence

Each phase is independently shippable:

- **Phase 1** (macOS) has no dependency on Phase 2 or 3. No overlapping files.
- **Phase 2** (reliability) has no dependency on Phase 1 or 3.
- **Phase 3a** (audio) and **Phase 3b** (C#) are independent of each other.

**Merge concerns:** Phases 2, 3a, and 3b all modify `SKILL.md`, `scene-generation.md`, `scaffold.md`, and `decomposer.md`. These are additive changes (new sections/steps), not conflicting edits, but concurrent work on the same files requires careful merging. If Phase 2 ships first, Phase 3b must retrofit the pre-validation gate to be language-aware. Recommended sequencing: Phase 1 → Phase 2 → Phase 3a and 3b in parallel.

## Out of Scope

- Animated 3D models (skeletal animation) — separate initiative
- Android/web export — separate initiative
- Bevy Engine exploration — separate initiative
- Migration to Grok for image generation — separate initiative
