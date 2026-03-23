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
The prompt that worked yesterday may not behave the same way tomorrow. CH02 defined the Prompt Contract. CH03 turned vague requests into product specs, acceptance criteria, and ADRs. The next question is operational: how do you decide whether one prompt is actually better than another?

Prompt Engineering only becomes engineering when prompt quality is evaluated rather than assumed. That requires eval cases, rubrics, regression checks, and version comparison. This chapter stays at the prompt level. Context Engineering and Harness Engineering are evaluated later.

## Learning Objectives
- Design eval cases separately from rubrics
- Run prompt regression checks automatically
- List comparison points for prompt or model updates

## Outline
### 1. Good prompts must be evaluated
### 2. Build an eval set
### 3. Distinguish rubrics from goldens
### 4. Run prompt regression checks
### 5. Version and compare prompt changes

## 1. Good Prompts Must Be Evaluated
Prompt quality should be judged by behavior, not by impression. A prompt for `FEATURE-001` might appear successful once, but a single success does not prove that the prompt is good. The input may have been unusually easy, or the model may have filled in missing details in a convenient way. The engineering question is whether the prompt remains stable across similar tasks, boundary cases, and later revisions.

In this chapter, evaluation is limited to the prompt layer. The target is the Prompt Contract or requirements-shaping prompt itself: does it consistently produce the required structure, boundaries, and reporting shape? That keeps the responsibility of Prompt Engineering narrow and testable.

| Lens | What it checks | Covered in this chapter? |
|---|---|---|
| Prompt-level evaluation | whether purpose, constraints, completion criteria, and output format remain stable | Yes |
| Context-level evaluation | whether the right artifacts stay visible to the agent over time | Not yet |
| Harness-level evaluation | whether verify, retries, permissions, and evidence capture work | Not yet |

Good prompts can be evaluated. Prompts that cannot be evaluated cannot be versioned or improved reliably.

## 2. Build an Eval Set
An eval set is a list of inputs that are likely to expose prompt weaknesses. It is not just a collection of random examples. The most useful cases are the ones that stress the prompt with ambiguity, missing information, scope pressure, reporting drift, and artifact-sync risk.

`evals/prompt-contract-cases.json` defines five cases across `feature-contract` and `bugfix-contract`. The set is intentionally small, but it already covers several failure patterns:

- whether the prompt keeps `FEATURE-001` inside scope
- whether the prompt handles missing information explicitly
- whether docs, acceptance criteria, and ADRs remain part of the artifact-sync boundary
- whether the bugfix contract preserves its regression guard
- whether the reporting format remains reviewable

Eval cases are more useful when they are built from failure modes than when they are built from easy examples. If you only test ideal inputs, prompt weaknesses stay hidden. A feature prompt should be tested not only against “make search easier to use” but also against requests that quietly invite scope creep or guesswork.

A practical sequence is:

1. list the failure modes
   - scope creep
   - missing information
   - artifact update drift
   - missing verify requirements
2. assign at least one case to each failure mode
3. define `must_include` and `must_not_include`
4. reuse the same cases after every prompt revision

An eval set is also not a one-time asset. When a new failure is discovered, the correct response is to add a case that reproduces it. That is the foundation of prompt regression checking.

## 3. Rubrics Versus Goldens
Prompt evaluation works better when goldens and rubrics are treated as separate tools. A golden tries to match a fixed expected output. A rubric scores whether the output satisfies the required structure or behavior.

| Method | Best for | Weakness |
|---|---|---|
| Golden | fixed section order, fixed wording, short outputs | brittle when wording varies |
| Rubric | requirement shaping, design comparison, structured free text | needs scoring logic or human review |

The outputs in CH03, such as a product spec or ADR, contain free text. A full-string golden would reject good answers simply because the wording is different. That is why CH04 centers the rubric instead. `evals/rubrics/feature-spec.json` defines criteria such as Objective, Scope, Inputs, Constraints, Completion, Missing Information, and Output Format.

The rubric does not ask whether the prompt output matches an ideal paragraph verbatim. It asks whether the result is usable as an implementation-ready artifact. That is the engineering move: evaluate structure and decision quality rather than literary similarity.

This does not mean goldens are useless. A golden check is still a good fit for section names or output ordering. In practice, both methods are useful. The center of gravity in this chapter remains the rubric because the artifacts are structured but not fully fixed strings.

