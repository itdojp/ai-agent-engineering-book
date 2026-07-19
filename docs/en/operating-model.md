# Operating Model

## Purpose

The minimum operating model for putting AI agents into team workflows. It fixes responsibility split, review budget, cadence, rollout stages, and what to do when the budget is exceeded.

## Operating Principles

- keep `1 issue = 1 work package`
- keep humans as the accountability owner and agents as the execution worker
- do not treat a diff without current-run verify as review-ready
- when the review budget is exceeded, reduce the queue before opening new work
- make entropy cleanup part of the cadence instead of leaving it for later
- record review completion, deployment approval, and production confirmation as separate decisions

## Runtime-managed capability and team-owned duty

A runtime can provide mechanisms such as background execution, hosted tools, and managed context. The repo or team still has to define and operate the duties below.

| Area | What the runtime may provide | Duty the repo or team must keep |
|---|---|---|
| execution | background execution, job status, reconnect support | issue-sized work packages, stop conditions, retry conditions |
| capability | hosted tools, external connections, resource access | permission boundaries, approval rules, secret handling |
| context | managed context, session storage | source of truth, artifact sync, refresh policy |
| verification | verify-job execution and display | which verify steps are required and what evidence is sufficient |
| review | status surfaces and diff display | final review, approval, and merge decisions |

The runtime provides mechanisms, not policy. If that distinction becomes blurry, convenience features hide responsibility instead of removing it.

## Deciding Between a Runtime-managed Loop and a Repo-owned Manual Harness

Final review and merge always remain human-owned, and source-of-truth artifacts remain repo-owned. With that fixed, decide whether a runtime-managed loop is enough or whether a manual harness should stay explicit by using the table below.

| Decision Factor | When a runtime-managed loop is enough | When a repo-owned manual harness is still required |
|---|---|---|
| human approval | there is no additional approval gate beyond final review | the team wants artifact-managed approval before, during, or after execution |
| evidence / audit trail | runtime status and verify results are enough to explain the work | a custom evidence bundle or audit-oriented record must be preserved |
| stop / resume logic | the run is linear and closes with simple retry and simple stop behavior | conditional stop / resume, handoff, or retry rules must be preserved explicitly |
| source-of-truth maintenance | the task brief and done criteria stay fixed during the run | artifact sync, refresh policy, or owned files must stay explicit during the run |
| review packaging | the reviewer can read the runtime surface as-is | `Changed Files`, `Verification`, and `Remaining Gaps` need custom packaging |

The key test is not whether the runtime feels convenient. The key test is how much custom policy and evidence the team still needs. As those needs grow, it becomes unsafe to thin the repo-owned manual harness too far.

## Responsibilities

### Human / Team

- set objectives and priorities
- make important design decisions
- approve destructive changes and approval-boundary decisions
- maintain artifact sync and source of truth
- perform final review and decide on merge
- maintain repo hygiene and entropy cleanup

### Agent

- explore the existing repo
- make routine edits and scoped implementation changes
- update tests, docs, and artifacts
- run verify
- explain the resulting diff

## Human Role Split

### Lead

- decide issue priority and work-package size
- approve destructive changes, public-contract changes, and operating-policy changes
- decide how to throttle new work when the review budget is exceeded

### Operator

- prepare briefs, artifacts, and verify inputs for agent execution
- leave current-run verify and evidence in the PR
- make `Remaining Gaps` explicit and avoid ambiguous completion claims

### Reviewer

- inspect `Goal`, `Changed Files`, `Scope and Non-goals`, `Verification`, `Evidence / Approval`, and `Remaining Gaps`
- check docs drift, artifact drift, and scope drift
- decide whether the PR is mergeable or whether more verify is required

### Delivery Owner

- finalize the target, marker, metric, and halt / rollback / restart conditions in the production-ready plan
- inspect the target deployment and production evidence, then record either `Production Confirmed` or `Halted`
- record rollback and restart decisions with owner, timestamp, and evidence location

In a one-person operation, the same person may hold Lead, Operator, Reviewer, and Delivery Owner roles. That person must not collapse review completion, deployment approval, and production confirmation into one checkbox. Keep separate timestamps, target SHAs, and evidence for each decision.

## Delivery State Model

A merge closes code review; it does not prove production success. A work package that affects production moves through the following states.

| State | Entry condition | Owner | Required evidence | Exit condition |
|---|---|---|---|---|
| `Review Complete` | review bodies, inline comments, and suggestions handled; zero unresolved threads; green CI | Reviewer | review responses, thread status, CI URL | merge decision recorded |
| `Production Ready` | the production-ready record below is complete and rollback is possible | Delivery Owner | target, SHA/version, routes/markers, metric, owner, rollback plan | deployment start approved |
| `Deployment Approved` | required environment or equivalent protection conditions passed, or non-applicability recorded | Approver | approval/deployment record or `N/A` reason | deployment job started |
| `Deployed` | deployment job for the target artifact succeeded | Operator | deployment and workflow URL for the target SHA | production smoke started |
| `Production Confirmed` | HTTP, semantic markers, representative routes, and metrics match expectations | Delivery Owner | confirmation record with owner and timestamp | work package may close |
| `Halted` | deployment failed/is unknown, marker mismatch, route failure, or metric breach | Delivery Owner | halt reason, observations, impact, next decision | rollback or remediation chosen |
| `Rollback in Progress` | approved rollback started | Operator | rollback change such as a revert PR and deployment URL | rollback production rechecked |

