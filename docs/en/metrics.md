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
- `review completion rate`
  - measures the share of PRs whose review bodies, inline comments, suggestions, and zero unresolved threads were handled before merge
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
- `unresolved review thread residual count`
  - detects whether unresolved threads remain before merge
- `eval rerun coverage`
  - detects whether evals or smoke checks reran after prompt, model/runtime profile, or tool-policy changes

## Production Delivery

Use only production-affecting work packages as the denominator. The Delivery Owner records these metrics weekly or per release. Do not count `N/A` as zero; preserve the reason the metric does not apply.

| Metric | Definition | Window / owner | Intervention threshold |
|---|---|---|---|
| `production confirmation latency` | time from merge timestamp to `Production Confirmed` timestamp | per work package / Delivery Owner | when the defined SLO is exceeded, classify delay as deployment, smoke, or metric wait |
| `production confirmation rate` | numerator: production-affecting merged work packages confirmed within the deadline; denominator: all production-affecting merged work packages in the window | weekly or per release / Delivery Owner | below 100%, inventory unconfirmed work and do not count it complete |
| `deployment failure / unknown count` | target-SHA deployments that failed, were cancelled without explanation, or stayed unknown beyond the defined timeout; excludes `Superseded` runs confirmed through a successor deployment containing the target change | weekly / Operator | at one or more, record cause and retry scope |
| `marker mismatch count` | cases where the expected SHA/version/semantic marker disagreed with the production response | per deployment / Delivery Owner | at one or more, halt rollout |
| `post-deploy metric regression count` | deployments that breached the predefined baseline/threshold/window | deployment observation window / Delivery Owner | at one or more, make a rollback decision |
| `rollback rate` | numerator: rollbacks started; denominator: production-affecting deployments | per release / Lead | when rising, revisit the production-ready gate and change size |
| `rollback recovery time` | time from `Rollback in Progress` start to post-rollback `Production Confirmed` | per rollback / Delivery Owner | when the target is exceeded, improve rollback steps and evidence collection |

Use a metric for a decision only when its baseline, threshold, window, source, and owner are present. If low traffic prevents a numerical metric decision, keep the HTTP and semantic-marker checks and record a reason such as `N/A: low traffic` instead of silently omitting the metric.

## Hygiene

- `stale docs count`
  - shows whether entropy cleanup is keeping up
- `orphaned task brief count`
  - shows whether non-canonical task artifacts are piling up
- `missing verification evidence count`
  - detects weak review evidence for user-visible changes
- `evidence freshness failures`
  - shows whether stale verify results or screenshots are reaching review
- `model/runtime profile drift count`
  - detects whether model, API, SDK, runtime, or tool-set changes entered without confirmation dates and eval reruns
- `external-input exception count`
  - detects rising exceptions around redaction, provider terms, and approval for AI / external-service submission
- `hygiene backlog age`
  - shows whether the cleanup backlog is being neglected

## Observability Inputs

- `trace coverage`
  - shows whether traces that satisfy the minimum trace reference contract remain for work packages with long-running work, handoff, retry, or restart
- `current-run verify availability`
  - shows whether reviewers can inspect the latest run directly
- `review-response evidence availability`
  - shows whether reviewers can inspect responses to review bodies, inline comments, suggestions, and thread resolution
- `retry concentration`
  - shows whether failure loops are clustering in one stage of the flow

## Trace Coverage Definition

- denominator
  - the number of work packages that involve long-running work, handoff, retry, or restart and therefore require trace references
- numerator
  - the number of work packages whose trace records satisfy the required fields among task / work-package id, run timestamp or run id, owner / handoff, retry / restart reason, verify reference, evidence linkage, and redaction note

Use the following rule to decide what counts as “required.”

- always required
  - task / work-package id
  - run timestamp or run id (at least one of the two)
  - verify reference
  - evidence linkage
- conditionally required
  - owner / handoff: required when the work package includes a handoff. When there is no handoff, record the current owner, and use `N/A` only in workflows that do not use an owner concept at all
  - retry / restart reason: required when retry or restart happened. Otherwise state `N/A`
  - redaction note: required when any part was redacted. Otherwise state `none` or `N/A`

Do not leave non-applicable fields blank or silently omit them. Use a non-applicable marker such as `N/A` or `none`. A work package only counts in the numerator when all always-required fields are present and conditionally required fields are present whenever the condition applies.

Trace coverage here does not mean only “a trace file exists.” It also measures whether a reviewer can explain which verify run and which task the trace belongs to.

## Intervention Rules

- when `PR cycle time` or `queue wait time` grows
  - cut work packages smaller and suspect review-budget overflow first
- when `verify failure rate` stays high
  - suspect missing prompt, brief, or context-pack inputs before blaming the model
- when `review completion rate` is low or `unresolved review thread residual count` remains nonzero
  - revisit the PR template, review-response workflow, and pre-merge gate
- when `artifact drift incidents` increase
  - revisit done criteria and checklists
- when `model/runtime profile drift count` rises or `eval rerun coverage` falls
  - restore confirmation-date recording and eval reruns to the pre-merge gate for model / API / SDK changes
- when `external-input exception count` increases
  - revisit redaction policy, provider-term checks, and the approval boundary
- when `production confirmation rate` is below 100% or `production confirmation latency` exceeds its SLO
  - do not count merged work complete; classify the wait as deployment, HTTP/marker, or metric confirmation
- when `deployment failure / unknown count`, `marker mismatch count`, or `post-deploy metric regression count` is one or more
  - halt rollout, preserve target-SHA evidence, and decide rollback or remediation
- when `rollback rate` or `rollback recovery time` worsens
  - revisit the production-ready gate, change size, revert procedure, and confirmation owner
- when `stale docs count`, `evidence freshness failures`, or `hygiene backlog age` worsen
  - open cleanup work packages before adding more feature work

## Review Questions

- Is throughput increasing without exceeding the review budget?
- Is the main cause of verify failure prompt, context, or harness design?
- Is queue wait time caused mainly by reviewer wait, verify wait, or approval wait?
- Is low trace coverage making failure analysis impossible?
- If trace coverage is low, is the real gap missing trace, missing verify reference, or missing evidence linkage?
- When review completion rate is low, is the cause unanswered comments, unapplied suggestions, or unresolved thread cleanup?
- Are eval reruns missing after model/runtime profile changes?
- Where are AI / external-service submission exceptions increasing: redaction, approval, or provider-term checks?
- Can delay from merge to production confirmation be attributed to deployment, HTTP/marker, or metric wait?
- Is deployment success being used as a substitute for production confirmation?
- After rollback, were the new main SHA and production marker checked again?
- Is worsening repo hygiene slowing the next round of work?
- Are stale drafts and stale docs increasing at the same time?
