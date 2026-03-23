---
id: ch06
title: Design Repo Context
status: drafted
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
If an AI agent enters a repo and immediately bounces between `AGENTS.md`, `README.md`, and `sample-repo/tests/`, the entry design is weak. CH05 introduced the context categories. The next step is to design the persistent context that helps a coding agent find the right starting point the moment it enters the repo.

This chapter explains how to divide work among `AGENTS.md`, a repo map, an architecture document, and coding standards. The primary target is a coding agent such as Codex CLI, but the same structure also reduces review overhead for humans.

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

## 1. `AGENTS.md` Is a Map, Not an Encyclopedia
`AGENTS.md` should not try to explain the entire repo. Its job is to tell the AI agent what must not be violated, what to read next, and which artifacts matter first. In this repo, the root `AGENTS.md` keeps only the repo-wide invariants, while `manuscript-en/AGENTS.md` and `sample-repo/AGENTS.md` carry the local detail for their own areas.

That split matters because a root file that contains everything mixes unrelated detail into every task. A manuscript-only edit does not need the sample domain rules every time. A sample-repo code change cares more about verify commands and domain constraints than about prose style for book chapters. Layering lets the agent read only the detail that belongs to the current directory.

Good `AGENTS.md` files are not encyclopedias. They are routing artifacts. Deeper explanations of repo structure and design rationale belong in other docs.

## 2. Divide Work Between the Repo Map and the Architecture Doc
`sample-repo/docs/repo-map.md` and `sample-repo/docs/architecture.md` can look similar, but they solve different problems. The repo map tells the agent where things are and in what order to read them. The architecture doc explains why the structure exists and where behavior should change.

`sample-repo/docs/repo-map.md` gives a read order across docs, tasks, context packs, code, and tests. It is the indexing document. `sample-repo/docs/architecture.md` explains the responsibilities of `models.py`, `store.py`, `service.py`, and `tests/`, along with the change rules. If `FEATURE-001` should be implemented in `service.py`, that rationale belongs in the architecture doc, not in the repo map.

The difference is simple:

- the repo map is for finding
- the architecture doc is for deciding

If one document tries to do both jobs, the map becomes long and the architecture doc turns into an index.

## 3. Define Update Boundaries for Coding Standards and Docs
`sample-repo/docs/coding-standards.md` should do more than describe coding style in the abstract. Its more important role is to define which artifacts must be updated together when behavior changes.

Docs drift usually happens because the repo treats code changes, spec changes, and task-artifact changes as separate concerns. In this repo, a public behavior change requires tests. A spec change requires product spec, acceptance criteria, and ADR updates. If a task is paused or handed off, the progress note must also be updated. Those rules make it harder for an AI agent to stop after code-only green results.

This is also how repo context helps defend against the failure modes from CH01. The update boundary reduces both accidental breakage and stopping early. In an artifact-heavy repo, update boundaries often matter more than style guidance.

## 4. Estimate Ownership and Change Impact
Repo context also supports ownership and impact estimation. If `sample-repo/src/support_hub/service.py` changes, the minimum downstream check usually includes related tests such as `sample-repo/tests/test_service.py` or `sample-repo/tests/test_ticket_search.py`, plus the relevant spec, acceptance criteria, and progress note.

Ownership does not have to mean named people. It can also mean artifact responsibility:

- `architecture.md` owns design rationale
- `coding-standards.md` owns update discipline
- `tasks/` own current task scope
- `context-packs/` own reusable reading bundles

If those responsibilities stay fuzzy, the same explanation appears in multiple places and starts to drift. Context Engineering is not just about showing file paths. It is also about telling the agent what to re-check when a file changes.

## 5. Build Instruction Layering for Codex CLI
This repo becomes easier to reason about when instruction layering is kept explicit:

1. root `AGENTS.md`: repo-wide invariants, verify expectations, artifact-sync obligations
2. `manuscript/AGENTS.md`: chapter structure and manuscript style rules
3. `sample-repo/AGENTS.md`: domain constraints, verification rules, update boundaries
4. task brief or context pack: the scope, inputs, and done conditions for the current issue

