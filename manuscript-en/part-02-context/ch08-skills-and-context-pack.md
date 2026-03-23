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

This chapter explains when a prompt should become a skill, how to structure `SKILL.md`, how to separate repo skills from user skills, how to build a context pack, and how to manage breaking changes. The goal is not to create more instructions. It is to manage reusable units of work as artifacts.

## Learning Objectives
- Explain the boundary between a skill and a normal prompt
- Define a standard SKILL.md structure
- Design context packs at the right granularity

## Outline
### 1. When a prompt becomes a skill
### 2. Structure a SKILL.md
### 3. Separate repo skills from user skills
### 4. Build a context pack
### 5. Manage skill versioning and breaking changes

## 1. When a Prompt Becomes a Skill
The difference between a one-off prompt and a skill is not length. The real question is whether the same inputs, the same workflow, and the same output contract must be repeated across multiple tasks.

Chapter drafting is a clear example. Every chapter task in this repo follows the same workflow: read the brief and relevant `AGENTS.md`, confirm referenced artifacts, include a bad / good example pair, preserve exactly two exercises, and run verify. That repeatable structure is why `.agents/skills/draft-chapter/SKILL.md` exists.

This is also where CH08 must stay distinct from CH02. A `Prompt Contract` fixes the objective, constraints, completion criteria, and output format for one task. A skill fixes a reusable workflow and output contract that apply across many tasks. If that boundary is ignored, a long prompt is simply renamed as a skill.

Not every recurring thought deserves a skill. “Think about whether `FEATURE-001` should add ranking” is still a one-off design question. A workflow should become a skill only when reuse cost is lower than repeated rediscovery cost. Common candidates are chapter drafting, issue-to-plan conversion, verification, and review.

## 2. Structure a `SKILL.md`
A useful `SKILL.md` is not a slogan. It is an operational contract. In this repo, `.agents/skills/draft-chapter/SKILL.md`, `.agents/skills/review-chapter/SKILL.md`, `sample-repo/.agents/skills/issue-to-plan/SKILL.md`, and `sample-repo/.agents/skills/verification/SKILL.md` all define a stable purpose, an activation condition, required inputs or read order, a workflow, an output contract, and guardrails.

That structure matters because each section answers a different operational question:

- `Purpose`: why this skill exists
- `Use When` or `Read First`: when the skill applies and what context must be loaded first
- `Workflow` or `Steps`: what sequence should be repeated
- `Output Contract`: what the skill must produce
- `Guardrails`: what the skill must not do

If any of those elements are missing, the skill becomes a memo rather than a reusable work unit. The output contract is especially important. If the skill does not define what must come out, downstream task briefs, verify steps, and handoffs have nothing concrete to depend on.

## 3. Separate Repo Skills from User Skills
Some skills belong to the repo. Others belong to an individual's environment. If those are mixed together, the workflow stops being reproducible for anyone else who clones the repository.

This repo keeps reusable book-specific workflows in `.agents/skills/` and sample-repo-specific workflows in `sample-repo/.agents/skills/`. Those are repo skills because they are versioned with the same artifacts they depend on. A personal review helper that assumes local credentials, proprietary tools, or private heuristics should stay outside the repo.

From a Context Engineering perspective, repo skills are part of persistent repo context. User skills are external dependencies. Treating user skills as if they were source of truth creates hidden coupling and makes onboarding fragile.

## 4. Build a Context Pack
A skill alone is not enough for task-specific judgment. The skill tells the coding agent how to work. The context pack tells it what to read for this specific task.

`sample-repo/context-packs/ticket-search.md` is the concrete example in this chapter. It defines:

- `Purpose`
- `Read Order`
- `Canonical Facts`
- `Live Checks`
- `Exclusions`
- `Done Signals`

That is why a context pack is not just a link dump. For `FEATURE-001`, the pack tells the reader to start with the domain overview and task brief, then move through product spec, ADR, acceptance criteria, implementation, tests, and finally the Progress Note. It also freezes canonical facts such as matching `title`, `description`, and `tags`, using case-insensitive comparison, trimming the query, and returning all tickets for a blank query. At the same time, it keeps ranking, typo correction, external search engines, and UI redesign out of scope.