`Deployment Approved` is a control decision that allows a change to enter an environment. It does not prove deployment success or production health. `Deployed` proves only that an artifact was sent. Do not claim completion until `Production Confirmed`.

## Production-ready Gate

Before merge, record the following in the PR or linked issue. For a non-applicable change, write `N/A` and the reason.

- target environment and public URL
- where the post-merge SHA/version will be recorded and which semantic marker production must expose
- deploy owner, production-confirmation owner, and approver when one is required
- root smoke plus representative routes and expected HTTP status / content marker
- metric name, baseline, allowed threshold, observation window, and source
- halt conditions, rollback method, and restart conditions
- locations for workflow, deployment, HTTP, and metric evidence

## Post-deploy Confirmation

The Delivery Owner checks evidence tied to the target SHA instead of relying on an aggregate status or a screen that merely appears to be current.

1. Match deployment status and workflow run to the target SHA/version.
2. Run an HTTP smoke against the target URL and check representative-route status.
3. Compare a semantic marker such as SHA, version, or release-specific text rather than relying only on the title.
4. Observe the predefined metric for its complete observation window.
5. Record owner, UTC timestamp, observed values, and evidence URLs in the linked issue or PR.

If repository-level aggregate status disagrees with the target deployment, record the discrepancy and use the target-SHA deployment, workflow, and public URL/marker as the decision evidence. If the discrepancy cannot be explained, move to `Halted`.

## Halt, Rollback, and Restart

| Trigger | Action | Evidence that blocks completion | Restart condition |
|---|---|---|---|
| deployment `failure` / `cancelled` / prolonged `unknown` | move to `Halted` and classify the cause before rerun | workflow/deployment URL, log, target SHA | cause and retry scope approved |
| SHA/version/marker mismatch | stop traffic or further rollout | expected/actual marker and HTTP response | correct artifact deployed and rechecked |
| representative-route failure | record impact and decide rollback | route, status, response marker | root and representative routes healthy |
| metric exceeds threshold | preserve the window and roll back | baseline, threshold, actual value, window | post-rollback or post-fix window is healthy |

Use a new main commit such as a reviewed revert PR as the default rollback; do not rewrite history. Rerunning a historical source-built Pages workflow uses the original run's SHA/ref and can make production diverge from main, so a historical rerun is not the default rollback. Restart only after cause, remediation, re-verification, and an explicit restart decision are present.

## Deployment Scenario Walkthrough

### Success

Complete review, create the production-ready record, and merge. The target-SHA deployment succeeds; the root and representative route return HTTP 200; the semantic marker matches; and the metric stays within threshold. The Delivery Owner records timestamped evidence and moves the work package to `Production Confirmed`.

### Deployment Failure or Unknown

If deployment fails or remains unknown beyond the defined timeout, move to `Halted`. Do not close the work merely because CI was green or merge completed. Preserve the run/deployment URL, failed stage, target SHA, and impact. Start a new run only after the cause and retry scope are approved.

### Marker or Metric Regression and Rollback

Even if deployment itself succeeds, a marker mismatch or metric breach moves the work to `Rollback in Progress`. Review and merge a revert PR, then deploy the new main SHA. Repeat the same HTTP, marker, and metric checks after rollback. Do not begin another rollout until root cause, remediation, re-verification, and the restart decision are all recorded.

## Review Budget

- one reviewer should hold at most two deep reviews at once
- one reviewer should hold at most one PR that requires an evidence bundle
- if more than three stale drafts accumulate, reduce the queue before opening another work package
- when the review budget is exceeded, close or finish existing PRs before opening new work

## Budget Overflow Actions

1. stop starting new issues
2. inventory stale drafts and blocked PRs
3. cut work packages into smaller units
4. close verify gaps and evidence gaps before new implementation starts

## Cadence

1. cut one issue into one work package
2. prepare the task brief and related artifacts
3. let the agent implement and run verify
4. let humans review and approve
5. for production-affecting work, confirm the production-ready plan before merge and deployment
6. confirm production evidence for the target SHA, then record metrics and learnings
7. run weekly entropy cleanup

## Weekly Review

- check PR cycle time and stale-draft count
- classify whether verify failures mostly come from prompt, context, or harness design
- add stale docs, orphaned task briefs, and missing evidence to the cleanup backlog

## Rollout Stages

### Pilot

- limit usage to docs, tests, and scoped bugfix work
- Exit Criteria
  - verify and PR summaries are consistently present
  - the team stays under the review budget

### Guided Delivery

- standardize issue, brief, verify, and PR-template usage
- Exit Criteria
  - current-run verify and evidence use a consistent format
  - weekly repo-hygiene work has started

### Team Scale

- make review budget, metrics, and repo hygiene part of the regular operating cadence
- Exit Criteria
  - the team can tune input volume from throughput / quality / hygiene indicators
  - cleanup and rollout decisions do not stall on one specific person
