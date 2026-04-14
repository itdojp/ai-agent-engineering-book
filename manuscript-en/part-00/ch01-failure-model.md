---
id: ch01
title: Where AI Agents Fail
status: drafted
source_ja: manuscript/part-00/ch01-failure-model.md
artifacts:
  - sample-repo/README.md
  - sample-repo/docs/domain-overview.md
  - sample-repo/docs/seed-issues.md
dependencies:
  - none
---

# Where AI Agents Fail

## Role in This Book
An AI agent can look capable in conversation and still break things as soon as it touches a repo. That gap is the first problem many readers encounter. The front matter already explained the promise of the book, the intended reader, and the three-part structure. From here, the manuscript moves into the main body. The first question is where AI agents actually fail in engineering work.

The role of CH01 is to define the failure model. The chapter expands the model into eight failure classes that include wrong answers, context poisoning, tool misuse, approval misses, and insufficient verification. That failure model explains why Prompt Engineering alone is not enough and why Context Engineering and Harness Engineering are also required. The rest of the book then adds artifacts one layer at a time against those failure classes.

## Learning Objectives
- Explain the difference between a one-off wrong answer and an execution failure that includes context, permissions, verify, and approvals
- Understand the role differences among an interactive assistant, a local CLI coding agent, and a cloud or background agent
- Understand which artifacts later chapters will add and which signals will be used as verification evidence

## Outline
### 1. Getting one answer right is different from getting work done
Returning a good answer in a chat is not the same thing as completing work in a repo. An agent may say that ticket search should look at `description` and `tags` in addition to `title`. That sounds reasonable. It may even be correct. But practical work does not end there. Which issue is in scope? Which artifacts must change? What verification closes the task? If those questions are still open, the work is not done.

`sample-repo` makes this difference easy to observe. As `sample-repo/README.md` explains, the repo models a small support-ticket domain in Python. The job is not to invent a nice implementation idea. The job is to improve behavior without breaking ticket listing, status updates, or existing constraints, and to close the work with code, docs, tests, and verification.

The practical difference looks like this:

| Lens | Plausible Output | Completed Work |
|---|---|---|
| Target | The question in front of the model | The issue plus the artifacts that must change |
| Result | Advice or code fragments | Code, docs, tests, and verify results |
| Judgment | “This sounds right” | “The rationale and completion boundary are traceable” |
| Failure Mode | The problem is easy to miss in the moment | The problem surfaces later as wrong answer, forgetting, breakage, or stopping early |

### 2. Eight failure classes: wrong answer, poisoning, misuse, omission, and stop
Four failure classes are no longer enough for practical work in 2026. At minimum, engineering teams need to distinguish the following eight.

1. Wrong answer
   The agent misreads the requirement or the domain but still produces something that sounds coherent.
2. Context poisoning
   The agent treats an outdated Progress Note, stale summary, or obsolete spec as canonical and contaminates later decisions.
3. Stale state
   The agent misreads the current branch, review state, pending approval, or runtime setting.
4. Tool misuse
   The agent performs writes, external calls, deletions, or billable API usage outside the approved boundary.
5. Approval miss
   The agent executes an operation that should have passed a human approval gate and breaks auditability.
6. Insufficient verification
   The agent treats work as done before tests, lint, docs, policy checks, or evidence are complete.
7. Opaque background execution
   Long-running or remote work becomes hard to restart, hand off, or roll back because intermediate state is not visible.
8. Cost / latency runaway
   Wasteful retries, unnecessary tool calls, or oversized context make waiting time and cost hard to control.

These failures chain together. Context poisoning and stale state increase wrong answers. Tool misuse and approval misses create breakage and audit failures. Insufficient verification and opaque background execution make it easier to miss early stopping.

In `sample-repo/docs/seed-issues.md`, the recurring cases line up with those failures as follows:

