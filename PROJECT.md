# Godogen — AI-Powered Game Development Pipeline

## What Is This?

Godogen is a system that turns a sentence into a playable game. You describe what you want — "a 3D snowboarding game with procedural terrain and tricks" — and an AI pipeline designs the architecture, generates the art, writes all the code, tests it visually, and delivers a working Godot project. The entire process runs autonomously, with the human receiving progress updates over Telegram, Slack, or another connected channel.

It is not a game engine, a code generator, or an asset marketplace. It is an autonomous development pipeline, orchestrated by AI, that performs the full creative and engineering process from concept to playable build.

## The Problem

Building a game, even a simple one, requires a rare combination of skills: software architecture, graphics programming, art direction, asset creation, and relentless debugging. The typical indie developer spends weeks wiring up boilerplate before reaching the interesting parts. Prototyping a game idea to see if it's fun takes days or weeks, not minutes.

Large language models can write game code, but they struggle with the full picture: maintaining visual consistency across dozens of assets, debugging spatial bugs that only appear on screen, and coordinating the dozens of interdependent files that make up a real project. Asking an LLM to "make a game" produces impressive demos that fall apart the moment you look closely.

## The Approach

Godogen solves this by decomposing game development into focused stages — art direction, architecture, asset generation, implementation, visual QA — and encoding deep domain expertise into each one. Rather than one monolithic prompt trying to do everything, each stage has focused instructions, clear inputs, and clear outputs. The stages communicate through structured documents, not conversation, which means the system scales without drowning in context.

The system is implemented as three Claude Code skills: **godogen** (the orchestrator and task executor, running the full pipeline in a single 1M-token context window), **godot-api** (Godot class API lookup, forked to avoid loading large docs into the main context), and **visual-qa** (visual quality assurance via Gemini Flash and Claude vision, also forked). The godogen skill loads stage-specific instructions progressively — reading each sub-file only when that pipeline stage begins — so the context window stays focused throughout a multi-stage run.

The key insight: **visual verification closes the loop.** Every piece of work is tested by capturing actual screenshots from the running game and analyzing them with a vision model. This is how a human QA tester works — they look at the screen and say "that's wrong." Godogen does the same thing automatically, catching bugs that would be invisible to text-based analysis: z-fighting, floating objects, broken physics, placeholder textures, and mismatched art styles.

## How It Works

### The Pipeline

The system runs as a sequential pipeline of stages. The godogen skill orchestrates the flow, loading instructions for each stage from a sub-file when it's time to execute that stage.

**1. Visual Target** — Before writing a single line of code, the system generates a reference screenshot — what the final game should look like. This image anchors every decision downstream: the art direction it establishes guides every asset prompt, the camera angle informs the architecture, and the composition sets the bar for visual QA. One image, seven cents, and it defines the entire project's identity.

**2. Decomposition** — The decomposer stage analyzes the game for implementation risks and defines verification criteria. Its philosophy is ruthlessly pragmatic: most game features are routine (movement, UI, spawning, cameras) and should be built together. Only genuinely hard problems — procedural generation, custom physics, ragdolls, complex shaders — get isolated as risk tasks requiring separate verification. The output is `PLAN.md`, which separates risk tasks (features that fail unpredictably and need isolation) from the main build (everything else, implemented in one pass).

**3. Architecture** — The scaffold stage designs the game's technical architecture: scene hierarchy, script responsibilities, signal flow, physics layers, input mapping. It produces a compilable Godot project skeleton — not pseudocode, but real files that Godot can open and validate. It also writes `STRUCTURE.md`, a complete map of what goes where, including an explicit build order for scene builders and asset hints that the next stage uses to plan what to generate.

**4. Asset Generation** — The asset planner stage reads the architecture and task plan, then decides what visual assets the game needs. It works within a cost budget (measured in cents), prioritizing by visual impact: a hero character matters more than a background shrub. Two image backends cover different needs: Gemini (5–15 cents) for references, characters, and anything requiring precise prompt following, and xAI Grok (2 cents) for textures, simple objects, and scenic backgrounds where exact adherence doesn't matter. Selected images are converted to 3D models via Tripo3D. Every asset gets a specific in-game size in the manifest — this prevents the classic mistake of generating a richly detailed texture and then shrinking it to 32 pixels where all that detail becomes noise.

The asset-gen tooling provides sophisticated capabilities: animated sprite generation via xAI Grok video (reference image → pose frame → video → frame extraction → loop trim), image-to-image editing for style consistency across asset families, alpha-channel background removal with multi-signal matting (handling hair, glass, and semi-transparent materials), grid slicing for item kits, and 3D model generation at multiple quality tiers.

