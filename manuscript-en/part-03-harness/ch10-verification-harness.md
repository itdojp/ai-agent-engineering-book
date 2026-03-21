---
id: ch10
title: Build a Verification Harness
status: scaffold
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
This scaffold mirrors the Japanese chapter that defines verification as more than tests. The English version must preserve the same combination of tests, execution order, evidence, CI, and approval gates.

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

## Exercises
1. Add a failing test before fixing the behavior.
2. Create an evidence bundle for a UI change.

## Referenced Artifacts
- `.github/workflows/verify.yml`
- `checklists/verification.md`
- `sample-repo/tests/test_ticket_search.py`
- `artifacts/evidence/README.md`

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch10-verification-harness.md`
- Publication target: preserve the same verification pipeline, evidence model, and review-ready framing.
