---
id: ch08
title: Reuse Skills and Context Packs
status: scaffold
source_ja: manuscript/part-02-context/ch08-skills-and-context-pack.md
artifacts:
  - .agents/skills/draft-chapter/SKILL.md
  - .agents/skills/review-chapter/SKILL.md
  - sample-repo/.agents/skills/issue-to-plan/SKILL.md
  - sample-repo/.agents/skills/verification/SKILL.md
  - sample-repo/context-packs/ticket-search.md
dependencies:
  - ch05
  - ch06
  - ch07
---

# Reuse Skills and Context Packs

## Role in This Book
This scaffold mirrors the Japanese chapter that separates repeatable workflows from task-specific context. The English version must preserve the same distinction between skills, user skills, repo skills, and context packs.

## Learning Objectives
- Explain the boundary between a skill and a normal prompt
- Define a standard SKILL.md structure
- Design context packs at the right granularity

## Outline
### 1. When a prompt becomes a skill
### 2. Structure a SKILL.md
### 3. Separate repo skills from user skills
### 4. Build a context pack
### 5. Manage skill versioning and breaking changes

## Exercises
1. Create an issue-to-plan skill.
2. Create a PR review skill and fix the review criteria.

## Referenced Artifacts
- `.agents/skills/draft-chapter/SKILL.md`
- `.agents/skills/review-chapter/SKILL.md`
- `sample-repo/.agents/skills/issue-to-plan/SKILL.md`
- `sample-repo/.agents/skills/verification/SKILL.md`
- `sample-repo/context-packs/ticket-search.md`

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch08-skills-and-context-pack.md`
- Publication target: preserve the same workflow reuse model and context-pack design rules.
