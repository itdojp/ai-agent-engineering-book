---
id: ch09
title: Foundations of Harness Engineering
status: drafted
source_ja: manuscript/part-03-harness/ch09-harness-fundamentals.md
artifacts:
  - scripts/init.sh
  - scripts/verify-sample.sh
  - scripts/check-guardrail-coverage.py
  - docs/en/guardrail-coverage-matrix.md
  - evals/guardrail-surface-cases.json
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

Modern runtimes may provide convenience features such as background execution, hosted tools, and managed context. Those mechanisms can reduce execution friction, but they do not remove repo responsibility for approval boundaries, artifact sync, verify, or review. Making that distinction reader-facing is part of this chapter's job.

## Learning Objectives
- Explain the components of a single-agent harness
- Understand why permission policy and escalation matter
- Explain guardrail coverage and blind spots per tool surface and external-service boundary
- Make done criteria explicit

## Outline
### 1. The shape of a single-agent harness
### 2. Init, permissions, and work boundaries
### 3. Completion criteria and exit rules
### 4. Safe retry and rollback
### 5. What lets a coding agent finish the work

## 1. The Shape of a Single-Agent Harness
A single-agent harness is the execution frame for one coding agent working on one work package. A harness is not another name for a prompt. Even if the prompt and context pack are good, the work still fails when startup steps, work boundaries, permissions, verification, and exit conditions are left implicit.

In this repo, the single-agent harness has seven parts:

| Component | Role | Artifact in this chapter |
|---|---|---|
| init | fixes what to read first and which verify command to use | `scripts/init.sh` |
| work boundary | limits what the current task may touch | task brief, `sample-repo/docs/harness/single-agent-runbook.md` |
| permission policy | separates autonomous changes from approval-required changes | `sample-repo/docs/harness/permission-policy.md` |
| external input boundary | checks classification, redaction, provider terms, and per-surface guardrail coverage before AI / external-service submission | `docs/en/guardrail-coverage-matrix.md`, permission policy, and `checklists/en/verification.md` |
| done criteria | defines `done`, `blocked`, and `needs-human-approval` | `sample-repo/docs/harness/done-criteria.md` |
| verify command | fixes the minimum local validation | `scripts/verify-sample.sh` |
| report format | standardizes what must be reported at finish | runbook and done criteria |

`BUG-001` makes the difference clear. If the instruction is only “fix the bug,” the agent can stop after producing a plausible root-cause guess. Once the task runs inside a single-agent harness, startup inputs, permission boundaries, exit states, and verify command are fixed before the first edit begins.

This is also where runtime-managed capability diverges from harness-owned duty. Background execution and hosted tools help with how the work runs, but the repo still has to fix which task brief is the source of truth, where approval begins, and which verify line counts as done. Managed context does not remove artifact sync or report format.

To decide whether a runtime-managed loop is enough or whether a repo-owned manual harness should remain explicit, use the following table. The baseline is fixed: final review / merge remains human-owned, and source-of-truth artifacts remain repo-owned even when the runtime manages execution state.

| Decision factor | When a runtime-managed loop is enough | When a repo-owned manual harness should stay explicit |
|---|---|---|
| human approval | there is no extra approval gate beyond final review | human approval is needed before, during, or after execution |
| evidence / audit trail | runtime status and current-run verify are enough for review | task-specific evidence bundles or audit-oriented records must be preserved |
| stop / resume logic | the run is linear and closes with simple retry | conditional stop / resume, retry classification, or handoff must be fixed in repo artifacts |
| source of truth | the task brief, runbook, and done criteria remain fixed during the run | artifact sync, refresh policy, or owned files must stay explicit during the run |
| review responsibility | the reviewer can read the runtime result as-is | `Changed Files`, `Verification`, and `Remaining Gaps` need explicit packaging for review |

In other words, a runtime-managed loop is a question of whether the mechanism is sufficient, not a question of whether responsibility disappears. Once approval, evidence, stop / resume, or artifact sync become custom, it is unsafe to thin the repo-owned manual harness too far.

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

#### AI / external-service submission and tool guardrails

AI / external-service submission does not become safe just because secrets are absent. Issues, PRs, logs, eval cases, traces, and evidence bundles may contain customer data, personal data, sensitive data, unpublished specifications, vulnerability information, or internal decision traces. Before sending them to an external API, hosted tool, web search, tracing surface, or eval judge, confirm the data classification, redaction, provider retention / training-use / logging terms, storage location, and approver.