| Failure Class | Typical `sample-repo` Example | First Missing Artifact to Suspect |
|---|---|---|
| Wrong answer | Guessing the search scope in `FEATURE-001` | Issue boundary and domain understanding |
| Context poisoning / stale state | Treating an old Progress Note as canonical in `FEATURE-002` | Source hierarchy and the `restart packet (Resume Packet)` |
| Tool misuse / approval miss | Running risky operations or external access before verify | Permission policy and approval gate |
| Insufficient verification / stopping early | Treating `HARNESS-001` as done without leaving evidence | Verification harness and done criteria |
| Cost / latency runaway | Overfeeding context and letting long runs continue without control | Context budget and operating model |

### 3. Design surfaces that reduce failure, and agent types
These failures do not go away through good intentions. They go down when the design target is separated by failure class. This book treats that work through Prompt, Context, and Harness.

| Design Surface | Failures It Primarily Reduces | What You Design | Representative Artifacts |
|---|---|---|---|
| Prompt Engineering | Wrong answer, scope drift, output-contract failure | task objective, constraints, tool contract, done criteria, output schema | prompt artifacts, review checklists, eval cases |
| Context Engineering | Context poisoning, stale state, lost assumptions | canonical repo / task / session / memory / context-pack inputs and their priority | task briefs, Progress Notes, context packs, repo maps |
| Harness Engineering | Tool misuse, approval miss, insufficient verification, stopping early | execution boundary, permission policy, verify, restart, evidence, approval | verify checklists, runbooks, restart packets, operating model |

The design responsibility also changes by agent type.

| Agent Type | Main Role | Boundary to Fix First |
|---|---|---|
| Interactive assistant | requirement shaping, comparison, issue framing | do not treat exploratory dialogue as the source of truth |
| Local CLI coding agent | read the repo, change files, run local verify | write scope, shell permission, verify procedure |
| Cloud / background coding agent | long-running tasks, remote execution, asynchronous restart | approval, polling / notification, restart packet |
| API / managed-runtime agent | embed agent behavior inside product workflows | tool policy, observability, auditability, cost / latency |

The important point is that later surfaces do not replace earlier ones. They stack. If the prompt is weak, a strong harness only executes the wrong task more carefully. If the context is weak, a good prompt still collapses when the session changes. If the harness is weak, a good prompt and good context still fail to close verify and approval.

### 4. The recurring cases and the sample-repo
This book uses `support-hub` as `sample-repo`. It is not only a toy app. It is a simplified support-ticket domain where a first-line operator triages tickets, a lead watches assignees and backlog, and implementation or operations staff decide how to improve search and operations. As `sample-repo/docs/domain-overview.md` explains, the core objects are `Ticket`, `InMemoryTicketStore` (treated conceptually as `TicketStore`), and `SupportHubService`, with behavior for listing tickets, updating status, keyword search, and filtering by assignee. The codebase is small, but it can still carry real pains such as status inconsistency, weak search, unclear ownership, and insufficient verification.

The book keeps returning to the four cases in `sample-repo/docs/seed-issues.md`.

| Case | Practical Pain | What the Book Adds | Typical Failure |
|---|---|---|---|
| `BUG-001` | Older status appears and can trigger duplicate work | bugfix brief, tests, single-agent harness | breakage, stopping early |
| `FEATURE-001` | Similar tickets are hard to find and the request is vague | spec, ADR, acceptance criteria, context pack, verify guard | wrong answer |
| `FEATURE-002` | assignee handling and audit behavior become long-running work | plan, feature list, restart packet, role split | forgetting, stopping early |
| `HARNESS-001` | verify and evidence are weak, so review is hard to justify | done criteria, CI, evidence bundle, operating model | stopping early, breakage |

`FEATURE-001` is the spine of the book. It follows how an ambiguous request is turned into spec, context, and verify artifacts. `BUG-001` is the bounded bugfix case. `FEATURE-002` is the case for not losing work across sessions. `HARNESS-001` is the case for connecting verification and evidence to team operations. Later chapters do not re-explain the cases from zero. They only clarify what each chapter learns from the current case.