## 4. Prompt Regression Checks
A one-line prompt change can break cases that used to pass. That is why prompts need regression checks in the same way code does. The workflow is simple: run the same eval set against prompt version 1 and version 2, then compare the differences.

This repo includes `scripts/run-prompt-evals.py` as a lightweight consistency check. At this stage it does not call a model. Instead, it verifies that the prompt-eval artifacts remain internally consistent:

- required Prompt Contract headings exist
- `evals/prompt-contract-cases.json` is structurally valid
- `evals/rubrics/feature-spec.json` is structurally valid

That is not yet a full evaluation runner, but it is still useful. Prompt evaluation has to start by keeping the cases and rubric themselves healthy inside the repo. If the evaluation assets drift or break, later comparisons stop being trustworthy.

The actual regression idea is still the same. Suppose version 1 of `feature-contract` handled missing information weakly. Version 2 adds a `Missing Information Policy`, tighter artifact-sync wording, and a stronger prohibition against out-of-scope UI or API changes. The same suite should then show whether the target cases improved and whether other cases regressed.

## 5. Version and Compare Prompt Changes
Prompt comparison should not be a debate about which phrasing feels better. The comparison should use the same cases, the same rubric, and, when possible, the same model conditions. Three questions matter most:

1. did the number of passing cases increase?
2. did the severe failure modes decrease?
3. did the variance in output decrease?

Aggregate scores are not enough on their own. Two prompts can have similar average scores while behaving very differently on a high-risk case. A prompt that still allows regression guard failure in `BUG-001` is not acceptable just because its overall average rises slightly elsewhere.

A practical comparison record should track:

- prompt version
- model version
- eval suite version
- rubric version

That makes it possible to explain why a prompt passed last week and failed this week. Sometimes the prompt changed. Sometimes the model changed. Sometimes the rubric became stricter. Version comparison only becomes useful when those variables are recorded explicitly.

## Bad / Good Example
Bad:

```text
This prompt worked once yesterday, so it is good enough.
```

That is folklore, not evaluation. It cannot distinguish an easy input from a reliable prompt, and it cannot detect regression after the prompt changes.

Corrected:

```text
Use the 5 cases in `evals/prompt-contract-cases.json` as the fixed eval set.
Compare v1 and v2 with the rubric in `evals/rubrics/feature-spec.json`.
Treat `feature-001-missing-info` and `bugfix-001-regression-guard` as high-priority cases and record improvements and regressions separately.
```

This version treats the prompt as an engineering artifact. The same inputs and the same evaluation axis make the comparison reproducible.

Comparison points:
- The bad version mistakes one successful run for quality.
- The corrected version fixes the eval cases, rubric, and high-priority cases.
- The corrected version assumes regression checking and version comparison from the start.

## Worked Example
Use `FEATURE-001` in `sample-repo` and compare two versions of the feature prompt. Assume version 1 has three weaknesses:

- it handles missing information vaguely
- it is weak on artifact synchronization
- it does not clearly block scope creep

Version 2 strengthens those points by adding a `Missing Information Policy`, requiring docs and tests to be updated together, and forbidding out-of-scope UI or API changes. To evaluate the change, focus on these cases from `evals/prompt-contract-cases.json`:

1. `feature-001-scope`
   - does the prompt keep ranking and typo correction out of the current requirement?
2. `feature-001-missing-info`
   - does the prompt surface missing information explicitly and stop or record it in `Open Questions`?
3. `feature-001-artifact-sync`
   - does the prompt treat the product spec, acceptance criteria, and ADR as required synchronized artifacts?

Use `evals/rubrics/feature-spec.json` as the scoring axis. The expected improvement looks like this:

| Criterion | Typical v1 failure | Improvement expected in v2 |
|---|---|---|
| Scope | adds ranking without approval | preserves the written Non-goals |
| Missing Information | silently fills gaps | lists missing information explicitly |
| Artifacts | leaves docs behind | names spec, acceptance criteria, and ADR together |

The important point is that prompt quality is not described as a feeling. It is compared case by case, with a stated rubric and a record of what improved and what remains weak.

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
- Prompt evaluation becomes practical when the repo keeps a reusable input set and a scoring structure that can survive prompt revisions.
- Once prompts become evaluable, the next bottleneck is keeping the right assumptions and artifacts visible over time. The next chapter moves into Context Engineering.

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch04-prompt-evals.md`
- This English draft preserves the same worked example, evaluation framing, and regression workflow as the Japanese chapter.