**5. Task Execution** — Execution runs inline within the godogen skill's 1M-token context window, not in a forked context. This means the executor has full access to everything that happened during planning — the reference image analysis, the architectural decisions, the asset generation results — without needing to reload it from documents. Execution proceeds in two phases: risk tasks first (each implemented and verified in isolation), then the main build (everything else in one pass). For each phase, the executor:

- Generates scene builder scripts — GDScript programs that run headlessly in Godot to produce `.tscn` scene files programmatically (avoiding the fragility of hand-editing serialized scene formats)
- Writes runtime scripts — the actual game logic
- Pre-validates each script individually, then validates the full project by running Godot in headless mode
- Writes a test harness that loads the scene and exercises the feature
- Captures screenshots from the running game
- Runs automated visual QA via the forked visual-qa skill

The executor loads deep knowledge of Godot's quirks progressively from sub-files: scene generation patterns, engine quirks, capture commands, and visual QA instructions. When it needs to look up a Godot class API, it delegates to the **godot-api** skill — which runs in a forked context with a Sonnet model and the Explore agent, keeping the large API documentation (850+ classes) out of the main context window. This institutional knowledge prevents the class of bugs that waste hours of human debugging time.

Task execution is where the hardest unsolved problem in AI code generation shows up: writing correct code in a language the model barely knows. This is covered in depth below.

### The GDScript Problem

GDScript is not Python, not JavaScript, not any language that LLMs have seen millions of examples of. It's a domain-specific language used by one game engine, with a relatively small corpus of open-source code on the internet. When an LLM writes GDScript, it's working from thin training data — and GDScript has enough surface similarity to Python to make hallucination dangerous. The model confidently writes code that *looks* right but uses APIs that don't exist, patterns that don't work, or type constructs that GDScript's parser rejects.

This is the core technical challenge of Godogen: making an LLM reliably produce correct GDScript for a 850+ class engine API, without the luxury of abundant training examples.

#### Teaching the Language

The solution is a custom-built reference system, split across skills, that gives the executor a complete, token-efficient language specification and API reference on demand.

The first layer is a hand-written GDScript language reference (`gdscript.md`, housed in the godot-api skill) covering everything from type inference rules to signal connection patterns to physics gotchas. This isn't a tutorial — it's written for an expert who needs precise answers fast. It covers the traps that trip up code generators specifically: that `:=` type inference fails on `instantiate()` because it returns Variant, that `abs()` and `clamp()` are polymorphic and need explicit typing, that lambda captures work by reference for collections but by value for primitives. It also encodes game development patterns in GDScript idiom: state machines, spawning, camera rigs, tween chains, navigation — the patterns that an LLM would otherwise approximate from Python or C# examples and get subtly wrong.

The second layer is a complete Godot API reference — all 850+ engine classes — converted from Godot's XML documentation into compact Markdown. A bootstrap script (`ensure_doc_api.sh`) does a sparse git clone of the Godot repository (pulling only the `doc/classes/` directory, not the entire engine source), then a converter transforms each XML class definition into a token-efficient Markdown file: properties, methods, signals, constants, enums, with descriptions trimmed to first sentences.

#### Lazy Two-Tier Lookup

Loading documentation for 850 classes at once would consume the entire context window and leave no room for actual work. So the system isolates API lookup in the **godot-api** skill, which runs in a forked context with its own model (Sonnet) and the Explore agent. Inside that fork, two-tier lazy loading keeps things efficient: a small index file (`_common.md`) lists the ~128 most commonly used classes (nodes, physics bodies, sprites, cameras, UI elements) with one-line descriptions, and a second index (`_other.md`) covers the remaining ~730 classes. The godot-api skill checks the index, loads the full documentation for the specific class needed, and returns a targeted answer — keeping the main pipeline's 1M context window entirely free for reasoning and code generation.

#### Two Kinds of Code

The task executor generates two fundamentally different types of GDScript, and confusing them is a source of bugs that took real iteration to solve.

**Scene builders** are headless programs that construct Godot scenes programmatically. They extend `SceneTree`, run once in Godot's headless mode, build a node hierarchy in memory, serialize it to a `.tscn` file, and exit. They cannot use any runtime features — no `@onready`, no `preload()`, no signal connections, no spatial methods like `look_at()` (the nodes aren't in a live scene tree yet). Their critical job is getting the **ownership chain** right: every node must have its `owner` set to the scene root, or it silently vanishes from the saved file. But ownership must *stop* at instantiated sub-scenes (like imported 3D models), or the serializer inlines their entire internal structure, bloating a scene file from kilobytes to hundreds of megabytes.

**Runtime scripts** are the actual game logic — they extend node types, use the full Godot lifecycle (`_ready()`, `_process()`, `_physics_process()`), connect signals, and respond to input. They're attached to nodes by the scene builders via `set_script()`, but they don't actually execute until the game runs. This timing gap matters: signals must be connected in the runtime script's `_ready()`, not in the scene builder, because the script doesn't exist as a live object during build time.

