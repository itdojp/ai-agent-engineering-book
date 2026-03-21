---
id: ch01
title: Where AI Agents Fail
status: draft
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
AI agents can look highly capable over a few conversational turns. They answer questions, propose designs, and produce code-shaped text that sounds plausible. The problem is that practical engineering work is not measured by plausible output. It is measured by whether the work is actually complete: the agent read the repo, found the right artifacts, made the change, ran verification, and updated the surrounding docs when needed.

This book is not about making an agent sound smart. It is about getting work to completion. ChatGPT helps shape requirements and compare design options. Codex CLI reads and edits a repo, runs commands, and verifies the result. To get from a plausible answer to finished work, the book uses a three-stage maturity model: Prompt Engineering, Context Engineering, and Harness Engineering. This chapter introduces that model by looking at the failure patterns that show up in `sample-repo`.

## Learning Objectives
- Explain the difference between a one-off correct answer and actual work completion
- Understand the roles of the sample-repo, ChatGPT, and Codex CLI in this book
- Understand which artifacts later chapters will add and why they matter

## Outline
### 1. Getting one answer right is different from getting work done
Returning a good answer in a chat is not the same thing as completing work in a repo. An agent may say that ticket search should look at `description` and `tags` in addition to `title`. That sounds reasonable. It may even be correct. But practical work does not end there. Which issue is in scope? Which artifacts must change? What verification closes the task? If those questions are still open, the work is not done.

`sample-repo` makes this difference easy to see. As `sample-repo/README.md` explains, the repo models a small support ticket domain in Python. The job is not to invent a nice implementation idea. The job is to improve behavior without breaking ticket listing, status updates, or existing constraints, and to close the work with code, docs, tests, and verification.

The practical difference looks like this:

| Lens | Plausible Output | Completed Work |
|---|---|---|
| Target | The question in front of the model | The issue plus the artifacts that must change |
| Result | Advice or code fragments | Code, docs, tests, and verification output |
| Judgment | “This sounds right” | “The change is traceable and verifiable” |
| Failure Mode | The problem is easy to miss in the moment | The problem surfaces later as wrong answer, forgetting, breakage, or early stop |

### 2. Four failure modes: wrong answer, forgetting, breaking things, stopping early
Most AI agent failures fall into four categories.

1. Wrong answer  
   The agent misreads the requirement or the domain, but still produces something that sounds coherent. If it starts a search improvement without reading `sample-repo/docs/domain-overview.md`, it can make a proposal that ignores the actual behavior of the system.

2. Forgetting  
   The agent drops assumptions, constraints, or work history in the middle of the task. It may start from `FEATURE-001` and then drift into a different set of assumptions halfway through the session. The later change no longer connects to the earlier intention.

3. Breaking things  
   The agent fixes one area and damages another. Search may improve, but docs, tests, or a related filter path may fall out of sync. A change that only works in one narrow place is still a broken change.

4. Stopping early  
   The agent decides the task is done before the work is actually closed. Common forms are: code changed but no verification ran, docs were not updated, or change impact was never checked.

These failure modes tend to chain together. A wrong answer makes forgetting more likely. Forgetting increases the chance of breaking something. Once breakage is hidden, the agent may stop early and declare success.

In `sample-repo/docs/seed-issues.md`, the recurring cases line up with these failure modes:

| Failure Mode | Typical `sample-repo` Example | First Missing Artifact to Suspect |
|---|---|---|
| Wrong answer | Guessing the search scope in `FEATURE-001` | The issue boundary and domain understanding |
| Forgetting | Losing decisions during `FEATURE-002` | The task brief and progress note |
| Breaking things | Fixing `BUG-001` while drifting from docs or adjacent behavior | Tests and impact analysis |
| Stopping early | Treating `HARNESS-001` as done before verification and evidence | The verification harness and done criteria |

### 3. Prompt Engineering, Context Engineering, and Harness Engineering
These failures do not go away through good intentions. They go down when you design the right artifact for the right class of failure. This book organizes that work as a three-stage maturity model.

| Maturity Stage | Failures It Primarily Reduces | What You Design | Representative Artifacts |
|---|---|---|---|
| Prompt Engineering | Wrong answer | Objective, constraints, completion criteria, output expectations | Prompt artifacts, review checklists |
| Context Engineering | Forgetting | Repo, task, and session information that must stay visible | Task briefs, context packs, AGENTS.md |
| Harness Engineering | Breaking things, stopping early | Execution boundaries, verification, retries, and evidence | Verify scripts, runbooks, verification harness artifacts |

