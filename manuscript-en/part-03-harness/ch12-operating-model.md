---
id: ch12
title: Operating Model and Organizational Adoption
status: drafted
source_ja: manuscript/part-03-harness/ch12-operating-model.md
artifacts:
  - docs/en/operating-model.md
  - docs/en/metrics.md
  - checklists/en/verification.md
  - checklists/en/repo-hygiene.md
  - .github/pull_request_template.md
dependencies:
  - ch09
  - ch10
  - ch11
---

# Operating Model and Organizational Adoption

## Role in This Book
Even when individual runs succeed, adoption fails if PRs pile up, the repo degrades, and no one owns the final decisions. CH09 through CH11 covered the single-agent harness, the verification harness, and long-running tasks with multi-agent coordination. After that point, the next problem is not model capability. It is operating discipline.

This chapter defines the operating model for introducing AI agents into a team. The subject is not model selection. The subject is role ownership, review budget, repo hygiene, metrics, and rollout order. The goal is not to turn AI agents into a fast substitute for missing staff. The goal is to keep human responsibilities explicit and make artifact-driven work sustainable across the team.

## Learning Objectives
- Make human responsibilities explicit
- Explain the tradeoff between review budget and throughput
- Design repo hygiene and entropy cleanup operations
- Design gates from merge through production confirmation, halt, rollback, and restart

## Outline
### 1. Human responsibilities that remain
### 2. Review budget and throughput
### 3. Repo hygiene and AI slop control
### 4. Metrics and retrospectives
### 5. Plan an adoption roadmap

## 1. Human Responsibilities That Remain
Introducing AI agents does not remove human responsibility. It only removes part of the repetitive execution load. The repo's `docs/en/operating-model.md` already separates `Human` and `Agent` responsibilities, but five human responsibilities must stay explicit:

1. deciding goals and priorities
2. approving destructive or boundary-crossing changes
3. making major design decisions
4. performing final review and merge decisions
5. maintaining repo hygiene and entropy cleanup

By contrast, AI agents are well suited to repo exploration, repetitive edits, scoped implementation, test and doc updates, verify execution, and change explanation. `ChatGPT` remains useful for requirements shaping and design comparison. `Codex CLI` remains useful for reading the repo, changing artifacts, and running verification. An operating model breaks these roles apart instead of blending them.

The common failure is to assume that if the agent can write code, it should also own design judgment and merge judgment. That does not produce speed. It produces responsibility gaps. In this chapter's operating model, AI agents are execution actors, not accountability owners.

## 2. Review Budget and Throughput
The first bottleneck after AI-agent adoption is rarely implementation speed. It is review capacity. As generation speed rises, human review budget saturates quickly. If that limit is ignored, unread PRs accumulate, review quality drops, and post-merge regressions increase.

CH12 does not treat throughput as “number of PRs.” `docs/en/metrics.md` frames it through `closed issues / week`, `PR cycle time`, and `draft-to-merge time`, together with review-budget usage. `docs/en/operating-model.md` makes the constraint concrete:

- one reviewer should deeply review at most two PRs at a time
- PRs that require an evidence bundle should be limited to one per reviewer at a time

The rule is simple: do not increase agent speed before protecting review flow. Smaller PRs, smaller work packages, and a stable PR template usually improve throughput more than a more aggressive model does. `.github/pull_request_template.md` supports this by fixing `Goal`, `Changed Files`, `Verification`, `Evidence / Approval`, and `Remaining Gaps`.

#### PR completion gate and review response

In AI-agent work, a PR can easily be treated as complete merely because CI is green. To stay aligned with the Phase 2 GitHub / AgentOps books, the completion gate should include review bodies, inline comments, suggestions, unresolved review threads, CI, and post-merge checks. `.github/pull_request_template.md` should let the operator record whether Copilot review was requested, whether every comment was fixed or answered with a reason, whether unresolved threads are zero, and whether main checks and public-site reflection were confirmed after merge.

This `review completion gate` exists to protect review budget, not to add more ceremony. If suggestions or unresolved threads remain at merge time, the team cannot tell whether a post-merge regression came from review miss, verify miss, or a product decision. The operator leaves current-run verify and review-response evidence in the PR body, and the reviewer treats zero unresolved threads plus green CI as merge preconditions.

#### Close the path from merge to production confirmation

Review completion and merge show that the code change was accepted. They do not show that the correct artifact reached the public target or that expected behavior and metrics remained healthy. `docs/en/operating-model.md` treats `Review Complete`, `Production Ready`, `Deployment Approved`, `Deployed`, and `Production Confirmed` as separate states. Environment approval is permission to deploy, while a successful deployment job still does not prove production health.

