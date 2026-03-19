---
id: ch02
title: Design Prompts as Contracts
status: scaffold
source_ja: manuscript/part-01-prompt/ch02-prompt-as-contract.md
artifacts:
  - prompts/bugfix-contract.md
  - prompts/feature-contract.md
  - checklists/prompt-contract-review.md
dependencies:
  - ch01
---

# Design Prompts as Contracts

## Role in This Book
This scaffold mirrors the Japanese chapter that defines Prompt Engineering as contract design. The English version must preserve the same operational framing and avoid drifting into generic chatbot advice.

## Learning Objectives
- Separate objective, constraints, completion criteria, and forbidden actions
- Compare weak prompts and operational prompts with explicit review criteria
- Build different prompt contracts for feature work and bugfix work

## Outline
### 1. A prompt is an input/output contract
### 2. Separate objective, constraints, completion criteria, and forbidden actions
### 3. State assumptions and handle missing information
### 4. Compare bad prompts and good prompts
### 5. Review prompts as operational artifacts

## Exercises
1. Rewrite “add search” as a contract prompt.
2. Make `done` explicit for a bugfix task in five points.

## Referenced Artifacts
- `prompts/bugfix-contract.md`
- `prompts/feature-contract.md`
- `checklists/prompt-contract-review.md`

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch02-prompt-as-contract.md`
- Publication target: preserve the same contract elements, examples, and single-task reliability scope.