The task brief still defines what the issue is trying to complete. The context pack defines the minimum reading bundle and reading order for the issue. It strengthens the task brief, but it does not replace it.

## Reader-facing Table
### Boundary Between Prompt Contract, Skill, and Context Pack

| Artifact | Primary purpose | Input stability | Output contract | Typical example |
|---|---|---|---|---|
| `Prompt Contract` | Fix the objective and completion criteria for one task | low to medium | task-specific done conditions | bugfix prompt, feature prompt |
| `skill` | Fix a reusable workflow | medium to high | repeated steps and report format | `issue-to-plan`, `verification`, chapter drafting |
| `context pack` | Fix task-specific reading order and canonical facts | medium | read order, exclusions, done signals | `ticket-search` pack |

When these three are mixed together, the result is usually a giant prompt that tries to do planning, reading guidance, and execution at the same time. CH08 separates them so each artifact has one stable job.

## 5. Manage Skill Versioning and Breaking Changes
Skills and context packs are artifacts, so they also need change management. A change becomes breaking when it alters any part of the operational contract:

- required inputs change
- output section names change
- verify steps are added or removed
- read order depends on different artifacts

For example, if the `verification` skill stops at unit tests today but later requires evidence collection and progress-note updates before completion, that is not a wording tweak. It changes the work contract and the expected output.

Small repos do not always need an explicit version field, but they still need discipline about what counts as contract and what counts as explanation. Changes to `Purpose`, `Output Contract`, `Guardrails`, or mandatory read inputs should be treated as skill-version changes. Wording cleanup and examples usually are not breaking changes.

The goal is not to accumulate skills forever. The goal is to keep reusable workflows trustworthy. A stale skill is worse than no skill because it gives the coding agent false confidence.

## Bad / Good Example
Bad:

```text
For every issue, paste the same planning steps, the same verification steps,
and the same reading list into a long free-form prompt.
Use the same style for search work, chapter review, and PR review.
```

This approach guarantees drift. Reused workflow never becomes an artifact, and task-specific facts are mixed together with generic process instructions.

Corrected:

```text
Keep planning in `sample-repo/.agents/skills/issue-to-plan/SKILL.md`.
Keep verification in `sample-repo/.agents/skills/verification/SKILL.md`.
For `FEATURE-001`, use `sample-repo/context-packs/ticket-search.md`
as the source of truth for reading order and canonical facts.
```

This version separates reusable workflow into skills and task-specific reading input into a context pack.

Comparison points:
- The bad version never turns repeatable workflow into an artifact.
- The bad version mixes task-specific context with reusable process.
- The corrected version gives workflow to skills and task-specific reading bundles to context packs.

## Exercises
1. Create an issue-to-plan skill.
2. Create a PR review skill and fix the review criteria.

## Referenced Artifacts
- `.agents/skills/draft-chapter/SKILL.md`
- `.agents/skills/review-chapter/SKILL.md`
- `sample-repo/.agents/skills/issue-to-plan/SKILL.md`
- `sample-repo/.agents/skills/verification/SKILL.md`
- `sample-repo/context-packs/ticket-search.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `.agents/skills/draft-chapter/SKILL.md`, `.agents/skills/review-chapter/SKILL.md`, `sample-repo/.agents/skills/issue-to-plan/SKILL.md`, `sample-repo/.agents/skills/verification/SKILL.md`, and `sample-repo/context-packs/ticket-search.md`. Read the skills as reusable workflow contracts and the context pack as the task-specific minimum input.
- For the backmatter path, see `manuscript/backmatter/00-source-notes.md` under `### CH08 Skills と Context Pack を再利用する` and `manuscript/backmatter/01-読書案内.md` under `## Context と repo 設計`.

## Chapter Summary
- A skill is not just a long prompt. It is an artifact that fixes a reusable workflow and output contract.
- A context pack does not replace a task brief. It supplies the reading order, canonical facts, exclusions, and done signals for a specific task.
- Once reusable workflow and task-specific context are separated cleanly, the next problem is execution control. The next chapter moves into Harness Engineering and defines the single-agent harness.

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch08-skills-and-context-pack.md`
- This English draft preserves the same workflow reuse model, prompt-versus-skill boundary, and context-pack design rules as the Japanese chapter.
