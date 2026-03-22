# Contributing to Godogen

## Philosophy

Godogen is an autonomous pipeline. The goal is to generate the best possible games with as little human guidance as possible. Every piece of this repo exists to serve that goal.

We keep things lean and focused. We don't add features just to have them — we'd rather have one clear, well-built tool than several mediocre ones. Less surface area means easier maintenance and better agent efficiency. If a new feature doesn't make the pipeline meaningfully better at producing games autonomously, it doesn't belong here.

## How to Contribute

### Step 1: Open an Issue First

**All contributions start with an issue. Do not open a PR without an approved issue.**

In your issue, explain:

- **What** you want to change or add.
- **Why** — how does this improve the autonomous pipeline? What concrete problem does it solve? Show evidence if you can (failed generations, error logs, before/after comparisons).
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
- Improve reliability of the pipeline (fewer crashes, better error recovery).
- Improve or correct the GDScript docs / API reference.

**We'll likely close contributions that:**

- Add features the pipeline doesn't need to function.
- Introduce alternative approaches when the existing one works fine.
- Add configuration options for things that should have good defaults.
- Are large refactors without a demonstrated problem they solve.
- Touch many files with cosmetic or stylistic changes.

## Code Expectations

- Match the existing style and conventions in the repo.
- Keep changes minimal and surgical. Small, focused PRs are easier to review and merge.
- If your change touches a skill, test it by running the pipeline end-to-end and include the output or a summary of results.

## PRs Without an Approved Issue Will Be Closed

This isn't to be unwelcoming — it's to protect both maintainer time and contributor effort. The worst outcome is someone spending hours on a PR that was never going to be merged. The issue-first process prevents that.

## Bug Reports and Questions

Bug reports don't need prior approval — just open an issue with reproduction steps. Questions and discussions are welcome in issues too.
