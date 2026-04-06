# Glossary

## Purpose

This book intentionally separates concepts that are often collapsed into one another in AI-agent discussions. Prompt Engineering, Context Engineering, and Harness Engineering are related, but they solve different problems. `task brief`, `Progress Note`, and `context pack` are also different artifacts with different jobs. If the terminology drifts, the artifact boundaries drift with it.

For the English manuscript, [`docs/en/glossary.md`](../../docs/en/glossary.md) is the English counterpart used by the English chapters and appendices. It must stay aligned with the repo-wide glossary in [`docs/glossary.md`](../../docs/glossary.md), which remains the single source of truth for terminology. This appendix is the reader-facing guide: it groups the terms that are easiest to confuse and explains why the distinctions matter in practice.

## Included Artifacts

- `docs/glossary.md`
- `docs/en/glossary.md`

## 1. Terms for the maturity model

The book moves through three stages.

- `Prompt Engineering`: define the input and output contract for one task
- `Context Engineering`: select and maintain the repo, task, session, and tool context needed for that task
- `Harness Engineering`: design execution boundaries, verification, restart rules, and approval gates

The order is deliberate. If the prompt contract is weak, adding more context only wraps a weak task definition in a larger pile of text. If the context is weak, adding a harness only verifies work built on the wrong assumptions.

## 2. Terms for actors and tools

`AI agent`, `coding agent`, `ChatGPT`, and `Codex CLI` are not interchangeable.

- `AI agent`: an actor that advances work through multi-step decisions and tool use
- `coding agent`: an AI agent that reads a repo, changes code or docs or tests or artifacts, and runs verify steps
- `ChatGPT`: a conversational environment for shaping requirements, comparing options, and surfacing review angles
- `Codex CLI`: an execution environment for making repo changes, running commands, and collecting verification evidence

This distinction protects the book's core claim. Explaining a solution well in a chat is not the same as finishing the work inside a repository.

## 3. Terms for work artifacts

The most reused artifacts in the book are these.

- `Prompt Contract`: a prompt artifact that fixes objective, constraints, completion criteria, and output format for one task
- `task brief`: a task specification that restructures an issue for coding-agent execution
- `Progress Note`: a short progress record for interruption, handoff, and restart
- `context pack`: the smallest bundle of reference material required for one task
- `verification harness`: the verification system that bundles tests, lint, typecheck, evidence, CI, and approval rules

These are not just explanatory documents. They are operational inputs. A good artifact must be readable by humans and difficult for an agent to misuse.

## 4. Terms for harness operations

The later chapters depend on a second layer of terminology.

- `acceptance criteria`: the conditions a feature or change must satisfy from the specification side
- `done criteria`: the conditions that make the work complete from the operational side
- `evidence bundle`: the logs, commands, screenshots, and summaries that let a reviewer verify the result
- `Restart Packet`: the minimum input needed to resume work after interruption
- `permission policy`: the rule set that separates autonomous execution from human approval
- `work package`: the smallest unit of work that can be completed safely in one session or by one owner

The near-miss pairs matter. `acceptance criteria` and `done criteria` are close, but not identical. Meeting the spec without running verify is not done. Running verify without meeting the spec is also not done.

## 5. Spelling and naming rules

To reduce drift, the English manuscript uses these rules.

- Use repo and artifact names exactly as they appear in code and files
- Keep `sample-repo` hyphenated
- Preserve product and artifact spellings such as `ChatGPT`, `Codex CLI`, `Prompt Contract`, and `Progress Note`
- Prefer the English glossary terms in the English manuscript, even when the Japanese text allows a Japanese equivalent such as `AIエージェント`

When a new chapter or artifact is added, normalize the wording against [`docs/en/glossary.md`](../../docs/en/glossary.md) first. Early naming discipline is cheaper than retroactive terminology cleanup.

## Parity Notes

- Japanese source: `manuscript/appendices/app-d-用語集.md`
- Publication target: preserve the Japanese appendix's terminology groups, maturity-model ordering, and naming-discipline guidance while making the English glossary usable on its own.

## Referenced Artifacts

- `docs/glossary.md`
- `docs/en/glossary.md`
