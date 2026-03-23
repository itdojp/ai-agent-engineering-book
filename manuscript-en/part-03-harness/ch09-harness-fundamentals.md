---
id: ch09
title: Foundations of Harness Engineering
status: drafted
source_ja: manuscript/part-03-harness/ch09-harness-fundamentals.md
artifacts:
  - scripts/init.sh
  - scripts/verify-sample.sh
  - sample-repo/docs/harness/single-agent-runbook.md
  - sample-repo/docs/harness/permission-policy.md
  - sample-repo/docs/harness/done-criteria.md
dependencies:
  - ch05
  - ch06
  - ch07
  - ch08
---

# Foundations of Harness Engineering

## Role in This Book
Even when repo context, task briefs, and skills are all present, a coding agent can still stop before verification, cross an approval boundary, or repeat the same failed move. CH05 through CH08 focused on what to show the agent. That is necessary, but it still does not close the work.

Harness Engineering starts where Context Engineering stops. Context Engineering designs what the agent should read. Harness Engineering designs how the agent starts, what it may touch, when it may say “done,” and how it should retry or stop. This chapter defines the minimum unit of that system: the single-agent harness. The scope here is not the full verification harness yet. The goal is to establish the minimal execution frame that lets one coding agent finish work safely.

## Learning Objectives
- Explain the components of a single-agent harness
- Understand why permission policy and escalation matter
- Make done criteria explicit

## Outline
### 1. The shape of a single-agent harness
### 2. Init, permissions, and work boundaries
### 3. Completion criteria and exit rules
### 4. Safe retry and rollback
### 5. What lets a coding agent finish the work

## 1. The Shape of a Single-Agent Harness
A single-agent harness is the execution frame for one coding agent working on one work package. A harness is not another name for a prompt. Even if the prompt and context pack are good, the work still fails when startup steps, work boundaries, permissions, verification, and exit conditions are left implicit.

In this repo, the single-agent harness has six parts:

| Component | Role | Artifact in this chapter |
|---|---|---|
| init | fixes what to read first and which verify command to use | `scripts/init.sh` |
| work boundary | limits what the current task may touch | task brief, `sample-repo/docs/harness/single-agent-runbook.md` |
| permission policy | separates autonomous changes from approval-required changes | `sample-repo/docs/harness/permission-policy.md` |
| done criteria | defines `done`, `blocked`, and `needs-human-approval` | `sample-repo/docs/harness/done-criteria.md` |
| verify command | fixes the minimum local validation | `scripts/verify-sample.sh` |
| report format | standardizes what must be reported at finish | runbook and done criteria |

`BUG-001` makes the difference clear. If the instruction is only “fix the bug,” the agent can stop after producing a plausible root-cause guess. Once the task runs inside a single-agent harness, startup inputs, permission boundaries, exit states, and verify command are fixed before the first edit begins.

CH08 completed the reusable context side. CH09 begins the execution side.

## 2. Init, Permissions, and Work Boundaries
The first job of a single-agent harness is to fix the source of truth at startup. `scripts/init.sh` prints the repo root, the `sample-repo` path, the selected task brief, the first documents to read, the runbook, the permission policy, the done criteria, and the verify command. That means the agent does not have to improvise the startup contract at the start of each session.

For `BUG-001`, the entry point is explicit:

```bash
./scripts/init.sh sample-repo/tasks/BUG-001-brief.md
```

The output is not a convenience banner. It is the startup contract for the harness.

The next requirement is a permission policy. `sample-repo/docs/harness/permission-policy.md` allows the agent to update code, docs, and tests within the task brief, add or update failing tests, run read-only investigation commands, run `./scripts/verify-sample.sh`, and update the in-scope Progress Note. But it requires human approval for public-interface changes, domain-assumption changes, verify or CI changes, dependency additions, external services, secrets, or scope expansion outside the stated work package.

