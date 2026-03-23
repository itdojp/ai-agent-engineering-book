---
id: ch02
title: Design Prompts as Contracts
status: drafted
source_ja: manuscript/part-01-prompt/ch02-prompt-as-contract.md
artifacts:
  - prompts/bugfix-contract.md
  - prompts/feature-contract.md
  - checklists/prompt-contract-review.md
dependencies:
  - ch01
---

# Design Prompts as Contracts

## Role in This Book
An AI agent can respond to almost any request, including a one-line prompt such as “improve search.” That does not mean the work boundary is clear. In CH01, the failure model explained why capable-looking agents still return wrong answers, forget important context, break working behavior, or stop before the job is actually done. The first Prompt Engineering move is to reduce that ambiguity.

In engineering work, a prompt is not a casual instruction. It is a Prompt Contract that fixes the objective, inputs, constraints, forbidden actions, completion criteria, and reporting shape for one task. If those elements are vague, the agent can still produce plausible output, but it will guess where the boundary is. Single-task reliability starts with making that boundary explicit.

## Learning Objectives
- Separate objective, constraints, completion criteria, and forbidden actions
- Compare weak prompts and operational prompts with explicit review criteria
- Build different prompt contracts for feature work and bugfix work

## Outline
### 1. A prompt is an input/output contract
### 2. Separate objective, constraints, completion criteria, and forbidden actions
### 3. State assumptions and handle missing information
### 4. Compare bad prompts and good prompts
### 5. Review prompts as operational artifacts

## 1. A Prompt Is an Input/Output Contract
“Improve search” or “fix the bug” can produce an answer from an AI agent, but an answer is not the same thing as a contract. A contract prompt must define at least two things. First, it must make the target outcome explicit. Second, it must describe the allowed and forbidden behavior in observable terms.

In practice, a prompt is not a substitute for a full requirements document. It is the minimum execution contract for a bounded task. For example, if the task is `BUG-001` in `sample-repo`, the objective might be “reproduce and fix the defect without changing the public interface.” A constraint might be “add or update the failing test first.” The point is not to sound persuasive. The point is to make the work boundary hard to misread.

This book treats a Prompt Contract as six elements.

| Element | Role | What fails without it |
|---|---|---|
| Objective | Fix the purpose of the task in one sentence | The agent optimizes for the wrong thing |
| Inputs | Fix the artifacts and information sources to read | Wrong answers become more likely |
| Constraints | Fix the boundaries that must be preserved | Scope creep and accidental breakage increase |
| Forbidden Actions | Block dangerous shortcuts | Superficial success hides real regressions |
| Completion Criteria | Fix what counts as done | The agent stops too early |
| Output Format | Fix the reporting shape | Review and handoff become unstable |

Once these six elements are present, the prompt stops being a loose instruction and starts behaving like an execution contract.

## 2. Separate Objective, Constraints, Completion Criteria, and Forbidden Actions
Weak prompts often fail because they mix goal, limits, and done conditions into one paragraph. When those categories are blended together, the agent has to infer priority and trade-offs on its own. That is exactly where unnecessary breakage and premature stopping tend to enter.

`prompts/bugfix-contract.md` and `prompts/feature-contract.md` show the smallest reusable templates for that separation. The center of gravity is different for bugfix work and feature work. A bugfix contract emphasizes preserving existing behavior and proving the fix with a failing test. A feature contract emphasizes staying within the written spec and acceptance criteria while updating docs and tests together.

The six elements become easier to write if each one answers a different question.

| Element | Question it answers | Example |
|---|---|---|
| Objective | What should this task accomplish? | `Identify the root cause of the defect and fix it with the smallest safe change.` |
| Inputs | What evidence must the agent read first? | `issue`, repro steps, relevant tests, relevant docs, verify command |
| Constraints | What boundaries must remain intact? | `Do not change the public interface.` |
| Forbidden Actions | What tempting shortcuts are disallowed? | `Do not delete the failing test just to get green results.` |
| Completion Criteria | What observable evidence proves the task is done? | `A test fails before the fix and passes after the fix.` |
| Output Format | How must the agent report the result? | `Files Changed`, `Verification`, `Remaining Risk` |

It is also important to separate constraints from forbidden actions. A constraint states a boundary that must hold. A forbidden action blocks a common shortcut that would hide failure. “Do not make out-of-scope UI or API changes” is a constraint. “Do not lock in an ambiguous requirement by guessing” is a forbidden action. The former protects scope. The latter protects the task against a known failure mode.

## 3. State Assumptions and Handle Missing Information
An operational Prompt Contract does not require complete information. It requires an explicit policy for what to do when information is missing. Weak prompts leave that behavior unspecified and silently encourage the agent to fill gaps with guesses. That is a direct path to wrong answers.

Suppose `FEATURE-001` is still underspecified and the search behavior is not fully written down. The feature prompt should not ask the agent to “use best judgment.” It should state that missing information must either be resolved from existing artifacts, surfaced as an assumption, or treated as a blocker. CH02 is still at the prompt level, so the goal here is not to solve context quality yet. The goal is to stop hidden guesswork inside a single task.

