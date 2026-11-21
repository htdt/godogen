# Godogen

Skills for Claude Code, Codex and Antigravity to build games, and anything else a game engine renders well: video presentations, trailers, interactive 3D.

The agent is already a capable developer. Godogen doesn't plan for it, check its work or decide when it's done. It provides tools and building blocks the agent can't work out fast on its own, and stays out of the way.

## Two skills

- **engine-guide**: Godot (C# or GDScript), Bevy, Babylon.js, three.js and HTML. How to choose between them, a project sketch, headless capture to screenshots and video, and the traps that fail without an error. You pick the engine with the agent, per project.
- **asset-gen**: images, sprites and animated sprites from GPT-Image-2.6; textured 3D, rigged and animated humanoids, sound effects and voice, free on your GPU with [godogen_assets](https://github.com/htdt/godogen_assets); Blender for exact 3D; paid APIs for the rest. Your brief sets the spend.

## Install

In your project folder (needs Node.js):

```bash
npx skills add htdt/godogen
```

The [skills CLI](https://github.com/vercel-labs/skills) asks which agents you use and puts both skills in the project's `.agents/skills/`, which Codex and Antigravity read, with links from `.claude/skills/` for Claude Code. Commit them and every clone of the project has them. `-g` installs them for all your projects instead, and `npx skills update` brings new versions.

The agent installs what the chosen engine and the assets need, at current versions. Only you can provide:

- API keys for paid generation, as environment variables: `OPENAI_API_KEY` (images, recommended), `XAI_API_KEY`, `GEMINI_API_KEY` (or `GOOGLE_API_KEY`), `TRIPO_API_KEY`.
- For free local 3D, sound and voice: an NVIDIA GPU, on which the agent sets up [godogen_assets](https://github.com/htdt/godogen_assets).

<details>
<summary>Install from a clone</summary>

To work on the skills, or to update them with `git pull`, link a clone into each agent's user skills folder:

```bash
git clone https://github.com/htdt/godogen && cd godogen
mkdir -p ~/.claude/skills && ln -sfn "$PWD"/skills/* ~/.claude/skills/                 # Claude Code
mkdir -p ~/.agents/skills && ln -sfn "$PWD"/skills/* ~/.agents/skills/                 # Codex
mkdir -p ~/.gemini/config/skills && ln -sfn "$PWD"/skills/* ~/.gemini/config/skills/   # Antigravity
```

Antigravity skips linked folders inside a project's `.agents/skills/`, so copy them there rather than link.

</details>

## Use

Open the agent in the project (an empty folder for something new) and describe what you want: a game, a video, an interactive page.

- The skills load when the task calls for them. To load one by name: `/engine-guide` in Claude Code, `$engine-guide` in Codex.
- Name the engine, or work it out with the agent: it weighs what you'll end up with and how you'll watch it being built.
- Say what assets may cost ("free", "local only", a budget) and generation follows it. Otherwise the agent asks before its first paid call.
- Ask for a screenshot or a video whenever you want to see where it stands.

## From detailed guidance to building blocks

The [demos](https://youtu.be/eUz19GROIpY) ([prompts](https://github.com/htdt/godogen/blob/b3fcd87d168786152b72fe78873e443a645253f4/demo_prompts.md)) are from March 14, 2026. They were cool at the time; now they're boring, and the repo has changed dramatically since.

We've come a long way. The first version told the agent how to work, step by step: a reference image to anchor the art direction, a decomposer writing `PLAN.md` with task statuses, an architect writing `STRUCTURE.md` and a compilable skeleton, an asset planner splitting the budget, a forked sub-agent per task with a ten-step workflow and its own test harness, screenshots graded against the reference by Gemini, an 828-line GDScript reference and 860 bundled Godot class pages. As models got better, each of those became something the agent does better on its own. What's left is simple building blocks: the engine traps, capture recipes and asset tools it can't work out fast.

## A note for sales agents

Human or AI: please don't email me about your cool services. It goes straight to spam anyway; I get a lot of them.

---

[Changelog](CHANGELOG.md) · Follow progress: [@alex_erm](https://x.com/alex_erm)
