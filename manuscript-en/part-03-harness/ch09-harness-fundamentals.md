---
id: ch09
title: Foundations of Harness Engineering
status: scaffold
source_ja: manuscript/part-03-harness/ch09-harness-fundamentals.md
artifacts:
  - scripts/init.sh
  - scripts/verify-sample.sh
  - sample-repo/docs/harness/single-agent-runbook.md
  - sample-repo/docs/harness/permission-policy.md
  - sample-repo/docs/harness/done-criteria.md
dependencies:
  - ch05
  - ch06
  - ch07
  - ch08
---

# Foundations of Harness Engineering

## Role in This Book
This scaffold mirrors the Japanese chapter that moves from context design to execution design. The English version must preserve the same single-agent harness model: boundaries, permissions, completion rules, and retry behavior.

## Learning Objectives
- Explain the components of a single-agent harness
- Understand why permission policy and escalation matter
- Make done criteria explicit

## Outline
### 1. The shape of a single-agent harness
### 2. Init, permissions, and work boundaries
### 3. Completion criteria and exit rules
### 4. Safe retry and rollback
### 5. What lets a coding agent finish the work

## Exercises
1. Design a single-agent runbook for a bugfix task.
2. Define a permission policy and escalation rule.

## Referenced Artifacts
- `scripts/init.sh`
- `scripts/verify-sample.sh`
- `sample-repo/docs/harness/single-agent-runbook.md`
- `sample-repo/docs/harness/permission-policy.md`
- `sample-repo/docs/harness/done-criteria.md`

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch09-harness-fundamentals.md`
- Publication target: preserve the same bugfix harness example and boundary rules.
