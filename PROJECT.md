# Godogen — AI-Powered Game Development Pipeline

## What Is This?

Godogen is a system that turns a sentence into a playable game. You describe what you want — "a 3D snowboarding game with procedural terrain and tricks" — and a team of AI agents designs the architecture, generates the art, writes all the code, tests it visually, and delivers a working Godot project. The entire process runs autonomously, with the human receiving progress updates over Telegram.

It is not a game engine, a code generator, or an asset marketplace. It is an autonomous development team, orchestrated by AI, that performs the full creative and engineering pipeline from concept to playable build.

## The Problem

Building a game, even a simple one, requires a rare combination of skills: software architecture, graphics programming, art direction, asset creation, and relentless debugging. The typical indie developer spends weeks wiring up boilerplate before reaching the interesting parts. Prototyping a game idea to see if it's fun takes days or weeks, not minutes.

Large language models can write game code, but they struggle with the full picture: maintaining visual consistency across dozens of assets, debugging spatial bugs that only appear on screen, and coordinating the dozens of interdependent files that make up a real project. Asking an LLM to "make a game" produces impressive demos that fall apart the moment you look closely.

## The Approach

Godogen solves this by decomposing game development into the same roles a real studio uses — but each role is played by a specialized AI agent with deep knowledge of its domain. Rather than one monolithic prompt trying to do everything, each agent has a focused job, clear inputs, and clear outputs. They communicate through structured documents, not conversation, which means the system scales without drowning in context.

The key insight: **visual verification closes the loop.** Every piece of work is tested by capturing actual screenshots from the running game and analyzing them with a vision model. This is how a human QA tester works — they look at the screen and say "that's wrong." Godogen does the same thing automatically, catching bugs that would be invisible to text-based analysis: z-fighting, floating objects, broken physics, placeholder textures, and mismatched art styles.

## How It Works

### The Pipeline

The system runs as a pipeline of six stages. Each stage is handled by a specialized agent or skill, and the output of each stage feeds into the next.

**1. Visual Target** — Before writing a single line of code, the system generates a reference screenshot — what the final game should look like. This image anchors every decision downstream: the art style it establishes gets baked into every asset prompt, the camera angle informs the architecture, and the composition sets the bar for visual QA. One image, seven cents, and it defines the entire project's identity.

**2. Architecture & Planning** (run in parallel) — Two agents work simultaneously:

- The **Scaffold** agent designs the game's technical architecture: scene hierarchy, script responsibilities, signal flow, physics layers, input mapping. It produces a compilable Godot project skeleton — not pseudocode, but real files that Godot can open and validate. It also writes `STRUCTURE.md`, a complete map of what goes where.

- The **Decomposer** agent breaks the game into a minimal set of development tasks. Its philosophy is ruthlessly pragmatic: most game features are routine (movement, UI, spawning, cameras) and should be bundled together. Only genuinely hard problems — procedural generation, custom physics, ragdolls, complex shaders — get isolated into their own tasks. Fewer tasks means fewer integration boundaries, and fewer integration boundaries means fewer bugs. The output is `PLAN.md`, a directed acyclic graph of tasks with concrete verification criteria.

**3. Asset Generation** — The **Asset Planner** reads the architecture and task plan, then decides what visual assets the game needs. It works within a cost budget (measured in cents), prioritizing by visual impact: a hero character matters more than a background shrub. It generates images via Gemini and converts selected ones to 3D models via Tripo3D. Every asset gets a specific in-game size in the manifest — this prevents the classic mistake of generating a richly detailed texture and then shrinking it to 32 pixels where all that detail becomes noise.

Behind the scenes, the **asset-gen** skill provides sophisticated tooling: sprite sheet generation from numbered templates (guaranteeing exact grid alignment), alpha-channel background removal with multi-signal matting (handling hair, glass, and semi-transparent materials), and 3D model generation at multiple quality tiers.

**4. Task Execution** — The **Task Executor** picks up each task from the plan and implements it. This is the most complex agent, because implementation is the most complex job. For each task it:

- Generates scene builder scripts — GDScript programs that run headlessly in Godot to produce `.tscn` scene files programmatically (avoiding the fragility of hand-editing serialized scene formats)
- Writes runtime scripts — the actual game logic
- Validates everything compiles by running Godot in headless mode
- Writes a test harness that loads the scene and exercises the feature
- Captures screenshots from the running game

The agent carries deep knowledge of Godot's quirks: ownership chains that determine what gets serialized, RID leaks in physics queries, `_ready()` not firing during `_initialize()`, MultiMesh serialization bugs, and dozens of others. This institutional knowledge prevents the class of bugs that waste hours of human debugging time.