The stages stack. Prompt Engineering does not become unnecessary when Context Engineering begins. Context Engineering does not replace Harness Engineering. First you fix what the agent is supposed to do. Then you fix what the agent must continue seeing. Finally you fix how the work is executed, verified, and closed.

That order is both a learning order and an engineering order. If the prompt is still vague, more context only gives the agent more room to be wrong. If the context is stable but the harness is weak, the agent can still ship a broken or incomplete change.

### 4. The recurring cases, the sample-repo, ChatGPT, and Codex CLI
This book uses `support-hub` as its running case study. As `sample-repo/docs/domain-overview.md` shows, the current system centers on `Ticket`, `TicketStore`, and `SupportHubService`, with behaviors such as listing tickets, updating status, keyword search, and filtering by assignee. The repo is small, but it is large enough to show practical concerns: requirements shaping, change impact, verification, and long-running work.

The recurring cases in `sample-repo/docs/seed-issues.md` are the spine of the book:

| Case | What It Teaches | Typical Failure |
|---|---|---|
| `BUG-001` | How to close a bugfix safely | Breaking things, stopping early |
| `FEATURE-001` | How to turn an ambiguous request into a spec | Wrong answer |
| `FEATURE-002` | How to split and continue long-running work | Forgetting, stopping early |
| `HARNESS-001` | How to build verification and evidence | Stopping early, breaking things |

ChatGPT and Codex CLI also have different jobs. ChatGPT is useful for shaping vague requests, comparing alternatives, and surfacing review questions. Codex CLI is useful when the agent must read the repo, edit files, run verification, and update artifacts. This distinction matters throughout the book. A useful conversation is not yet a completed change.

### 5. Read this book as a book about artifacts
Each chapter in this book adds an artifact layer. Prompt chapters add prompt artifacts and review criteria. Context chapters add task briefs, context packs, and session-memory rules. Harness chapters add verify scripts, runbooks, evidence, and operating rules. The value of the book is not only in the explanation. It is in what exists in the repo after the chapter is applied.

This artifact-driven approach has three practical advantages.

- It makes progress observable. If the artifacts exist, verification runs, and the change can be explained, the workflow improved.
- It makes failure recoverable. You can see which layer is missing and what to add next.
- It makes later chapters cumulative instead of decorative. Each chapter adds a layer that helps the same work get closer to completion.

The conclusion of CH01 is simple: AI agents do not fail only because the model is weak. They fail because the path from request to completion is under-designed. The rest of the book builds that path, starting with Prompt Engineering.

## Bad / Good Example
Bad:

```text
Improve search in sample-repo. Make it feel nicer.
```

This request leaves the target issue, affected artifacts, completion criteria, and verification path undefined. An agent can produce reasonable-looking advice or partial code, but nothing in the request prevents wrong answer, forgetting, breakage, or an early stop.

Good:

```text
Start with `sample-repo/docs/seed-issues.md` and review `FEATURE-001`.
For this step, do not implement yet. Summarize the objective, the artifacts that will change,
and how the work will be verified.
Completion means the next worker can start from the same assumptions.
```

This is not yet a full Prompt Contract, but it already fixes three important things: the issue in scope, the artifacts to inspect, and what counts as completion for the current step. It turns a vague request into a practical setup action.

Comparison points:
- The bad example manages only the surface appearance of the output.
- The good example fixes issue scope, artifacts, and a completion condition before implementation starts.
- The good example assumes future verification and handoff instead of treating the current answer as the endpoint.

## Exercises
1. Read the four recurring cases in `sample-repo/docs/seed-issues.md`. For each one, identify the main failure mode it is best suited to teach and write one line of reasoning.
2. Read this request: “We want support-hub to be easier to use. Update code or docs if needed.” Pick two likely failure modes and name two artifacts you would add first to move the work closer to completion.

## Referenced Artifacts
- `sample-repo/README.md`
- `sample-repo/docs/domain-overview.md`
- `sample-repo/docs/seed-issues.md`

## Parity Notes
- Japanese source: `manuscript/part-00/ch01-failure-model.md`
- This file is now a full English draft and should stay aligned with the Japanese chapter's failure model, recurring cases, and maturity-model framing.

## Chapter Summary
- AI agents fail in four recurring ways: wrong answer, forgetting, breaking things, and stopping early.
- This book is about completing work with artifacts and verification, not producing plausible output.
- Prompt Engineering, Context Engineering, and Harness Engineering are layered because each one addresses a different failure pattern. The next chapter starts with Prompt Engineering.