The key question is not whether the agent is trustworthy in general. The key question is whether the approval boundary is embedded in repo artifacts before execution starts. A coding agent such as Codex CLI can run commands. That is exactly why the allowed surface must be narrow and explicit.

Work boundaries matter for the same reason. In `BUG-001`, the agent should begin with the task brief, the repo map, the architecture doc, and the relevant tests. At this stage, it should not wander across the entire repo. A smaller work package produces a smaller verify unit and a safer rollback unit.

## 3. Completion Criteria and Exit Rules
The center of Harness Engineering is not startup. It is exit. Many agents behave as if “I changed something” were enough to declare completion. In practice, completion means satisfying explicit done criteria.

`sample-repo/docs/harness/done-criteria.md` defines three exit states:

- `done`
- `blocked`
- `needs-human-approval`

The agent may only say `done` when the task brief's goal and acceptance criteria are satisfied, changed files stay inside the current issue or work package, code / docs / tests / task artifacts do not drift apart, and `./scripts/verify-sample.sh` passes. In other words, completion inside a harness means “the verified work package is closed,” not “a plausible change exists.”

`scripts/verify-sample.sh` gives that exit rule a mechanical check. At this stage it confirms required sample-repo docs and harness docs exist, checks task briefs, and runs unit tests. It does not yet include lint, type checking, or an evidence bundle. Those belong to CH10, where the verification harness becomes its own subject. CH09 only needs one fixed minimum verify command that must run before exit.

That separation matters. CH09 defines the frame that invokes verification. CH10 will deepen the contents of verification itself.

## 4. Safe Retry and Rollback
Retry should be designed by condition, not by count. Without a harness, an agent can easily rerun the same failed move every time verification fails. That is not progress. It is a failure loop.

`sample-repo/docs/harness/single-agent-runbook.md` classifies failure before retry:

| Failure mode | What is missing | Required action |
|---|---|---|
| `missing-context` | required artifacts were not read | identify the missing artifacts and restate scope |
| `verify-failure` | the change hypothesis is wrong | inspect the current diff and retry with the smallest correction |
| `permission-boundary` | the next change needs approval | stop and escalate |
| `environment-failure` | command, path, or tool is broken | report the exact command and stderr |

Rollback is equally important. In this chapter, rollback does not mean resetting the whole repo to a previous snapshot. It means discarding the agent's own tentative diff inside the current work package and returning to the last known good state. Unrelated user changes and unexplained external diffs must not be reverted. This is an execution-safety rule, not just a Git preference.

Safe retry always includes reclassification and scope reduction. Repeating the same verify command with no new hypothesis and no new input is a harness failure.

## 5. What Lets a Coding Agent Finish the Work
For a coding agent to finish work reliably, five conditions must be present:

1. one clear startup command
2. artifact-defined work and permission boundaries
3. explicit exit states: `done`, `blocked`, `needs-human-approval`
4. one fixed verify command
5. retry and rollback units that stay small

Without these conditions, the agent either stops too early or keeps going past the correct stopping point. The first failure mode maps to “stopping early.” The second maps to “breaking things.” From the CH01 perspective, Harness Engineering is one way to suppress those failure modes with artifacts instead of hope.

Even when task briefs, context packs, and skills are present, the last ten percent of the work still fails if startup, permission, exit, and retry remain vague. In practice, that last ten percent is where teams lose trust. Harness Engineering exists to make that part explicit.

## Reader-facing Table
### Single-Agent Harness Flow

| Stage | What it fixes | Main artifact or command | Failure it prevents |
|---|---|---|---|
| init | reading order and verify command | `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md` | confusion at task start |
| boundary | task scope and editable surface | task brief, runbook | scope expansion |
| permission | approval-required changes | `sample-repo/docs/harness/permission-policy.md` | unauthorized contract changes |
| verify | minimum validation line | `./scripts/verify-sample.sh` | stopping before verification |
| exit | `done / blocked / needs-human-approval` | `sample-repo/docs/harness/done-criteria.md` | ambiguous finish conditions |
| report | `Changed Files`, `Verification`, `Remaining Gaps` | runbook, done criteria | non-reviewable completion reports |

