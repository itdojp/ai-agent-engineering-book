# Operating Model

## Purpose

The minimum operating model for putting AI agents into team workflows. It fixes responsibility split, review budget, cadence, rollout stages, and what to do when the budget is exceeded.

## Operating Principles

- keep `1 issue = 1 work package`
- keep humans as the accountability owner and agents as the execution worker
- do not treat a diff without current-run verify as review-ready
- when the review budget is exceeded, reduce the queue before opening new work
- make entropy cleanup part of the cadence instead of leaving it for later

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
5. record metrics and learnings after merge
6. run weekly entropy cleanup

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
