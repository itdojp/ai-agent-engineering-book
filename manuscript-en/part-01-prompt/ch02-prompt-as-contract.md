---
id: ch02
title: Design Prompts as Contracts
status: drafted
source_ja: manuscript/part-01-prompt/ch02-prompt-as-contract.md
artifacts:
  - prompts/en/bugfix-contract.md
  - prompts/en/feature-contract.md
  - checklists/en/prompt-contract-review.md
dependencies:
  - ch01
---

# Design Prompts as Contracts

## Role in This Book
An AI agent can respond to almost any request, including a one-line prompt such as “improve search.” That does not mean the work boundary is clear. In CH01, the failure model showed why capable-looking agents still return wrong answers, ignore approval boundaries, or stop before the job is actually closed. The first Prompt Engineering move is to reduce that ambiguity.

In engineering work, a prompt is not a casual instruction. It is an operational artifact for a single task. It fixes the objective, inputs, constraints, tool contract, forbidden actions, completion boundary, approval conditions, and reporting schema. If those elements are vague, the agent can still produce plausible output, but it will guess where the boundary is. Single-task reliability starts with making that boundary explicit.

## Learning Objectives
- Separate objective, constraints, completion criteria, and forbidden actions together with tool-contract and approval conditions
- Design a Prompt Contract that includes a schema and `output_version`
- Build different Prompt Contracts for feature work and bugfix work and define review criteria for both

## Outline
### 1. A prompt is not an instruction sentence but an input/output contract
### 2. Separate objective, constraints, tool contract, and completion criteria
### 3. Handle assumptions, approval, and refusal conditions
### 4. Compare bad prompts and good prompts
### 5. Review prompt contracts through failure modes

## 1. A Prompt Is an Input/Output Contract
“Improve search” or “fix the bug” can produce an answer from an AI agent, but an answer is not the same thing as a contract. A contract prompt must define at least three things: what should be achieved, which tools and authority are available, and when the agent must stop.

In 2026 practice, a prompt is not merely an instruction sentence. It is the contract for one run. If the task is `BUG-001` in `sample-repo`, the objective may be “reproduce and fix the defect without changing the public interface.” Constraints may include “add or update the failing test first.” An operational prompt then goes further and fixes which tools may be used, which operations require approval, and which schema should be returned.

This chapter treats a Prompt Contract through the following nine core elements.

| Element | Role | What fails without it |
|---|---|---|
| Objective | Fix the purpose of the work in one sentence | The agent optimizes for the wrong thing |
| Inputs | Fix the artifacts and information sources to read | Wrong answers become more likely |
| Constraints | Fix the boundaries that must hold | Scope creep and accidental breakage increase |
| Tool Contract | Fix the allowed tools, commands, and external access | Tool misuse becomes more likely |
| Approval Gate | Name the operations that require human approval | Approval misses become more likely |
| Forbidden Actions | Block tempting shortcuts and risky behavior | Superficial success hides real regressions |
| Refusal / Stop Conditions | Fix when the agent must stop instead of guessing | The agent pushes into unsafe work |
| Completion Criteria | Fix what counts as done | The agent stops too early |
| Output Schema | Fix report structure and include `output_version` | Handoff and review become unstable and drift from older consumers |

Once these elements are present, the prompt stops being a loose instruction and starts behaving like an execution contract.

## 2. Separate Objective, Constraints, Tool Contract, and Completion Criteria
Weak prompts often fail because they mix goal, limits, and done conditions into one paragraph. When those categories are blended together, the agent has to infer priority and trade-offs on its own.

`prompts/en/bugfix-contract.md` and `prompts/en/feature-contract.md` show the smallest reusable templates for that separation. The center of gravity is different for bugfix work and feature work. A bugfix contract emphasizes preserving existing behavior and proving the fix with a failing test. A feature contract emphasizes staying within the written spec and acceptance criteria while updating docs and tests together.

The elements become easier to write if each one answers a different operational question.

