---
id: ch08
title: Reuse Skills and Context Packs
status: drafted
source_ja: manuscript/part-02-context/ch08-skills-and-context-pack.md
artifacts:
  - .agents/skills/draft-chapter/SKILL.md
  - .agents/skills/review-chapter/SKILL.md
  - sample-repo/.agents/skills/issue-to-plan/SKILL.md
  - sample-repo/.agents/skills/verification/SKILL.md
  - sample-repo/context-packs/ticket-search.md
dependencies:
  - ch05
  - ch06
  - ch07
---

# Reuse Skills and Context Packs

## Role in This Book
If the same planning prompt or verification prompt is pasted into every new task, speed does not improve. Repetition without structure usually creates drift. CH05 through CH07 introduced persistent context, repo context, task briefs, and session memory. The next step is to package recurring work as reusable artifacts.

This chapter explains when a prompt should become a skill, how to structure `SKILL.md`, how to separate repo skills from user skills, how to build a context pack, and how to manage breaking changes. The goal is not to create more instructions. It is to manage reusable units of work as artifacts. That does not mean simply renaming a long prompt as a skill, and it does not mean assuming that repo artifacts become unnecessary once an MCP-connected capability exists.

## Learning Objectives
- Explain the boundary between a skill and a normal prompt
- Define a standard `SKILL.md` structure
- Design context packs at the right granularity

## Outline
### 1. When a prompt becomes a skill
### 2. Structure a `SKILL.md`
### 3. Separate repo skills from user skills
### 4. Build a context pack
### 5. Manage skill versioning and breaking changes

## 1. When a Prompt Becomes a Skill
The difference between a one-off prompt and a skill is not length. The real question is whether the same inputs, the same workflow, and the same output contract must be repeated across multiple tasks. Chapter drafting is a clear example. Every chapter task in this repo follows the same workflow: read the brief and relevant `AGENTS.md`, confirm referenced artifacts, include a bad / good example pair, preserve exactly two exercises, and run verify. That repeatable structure is why `.agents/skills/draft-chapter/SKILL.md` exists.

This is where CH08 must stay distinct from CH02. A Prompt Contract fixes the objective, constraints, completion criteria, and output schema for one task. A skill fixes a reusable workflow and output contract that apply across many tasks. If that boundary is ignored, a long prompt is simply renamed as a skill.

Not every recurring thought deserves a skill. “Think about whether `FEATURE-001` should add ranking” is still a one-off design question. A workflow should become a skill only when reuse cost is lower than repeated rediscovery cost. Common candidates are chapter drafting, issue-to-plan conversion, verification, and review.

## 2. Structure a `SKILL.md`
A useful `SKILL.md` is not a slogan. It is an operational contract. In this repo, `.agents/skills/draft-chapter/SKILL.md`, `.agents/skills/review-chapter/SKILL.md`, `sample-repo/.agents/skills/issue-to-plan/SKILL.md`, and `sample-repo/.agents/skills/verification/SKILL.md` all define Purpose, Use When or Read First, Workflow or Steps, Output Contract, and Guardrails.

That structure matters because each section answers a different operational question. Purpose explains why the skill exists. Use When fixes the activation boundary. Read First names the dependent artifacts. Workflow defines the repeatable procedure. Output Contract fixes what must be produced. Guardrails block scope drift. If any of those elements are missing, the skill becomes a memo rather than a reusable work unit.

It is also important to keep `AGENTS.md` separate from `SKILL.md`. `AGENTS.md` is the repo entrypoint. It defines non-negotiable invariants for that area and points to the next artifacts that must be read. `SKILL.md` is a repeatable work unit. It defines the workflow and output contract needed to run the same kind of work safely many times. Repo-wide invariants belong in `AGENTS.md`. Repeatable procedures belong in `SKILL.md`. Mixing them causes root instructions to grow while the skill absorbs too much repo-specific knowledge.

## 3. Separate Repo Skills from User Skills
Some skills belong to the repo. Others belong to an individual's environment. If those are mixed together, the workflow stops being reproducible for anyone else who clones the repository.

This repo keeps reusable book-specific workflows in `.agents/skills/` and sample-repo-specific workflows in `sample-repo/.agents/skills/`. Those are repo skills because they are versioned with the same artifacts they depend on. A personal review helper that assumes local credentials, proprietary tools, or private heuristics should stay outside the repo.

From a Context Engineering perspective, repo skills are part of persistent repo context. User skills are external dependencies. Treating user skills as if they were source of truth creates hidden coupling and makes onboarding fragile.

Repo skills also need to stay small. If a skill tries to include the entire domain explanation, repo map, and issue history, reusable workflow and repo-specific knowledge stop being separable. Skills should stay centered on “what to take as input, how to proceed, and how to report,” while detailed design rationale and source-of-truth content stay in `AGENTS.md`, briefs, specs, and docs.

## 4. Build a Context Pack
A skill alone is not enough for task-specific judgment. The skill tells the coding agent how to work. The context pack tells it what to read for this specific task.

`sample-repo/context-packs/ticket-search.md` is the concrete example in this chapter. It defines Purpose, Read Order, Canonical Facts, Live Checks, Exclusions, and Done Signals. That is why a context pack is not just a link dump. For `FEATURE-001`, the pack tells the reader to move through the domain overview, task brief, product spec, ADR, acceptance criteria, `service.py`, `test_ticket_search.py`, and the `Progress Note` in order. It also freezes canonical facts such as matching `title`, `description`, and `tags`, using case-insensitive comparison, handling blank queries, and keeping ranking or external search infrastructure out of scope.

