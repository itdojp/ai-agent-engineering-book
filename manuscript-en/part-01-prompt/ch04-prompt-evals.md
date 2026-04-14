---
id: ch04
title: Evaluate Prompts
status: drafted
source_ja: manuscript/part-01-prompt/ch04-prompt-evals.md
artifacts:
  - evals/prompt-contract-cases.json
  - evals/rubrics/feature-spec.json
  - scripts/run-prompt-evals.py
dependencies:
  - ch02
  - ch03
---

# Evaluate Prompts

## Role in This Book
The prompt that worked yesterday may not behave the same way tomorrow. CH02 defined the Prompt Contract. CH03 turned vague requests into product specs, acceptance criteria, ADRs, and eval seeds. The next question is operational: how do you decide whether one prompt is actually better than another?

Prompt Engineering only becomes engineering when prompt quality is evaluated rather than assumed. That requires eval cases, rubrics, regression checks, and version comparison. The 2026 edition does not keep the scope at prompt wording alone. Even if the Prompt Contract looks good, the overall work can still fail when tool calls, approval handling, trace quality, or cost / latency behavior drift. This chapter therefore starts with prompt-level evaluation and extends the frame to workflow-level evaluation.

## Learning Objectives
- Design eval cases, rubrics, judge logic, and human spot-checks as separate tools
- Add workflow metrics and trace review to prompt regression comparison
- List quality, tool-call behavior, cost / latency, and approval signals as comparison points during model updates

## Outline
### 1. Good prompts and workflows can be evaluated
### 2. Build an eval set
### 3. Distinguish rubrics, goldens, judges, and human spot-checks
### 4. Run prompt regression tests and review traces
### 5. Version and compare prompt changes

## 1. Good Prompts and Workflows Can Be Evaluated
Prompt quality should be judged by behavior, not by impression. A prompt for `FEATURE-001` might appear successful once, but a single success does not prove that the prompt is good. The input may have been unusually easy, or the model may have filled in missing details in a convenient way. The engineering question is whether the prompt remains stable across similar tasks, boundary cases, and later revisions.

The 2026 edition does not limit the evaluation target to the prompt text alone. A Prompt Contract can be structurally sound and still lead to poor work if tool calls cross the boundary, approval-required steps are not surfaced, traces are missing, or cost / latency behavior becomes wasteful. This chapter keeps prompt-level evaluation as the foundation while making room for workflow-level evaluation.

| Lens | What it checks | Covered in this chapter? |
|---|---|---|
| Prompt-level evaluation | whether purpose, constraints, completion criteria, and output schema remain stable | Yes |
| Workflow-level evaluation | whether tool calls, approvals, traces, and evidence close reliably | Yes |
| Context-level evaluation | whether the right artifacts stay visible to the agent over time | Later chapters cover it in depth |
| Harness-level evaluation | whether verify, retries, restart, and evidence capture work | Later chapters cover it in depth |

Good prompts and workflows can be evaluated. If they cannot be evaluated, they also cannot be improved or versioned reliably.

## 2. Build an Eval Set
An eval set is a list of inputs that are likely to expose prompt or workflow weaknesses. It is not just a collection of random examples. The most useful cases are the ones that stress the workflow with ambiguity, missing information, scope pressure, approval waits, reporting drift, and tool misuse.

`evals/prompt-contract-cases.json` defines cases across `feature-contract` and `bugfix-contract`. The set is small, but it already covers several failure patterns.

- whether the prompt keeps `FEATURE-001` inside scope
- whether the prompt handles missing information explicitly
- whether docs, acceptance criteria, and ADRs remain part of the artifact-sync boundary
- whether structured output and `output_version` remain stable
- whether approval-required steps stop correctly
- whether the bugfix contract preserves its regression guard
- whether the final report remains reviewable

A practical sequence is:

1. list the failure modes
   - scope creep
   - missing information
   - artifact update drift
   - missing verify requirements
   - approval-boundary violations
   - tool misuse
   - cost / latency waste