Treat that check as the `external input boundary`. This boundary covers not only whether a tool call is allowed, but also what granularity may be sent, where output may be stored, and what trace may be retained. Guardrails sit before and after the boundary to block secret values, personal data, out-of-scope tool calls, and approval-required operations. They do not replace final review, current-run verify, or human approval.

`docs/en/guardrail-coverage-matrix.md` divides this boundary into external input, model output, tool definition, tool call, tool execution, tool result, resource, trace, session, external-service, protocol prompts / roots, and protocol sampling / elicitation surfaces. Check classification, redaction, permission, approval, storage / retention, and verification independently at each surface. In particular, tool definitions, tool results, server prompts, and resource content are external input, not trusted instructions. Do not close a side effect at argument inspection; require immediate approval, least privilege, a postcondition, and rollback evidence.

| Surface | Minimum controls | Representative blind spot |
|---|---|---|
| external input | provenance, classification, redaction | mid-chain retrieval and tool results can sit outside an ingress guardrail |
| model output | destination-specific reclassification plus schema and fact checks | intermediate-agent output and tool arguments can sit outside final-output inspection |
| tool definition | trusted registry, version, and capability checks | descriptions and annotations can contain instruction injection |
| tool call | permission checks for arguments, paths, hosts, and payloads | teams can assume the same coverage for unattached tool types |
| tool execution | least privilege, immediate approval, and postconditions | argument checks do not enforce OS permissions or irreversible side effects |
| tool result | reclassification as untrusted input plus provenance checks | stdout, web, or MCP results can become the next instruction |
| resource | path, domain, and URI allowlists plus integrity and freshness | file or resource retrieval can use a path outside tool-call guardrails |
| trace / log | redaction, viewer restrictions, retention, and leakage scans | tracing SDKs, CI logs, and artifact uploads may not be inspected automatically |
| session / memory | task boundary, TTL, refresh / invalidation, and source-of-truth checks | persisted secrets and stale context survive ingress checks |
| external service | provider, purpose, region, retention, and training-use checks | a local guardrail cannot enforce provider storage or subprocessor behavior |
| protocol prompts / roots | server, prompt, and root allowlists plus prompt provenance and host ACLs or sandboxes | prompt discovery does not establish instruction trust, and root notification does not enforce a filesystem boundary |
| protocol sampling / elicitation | request and destination display, explicit approval, and field restrictions | the protocol does not guarantee a host consent UI or policy enforcement |

State what the coverage applies to. If a runtime applies input guardrails only at chain ingress, output guardrails only to the final agent, or tool guardrails only to attached function tools, then retrieval, hosted tools, MCP resources, intermediate agents, traces, and sessions need separate controls. Check official runtime documentation and make the permission policy return `deny` or `escalate` for an unknown or uncovered surface.

The minimum walkthrough is fixed in `evals/guardrail-surface-cases.json`. It covers hostile input, hostile tool output, tainted tool metadata, unsafe side effects, trace leakage, stale or sensitive sessions, and external-provider boundaries with required controls, expected decisions, and verification evidence. `scripts/check-guardrail-coverage.py` rejects fixtures that omit a required surface or control so that prose cannot drift away from the verification contract.

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
For a coding agent to finish work reliably, the seven harness components must be explicit in artifacts and commands:

1. a clear `init` command
2. an artifact-defined work boundary, including owned files
3. a permission policy that stops approval-required operations
4. an external-input boundary with guardrail-coverage checks before AI / external-service submission
5. done criteria that separate `done`, `blocked`, and `needs-human-approval`
6. one fixed verify command that must pass before completion
7. a report format that includes Exit State, Changed Files, Verification, and Remaining Gaps

Retry and rollback are operating rules applied by failure mode without weakening those seven components. Without these components, the agent either stops too early or keeps going past the correct stopping point. The first failure mode maps to “stopping early.” The second maps to “breaking things.” From the CH01 perspective, Harness Engineering is one way to suppress those failure modes with artifacts instead of hope.

Even when task briefs, context packs, and skills are present, the last ten percent of the work still fails if init, work boundary, permission policy, external-input boundary, done criteria, verify command, and report format remain vague. In practice, that last ten percent is where teams lose trust. Harness Engineering exists to make that part explicit.