For a production-affecting PR, record the target URL, post-merge SHA/version, semantic marker, representative routes, metric baseline/threshold/window, owner, and halt/rollback/restart conditions before merge. After merge, match the deployment and workflow to the target SHA, then check HTTP, markers, and metrics. If aggregate status disagrees with the target deployment, prefer target-SHA evidence and do not complete the work when the discrepancy cannot be explained.

Move to `Halted` when deployment fails or stays unknown, markers mismatch, representative routes fail, or metrics exceed their threshold. If a successor SHA cancels the target run, use `Superseded` evidence for the original work package only when the successor includes the target change and satisfies the same route/marker/metric contract. Use a reviewed new main commit such as a revert PR as the default rollback rather than rewriting history. A historical rerun uses the original SHA/ref and is therefore a poor default when it can make main and production diverge. After rollback, repeat production confirmation against the new SHA. Resume only after cause, remediation, re-verification, and the restart decision are recorded.

## 3. Repo Hygiene and AI Slop Control
AI-agent operations accelerate good diffs and bad diffs at the same time. The accumulated low-quality residue is AI slop. It includes more than obvious bugs. It also includes stale docs, broken paths, orphaned task briefs, drift between verify scripts and the repo, terminology inconsistency, and long explanations that are no longer tied to real artifacts.

`checklists/en/repo-hygiene.md` separates checks before merge from weekly cleanup. That split matters. A team cannot rely on “we will clean it up later” once agent throughput increases. Cleanup needs a cadence, owners, and explicit escalation conditions.

Repo hygiene stays a human responsibility for that reason. An agent can detect candidate stale artifacts, but deciding which artifact still holds source-of-truth status often requires human judgment. In this chapter, hygiene does not mean aesthetics. It means keeping the repo safe for the next agent run.

## 4. Metrics and Retrospectives
Metrics are not here to answer whether AI agents feel useful. They exist to show whether the operating model is healthy and where it is currently blocked. `docs/en/metrics.md` groups them into five sets:

| Group | Example metrics | What they reveal |
|---|---|---|
| throughput | `closed issues / week`, `PR cycle time`, `review completion rate` | whether work packages are small enough and flow is moving |
| quality | `verify failure rate`, `post-merge regression count` | whether review and verification are actually catching problems |
| production delivery | `production confirmation rate/latency`, `marker mismatch count`, `rollback recovery time` | whether post-merge confirmation and recovery close correctly |
| hygiene | `stale docs count`, `orphaned task brief count`, `missing verification evidence count` | whether entropy cleanup is keeping pace with generation |
| observability | `trace coverage`, `current-run verify availability`, `retry concentration` | where current-run visibility and failure analysis are weak |

The critical rule is to attach action to each metric. If verify failure rate rises, the team should inspect prompt or brief quality. If PR cycle time grows, the team should inspect review budget. If review completion rate falls or unresolved review thread residuals remain, the team should inspect the pre-merge gate and PR template. If production confirmation rate is below 100%, a marker mismatches, or a post-deploy metric regresses, merged work must remain incomplete. If trace coverage falls, the team should suspect a lack of material for failure analysis. If evidence freshness failure rises, the team should suspect that reviewers can no longer confirm current-run verify. If stale docs count and hygiene backlog age worsen, cleanup work should be opened before more feature work. Metrics should support queue diagnosis, failure analysis, and review-quality improvement, not throughput bragging.

Trace coverage here does not mean only “a `trace.md` file exists.” For work packages that need traces because they involve long-running work, handoff, retry, or restart, the team should ask whether the minimum trace reference contract is actually present: task / work-package id, run timestamp or run id, owner / handoff, retry / restart reason, verify reference, evidence linkage, and redaction note. That is what keeps historical traces from being confused with current-run verify while still making trace coverage useful for failure analysis.

## 5. Plan an Adoption Roadmap
AI-agent adoption is safer when rolled out in stages instead of across the entire repo at once. `docs/en/operating-model.md` already defines three stages:

1. `Pilot`
   - limit work to docs, tests, and scoped bugfixes
2. `Guided Delivery`
   - standardize issue structure, task briefs, verify, and PR templates
3. `Team Scale`
   - make review budget, metrics, and repo hygiene part of regular team operation

