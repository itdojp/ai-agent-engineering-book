# Metrics

## Purpose

These metrics are not for bragging about throughput. They exist to identify where the operation is getting stuck and which artifacts need to be strengthened. From the verification-harness perspective, verify logs, traces, and evidence bundles are part of the measurement surface.

## Throughput

- `closed issues / week`
  - shows whether work packages are closing at the intended size
- `PR cycle time`
  - shows whether the review budget is backing up
- `draft-to-merge time`
  - measures how long verify and review are delaying closure
- `queue wait time`
  - shows where PRs are stalling in the flow
- `stale draft count`
  - shows whether the queue is starting to clog

## Quality

- `verify failure rate`
  - shows the quality of briefing, prompting, and task decomposition
- `post-merge regression count`
  - shows how well review and the verification harness are working
- `approval-stop rate`
  - shows whether approval boundaries are causing avoidable rework
- `artifact drift incidents`
  - shows missed synchronization among docs, tests, and task artifacts
- `reviewer re-open rate`
  - shows whether review churn is increasing

## Hygiene

- `stale docs count`
  - shows whether entropy cleanup is keeping up
- `orphaned task brief count`
  - shows whether non-canonical task artifacts are piling up
- `missing verification evidence count`
  - detects weak review evidence for user-visible changes
- `evidence freshness failures`
  - shows whether stale verify results or screenshots are reaching review
- `hygiene backlog age`
  - shows whether the cleanup backlog is being neglected

## Observability Inputs

- `trace coverage`
  - shows whether long-running work and handoffs leave enough history for failure analysis
- `current-run verify availability`
  - shows whether reviewers can inspect the latest run directly
- `retry concentration`
  - shows whether failure loops are clustering in one stage of the flow

## Intervention Rules

- when `PR cycle time` or `queue wait time` grows
  - cut work packages smaller and suspect review-budget overflow first
- when `verify failure rate` stays high
  - suspect missing prompt, brief, or context-pack inputs before blaming the model
- when `artifact drift incidents` increase
  - revisit done criteria and checklists
- when `stale docs count`, `evidence freshness failures`, or `hygiene backlog age` worsen
  - open cleanup work packages before adding more feature work

## Review Questions

- Is throughput increasing without exceeding the review budget?
- Is the main cause of verify failure prompt, context, or harness design?
- Is queue wait time caused mainly by reviewer wait, verify wait, or approval wait?
- Is low trace coverage making failure analysis impossible?
- Is worsening repo hygiene slowing the next round of work?
- Are stale drafts and stale docs increasing at the same time?