The task brief still defines what the issue is trying to complete. The context pack defines the minimum reading bundle and reading order for the issue. It strengthens the task brief, but it does not replace it.

The distinction from an MCP-connected capability also matters. MCP or tool connections extend the runtime with new tools, resources, or prompt surfaces. That is an access layer for live information and external capability. It is not a replacement for repo skills or context packs. Task briefs, `AGENTS.md`, specs, and tests remain the repo's source of truth. An MCP-connected capability can help the agent reach or enrich that information, but the context pack still decides what to trust and in what order to read it.

## 5. Manage Skill Versioning and Breaking Changes
Skills and context packs are artifacts, so they also need change management. A change becomes breaking when it alters any part of the operational contract:

- required inputs change
- output section names change
- verify steps are added or removed
- read order depends on different artifacts

For example, if the `verification` skill stops at unit tests today but later requires evidence collection and Progress Note updates before completion, that is not a wording tweak. It changes the work contract and the expected output.

Small repos do not always need an explicit version field, but they still need discipline about what counts as contract and what counts as explanation. Changes to Purpose, Output Contract, Guardrails, or mandatory read inputs should be treated as skill-version changes. Wording cleanup and examples usually are not breaking changes.

The goal is not to accumulate skills forever. The goal is to keep reusable workflows trustworthy. A stale skill is worse than no skill because it gives the coding agent false confidence.

## Reader-facing Table
### Boundary Among Prompt Contract, `AGENTS.md`, Skill, Context Pack, and MCP-connected Capability

| Artifact | Primary purpose | What it fixes | Typical example |
|---|---|---|---|
| `Prompt Contract` | Fix the objective and completion criteria for one task | the input/output contract for that task | bugfix prompt, feature prompt |
| `AGENTS.md` | Define the repo entrypoint and invariants | where to start reading, verify obligations, update boundaries | root / local `AGENTS.md` |
| `skill` | Fix a reusable workflow | inputs, steps, output contract | `issue-to-plan`, `verification` |
| `context pack` | Fix task-specific reading order and canonical facts | read order, exclusions, done signals | `ticket-search` pack |
| MCP-connected capability | Connect new runtime capability | tool / resource / prompt surface | external search, DB lookup, remote tool |

When these five are mixed together, the result is usually a giant prompt that tries to do planning, reading guidance, execution, and live access at the same time. CH08 separates them so each artifact has one stable job.

## Bad / Good Example
Bad:

```text
For every issue, paste the same planning steps, the same verification steps,
and the same reading list into a long free-form prompt.
Because MCP can call external search, decide that repo `AGENTS.md` and specs do not need to be read every time.
```

This approach guarantees drift. Reused workflow never becomes an artifact, and task-specific facts are mixed together with generic process instructions. It also mistakes MCP access for repo source of truth.

Good:

```text
Keep the repo entrypoint in `AGENTS.md` and the local `AGENTS.md` files.
Keep planning in `sample-repo/.agents/skills/issue-to-plan/SKILL.md`.
Keep verification in `sample-repo/.agents/skills/verification/SKILL.md`.
For `FEATURE-001`, use `sample-repo/context-packs/ticket-search.md`
as the source of truth for reading order and canonical facts.
Use MCP-connected capability only for live additional investigation, not as a replacement for repo artifacts.
```

This version separates repo entrypoint, reusable workflow, task-specific context, and runtime capability.

Comparison points:
- The bad version simply renames a long prompt as a skill.
- The bad version omits `AGENTS.md` and the context pack and mistakes MCP for the source of truth.
- The good version separates repo entrypoint, workflow, task-specific context, and runtime capability.

## Exercises
1. Create an issue-to-plan skill.
2. Create a PR review skill and fix the review criteria.

## Referenced Artifacts
- `.agents/skills/draft-chapter/SKILL.md`
  Read this as an example of chapter drafting fixed as a reusable workflow. Pay attention to how Purpose, Read First, and Output Contract connect.
- `.agents/skills/review-chapter/SKILL.md`
  Read this as a review-oriented skill. Confirm how it preserves workflow without copying all repo invariants out of `AGENTS.md`.
- `sample-repo/.agents/skills/issue-to-plan/SKILL.md`
  Read this as an example of a repo skill that turns an issue into a plan. It is a workflow contract, not a Prompt Contract.
- `sample-repo/.agents/skills/verification/SKILL.md`
  Read this as a skill that avoids rewriting the same verify procedure in every task. It bridges into the verification harness in CH10.
- `sample-repo/context-packs/ticket-search.md`
  Read this as an example that bundles task-specific read order and canonical facts. Confirm why that bundle belongs in a context pack rather than in a skill.

## Source Notes / Further Reading
- To revisit this chapter, start with the `SKILL.md` files and `sample-repo/context-packs/ticket-search.md`. Read skills as reusable workflow contracts and the context pack as the minimum task input. Neither replaces repo source-of-truth artifacts.
- For the backmatter path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH08 Reuse Skills and Context Packs` and `manuscript-en/backmatter/01-reading-guide.md` under `## Context and Repo Design`.

## Chapter Summary
- A skill is not just a long prompt. It is an artifact that fixes a reusable workflow and output contract.
- `AGENTS.md` is the repo entrypoint, `SKILL.md` is the repeatable work unit, and the context pack is the task-specific reading set.
- An MCP-connected capability is an access layer for additional runtime capability, not a replacement for repo skills or context packs. The next chapter moves into Harness Engineering and defines the single-agent harness.

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch08-skills-and-context-pack.md`
- This English draft preserves the five-way boundary among Prompt Contract, `AGENTS.md`, skill, context pack, and MCP-connected capability.