Getting this build-time/runtime separation clean — what code goes where, what APIs are available when, what state exists at which phase — was one of the harder design problems. An LLM's instinct is to write one script that does everything. The system had to encode strict patterns for which operations belong to which phase.

#### Godot's Quirks as Institutional Knowledge

Beyond the language itself, Godot has engine-level behaviors that are difficult to discover from documentation alone. The task executor encodes dozens of these as explicit rules in `quirks.md`:

- `_ready()` doesn't fire on nodes during a scene builder's `_initialize()` — so initialization that runtime scripts expect from `_ready()` must be triggered manually
- `MultiMeshInstance3D` loses its mesh reference after pack-and-save — a serialization bug that silently produces invisible objects
- Collision state can't be changed inside collision callbacks — requires deferred operations
- Items spawned inside an active `Area2D` trigger `area_entered` on the same frame — requiring spawn immunity timers
- Camera2D has no `current` property despite what intuition (and some documentation) suggests — you must call `make_current()` after the node enters the tree
- High-polygon collision meshes cause single-digit framerates — convex decomposition must be used selectively
- GLB `material_override` doesn't serialize on internal mesh nodes — requires procedural ArrayMesh when custom material is needed
- Camera lerp from origin causes visible swoop on first frame — requires an initialization flag to snap position before lerping
- Frame-rate dependent drag via `(1 - drag)` per tick gives wildly different results at 60Hz vs 120Hz — use `exp(-rate * delta)` for frame-rate independent damping

Each of these represents a debugging session that a human developer would spend hours on. Encoded in the executor's prompt, they're avoided entirely. This is the unglamorous but essential work: converting hard-won Godot expertise into patterns that prevent the executor from falling into the same traps.

**6. Visual Quality Assurance** — Visual QA runs as a dedicated **visual-qa** skill in a forked context, invoked by the executor after capturing screenshots. It supports three backends: Gemini Flash (default), Claude's native vision (`--native`), or both with aggregated verdict (`--both`). It operates in three modes:

- **Static mode** — for scenes without meaningful motion (terrain, decoration, UI): sends the reference image plus one representative game screenshot.
- **Dynamic mode** — for scenes with motion, animation, or physics: sends the reference image plus a sequence of frames sampled at 2 FPS cadence, so the model can evaluate movement, physics behavior, and temporal consistency.
- **Question mode** — for free-form visual debugging without a reference image: asks any question about screenshots ("Are surfaces showing magenta?", "Does the enemy patrol path form a loop?"). This is particularly useful for isolating issues that are hard to detect from code alone.

The QA looks for:

- Visual defects: z-fighting, texture stretching, clipping, floating objects
- Rendering bugs: missing textures (the telltale magenta), culling errors, lighting leaks
- Implementation shortcuts: grid-like placement instead of organic arrangement, uniform scaling instead of natural variation
- Motion anomalies (dynamic mode): stuck entities, jitter, sliding animations, physics explosions

If QA fails, the task executor fixes the issues and re-captures. The number of fix cycles is guided by judgment: if there's progress, keep going; if the same fix is being attempted repeatedly without convergence, escalate. If the problem is architectural (wrong approach, not just wrong parameters), the system replans.

**7. Orchestration** — The **godogen** skill ties everything together. It manages the pipeline sequence, handles resume logic (if PLAN.md already exists, it skips to task execution), communicates progress to the user via a connected channel (Telegram, Slack, or another supported service), and makes the meta-decisions: when to replan, when to re-scaffold, when to regenerate assets. Context hygiene is maintained by keeping important state in files (PLAN.md, STRUCTURE.md, MEMORY.md, ASSETS.md) that survive context compaction — the pipeline can resume from any point by reading these files. The final task in every plan is a presentation video — a script that showcases gameplay in a ~30-second cinematic MP4.

### The Document Protocol

Pipeline stages communicate through structured documents:

- **`reference.png`** — The visual north star. Every stage references it.
- **`STRUCTURE.md`** — The architectural blueprint. Written by the scaffold stage, read by task execution. Includes an explicit build order for scene builders.
- **`PLAN.md`** — The risk analysis and verification criteria. Written by the decomposer, status-tracked by the orchestrator.
- **`ASSETS.md`** — The asset manifest with art direction, sizes, animated sprite tables, and file paths. Written by the asset planner, consumed by task execution.
- **`MEMORY.md`** — The project's institutional memory. Written by the executor as it discovers workarounds, quirks, and debugging insights. Read before starting work and updated after each task.

This document-based communication is deliberate. Even though task execution now runs in the same context as the orchestrator (not a forked context), the documents serve a critical purpose: they survive context compaction. When the 1M context window approaches its limit and earlier messages are compressed, these files preserve the full state — the pipeline can resume from any point by reading them.

### Deployment Model