| Element | How to write it | Example |
|---|---|---|
| Objective | State the task purpose in one sentence | `Identify the root cause of the defect and fix it with the smallest safe change.` |
| Inputs | Name the required references | `target issue`, repro steps, related tests, verify command |
| Constraints | Name the boundaries that must hold | `Do not change the public interface.` |
| Tool Contract | Name the allowed tools and commands | `Run only repo-local verify commands.` |
| Approval Gate | Name the operations that require human judgment | `Wait for approval before dependency changes or external access.` |
| Forbidden Actions | Name dangerous shortcuts explicitly | `Do not delete the failing test just to get green results.` |
| Refusal / Stop Conditions | State when the agent must stop | `Stop if the source of truth conflicts.` |
| Completion Criteria | State observable done conditions | `At least one test fails before the fix and passes after the fix.` |
| Output Schema | Fix section structure and version | `output_version: 2026-04-01` |
| Output Format | Fix the reader-facing final report | `Changed Files`, `Verification`, `Remaining Gaps` |

It is also important to separate constraints from forbidden actions. A constraint states a boundary that must hold. A forbidden action blocks a common shortcut that would hide failure. “Do not make out-of-scope UI or API changes” is a constraint. “Do not lock in an ambiguous requirement by guessing” is a forbidden action.

## 3. Handle Assumptions, Approval, and Refusal Conditions
A good Prompt Contract does not require perfect information. It requires an explicit policy for what to do when information is missing, when approval is required, or when the next operation would be risky. Weak prompts leave that behavior unspecified and silently encourage the agent to fill gaps with guesses.

For single-task reliability, missing information and approvals usually fall into four patterns.

1. The answer is already in existing artifacts.
   If the answer can be found in repo docs or tests, list those artifacts under `Inputs`.
2. A low-risk assumption can be made temporarily.
   If an assumption is acceptable, require the agent to record it in `Remaining Gaps` or `Assumptions`.
3. A human approval can unblock the task.
   Dependency changes, external calls, secret usage, or destructive changes belong under the approval gate.
4. An assumption would be unsafe.
   If guessing would materially change scope or behavior, the correct action is to stop and report the blocker.

The key point is that “what to do when you do not know” belongs inside the Prompt Contract. If the prompt never tells the agent when to stop, the model tends to fill the hole with plausible language instead of a real boundary. Later chapters improve the surrounding context with task briefs and context packs, but CH02 first fixes the behavior directly in the prompt.

## 4. Weak Prompts and Operational Prompts
The difference between a weak prompt and an operational prompt is not style. It is contract density. Start with this weak request.

```text
Improve search in sample-repo. Make it easier to use, and add tests if needed.
```

This sounds natural, but it is weak as an execution contract. The objective is vague. The agent is not told which artifacts to read. There are no explicit constraints, no completion criteria, and no reporting schema. “Make it easier to use” invites the model to invent its own success condition.

Now compare it with a more operational version tied to `FEATURE-001`.

```text
Scope this task to `FEATURE-001` in `sample-repo/docs/seed-issues.md`.
Objective: improve ticket search behavior according to the written spec without changing the existing public contract beyond that scope.
Inputs:
- `sample-repo/docs/product-specs/ticket-search.md`
- `sample-repo/docs/acceptance-criteria/ticket-search.md`
- `sample-repo/docs/design-docs/ticket-search-adr.md`
- `sample-repo/tests/test_ticket_search.py`
Constraints:
- Do not make out-of-scope UI or API changes
- Update docs and tests together with the implementation
Forbidden Actions:
- Do not add features that are not in the acceptance criteria
- Do not resolve ambiguous requirements by guessing
Completion Criteria:
- The written acceptance criteria are satisfied
- The main happy path and edge cases are covered by tests
- The specified verify command passes
Tool Contract:
- Operate only on repo code, docs, tests, and verify commands
- Do not call external APIs, add dependencies, or use secrets
Approval Gate:
- Wait for human approval before dependency changes, external access, or billable actions
Refusal / Stop Conditions:
- Stop if the source of truth conflicts
- Do not continue without approval when an approval-required operation appears
Output Schema:
- output_version: 2026-04-01
- sections: Implemented Scope, Changed Files, Verification, Remaining Gaps
```

This prompt is still short, but it contains the structure needed for reliable execution. A human reviewer can see what is in scope, which artifacts ground the task, what the agent must not do, and how completion will be judged. That is the difference between “please do something useful” and “here is the contract for this task.”

