---
id: ch11
title: Long-running Tasks and Multi-agent Work
status: scaffold
source_ja: manuscript/part-03-harness/ch11-long-running-and-multi-agent.md
artifacts:
  - sample-repo/docs/harness/feature-list.md
  - sample-repo/docs/harness/restart-protocol.md
  - sample-repo/docs/harness/multi-agent-playbook.md
  - sample-repo/tasks/FEATURE-002-plan.md
dependencies:
  - ch09
  - ch10
---

# Long-running Tasks and Multi-agent Work

## Role in This Book
This scaffold mirrors the Japanese chapter that explains how long-running work breaks and when multi-agent coordination is worth the cost. The English version must preserve the same restart packet and role-splitting model.

## Learning Objectives
- Explain why long-running tasks break
- Design a restart protocol
- Decide when to use single-agent versus multi-agent work

## Outline
### 1. Where long-running tasks break
### 2. Feature lists and progress tracking
### 3. Design a restart protocol
### 4. Separate planner, coder, and reviewer work
### 5. Decide when multi-agent work is justified

## Exercises
1. Split case C into planner, coder, and reviewer responsibilities.
2. Restart a failed long-running task through a restart protocol.

## Referenced Artifacts
- `sample-repo/docs/harness/feature-list.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/multi-agent-playbook.md`
- `sample-repo/tasks/FEATURE-002-plan.md`

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch11-long-running-and-multi-agent.md`
- Publication target: preserve the same long-running task model, restart rules, and role ownership guidance.
