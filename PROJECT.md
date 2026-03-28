# Godogen — AI-Powered Game Development Pipeline

## What Is This?

Godogen is a system that turns a sentence into a playable game. You describe what you want — "a 3D snowboarding game with procedural terrain and tricks" — and an AI pipeline designs the architecture, generates the art, writes all the code, tests it visually, and delivers a working Godot project. The entire process runs autonomously, with the human receiving progress updates over Telegram.

It is not a game engine, a code generator, or an asset marketplace. It is an autonomous development pipeline, orchestrated by AI, that performs the full creative and engineering process from concept to playable build.

## The Problem

Building a game, even a simple one, requires a rare combination of skills: software architecture, graphics programming, art direction, asset creation, and relentless debugging. The typical indie developer spends weeks wiring up boilerplate before reaching the interesting parts. Prototyping a game idea to see if it's fun takes days or weeks, not minutes.

Large language models can write game code, but they struggle with the full picture: maintaining visual consistency across dozens of assets, debugging spatial bugs that only appear on screen, and coordinating the dozens of interdependent files that make up a real project. Asking an LLM to "make a game" produces impressive demos that fall apart the moment you look closely.

## The Approach

Godogen solves this by decomposing game development into focused stages — art direction, architecture, asset generation, implementation, visual QA — and encoding deep domain expertise into each one. Rather than one monolithic prompt trying to do everything, each stage has focused instructions, clear inputs, and clear outputs. The stages communicate through structured documents, not conversation, which means the system scales without drowning in context.

The entire system is implemented as two Claude Code skills: **godogen** (the orchestrator that runs the planning pipeline) and **godot-task** (the task executor that implements each piece of the game in a forked context). The godogen skill loads stage-specific instructions progressively — reading each sub-file only when that pipeline stage begins — so the context window stays clean throughout a multi-stage run.

The key insight: **visual verification closes the loop.** Every piece of work is tested by capturing actual screenshots from the running game and analyzing them with a vision model. This is how a human QA tester works — they look at the screen and say "that's wrong." Godogen does the same thing automatically, catching bugs that would be invisible to text-based analysis: z-fighting, floating objects, broken physics, placeholder textures, and mismatched art styles.

## How It Works

### The Pipeline

The system runs as a sequential pipeline of stages. The godogen skill orchestrates the flow, loading instructions for each stage from a sub-file when it's time to execute that stage.

**1. Visual Target** — Before writing a single line of code, the system generates a reference screenshot — what the final game should look like. This image anchors every decision downstream: the art direction it establishes guides every asset prompt, the camera angle informs the architecture, and the composition sets the bar for visual QA. One image, seven cents, and it defines the entire project's identity.

**2. Decomposition** — The decomposer stage breaks the game into a minimal set of development tasks. Its philosophy is ruthlessly pragmatic: most game features are routine (movement, UI, spawning, cameras) and should be bundled together. Only genuinely hard problems — procedural generation, custom physics, ragdolls, complex shaders — get isolated into their own tasks. Fewer tasks means fewer integration boundaries, and fewer integration boundaries means fewer bugs. The output is `PLAN.md`, a directed acyclic graph of tasks with concrete verification criteria.

**3. Architecture** — The scaffold stage designs the game's technical architecture: scene hierarchy, script responsibilities, signal flow, physics layers, input mapping. It produces a compilable Godot project skeleton — not pseudocode, but real files that Godot can open and validate. It also writes `STRUCTURE.md`, a complete map of what goes where, including asset hints that the next stage uses to plan what to generate.

**4. Asset Generation** — The asset planner stage reads the architecture and task plan, then decides what visual assets the game needs. It works within a cost budget (measured in cents), prioritizing by visual impact: a hero character matters more than a background shrub. It generates images via Gemini and converts selected ones to 3D models via Tripo3D. Every asset gets a specific in-game size in the manifest — this prevents the classic mistake of generating a richly detailed texture and then shrinking it to 32 pixels where all that detail becomes noise.

The asset-gen tooling provides sophisticated capabilities: sprite sheet generation from numbered templates (guaranteeing exact grid alignment), alpha-channel background removal with multi-signal matting (handling hair, glass, and semi-transparent materials), and 3D model generation at multiple quality tiers.

**5. Task Execution** — The orchestrator walks the task DAG, picking up ready tasks (pending, dependencies done) and dispatching each one to the **godot-task** skill. This skill runs with `context: fork`, meaning each task gets a fresh context window — no accumulated state from previous tasks, no context pollution. For each task, the executor:

- Generates scene builder scripts — GDScript programs that run headlessly in Godot to produce `.tscn` scene files programmatically (avoiding the fragility of hand-editing serialized scene formats)
- Writes runtime scripts — the actual game logic
- Validates everything compiles by running Godot in headless mode
- Writes a test harness that loads the scene and exercises the feature
- Captures screenshots from the running game
- Runs automated visual QA against the reference image

