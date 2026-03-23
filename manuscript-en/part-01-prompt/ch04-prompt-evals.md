---
id: ch04
title: Evaluate Prompts
status: scaffold
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
This scaffold mirrors the Japanese chapter that treats prompt quality as an engineering concern. The English version must preserve the same focus on eval cases, rubrics, regression checks, and version comparison.

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

## Exercises
1. Create five eval cases.
2. Compare a v1 and v2 prompt and record which is more stable.

## Referenced Artifacts
- `evals/prompt-contract-cases.json`
- `evals/rubrics/feature-spec.json`
- `scripts/run-prompt-evals.py`

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch04-prompt-evals.md`
- Publication target: preserve the same worked example, evaluation framing, and practical regression workflow.
