# Introduction

This book is not about making an AI agent look clever. It is about getting work to completion. The scope does not stop at shaping a good-looking answer with prompts. It covers the full path from an ambiguous request to a spec, from a spec to repo work, and from repo work to verification and completion.

The book focuses on only three layers: Prompt Engineering, Context Engineering, and Harness Engineering. Prompt Engineering defines the contract for one task. Context Engineering makes the required decision inputs visible and durable. Harness Engineering makes execution, verification, retry, and restart safe. The book builds these layers in order so an AI agent can move from plausible output toward completed work.

## What This Book Promises

By the end of the book, the reader should be able to explain and reproduce the following in practical engineering terms.

- Turn ambiguous requests into Prompt Contracts, specs, acceptance criteria, and ADRs
- Use repo context, task briefs, Progress Notes, and context packs to keep an AI agent from losing its assumptions
- Use a verification harness, permission policy, restart protocol, and operating model to close AI-agent work safely

This book does not promise benchmark comparisons between models or a collection of conversational prompt tricks. The subject is work that includes code changes, verification, review, and handoff.

## Intended Reader

This book is for readers who fit at least one of these profiles.

- Engineers who want to introduce ChatGPT or coding agents into development work while keeping completion quality stable
- Tech leads who need AI agents to operate safely inside an issue, spec, tests, docs, and review process
- Practitioners who already feel the limit of prompt-only advice and want to design context and harness layers as well

The assumed background is basic familiarity with Git, issues, tests, and code review. Deep knowledge of Python or a specific framework is not required, but comfort with reading and changing a repo will make the book easier to use.

## Not the Intended Reader

This book does not directly target the following expectations.

- Readers who want a no-code introduction to AI agents
- Readers whose main goal is model selection or API parameter tuning
- Readers who want only conversational usage patterns or a general introduction to generative AI

The book assumes a development environment with a repo and persistent artifacts. It does not focus on workflows that never reach code changes or verification.

## Background Assumptions

This book is easiest to use when the reader already has three basics in place.

- A working understanding of Git, diffs, history, and branches
- Familiarity with development flow based on issues, specs, tests, and code review
- Comfort with opening a repo, changing files, and running verification

Deep knowledge of Python or any specific framework is not required. It is enough to be comfortable with shells, CI, tests, and pull requests as normal engineering artifacts.

## What This Book Covers and Does Not Cover

The book covers the design required to get an AI agent to complete work. In practical terms, that means artifacts and operating rules such as Prompt Contracts, task briefs, context packs, verification harnesses, restart packets, and review budgets.

It does not cover the following areas in depth.

- The internal theory of model training or academic optimization methods
- Publishing contracts, sales strategy, or final production design
- Organization-wide HR or performance-review systems

The book includes the theory it needs, but it always lands that theory in repo artifacts that can be reused.

## Safety Notes

Letting an AI agent touch a repo or verification flow does not mean the setup is safe for production by default. Review the following boundaries before reuse.

- Permission boundary: decide write access, secrets, external calls, and billable APIs before execution
- Verification boundary: decide which local checks, CI checks, and review evidence are required before a task can be called done
- Auditability: keep changes to Prompt, Context, and Harness in repo artifacts rather than only in chat history

The examples in this book are intentionally simplified for readers. When you reuse them in practice, confirm the active model, CLI, permission settings, organizational policy, and legal constraints in your own environment.

## How to Track Updates

- Public site: `https://itdojp.github.io/ai-agent-engineering-book/`
- Repository: `https://github.com/itdojp/ai-agent-engineering-book`
- Change history: GitHub commits and pull requests
- Pages pipeline notes: `docs/pages-publishing.md`

Prompt, Context, and Harness tooling changes quickly. The intended reading model is the manuscript plus the latest repository state plus the official documentation of the tool in use.

## How to Read the Recurring Cases

The running example is `support-hub`, provided as `sample-repo`. Instead of changing examples every chapter, the book keeps returning to the same repo and the same four recurring cases.

- `BUG-001`: how to close a bugfix safely
- `FEATURE-001`: how to turn an ambiguous request into a specification
- `FEATURE-002`: how to split and resume a long-running task
- `HARNESS-001`: how to structure verification and evidence

The point of repeating these cases is not to add isolated techniques. It is to show that Prompt, Context, and Harness are layered ways of moving the same work closer to completion.

## What to Watch While Reading

The book is designed to stand on its own, but it becomes more useful when read alongside the repo. The easiest way to stay oriented is to keep three questions in view.

1. What is this chapter trying to stabilize?
2. Which new artifacts does this chapter add?
3. Which recurring case in `support-hub` does that artifact improve?

If those three answers stay visible, it becomes easy to return later and re-find the relevant chapter or artifact. The next file explains the three-part structure and the main ways to read the book.
