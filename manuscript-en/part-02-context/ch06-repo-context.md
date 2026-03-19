---
id: ch06
title: Design Repo Context
status: scaffold
source_ja: manuscript/part-02-context/ch06-repo-context.md
artifacts:
  - AGENTS.md
  - manuscript/AGENTS.md
  - sample-repo/AGENTS.md
  - sample-repo/docs/repo-map.md
  - sample-repo/docs/architecture.md
  - sample-repo/docs/coding-standards.md
dependencies:
  - ch05
---

# Design Repo Context

## Role in This Book
This scaffold mirrors the Japanese chapter that explains how a coding agent reads a repo. The English version must preserve the same division of work between AGENTS.md, repo-map, architecture docs, and coding standards.

## Learning Objectives
- Explain why a giant AGENTS.md is a bad fit
- Design root / manuscript / sample-repo instruction layering for Codex CLI
- Separate the roles of a repo-map and an architecture doc

## Outline
### 1. AGENTS.md is a map, not an encyclopedia
### 2. Divide work between repo-map and architecture
### 3. Define update boundaries for coding standards and docs
### 4. Estimate ownership and change impact
### 5. Build instruction layering for Codex CLI

## Exercises
1. Split a root AGENTS.md and a sample-repo AGENTS.md by responsibility.
2. Draft a repo-map and identify high-change areas.

## Referenced Artifacts
- `AGENTS.md`
- `manuscript/AGENTS.md`
- `sample-repo/AGENTS.md`
- `sample-repo/docs/repo-map.md`
- `sample-repo/docs/architecture.md`
- `sample-repo/docs/coding-standards.md`

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch06-repo-context.md`
- Publication target: preserve the same repo-context layering and update-boundary guidance.
