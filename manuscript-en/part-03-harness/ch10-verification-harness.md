---
id: ch10
title: Build a Verification Harness
status: drafted
source_ja: manuscript/part-03-harness/ch10-verification-harness.md
artifacts:
  - .github/workflows/verify.yml
  - checklists/verification.md
  - sample-repo/tests/test_ticket_search.py
  - artifacts/evidence/README.md
dependencies:
  - ch09
---

# Build a Verification Harness

## Role in This Book
Even if tests are green, verification is not closed when the reviewer still cannot tell what to check. CH09 defined the startup conditions, permission boundaries, and done criteria for a single-agent harness. That still leaves a gap: one local verify command is not enough to make a change review-ready and reproducible.

That gap is where the verification harness begins. A verification harness combines tests, execution order, evidence collection, CI, and approval gates so that the result is not just “changed,” but “verified and explainable.” This chapter uses `support-hub` to show how to design the minimum verification harness in practice.

## Learning Objectives
- Separate the roles of local verify and CI verify
- Design an evidence bundle for UI changes
- Explain where human approval should sit

## Outline
### 1. Write tests before changing behavior
### 2. Order lint, typecheck, unit, and e2e checks
### 3. Keep evidence for UI changes
### 4. Divide work between CI and local verify
### 5. Place human approval explicitly

## 1. Write Tests Before Changing Behavior
The starting point of a verification harness is the test suite. Without tests, the repo cannot mechanically answer three questions: what was broken, what was fixed, and what behavior must stay stable.

That is especially important for bugfixes and behavior changes. Before the code changes, the harness should already contain either a failing test or a stronger regression guard. `sample-repo/tests/test_ticket_search.py` plays that role for `FEATURE-001`. It fixes the intended behavior for searching `title`, `description`, and `tags`, returning all tickets for a blank query, and treating query comparison as case-insensitive.

This is why tests are not post-hoc explanation. They are executable specification. In a coding-agent workflow, tests become source of truth alongside the product spec and acceptance criteria. The agent should inspect them before editing behavior, and add them first when the current regression guard is too weak.

## 2. Order Lint, Typecheck, Unit, and E2E Checks
A verification harness should be designed as an ordered pipeline, not as a bag of checks. In a larger system, the typical order is lint, typecheck, unit, integration, then e2e. The reason is practical: cheaper failures should stop the run before the expensive checks start.

This repo is still a minimal scaffold, so the active verification line is mostly unit-test based. That does not reduce the value of defining the pipeline shape now. `checklists/verification.md` captures the verification order as a practical review checklist: confirm the guarded behavior, decide whether a failing test is needed, run local verify, reflect the same bar in CI, preserve evidence when required, and isolate the parts that still need human approval.

The benefit of explicit order is not just speed. It also improves diagnosis. A lint failure, a unit-test failure, and a missing evidence bundle are all verification failures, but they are not the same failure mode. The harness should make that visible.

## 3. Keep Evidence for UI Changes
Even when tests pass, a reviewer may still be unable to judge the change. That is especially true for UI or other user-visible changes, where logs alone do not explain what actually changed.

That is why the verification harness needs an evidence bundle. `artifacts/evidence/README.md` defines the purpose, recommended layout, and minimum contents. The core set is usually enough:

- `summary.md`
- `verify.log`
- `repro.md`
- `before.png`
- `after.png`

The objective is not to create a glossy report. The objective is to preserve enough material that a reviewer can understand what changed, what commands were run, and what should be inspected.

`support-hub` is not a UI repo today, so the worked example in this chapter does not require screenshots. But the artifact still matters now, because it fixes the location and format before a UI task arrives. That prevents later ambiguity about where evidence belongs and what must be included.

## 4. Divide Work Between CI and Local Verify
Local verify and CI verify are not the same thing. Local verify exists for fast iteration before and after each change. CI verify exists to rerun the same acceptance line on the branch and make it shareable across reviewers.

`.github/workflows/verify.yml` makes that division concrete by separating book verification and sample-repo verification into distinct jobs. That matters because the failure modes are different. Manuscript path drift and prompt-eval scaffold problems belong to one harness. Sample-repo tests belong to another. Splitting the jobs makes failure classification, retry, and review faster.

The important rule is that CI does not replace local verify. The coding agent should still run `./scripts/verify-book.sh ch10` or `./scripts/verify-sample.sh` locally first. CI then reruns the same standard on the branch. The harness needs both: local speed and shared reproducibility.

## 5. Place Human Approval Explicitly
A verification harness is not a story about full automation. It also decides where human approval belongs. Approval is needed where verification alone cannot make the final call, or where a human still owns the risk.