The `publish.sh` script copies the `skills/` directory into a target game directory under `.claude/skills/`, drops in a `CLAUDE.md` (from `game.md`), and initializes a git repo. A `--force` flag will clean the target directory before publishing. The game project is then self-contained: anyone with Claude Code can open the folder and run `/godogen` to build or iterate on the game.

For remote operation, `game.md` configures the system to share progress via a connected channel — Telegram, Slack, or another supported service. The user sends a message, walks away, and receives screenshots, QA verdicts, and a final gameplay video as the game takes shape — a game studio in a chat window.

## What Makes This Different

**Visual verification, not just code generation.** Most AI coding tools generate text and hope it works. Godogen captures actual screenshots from the running game engine and uses vision AI to verify correctness — with Gemini Flash and Claude vision available as complementary backends. Question mode allows free-form visual debugging ("Are surfaces showing magenta?") beyond structured reference comparisons. This catches an entire category of bugs that are invisible to text analysis.

**Single context, progressive loading.** Rather than many small agents that each need extensive prompting, or one giant prompt that overwhelms the context window, Godogen runs the full pipeline — from planning through task execution — in a single 1M-token context window. Stage-specific instructions load progressively: the orchestrator reads each sub-file only when that stage begins, and support skills (API lookup, visual QA) run in forked contexts to keep large payloads out of the main window. This means the executor has full access to everything that happened during planning — reference image analysis, architectural decisions, asset generation results — without needing to reload it from documents.

**Structured document protocol, not conversation.** Stages communicate through versioned documents with clear schemas, not through message passing. This makes the system resumable (crash mid-pipeline, pick up where you left off), inspectable (read the documents to understand what happened), and debuggable (edit a document and re-run a stage). Documents also survive context compaction, preserving state when the 1M window approaches its limit.

**Budget-aware dual-backend asset generation.** The system treats visual assets as an economic optimization problem: maximize visual impact per cent spent. Two image backends serve different needs — Gemini (5–15 cents) for precise work like character design and reference images, xAI Grok (2 cents) for textures and simple objects where exact prompt adherence doesn't matter. Animated sprites use xAI video generation (reference → pose → video → frame extraction → loop trim), with image-to-image editing maintaining visual consistency across asset families. A 3D model costs 37 cents, a texture costs 2 cents, and procedural particles are free — the system plans accordingly.

**Risk-first decomposition.** Counter to the instinct to break everything into tiny pieces, the decomposer identifies genuine technical risks (procedural generation, custom physics, complex shaders) and isolates only those for separate verification. Everything else — the routine features that Godot handles well — gets built in one pass. This is informed by hard-won experience: every task boundary is an integration risk, and fewer boundaries means fewer bugs.

**Deep domain expertise for a niche language.** LLMs write confident but wrong GDScript because it looks like Python but isn't. Godogen solves this with a custom-built reference system — a hand-written language spec, 850+ class API docs converted from Godot's source, and a dedicated API lookup skill that keeps the large documentation out of the main context. Combined with dozens of encoded engine quirks, the system writes GDScript that actually compiles and runs, not GDScript that merely looks plausible.

## Comparison with Video Diffusion Approaches

A different paradigm for AI game generation has emerged in parallel: video diffusion models, like Google DeepMind's Genie series, that generate interactive experiences entirely through learned frame prediction, with no game engine or code. A neural network observes player inputs and recent frames, then predicts what the next frame should look like, having learned from millions of hours of gameplay footage what "looks right." The visual results are impressive. Genie 3 generates photorealistic 3D environments in real time from text prompts. DeepMind has reported that Genie learns latent world representations internally — suggesting that with enough scale, these models may converge on something functionally equivalent to a game engine, learned end-to-end from video.

Godogen takes a fundamentally different approach: instead of predicting frames, it generates a real Godot project — editable scenes, readable scripts, organized assets — that runs on commodity hardware with deterministic game logic. The visual quality of generated assets is already strong (photographic quality from services like Tripo3D and Gemini), with animation being the main remaining gap — one that external generation services are rapidly closing.

The most interesting direction may be a hybrid: Godogen produces a functional game with correct mechanics and basic visuals, then a real-time video diffusion model runs on top of the rendered output — transforming the visual stream the way Oasis 2.0 reskins Minecraft. The game engine handles state, logic, and interaction; the diffusion model handles visual polish. Structural correctness from code, visual fidelity from learned generation.

## What It Produces

From a single sentence and an optional budget:

- A complete, compilable Godot 4 project with scenes, scripts, and assets
- A visual reference image that defines the art direction
- Architecture documentation (`STRUCTURE.md`)
- A risk analysis with verification criteria (`PLAN.md`)
- Generated 2D and 3D assets with transparent backgrounds and correct sizing — including animated sprites from video generation
- Per-task visual QA reports with debug logs
- A 30-second gameplay video
- Android debug APK (if requested)
