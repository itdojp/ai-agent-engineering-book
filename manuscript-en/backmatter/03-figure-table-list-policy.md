# Figure and Table Listing Policy

This file is the source of truth for building the figure list and table list in ebook and print backmatter. The figure sources live under `manuscript/figures/`, and the table sources live in each chapter's Markdown tables.

## Role

- Help readers re-find figures and tables after they finish the book
- Preserve a stable seed before production adds figure numbers, table numbers, and page references
- Keep the figure plan, chapter prose, and production output aligned

## Figure List Policy

- Treat `manuscript/figures/figure-plan.md` as the source of truth for figure ID, chapter, caption, and first mention
- Keep each caption reader-facing so the main lesson of the figure is visible in one line
- Preserve the rule of one figure for one main message, then swap only the production numbering later

## Current Figure Seed

| Figure ID | Chapter | First Mention | Source |
|---|---|---|---|
| `fig-01` | CH01 | The map from Prompt / Context / Harness | `manuscript/figures/fig-01-maturity-model.mmd` |
| `fig-02` | CH05 | Persistent, task, session, and tool context | `manuscript/figures/fig-02-context-classes.mmd` |
| `fig-03` | CH07 | The minimum input for resuming a session | `manuscript/figures/fig-03-resume-packet.mmd` |
| `fig-04` | CH09 | The overall single-agent harness flow | `manuscript/figures/fig-04-single-agent-harness.mmd` |
| `fig-05` | CH10 | The order of lint, typecheck, unit, and e2e | `manuscript/figures/fig-05-verification-pipeline.mmd` |
| `fig-06` | CH11 | The split among planner, coder, and reviewer | `manuscript/figures/fig-06-long-running-multi-agent.mmd` |
| `fig-07` | CH12 | The responsibilities that remain with humans | `manuscript/figures/fig-07-operating-model.mmd` |

## Table List Policy

- Include only reader-facing tables, not temporary comparison tables or list substitutes
- Confirm production table titles by pairing the nearest heading with the table's main message
- Until page numbers exist, keep the seed in terms of return-to chapter and nearby heading

## Current Table Seed

| Return-to Chapter | Nearby Heading | Table Role |
|---|---|---|
| CH01 | Getting one answer right is different from getting work done | Shows the difference between plausible output and completed work |
| CH02 | Separate objective, constraints, completion criteria, and forbidden actions | Shows the Prompt Contract elements and the failures caused by missing ones |
| CH04 | Evaluate prompts as operational artifacts | Shows the boundary among prompt, context, and harness evaluation |
| CH07 | Task context and session memory | Shows the minimum elements required for a restart |
| CH09 | Foundations of Harness Engineering | Compresses the flow from init to final report |
| CH10 | Verification is a system, not a single test run | Shows the order from failing test to approval |
| CH11 | Decide when to stay single-agent and when to split roles | Shows the branching conditions between single-agent and multi-agent work |
| CH12 | Operate by metrics, review budget, and hygiene | Shows the measurement group for throughput, quality, and hygiene |