In this chapter, approval is easiest to place in three moments:

1. before verify
   - when the change would modify a public contract
   - when CI or verify scripts themselves would change
2. after verify
   - when the evidence bundle may still be too weak for review
   - when scope-outside effects may remain
3. before merge
   - when the PR summary, verification section, and `Remaining Gaps` must still be checked for clarity

`checklists/verification.md` carries these approval points in practical form. The goal is not to return all decisions to humans. The goal is to mechanize what can be checked and leave only the explicitly human judgments behind.

## Bad / Good Example
Bad:

```text
The search fix passed `python -m unittest` once.
CI can be checked later.
The task probably did not change the UI, so no evidence is needed.
```

This turns verification into a memory of one green run. It leaves unclear which tests are the regression guard, whether CI reruns the same bar, and whether evidence is truly unnecessary.

Corrected:

```text
First add or strengthen the regression guard in
`sample-repo/tests/test_ticket_search.py`.
Then run `./scripts/verify-sample.sh` locally.
Let `.github/workflows/verify.yml` rerun the same bar in CI.
If the change is UI-visible, create an evidence bundle using
`artifacts/evidence/README.md`.
Use `checklists/verification.md` to separate approval-required points.
```

This version treats tests, local verify, CI, evidence, and approval as one harness.

Comparison points:
- The bad version treats verify as a one-off command.
- The bad version leaves CI and evidence responsibilities vague.
- The corrected version separates regression guards, shared verify, review evidence, and approval gates.

## Worked Example
Use `FEATURE-001` as the verification-harness example. Its acceptance criteria already include the rule that query matching is case-insensitive. If the tests do not explicitly guard that behavior, a later refactor can break it without immediate notice.

The first step is therefore to strengthen `sample-repo/tests/test_ticket_search.py` with a case-insensitive regression guard. That is not a new feature. It is verification-harness work. The next step is to run `./scripts/verify-sample.sh` locally and confirm that the search regression line still passes. CI then reruns the same standard through `.github/workflows/verify.yml`, with book verification and sample verification isolated in separate jobs.

This particular task does not change a UI, so screenshots are unnecessary. The reviewer still needs an explanation, though: which acceptance criterion became a regression guard, and which verify command was run. If a later search UI is added, the same harness can extend into an evidence bundle by following `artifacts/evidence/README.md`.

The worked example matters because it shows that a verification harness is not “tests only” and not “CI only.” It becomes real only when specification guards, execution order, evidence, and approval are designed together.

## Reader-facing Table
### Verification Pipeline

| Stage | What it checks | Main artifact or command | What the reader should look for |
|---|---|---|---|
| failing test | whether the broken behavior is executable | `sample-repo/tests/test_ticket_search.py` | whether acceptance criteria became a regression guard |
| local verify | whether the minimum local bar passes | `./scripts/verify-sample.sh` | whether the bar is fast enough for iteration |
| CI | whether the same bar is reproducible on the branch | `.github/workflows/verify.yml` | whether local and shared verification still match |
| evidence | whether a reviewer can re-check the visible change | `artifacts/evidence/README.md` | whether required artifacts and rationale are explicit |
| approval | whether only human-owned judgments remain | `checklists/verification.md` | whether non-automated decisions are isolated clearly |

This table keeps the verification harness from collapsing into “the test chapter.” It starts with an executable guard, continues through local and shared verification, and ends with evidence and approval for review-readiness.

## Exercises
1. Add a failing test before fixing the behavior.
2. Create an evidence bundle for a UI change.

## Referenced Artifacts
- `.github/workflows/verify.yml`
- `checklists/verification.md`
- `sample-repo/tests/test_ticket_search.py`
- `artifacts/evidence/README.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `.github/workflows/verify.yml`, `checklists/verification.md`, `sample-repo/tests/test_ticket_search.py`, and `artifacts/evidence/README.md`. Read the verification harness as a flow across tests, CI, evidence, and approval rather than as a single command.
- For the backmatter path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH10 Build a Verification Harness` and `manuscript-en/backmatter/01-reading-guide.md` under `## Verification, Reliability, and Operations`.

## Chapter Summary
- A verification harness combines tests, execution order, evidence, CI, and approval gates into one verification system.
- Local verify serves iteration speed, while CI verify serves reproducibility. Both are required.
- Once the verify chain is stable, the next failure point is work that does not fit into a single session. The next chapter moves into long-running tasks and multi-agent coordination.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch10-verification-harness.md`
- This English draft preserves the same verification pipeline, evidence model, and review-ready framing as the Japanese chapter.