2. assign at least one case to each failure mode
3. define `must_include` and `must_not_include`
4. reuse the same cases after every prompt revision

An eval set is not a one-time asset. When a new failure is discovered, the correct response is to add a case that reproduces it. That is the foundation of prompt and workflow regression checking.

## 3. Distinguish Rubrics, Goldens, Judges, and Human Spot-checks
Prompt evaluation works better when goldens, rubrics, judges, and human spot-checks are treated as separate tools.

| Method | Best for | Weakness |
|---|---|---|
| Golden | fixed section order, fixed wording, short outputs | brittle when wording varies |
| Rubric | requirement shaping, design comparison, structured free text | needs scoring logic or reviewer design |
| Judge | scaling a rubric-like decision over many runs | can inherit the judge model's own bias or drift |
| Human spot-check | high-risk edge cases, approval correctness, subtle quality review | expensive and hard to scale |

The outputs in CH03, such as a product spec or ADR, contain free text. A full-string golden would reject good answers simply because the wording is different. That is why CH04 centers the rubric. `evals/rubrics/feature-spec.json` defines criteria such as Objective, Scope, Inputs, Constraints, Completion, Missing Information, approval boundary, and structured output.

The rubric does not ask whether the output matches an ideal paragraph verbatim. It asks whether the result is usable as an implementation-ready artifact. Goldens still help for section names and output ordering. A judge can help score a larger set consistently. Human spot-check remains necessary where approval correctness, subtle scope handling, or ambiguous trade-offs still need review. The engineering move is to pick the right evaluation tool for the right failure mode rather than overloading one method.

## 4. Run Prompt Regression Tests and Review Traces
A one-line prompt change can break cases that used to pass. That is why prompts need regression tests in the same way code does. The workflow is simple: run the same eval set against prompt version 1 and version 2, then compare the differences.

This repo includes `scripts/run-prompt-evals.py` as a lightweight consistency check. At this stage it does not call a model. Instead, it verifies that the prompt-eval artifacts remain internally consistent, including:

- required Prompt Contract headings exist
- `evals/prompt-contract-cases.json` is structurally valid
- `evals/rubrics/feature-spec.json` is structurally valid

That is not yet a full evaluation runner, but it is still useful. Prompt evaluation has to start by keeping the cases and rubric themselves healthy inside the repo. If those artifacts drift or break, later comparisons stop being trustworthy.

The actual regression idea is still the same. Suppose version 1 of `feature-contract` handled missing information weakly. Version 2 adds a `Missing Information Policy`, stronger artifact-sync wording, a clearer out-of-scope prohibition, and an explicit `Approval Gate`. The same suite should then show whether the target cases improved and whether other cases regressed.

The 2026 frame also connects regression checks to trace review and workflow metrics. In addition to pass/fail, reviewers should inspect signals such as:

- whether tool calls stayed inside the intended boundary
- whether approval-required runs stopped instead of self-executing
- whether cost / latency increased abnormally
- whether evidence and trace references remain re-checkable for reviewers

Trace review is not a separate fashion accessory. It is the evidence path that makes prompt regression and workflow behavior auditable.

## 5. Version and Compare Prompt Changes
Prompt comparison should not be a debate about which phrasing feels better. The comparison should use the same cases, the same rubric, and, when possible, the same model conditions. The most useful questions are:

1. did the number of passing cases increase?
2. did the severe failure modes decrease?
3. did structured output and approval handling become more stable?
4. did tool-call and trace behavior improve?
5. did cost / latency variance decrease?

Aggregate scores are not enough on their own. Two prompts can have similar average scores while behaving very differently on a high-risk case. A prompt that improves average quality but starts bypassing approval gates should not be adopted. Conversely, a small latency increase can be acceptable if it eliminates severe failure.

A practical comparison record should track at least:

- prompt version
- model or runtime version
- eval suite version
- rubric version
- tool / approval policy version

Once those variables are explicit, the team can explain why a prompt passed last week and failed this week. Versioning is not only about the prompt text. It is about the workflow contract around the prompt.

## Bad / Good Example
Bad:

```text
This prompt worked once yesterday, so it is good enough.
```

That is folklore, not evaluation. It cannot distinguish an easy input from a reliable prompt, and it cannot detect regression after the prompt changes.

Good:

```text
Use at least five cases from `evals/prompt-contract-cases.json` as the fixed eval set.
Compare v1 and v2 with the rubric in `evals/rubrics/feature-spec.json`.
Treat `feature-001-missing-info`, `feature-001-approval-boundary`, and
`bugfix-001-regression-guard` as high-priority cases and record improvements and regressions separately.
```

This version treats the prompt as an engineering artifact. The same inputs and the same evaluation axis make the comparison reproducible.

Comparison points:
- The bad version mistakes one successful run for quality.
- The good version fixes the eval set, rubric, and approval boundary.
- The good version assumes regression checking, trace review, and version comparison from the start.

## Worked Example
Use `FEATURE-001` in `sample-repo` and compare two versions of the feature prompt. Assume version 1 has three weaknesses:

- it handles missing information vaguely
- it is weak on artifact synchronization
- it does not clearly block scope creep

Version 2 strengthens those points by adding a `Missing Information Policy`, requiring docs and tests to be updated together, forbidding out-of-scope UI or API changes, and making the `Approval Gate` explicit. To evaluate the change, focus on these cases from `evals/prompt-contract-cases.json`:

1. `feature-001-scope`
   - does the prompt keep ranking and typo correction out of the current requirement?
2. `feature-001-missing-info`
   - does the prompt surface missing information explicitly and stop or record it in `Remaining Gaps`?
3. `feature-001-artifact-sync`
   - does the prompt treat the product spec, acceptance criteria, and ADR as required synchronized artifacts?
4. `feature-001-approval-boundary`
   - does the run stop at approval-required operations instead of continuing into external access or dependency changes?

Use `evals/rubrics/feature-spec.json` as the scoring axis. The expected improvement looks like this:

| Criterion | Typical v1 failure | Improvement expected in v2 |
|---|---|---|
| Scope | adds ranking without approval | preserves the written Non-goals |
| Missing Information | silently fills gaps | lists missing information explicitly |
| Artifacts | leaves docs behind | names spec, acceptance criteria, and ADR together |
| Approval boundary | proceeds into approval-required operations | returns an approval gate and stop condition |

The important point is that prompt quality is not described as a feeling. It is compared case by case, with a stated rubric and a record of what improved and what remains weak. That is how prompt evaluation becomes an engineering discipline.

## Exercises
1. Create five eval cases for `feature-contract`. Include at least one case each for `scope creep`, `missing information`, and `artifact sync`.
2. Create a comparison record template for prompt v1 and v2 on the same feature task. It must preserve per-case pass/fail, severe failures, and observation notes.

## Referenced Artifacts
- `evals/prompt-contract-cases.json`
- `evals/rubrics/feature-spec.json`
- `scripts/run-prompt-evals.py`

## Source Notes / Further Reading
- When you need to revisit this chapter, treat `evals/prompt-contract-cases.json`, `evals/rubrics/feature-spec.json`, and `scripts/run-prompt-evals.py` as the source of truth. Prompt quality should be judged by case and rubric deltas, not by tone or intuition.
- For the next navigation step, see `manuscript-en/backmatter/00-source-notes.md` under `### CH04 Evaluate Prompts` and `manuscript-en/backmatter/01-reading-guide.md` under `## Prompts and Requirements Shaping`.

## Chapter Summary
- Good prompts are judged by eval cases, rubrics, and regression checks rather than one-off success.
- Prompt and workflow evaluation become practical when the repo keeps a reusable input set, a scoring structure, and trace-linked evidence that survive prompt revisions.
- Once prompt and workflow behavior become evaluable, the next bottleneck is keeping the right assumptions and artifacts visible over time. The next chapter moves into Context Engineering.

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch04-prompt-evals.md`
- This English draft preserves the workflow-evaluation expansion, trace-review framing, and approval-boundary comparison model introduced in the Japanese chapter.