For single-task reliability, missing information usually falls into three patterns.

1. The answer is already in existing artifacts.  
   If the answer can be found in `sample-repo` docs or tests, list those artifacts under `Inputs`.
2. A low-risk assumption can be made temporarily.  
   If an assumption is acceptable, require the agent to list it explicitly in the final report.
3. An assumption would be unsafe.  
   If guessing would change scope or behavior materially, the correct action is to stop and report the gap.

The key point is that “what to do when you do not know” belongs inside the Prompt Contract. If the prompt never tells the agent when to stop, the model tends to fill the hole with plausible language instead of a real boundary.

## 4. Weak Prompts and Operational Prompts
The difference between a weak prompt and an operational prompt is not style. It is contract density. Start with this weak request.

```text
Improve search in sample-repo. Make it easier to use, and add tests if needed.
```

This sounds natural, but it is weak as an execution contract. The objective is vague. The agent is not told which artifacts to read. There are no explicit constraints, no completion criteria, and no reporting shape. “Make it easier to use” invites the model to invent its own success condition.

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
Output Format:
1. Implemented Scope
2. Files Changed
3. Verification
4. Open Questions
```

This prompt is still short, but it contains the structure needed for reliable execution. A human reviewer can see what is in scope, which artifacts ground the task, what the agent must not do, and how completion will be judged. That is the difference between “please do something useful” and “here is the contract for this task.”

## 5. Review Prompt Contracts Before Execution
A Prompt Contract is not reliable just because it exists. It has to be reviewed before execution. `checklists/prompt-contract-review.md` is a minimal review artifact for that step.

The review lens is simple. Do not ask whether the prompt sounds elegant. Ask whether it leaves a likely failure mode open.

1. Is the objective fixed in one sentence?
2. Are the inputs named at the artifact level?
3. Are the constraints observable rather than vague?
4. Do the forbidden actions block predictable shortcuts?
5. Are the completion criteria verifiable?
6. Does the output format make review and handoff easier?

This is how weak prompts reveal themselves quickly. “Update the docs if needed” is not a constraint. It is a delegation of judgment. “Do it nicely” and “make it better” have the same problem: they leave the success condition subjective. By contrast, even a plain-looking prompt can work well if the objective, inputs, and completion criteria are fixed clearly.

Prompt Engineering does not begin with clever phrasing. It begins with a Prompt Contract that can be reviewed before the task starts. Once that contract is stable, the next bottleneck is often upstream ambiguity in the request itself. CH03 moves there by using ChatGPT to turn vague requests into workable requirements and design artifacts.

## Bad / Good Example
Bad:

```text
Fix BUG-001. Do not break existing behavior, and check the tests if needed.
```

This prompt fixes only the target issue. It does not define the repro condition, the related artifacts, the forbidden shortcuts, the completion boundary, or the reporting format. The agent has too much room to invent its own boundary.

Corrected:

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
2. Files Changed
3. Verification
4. Remaining Risk
```

The corrected version makes the bugfix boundary explicit. The Prompt Contract is not longer for style. It is longer because it closes the specific judgment gaps that usually cause wrong answers, accidental breakage, and early stopping.

Comparison points:
- The bad prompt never defines what counts as done.
- The corrected prompt fixes inputs, forbidden actions, and completion criteria.
- The corrected prompt also fixes the reporting format so the result can be reviewed consistently.

## Exercises
1. Use the search feature in `sample-repo` as the task and rewrite “add search” as a Prompt Contract. Include Objective, Inputs, Constraints, Forbidden Actions, Completion Criteria, and Output Format.
2. Use `BUG-001` as the task and write only the Completion Criteria in five points. Each point must be verifiable rather than subjective.

## Referenced Artifacts
- `prompts/bugfix-contract.md`
- `prompts/feature-contract.md`
- `checklists/prompt-contract-review.md`

## Source Notes / Further Reading
- Treat `prompts/bugfix-contract.md`, `prompts/feature-contract.md`, and `checklists/prompt-contract-review.md` as the primary artifacts for this chapter. In this book, a Prompt Contract is a repo artifact, not a conversation trick.
- For the next navigation step, see `manuscript/backmatter/00-source-notes.md` under `### CH02 プロンプトを契約として設計する` and `manuscript/backmatter/01-読書案内.md` under `## Prompt と要求定義`.

## Chapter Summary
- Prompt Engineering begins by designing prompts as execution contracts rather than vague instructions.
- Single-task reliability improves when Objective, Inputs, Constraints, Forbidden Actions, Completion Criteria, and Output Format are written as separate elements.
- Once the contract is stable, the next bottleneck is often an ambiguous request. CH03 addresses that by turning vague requests into product specs, acceptance criteria, and design decisions.

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch02-prompt-as-contract.md`
- This English draft preserves the same single-task reliability scope, the same bad/corrected example pattern, and the same artifact references as the Japanese chapter.