## 5. Review Prompt Contracts Through Failure Modes
A Prompt Contract is not reliable just because it exists. It has to be reviewed before execution. `checklists/en/prompt-contract-review.md` is a minimal review artifact for that step.

The review lens is simple. Do not ask whether the prompt sounds elegant. Ask whether it leaves a likely failure mode open.

1. Is the objective fixed in one sentence?
2. Are the inputs named at the artifact level?
3. Are the constraints and tool contract observable rather than vague?
4. Are the approval gate and refusal / stop conditions explicit?
5. Do the forbidden actions block predictable shortcuts?
6. Are the completion criteria verifiable?
7. Is the output schema stable for downstream consumers, including `output_version`?

This is how weak prompts reveal themselves quickly. “Update the docs if needed” is not a constraint. It is a delegation of judgment. “Do it nicely” and “make it better” have the same problem: they leave the success condition subjective. By contrast, even a plain-looking prompt can work well if the objective, inputs, completion criteria, and stop conditions are fixed clearly.

Prompt Engineering does not begin with clever phrasing. It begins with a Prompt Contract that can be reviewed before the task starts. Once that contract is stable, the next bottleneck is often upstream ambiguity in the request itself. CH03 moves there by using ChatGPT to turn vague requests into workable requirements and design artifacts.

## Bad / Good Example
Bad:

```text
Fix `BUG-001`. Do not break existing behavior, and check the tests if needed.
```

This prompt fixes only the target issue. It does not define the reproduction condition, the related artifacts, the forbidden shortcuts, the completion boundary, or the reporting format. The agent has too much room to invent its own boundary.

Good:

```text
Scope this task to `BUG-001` in `sample-repo/docs/seed-issues.md`.
Objective: reproduce and fix the defect without changing the existing public interface.
Inputs:
- reproduction steps
- related files
- `sample-repo/tests/test_service.py`
- verify command
Constraints:
- Add or update the failing test first
- Keep the diff limited to the smallest safe change
Forbidden Actions:
- Do not perform unrelated refactoring
- Do not delete a failing test just to get green results
Completion Criteria:
- At least one test fails before the fix and passes after the fix
- Existing tests and the required verify command pass
Output Format:
1. Root Cause
2. Changed Files
3. Verification
4. Remaining Gaps
```

The corrected version makes the bugfix boundary explicit. The Prompt Contract is not longer for style. It is longer because it closes the specific judgment gaps that usually cause wrong answers, accidental breakage, and early stopping.

Comparison points:
- The bad prompt never defines what counts as done.
- The good prompt fixes inputs, forbidden actions, and completion criteria.
- The good prompt also fixes the reporting format so the result can be reviewed consistently.

## Exercises
1. Use the search feature in `sample-repo` as the task and rewrite “add search” as a Prompt Contract. Include Objective, Inputs, Constraints, Forbidden Actions, Completion Criteria, and Output Format.
2. Use `BUG-001` as the task and write only the Completion Criteria in five points. Each point must be verifiable rather than subjective.

## Referenced Artifacts
- `prompts/en/bugfix-contract.md`
- `prompts/en/feature-contract.md`
- `checklists/en/prompt-contract-review.md`

## Source Notes / Further Reading
- Treat `prompts/en/bugfix-contract.md`, `prompts/en/feature-contract.md`, and `checklists/en/prompt-contract-review.md` as the primary artifacts for this chapter. In this book, a Prompt Contract is a repo artifact, not a conversation trick.
- For the next navigation step, see `manuscript-en/backmatter/00-source-notes.md` under `### CH02 Design Prompts as Contracts` and `manuscript-en/backmatter/01-reading-guide.md` under `## Prompts and Requirements Shaping`.

## Chapter Summary
- Prompt Engineering begins by designing prompts as execution contracts rather than vague instructions.
- Single-task reliability improves when Objective, Inputs, Constraints, Forbidden Actions, Tool Contract, Refusal / Stop Conditions, Approval Gate, Completion Criteria, Output Format, and Output Schema are written as separate elements.
- Once the contract is stable, the next bottleneck is often an ambiguous request. CH03 addresses that by turning vague requests into product specs, acceptance criteria, ADRs, and eval-seed-ready artifacts.

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch02-prompt-as-contract.md`
- This English draft preserves the expanded contract surface, including tool contract, approval gate, refusal conditions, and schema versioning.
