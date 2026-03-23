# Operating Model

## Purpose

The minimum operating model for putting AI agents into team workflows. It fixes responsibility split, review budget, cadence, and rollout stages.

## Responsibilities

### Human

- set the objective
- make the important design decisions
- approve destructive changes
- perform final review and decide on merge
- own repo hygiene and entropy cleanup

### Agent

- explore the existing repo
- make routine edits and scoped implementation changes
- update tests, docs, and artifacts
- run verify
- explain the resulting diff

## Review Budget

- one reviewer should hold at most two deep reviews at once
- one reviewer should hold at most one PR that requires an evidence bundle
- when the review budget is exceeded, close existing PRs before opening another work package

## Cadence

1. cut one issue into one work package
2. prepare the task brief and related artifacts
3. let the agent implement and run verify
4. let the human review and approve
5. record metrics and learnings after merge

## Rollout Stages

### Pilot

- limit usage to docs, tests, and scoped bugfix work

### Guided Delivery

- standardize issue, brief, verify, and PR template usage

### Team Scale

- make review budget, metrics, and repo hygiene part of the regular operating cadence