This ordering keeps missing artifacts visible while the blast radius is small. If a team jumps directly to multi-agent implementation across broad codepaths, speed may increase before review and hygiene can absorb it. The maturity model in this book should therefore be read not only as Prompt -> Context -> Harness, but also as local success -> guided delivery -> stable team operation.

## Bad / Good Example
Bad:

```text
AI agents are fast, so make issues larger and review them whenever someone has time.
Stale docs and terminology drift are minor problems and can be cleaned up later.
CI was green and the PR merged, so count deployment approval and production confirmation as complete too.
```

This optimizes only raw throughput. Review budget, repo hygiene, and role ownership all collapse under the generated change volume.

Corrected:

```text
Keep 1 issue = 1 work package.
Use the PR template to require Goal, Changed Files, Verification,
Evidence / Approval, and Remaining Gaps.
Make Copilot review, responses to inline comments and suggestions,
zero unresolved threads, green CI, and post-merge checks part of completion.
For production-affecting work, define target, marker, metric, owner, and rollback before merge,
then check target-SHA deployment, HTTP, semantic markers, and metrics separately after merge.
Humans own goal setting, approval, final review, and entropy cleanup.
Review metrics and repo hygiene every week, and reduce input volume
before review budget is exceeded.
```

This operating model lets agent speed translate into completed work instead of uncontrolled queue growth.

Comparison points:
- The bad version optimizes throughput alone.
- The bad version ignores review capacity and hygiene cost.
- The corrected version fixes responsibility, cadence, metrics, and cleanup in artifacts.

## Worked Example
Consider a three-person team operating this repo.

- lead
  - owns prioritization, destructive-change approval, and final merge decisions
- operator
  - uses `ChatGPT` for requirements and design comparison, then uses `Codex CLI` for implementation and verify
- reviewer
  - reviews the PR template output, verification, and evidence

In this setup, one reviewer should hold at most two deep reviews at once. The operator must use `.github/pull_request_template.md` so that `Goal`, `Changed Files`, `Verification`, `Evidence / Approval`, and `Remaining Gaps` are always present. Every week, the team reviews `docs/en/metrics.md`. If `PR cycle time` grows, work packages are reduced further. If review completion rate falls or unresolved review thread residuals appear, the team tightens the pre-merge gate and review-response evidence. If stale artifacts grow, `checklists/en/repo-hygiene.md` drives the entropy-cleanup pass.
If trace coverage drops, the team should recheck long-running-task handoff quality instead of treating the missing history as acceptable noise.

For a public change, the lead owns the merge decision, the operator collects deployment evidence, the reviewer owns review completion, and the Delivery Owner owns production confirmation. One person may hold all roles, but keeps the decisions separate. The success scenario checks target-SHA deployment success, HTTP 200 for the root and representative routes, matching semantic markers, and metrics within threshold. Deployment failure or unknown status halts completion. A marker or metric regression triggers a revert PR and production confirmation for the new main SHA.

The point of this example is that adoption succeeds or fails based on whether roles and cadence are artifactized. CH12 is therefore an operations chapter, not a model-selection chapter.

## Exercises
1. Define an operating model for a three-person team, including ownership for the review completion gate, zero unresolved threads, the production-ready plan, post-deploy confirmation, and rollback/restart. Walk through success, deployment failure, and metric regression scenarios.
2. Create a weekly entropy cleanup checklist.

## Referenced Artifacts
- `docs/en/operating-model.md`
- `docs/en/metrics.md`
- `checklists/en/verification.md`
- `checklists/en/repo-hygiene.md`
- `.github/pull_request_template.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `docs/en/operating-model.md`, `docs/en/metrics.md`, `checklists/en/verification.md`, `checklists/en/repo-hygiene.md`, and `.github/pull_request_template.md`. Read adoption decisions through roles, review budget, cadence, the production gate, and cleanup instead of through model comparisons.
- For the backmatter path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH12 Operating Model and Organizational Adoption` and `manuscript-en/backmatter/01-reading-guide.md` under `## Verification, Reliability, and Operations`.

## Chapter Summary
- Human responsibilities remain in goal setting, approval, final review, and repo hygiene.
- Throughput improves only when review budget and work-package size are controlled together.
- Keep review completion, deployment approval, deployment success, and production confirmation separate; decide completion from target-SHA HTTP, semantic markers, and metrics.
- Once Prompt, Context, and Harness are translated into artifacts and an operating model, AI agents move closer to completing real work instead of only looking capable.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch12-operating-model.md`
- This English draft preserves the same team operating model, metrics framing, and hygiene responsibilities as the Japanese chapter.