## Reader-facing Table
### Single-Agent Harness Components

| Component | What it fixes | Main artifact or command | Failure it prevents |
|---|---|---|---|
| init | reading order and verify command | `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md` | confusion at task start |
| work boundary | task scope and editable surface | task brief, runbook | scope expansion |
| permission policy | approval-required changes | `sample-repo/docs/harness/permission-policy.md` | unauthorized contract changes |
| external input boundary | AI / external-service submission and per-surface guardrail coverage | `docs/en/guardrail-coverage-matrix.md`, permission policy, and verification checklist | sensitive data or out-of-scope tool use |
| done criteria | `done / blocked / needs-human-approval` | `sample-repo/docs/harness/done-criteria.md` | ambiguous finish conditions |
| verify command | minimum validation line | `./scripts/verify-sample.sh` | stopping before verification |
| report format | `Changed Files`, `Verification`, `Remaining Gaps` | runbook, done criteria | non-reviewable completion reports |

This component list shows that the single-agent harness is not advanced automation. It is a disciplined way to fix start and finish conditions. It is also why `verify` and `exit` stay separate. Green tests alone do not guarantee that scope, approvals, external-input boundaries, or reporting obligations were handled correctly.

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
Limit owned files to `sample-repo/src/support_hub/service.py` and `sample-repo/tests/test_service.py`.
Any change beyond `sample-repo/docs/harness/permission-policy.md`
requires approval.
Classify and redact issue, PR, log, and evidence data before sending it to AI or external services.
You may say `done` only if `sample-repo/docs/harness/done-criteria.md`
is satisfied and `./scripts/verify-sample.sh` passes.
Put the `Exit State` first.
Report `Changed Files`, `Verification`, and `Remaining Gaps`.
```

This version fixes init, work boundary, permission policy, external-input boundary, done criteria, verify command, and report format as one execution frame.

Comparison points:
- The bad version tries to run the task with prompt text alone.
- The bad version leaves a large gap for stopping before verification.
- The corrected version defines init, work boundary, permission policy, external-input boundary, done criteria, verify command, and report format as one harness.

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
   - limit owned files to `src/support_hub/service.py` and `tests/test_service.py`
   - do not change the verify script
   - make no AI / external-service submission; if it becomes necessary, stop at the external-input boundary and permission policy
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
2. Build a coverage matrix for hostile input, tool output, and trace leakage, then connect it to the permission policy and escalation rule.

## Referenced Artifacts
- `scripts/init.sh`
- `scripts/verify-sample.sh`
- `scripts/check-guardrail-coverage.py`
- `docs/en/guardrail-coverage-matrix.md`
- `evals/guardrail-surface-cases.json`
- `sample-repo/docs/harness/single-agent-runbook.md`
- `sample-repo/docs/harness/permission-policy.md`
- `sample-repo/docs/harness/done-criteria.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `scripts/init.sh`, `docs/en/guardrail-coverage-matrix.md`, `evals/guardrail-surface-cases.json`, `sample-repo/docs/harness/single-agent-runbook.md`, `sample-repo/docs/harness/permission-policy.md`, and `sample-repo/docs/harness/done-criteria.md`. Read the single-agent harness as a bundle of init, work boundary, permission policy, external-input boundary, done criteria, verify command, and report format rather than as a prompt variant.
- For the backmatter path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH09 Foundations of Harness Engineering` and `manuscript-en/backmatter/01-reading-guide.md` under `## Verification, Reliability, and Operations`.

## Chapter Summary
- Context Engineering decides what the agent sees. Harness Engineering decides how the agent starts, where it must stop, and what must be true before it may declare completion.
- The minimum single-agent harness consists of init, work boundary, permission policy, external-input boundary, done criteria, verify command, and report format. Retry rules are operating rules applied to failure modes on top of that structure.
- Runtime-managed loops may improve mechanism, but approval boundaries, artifact sync, and review-ready reporting still remain repo-owned duties.
- Once start and exit conditions are stable, the next missing piece is a verification chain that reviewers can trust. The next chapter focuses on the verification harness itself.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch09-harness-fundamentals.md`
- This English draft preserves the same single-agent harness model, bugfix example, and boundary rules as the Japanese chapter.