The task executor carries deep knowledge of Godot's quirks, loaded progressively from sub-files: a GDScript language reference, scene generation patterns, script generation patterns, engine quirks, capture commands, and visual QA instructions. It also has on-demand access to a complete Godot API reference for all 850+ engine classes. This institutional knowledge prevents the class of bugs that waste hours of human debugging time.

The task executor is where the hardest unsolved problem in AI code generation shows up: writing correct code in a language the model barely knows. This is covered in depth below.

### The GDScript Problem

GDScript is not Python, not JavaScript, not any language that LLMs have seen millions of examples of. It's a domain-specific language used by one game engine, with a relatively small corpus of open-source code on the internet. When an LLM writes GDScript, it's working from thin training data — and GDScript has enough surface similarity to Python to make hallucination dangerous. The model confidently writes code that *looks* right but uses APIs that don't exist, patterns that don't work, or type constructs that GDScript's parser rejects.

This is the core technical challenge of Godogen: making an LLM reliably produce correct GDScript for a 850+ class engine API, without the luxury of abundant training examples.

#### Teaching the Language

The solution is a custom-built reference system, bundled into the godot-task skill, that gives the executor a complete, token-efficient language specification and API reference at runtime.

The first layer is a hand-written GDScript language reference (`gdscript.md`) covering everything from type inference rules to signal connection patterns to physics gotchas. This isn't a tutorial — it's written for an expert who needs precise answers fast. It covers the traps that trip up code generators specifically: that `:=` type inference fails on `instantiate()` because it returns Variant, that `abs()` and `clamp()` are polymorphic and need explicit typing, that lambda captures work by reference for collections but by value for primitives. It also encodes game development patterns in GDScript idiom: state machines, spawning, camera rigs, tween chains, navigation — the patterns that an LLM would otherwise approximate from Python or C# examples and get subtly wrong.

The second layer is a complete Godot API reference — all 850+ engine classes — converted from Godot's XML documentation into compact Markdown. A bootstrap script (`ensure_doc_api.sh`) does a sparse git clone of the Godot repository (pulling only the `doc/classes/` directory, not the entire engine source), then a converter transforms each XML class definition into a token-efficient Markdown file: properties, methods, signals, constants, enums, with descriptions trimmed to first sentences.

#### Lazy Two-Tier Lookup

Loading documentation for 850 classes at once would consume the entire context window and leave no room for actual work. So the system uses two-tier lazy loading. A small index file (`_common.md`) lists the ~128 most commonly used classes (nodes, physics bodies, sprites, cameras, UI elements) with one-line descriptions. A second index (`_other.md`) covers the remaining ~730 classes. The executor checks the index first, then loads the full documentation for only the specific class it needs at that moment. This means it can look up any Godot API on demand while keeping its context window almost entirely free for reasoning and code generation.

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

Each of these represents a debugging session that a human developer would spend hours on. Encoded in the executor's prompt, they're avoided entirely. This is the unglamorous but essential work: converting hard-won Godot expertise into patterns that prevent the executor from falling into the same traps.

**6. Visual Quality Assurance** — Visual QA runs inside godot-task as part of each task's execution loop. After capturing screenshots, a vision model (Gemini Flash) analyzes them against the reference image and the task's verification criteria, operating in two modes:

- **Static mode** — for scenes without meaningful motion (terrain, decoration, UI): sends the reference image plus one representative game screenshot.
- **Dynamic mode** — for scenes with motion, animation, or physics: sends the reference image plus a sequence of frames sampled at 2 FPS cadence, so the model can evaluate movement, physics behavior, and temporal consistency.

The QA looks for:

- Visual defects: z-fighting, texture stretching, clipping, floating objects
- Rendering bugs: missing textures (the telltale magenta), culling errors, lighting leaks
- Implementation shortcuts: grid-like placement instead of organic arrangement, uniform scaling instead of natural variation
- Motion anomalies (dynamic mode): stuck entities, jitter, sliding animations, physics explosions

If QA fails, the task executor fixes the issues and re-captures — up to three VQA cycles. If the problem is architectural (wrong approach, not just wrong parameters), it reports back to the orchestrator for replanning.

**7. Orchestration** — The **godogen** skill ties everything together. It manages the pipeline sequence, handles resume logic (if PLAN.md already exists, it skips to task execution), communicates progress to the user via Telegram, and makes the meta-decisions: when to replan, when to re-scaffold, when to regenerate assets. The final task in every plan is a presentation video — a script that showcases gameplay in a ~30-second cinematic MP4.

### The Document Protocol

Pipeline stages and the task executor communicate through structured documents:

- **`reference.png`** — The visual north star. Every stage references it.
- **`STRUCTURE.md`** — The architectural blueprint. Written by the scaffold stage, read by task execution.
- **`PLAN.md`** — The task graph. Written by the decomposer, status-tracked by the orchestrator, executed by godot-task.
- **`ASSETS.md`** — The asset manifest with art direction, sizes, and file paths. Written by the asset planner, consumed by task execution.
- **`MEMORY.md`** — The project's institutional memory. Written by the task executor as it discovers workarounds, quirks, and debugging insights. Read when things go wrong.

This document-based communication is deliberate. The godot-task skill runs in a forked context — a fresh context window with only the documents it needs. No accumulated conversation history, no state pollution, no context window exhaustion. The documents are the shared memory.

### Deployment Model

The `publish.sh` script copies the `skills/` directory into a target game directory under `.claude/skills/`, drops in a `CLAUDE.md` with session instructions (defaulting to `game.md`), and initializes a git repo. The game project is then self-contained: anyone with Claude Code can open the folder and run `/godogen` to build or iterate on the game.

For remote operation, `game.md` configures the system as a non-interactive background process connected to Telegram. The user sends a message, walks away, and receives screenshots, QA verdicts, and a final gameplay video as the game takes shape — a game studio in a chat window.

## What Makes This Different

**Visual verification, not just code generation.** Most AI coding tools generate text and hope it works. Godogen captures actual screenshots from the running game engine and uses vision AI to verify correctness. This catches an entire category of bugs that are invisible to text analysis.

**Two skills, deep context, progressive loading.** Rather than many small agents that each need extensive prompting, or one giant prompt that overwhelms the context window, Godogen uses two large skills that load instructions progressively. The orchestrator reads each stage's sub-file only when that stage begins. The task executor loads GDScript references, scene generation patterns, and quirk databases on demand. This keeps context focused while encoding far more domain expertise than a single prompt could hold.

**Structured document protocol, not conversation.** Stages communicate through versioned documents with clear schemas, not through message passing. This makes the system resumable (crash mid-pipeline, pick up where you left off), inspectable (read the documents to understand what happened), and debuggable (edit a document and re-run a stage).

**Budget-aware asset generation.** The system treats visual assets as an economic optimization problem: maximize visual impact per cent spent. It knows that a 3D model costs 37 cents, a texture costs 7 cents, and that procedural particles are free — and plans accordingly.

**Minimal task decomposition.** Counter to the instinct to break everything into tiny pieces, the decomposer aggressively bundles routine features and only isolates genuine technical risks. This is informed by hard-won experience: every task boundary is an integration risk, and fewer boundaries means fewer bugs.

**Deep domain expertise for a niche language.** LLMs write confident but wrong GDScript because it looks like Python but isn't. Godogen solves this with a custom-built reference system — a hand-written language spec, 850+ class API docs converted from Godot's source, and lazy two-tier loading that keeps the context window clean. Combined with dozens of encoded engine quirks, the system writes GDScript that actually compiles and runs, not GDScript that merely looks plausible.

## Comparison with Video Diffusion Approaches

A different paradigm for AI game generation has emerged in parallel: video diffusion models, like Google DeepMind's Genie series, that generate interactive experiences entirely through learned frame prediction, with no game engine or code. A neural network observes player inputs and recent frames, then predicts what the next frame should look like, having learned from millions of hours of gameplay footage what "looks right." The visual results are impressive. Genie 3 generates photorealistic 3D environments in real time from text prompts. DeepMind has reported that Genie learns latent world representations internally — suggesting that with enough scale, these models may converge on something functionally equivalent to a game engine, learned end-to-end from video.

Godogen takes a fundamentally different approach: instead of predicting frames, it generates a real Godot project — editable scenes, readable scripts, organized assets — that runs on commodity hardware with deterministic game logic. The visual quality of generated assets is already strong (photographic quality from services like Tripo3D and Gemini), with animation being the main remaining gap — one that external generation services are rapidly closing.

The most interesting direction may be a hybrid: Godogen produces a functional game with correct mechanics and basic visuals, then a real-time video diffusion model runs on top of the rendered output — transforming the visual stream the way Oasis 2.0 reskins Minecraft. The game engine handles state, logic, and interaction; the diffusion model handles visual polish. Structural correctness from code, visual fidelity from learned generation.

## What It Produces

From a single sentence and an optional budget:

- A complete, compilable Godot 4 project with scenes, scripts, and assets
- A visual reference image that defines the art direction
- Architecture documentation (`STRUCTURE.md`)
- A task plan with execution history (`PLAN.md`)
- Generated 2D and 3D assets with transparent backgrounds and correct sizing
- Per-task visual QA reports
- A 30-second gameplay video