ChatGPT and Codex CLI also have different roles. ChatGPT is useful for requirement shaping, alternative comparison, and review framing. Codex CLI is useful for reading the repo, changing files, running verify, and updating artifacts. At the CH01 stage, that role split is enough. Detailed prompt design and task-brief format come later.

### 5. Read this book as a book about artifacts
This book does not stop at conceptual explanation. Every chapter lands its argument in repo artifacts. Prompt Engineering chapters add prompt artifacts. Context Engineering chapters add task briefs and context packs. Harness Engineering chapters add verify scripts and runbooks. Readers should track not only the explanation but also what new artifact exists in the repo after the chapter is applied.

That reading model has three practical advantages.

- It makes progress observable. If the artifacts exist, verify passes, and the rationale can be explained, the workflow improved.
- It makes failure recoverable. The missing artifact layer shows where to resume.
- It makes later chapters cumulative instead of decorative. Each layer moves the same work closer to completion.

The conclusion of CH01 is simple. AI agents do not fail only because the model is weak. They fail because the path from request to completion is under-designed. The rest of the book builds that path, starting with Prompt Engineering.

## Bad / Good Example
Bad:

```text
Improve search in sample-repo. Make it feel nicer.
```

This request leaves the target issue, affected artifacts, completion criteria, and verification path undefined. An agent can produce plausible advice or partial code, but nothing in the request prevents wrong answer, approval misses, insufficient verification, or early stopping.

Good:

```text
Start with `sample-repo/docs/seed-issues.md` and review `FEATURE-001`.
For this step, do not implement yet. Summarize the objective, the artifacts that will change,
and how the work will be verified.
Completion means the next worker can start from the same assumptions.
```

This is not yet a full Prompt Contract, but it already fixes three important things: the issue in scope, the artifacts to inspect, and what counts as completion for the current step. It is the smallest practical example of the design discipline that later chapters formalize.

Comparison points:
- The bad example manages only the surface appearance of the output.
- The good example fixes issue scope, artifacts, and a completion boundary before implementation starts.
- The good example assumes future verification and handoff instead of treating the current answer as the endpoint.

## Exercises
1. Read the four recurring cases in `sample-repo/docs/seed-issues.md`. For each one, identify the main failure class it is best suited to teach and write one line of reasoning.
2. Read this request: “We want support-hub to be easier to use. Update code or docs if needed.” Pick two likely failure classes and name two artifacts you would add first to move the work closer to completion.

## Referenced Artifacts
- `sample-repo/README.md`
- `sample-repo/docs/domain-overview.md`
- `sample-repo/docs/seed-issues.md`

## Source Notes / Further Reading
- When you need to revisit this chapter, start with `sample-repo/README.md`, `sample-repo/docs/domain-overview.md`, and `sample-repo/docs/seed-issues.md`. The failure model is useful only when it stays connected to the recurring cases.
- For the next navigation step, see `manuscript-en/backmatter/00-source-notes.md` under `### CH01 Where AI Agents Fail` and `manuscript-en/backmatter/01-reading-guide.md` under `## Prompts and Requirements Shaping` and `## Verification, Reliability, and Operations`.

## Chapter Summary
- AI agents fail not only through wrong answers but also through context poisoning, tool misuse, approval misses, insufficient verification, and cost / latency runaway.
- This book is about completing work with artifacts, permissions, verify, and evidence rather than producing plausible output.
- Once the failure model is visible, the first thing to stabilize is the contract for a single task. The next chapter begins Prompt Engineering by treating prompts as input/output contracts.

## Parity Notes
- Japanese source: `manuscript/part-00/ch01-failure-model.md`
- This English draft preserves the expanded eight-class failure model, the recurring-case framing, and the agent-type boundary introduced in the Japanese chapter.
