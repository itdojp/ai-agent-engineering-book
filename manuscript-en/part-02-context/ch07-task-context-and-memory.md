---
id: ch07
title: Task Context and Session Memory
status: scaffold
source_ja: manuscript/part-02-context/ch07-task-context-and-memory.md
artifacts:
  - sample-repo/tasks/FEATURE-001-brief.md
  - sample-repo/tasks/FEATURE-001-progress.md
  - docs/session-memory-policy.md
  - .github/ISSUE_TEMPLATE/task.yml
dependencies:
  - ch05
  - ch06
---

# Task Context and Session Memory

## Role in This Book
This scaffold mirrors the Japanese chapter that turns issues into task briefs and makes session restart reliable. The English version must preserve the same brief / Progress Note / verify packet model.

## Learning Objectives
- Convert a GitHub issue into a task brief
- Understand the minimum fields in a coding agent progress note
- Design a workflow that prevents summary drift

## Outline
### 1. Convert an issue into a task brief
### 2. Format a coding agent progress note
### 3. Design handoff and resume
### 4. Avoid summary drift
### 5. Define minimum inputs for session restart

## Exercises
1. Convert a GitHub issue into a task brief.
2. Build a resume packet that starts from a progress note and includes the task brief and verify result.

## Referenced Artifacts
- `sample-repo/tasks/FEATURE-001-brief.md`
- `sample-repo/tasks/FEATURE-001-progress.md`
- `docs/session-memory-policy.md`
- `.github/ISSUE_TEMPLATE/task.yml`

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch07-task-context-and-memory.md`
- Publication target: preserve the same handoff model, summary-drift controls, and resume order.