With this layering, Codex CLI can start from the repo-wide frame, add directory-local detail, and then narrow to the current task. That keeps the context budget under control and avoids giant root instructions that nobody rereads carefully.

The critical rule is that each layer must have a distinct responsibility. The root stays short. Local instructions stay local. Task artifacts stay issue-specific. When that separation is preserved, repo context behaves like an operational system rather than a pile of long documents.

## Reader-facing Table
### Repo Context Reading Order

| Artifact | First question it answers | When to read it | What decision it fixes |
|---|---|---|---|
| `AGENTS.md` | What repo-wide constraints must not be violated? | immediately at task start | verify requirements, artifact sync, issue-scoped work boundaries |
| `manuscript/AGENTS.md` | What does acceptable manuscript work look like? | before editing manuscript files | chapter structure, exercise count, artifact-driven prose |
| `sample-repo/AGENTS.md` | What is the source of truth inside sample-repo? | before editing sample-repo files | domain constraints, docs update boundaries, sample verify |
| `sample-repo/docs/repo-map.md` | Where do I start reading and where is everything? | when identifying the target area | read order, hot paths, starting points |
| `sample-repo/docs/architecture.md` | Why is the repo structured this way, and where should behavior change? | before deciding an implementation path | layer responsibilities, change rules, impact range |
| `sample-repo/docs/coding-standards.md` | What must be updated together when behavior changes? | before implementation and before finish | tests, specs, acceptance criteria, progress-note update boundaries |

This order is also the descent from index to rationale. If the agent reads architecture before it knows where the relevant files are, the reasoning starts too early. If it stops at the repo map, it still lacks the “why” behind the change boundary.

## Bad / Good Example
Bad:

```text
Put book-wide operations, manuscript style rules, sample-repo domain rules,
verify procedures, and task-specific exceptions into the root `AGENTS.md`.
Then duplicate the same explanation in both the repo map and the architecture doc.
```

This design makes the entry point noisy. The root instruction file becomes too long, and unrelated detail appears in every task.

Corrected:

```text
Keep only repo-wide invariants in root `AGENTS.md`.
Put chapter structure and prose rules in `manuscript/AGENTS.md`.
Put verify rules and domain constraints in `sample-repo/AGENTS.md`.
Use `sample-repo/docs/repo-map.md` as the index.
Use `sample-repo/docs/architecture.md` to explain the service layer and change rules.
```

This version separates instruction responsibilities and lets the agent read only the documents that matter for the current target.

Comparison points:
- The bad version bloats the root instruction layer and breaks the context budget.
- The bad version duplicates the roles of the repo map and the architecture doc.
- The corrected version creates clear root / local / task layering and makes update boundaries visible.

## Exercises
1. Split a root `AGENTS.md` and a `sample-repo/AGENTS.md` by responsibility. State what must stay global and what should move down to the local layer.
2. Draft a repo map for a small repo and identify the high-change areas that should become hot paths.

## Referenced Artifacts
- `AGENTS.md`
- `manuscript/AGENTS.md`
- `sample-repo/AGENTS.md`
- `sample-repo/docs/repo-map.md`
- `sample-repo/docs/architecture.md`
- `sample-repo/docs/coding-standards.md`

## Source Notes / Further Reading
- When you need to revisit this chapter, start with `AGENTS.md`, `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`, and `sample-repo/docs/coding-standards.md`. Read the repo map as the index and the architecture doc as the design rationale.
- For the next navigation step, see `manuscript/backmatter/00-source-notes.md` under `### CH06 Repo Context を設計する` and `manuscript/backmatter/01-読書案内.md` under `## Context と repo 設計`.

## Chapter Summary
- Repo Context does not exist to explain the whole repo. It exists to help the AI agent find the correct starting point and the correct update boundary quickly.
- `AGENTS.md` works best as the map, the repo map as the index, the architecture doc as the design rationale, and coding standards as the update discipline.
- Once the repo entry point is stable, the next requirement is a context bundle that shrinks down to the current task. The next chapter turns issues into task briefs and session memory.

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch06-repo-context.md`
- This English draft preserves the same repo-context layering, role separation, and update-boundary guidance as the Japanese chapter.