**5. Visual Quality Assurance** — After each task captures screenshots, they go through automated visual QA. A vision model (Gemini Flash) analyzes the screenshots against the reference image and the task's verification criteria, looking for:

- Visual defects: z-fighting, texture stretching, clipping, floating objects
- Rendering bugs: missing textures (the telltale magenta), culling errors, lighting leaks
- Implementation shortcuts: grid-like placement instead of organic arrangement, uniform scaling instead of natural variation
- Motion anomalies (for dynamic scenes): stuck entities, jitter, sliding animations, physics explosions

If QA fails, the task executor attempts to fix the issues and re-captures — up to three cycles. If the problem is architectural (wrong approach, not just wrong parameters), it escalates to the orchestrator for replanning.

**6. Orchestration** — The **Godogen** orchestrator ties everything together. It manages the pipeline sequence, handles resume logic (if interrupted, it picks up from the last incomplete task), communicates progress to the user via Telegram, and makes the meta-decisions: when to replan, when to re-scaffold, when to regenerate assets. After all tasks complete, it captures a 30-second gameplay video as the final deliverable.

### The Document Protocol

Agents don't talk to each other — they read and write structured documents:

- **`reference.png`** — The visual north star. Every agent references it.
- **`STRUCTURE.md`** — The architectural blueprint. Written by the scaffold, read by everyone.
- **`PLAN.md`** — The task graph. Written by the decomposer, status-tracked by the orchestrator, executed by the task agent.
- **`ASSETS.md`** — The asset manifest with style string, sizes, and file paths. Written by the asset planner, consumed by task execution.
- **`MEMORY.md`** — The project's institutional memory. Written by the task executor as it discovers workarounds, quirks, and debugging insights. Read when things go wrong.

This document-based communication is deliberate. Each agent runs in a fresh context window with only the documents it needs — no accumulated conversation history, no state pollution, no context window exhaustion. The documents are the shared memory.

### Deployment Model

The `publish.sh` script packages all agents and skills into a target game directory under `.claude/`, drops in a `CLAUDE.md` with session instructions, and initializes a git repo. The game project is then self-contained: anyone with Claude Code can open the folder and run `/godogen` to build or iterate on the game.

For remote operation, `teleforge.md` configures the system as a non-interactive background process connected to Telegram. The user sends a message, walks away, and receives screenshots, QA verdicts, and a final gameplay video as the game takes shape — a game studio in a chat window.

## What Makes This Different

**Visual verification, not just code generation.** Most AI coding tools generate text and hope it works. Godogen captures actual screenshots from the running game engine and uses vision AI to verify correctness. This catches an entire category of bugs that are invisible to text analysis.

**Specialized agents, not one giant prompt.** Each agent is an expert in one domain with focused context. The scaffold agent knows Godot architecture patterns. The asset planner knows cost optimization. The task executor knows engine quirks. This specialization produces better results than a generalist approach while keeping each agent's context window clean.

**Structured document protocol, not conversation.** Agents communicate through versioned documents with clear schemas, not through message passing. This makes the system resumable (crash mid-pipeline, pick up where you left off), inspectable (read the documents to understand what happened), and debuggable (edit a document and re-run a stage).

**Budget-aware asset generation.** The system treats visual assets as an economic optimization problem: maximize visual impact per cent spent. It knows that a 3D model costs 37 cents, a texture costs 7 cents, and that procedural particles are free — and plans accordingly.

**Minimal task decomposition.** Counter to the instinct to break everything into tiny pieces, the decomposer aggressively bundles routine features and only isolates genuine technical risks. This is informed by hard-won experience: every task boundary is an integration risk, and fewer boundaries means fewer bugs.

## What It Produces

From a single sentence and an optional budget:

- A complete, compilable Godot 4 project with scenes, scripts, and assets
- A visual reference image that defines the art direction
- Architecture documentation (`STRUCTURE.md`)
- A task plan with execution history (`PLAN.md`)
- Generated 2D and 3D assets with transparent backgrounds and correct sizing
- Per-task visual QA reports
- A 30-second gameplay video

Games that have been built with this system include a snowboarding game, a subway runner, a Quake-style shooter, and a bomber game.

## The Vision

Game development is one of the most creatively demanding forms of software engineering. It combines real-time graphics, physics simulation, input handling, asset creation, and game design — disciplines that traditionally require entire teams. Godogen demonstrates that these disciplines can be decomposed into agent-sized pieces, coordinated through structured documents, and verified through visual feedback loops.

The immediate goal is rapid prototyping: turning a game idea into a playable demo in minutes instead of weeks, so creators can test whether an idea is fun before investing real development time. The broader implication is that autonomous, visually-verified development pipelines can tackle problems that text-only AI coding tools cannot — any domain where correctness is visual, spatial, or physical rather than purely logical.