This order shows that the single-agent harness is not advanced automation. It is a disciplined way to fix start and finish conditions. It is also why `verify` and `exit` stay separate. Green tests alone do not guarantee that scope, approvals, or reporting obligations were handled correctly.

## Bad / Good Example
Bad:

```text
Fix BUG-001.
Check the tests if necessary, and report back when you think it is done.
```

This instruction has no startup condition, no approval boundary, no verify command, and no done criteria. The agent may still produce a plausible answer, but it has no reliable place to stop.

Corrected:

```text
Use `sample-repo/tasks/BUG-001-brief.md` as the source of truth.
Start by running `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md`.
Any change beyond `sample-repo/docs/harness/permission-policy.md`
requires approval.
You may say `done` only if `sample-repo/docs/harness/done-criteria.md`
is satisfied and `./scripts/verify-sample.sh` passes.
Report `Changed Files`, `Verification`, and `Remaining Gaps`.
```

This version fixes startup, boundary, verification, and exit as one execution frame.

Comparison points:
- The bad version tries to run the task with prompt text alone.
- The bad version leaves a large gap for stopping before verification.
- The corrected version defines init, permission policy, done criteria, and verify as one harness.

## Worked Example
Use the single-agent harness for `BUG-001`, the case where stale state appears after a status update and reload.

1. Startup
   - run `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md`
2. Read
   - `AGENTS.md`
   - `sample-repo/AGENTS.md`
   - `sample-repo/tasks/BUG-001-brief.md`
   - `sample-repo/docs/repo-map.md`
   - `sample-repo/docs/architecture.md`
   - `sample-repo/tests/test_service.py`
3. Confirm boundaries
   - do not change the public interface
   - do not change the verify script
   - keep the diff limited to the minimum bugfix and regression guard
4. Execute
   - reproduce the failing behavior in a test, or extend the existing regression guard
   - identify the root cause and fix it inside the allowed scope
   - run `./scripts/verify-sample.sh`
5. Exit
   - if verify passes, root cause is explained, and `Remaining Gaps` is short, return `done`
   - if the next change crosses the approval boundary, return `needs-human-approval`
   - if the brief and tests conflict and no source of truth can be chosen, return `blocked`

The point of this example is not automation theater. The point is to show that Harness Engineering fixes how work starts and how work ends.

## Exercises
1. Design a single-agent runbook for a bugfix task.
2. Define a permission policy and escalation rule.

## Referenced Artifacts
- `scripts/init.sh`
- `scripts/verify-sample.sh`
- `sample-repo/docs/harness/single-agent-runbook.md`
- `sample-repo/docs/harness/permission-policy.md`
- `sample-repo/docs/harness/done-criteria.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `scripts/init.sh`, `sample-repo/docs/harness/single-agent-runbook.md`, `sample-repo/docs/harness/permission-policy.md`, and `sample-repo/docs/harness/done-criteria.md`. Read the single-agent harness as a bundle of startup, boundary, and exit conditions rather than as a prompt variant.
- For the backmatter path, see `manuscript/backmatter/00-source-notes.md` under `### CH09 Harness Engineering の基礎` and `manuscript/backmatter/01-読書案内.md` under `## 検証・信頼性・運用`.

## Chapter Summary
- Context Engineering decides what the agent sees. Harness Engineering decides how the agent starts, where it must stop, and what must be true before it may declare completion.
- The minimum single-agent harness consists of init, work boundary, permission policy, done criteria, verify command, and retry rule.
- Once start and exit conditions are stable, the next missing piece is a verification chain that reviewers can trust. The next chapter focuses on the verification harness itself.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch09-harness-fundamentals.md`
- This English draft preserves the same single-agent harness model, bugfix example, and boundary rules as the Japanese chapter.
