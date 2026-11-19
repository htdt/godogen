# Contributing to Godogen

## Philosophy

Godogen is building blocks for coding agents. The agent is already capable: it plans, builds, checks its work and decides what to deliver. These skills exist to give it what it can't work out fast on its own, and to stay out of its way otherwise.

We keep things lean and focused. We don't add features just to have them — we'd rather have one clear, well-built tool than several mediocre ones. Less surface area means easier maintenance and better agent efficiency. If a new feature doesn't make the agent meaningfully better at what it builds, it doesn't belong here.

## How to Contribute

### Step 1: Open an Issue First

**All contributions start with an issue. Do not open a PR without an approved issue.**

In your issue, explain:

- **What** you want to change or add.
- **Why** — how does this improve what the agent builds? What concrete problem does it solve? Show evidence if you can (failed generations, error logs, before/after comparisons).
- **Why not something simpler** — if there's a lighter-weight way to achieve the same result, explain why your approach is better.

Wait for maintainer approval before writing code. This saves everyone's time — yours included.

### Step 2: Get Approval

A maintainer will respond to your issue. Possible outcomes:

- **Approved** — go ahead and implement.
- **Needs discussion** — the idea has merit but the approach needs refinement.
- **Closed** — doesn't fit the project direction. This isn't personal; the bar is high because scope discipline is how this project stays healthy.

### Step 3: Open a PR

Once approved, open a PR that references the issue. Keep it focused on what was discussed — avoid scope creep.

## What We're Looking For

**Good contributions** typically:

- Fix a bug that causes generation failures or degraded output.
- Improve output quality in a measurable way (better scenes, fewer broken scripts, more reliable asset generation).
- Reduce token usage or API costs without sacrificing quality.
- Improve reliability (fewer crashes, better error recovery).
- Improve or correct the engine guides or asset-generation reference material.

**We'll likely close contributions that:**

- Add process the agent can decide on its own: plans, checklists, review steps.
- Introduce alternative approaches when the existing one works fine.
- Add configuration options for things that should have good defaults.
- Are large refactors without a demonstrated problem they solve.
- Touch many files with cosmetic or stylistic changes.

## Code Expectations

- Match the existing style and conventions in the repo.
- Keep changes minimal and surgical. Small, focused PRs are easier to review and merge.
- If your change touches a skill, test it by having an agent build something with it end to end, and include the output or a summary of results.

## PRs Without an Approved Issue Will Be Closed

This isn't to be unwelcoming — it's to protect both maintainer time and contributor effort. The worst outcome is someone spending hours on a PR that was never going to be merged. The issue-first process prevents that.

## Bug Reports and Questions

Bug reports don't need prior approval — just open an issue with reproduction steps. Questions and discussions are welcome in issues too.
