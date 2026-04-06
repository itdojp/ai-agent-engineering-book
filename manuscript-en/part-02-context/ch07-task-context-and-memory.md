---
id: ch07
title: Task Context and Session Memory
status: drafted
source_ja: manuscript/part-02-context/ch07-task-context-and-memory.md
artifacts:
  - sample-repo/tasks/FEATURE-001-brief.md
  - sample-repo/tasks/FEATURE-001-progress.md
  - docs/en/session-memory-policy.md
  - .github/ISSUE_TEMPLATE/task.yml
dependencies:
  - ch05
  - ch06
---

# Task Context and Session Memory

## Role in This Book
CH06 explained how to design repo context so a coding agent can find the right entry point. That is still not enough to answer two operational questions: what does this specific issue require, and where did the previous session stop? Context Engineering becomes practical only when GitHub issues are converted into executable task briefs and session restart depends on artifacts rather than on chat history.

This chapter shows how to turn an issue into a task brief, how to structure a Progress Note, how to design handoff and restart, and how to prevent summary drift. The recurring example is `FEATURE-001` in `sample-repo`, but the same model also applies to manuscript work.

## Learning Objectives
- Convert a GitHub issue into a task brief
- Understand the minimum fields in a coding agent `Progress Note`
- Design a workflow that prevents summary drift

## Outline
### 1. Convert an issue into a task brief
### 2. Format a coding agent `Progress Note`
### 3. Design handoff and restart
### 4. Avoid summary drift
### 5. Define minimum inputs for session restart

## 1. Convert an Issue into a Task Brief
A GitHub issue is usually good enough for humans to agree on scope, but still too rough for a coding agent to execute safely. The repository task template in `.github/ISSUE_TEMPLATE/task.yml` only asks for `Goal`, `Deliverables`, and `Acceptance Criteria`. Those fields are necessary, but they still leave out artifact inputs, constraints, verification, and explicit out-of-scope boundaries.

That is why the issue should be normalized into a task brief. `sample-repo/tasks/FEATURE-001-brief.md` adds `Source`, `Scope`, `Inputs`, `Constraints`, `Verification`, `Open Questions`, and `Out of Scope`. This is not just a longer issue description. It is the format that turns a work request into an execution contract.

Two rules matter during the conversion:

- do not duplicate repo context that already belongs in architecture docs or coding standards
- make done conditions and verification explicit before implementation starts

If the brief restates the whole repo, it becomes noisy. If it omits verification or out-of-scope boundaries, the coding agent can stop after a plausible partial change and still claim progress.

## 2. Format a Progress Note
If the task brief is the stable task context, the Progress Note is the mutable session context. `sample-repo/tasks/FEATURE-001-progress.md` and `docs/en/session-memory-policy.md` define the required fields: `Current Goal`, `Completed`, `Decided`, `Open Questions`, `Changed Files`, `Last Verify`, `Resume Steps`, and `Next Step`. `Status` can exist as a quick scan aid, but it is not the source of truth.

The purpose of this format is not to preserve every step of exploration. Its purpose is to let the next session resume without rereading the full chat log. That means the Progress Note should only record what changed in this session:

- `Decided` contains conclusions confirmed by verification or by an artifact update
- `Open Questions` contains unresolved scope or design points
- `Last Verify` records the most recent verification command and result

The most common mistake is to paste brief content into the Progress Note. Goal, constraints, and acceptance criteria already belong in the task brief. The Progress Note should record session delta, not duplicate stable context.

## 3. Design Handoff and Restart
Good handoff is not a long narrative. It is a restart procedure. `docs/en/session-memory-policy.md` defines the minimum `Restart Packet (Resume Packet)` as four items. In this chapter, that minimal packet is also referred to as a `Restart Packet (Resume Packet)`:

1. the task brief
2. the latest Progress Note
3. the latest verification result
4. the file list to reopen when resuming

That set is small, but it is enough. In `FEATURE-001`, a new agent can read `tasks/FEATURE-001-brief.md` to reestablish scope, read `tasks/FEATURE-001-progress.md` to see what was decided and what remains open, and then rerun or confirm the latest verify command before continuing.

Without that packet, handoff turns into vague memory: “we were probably still discussing search behavior.” That is not operational context. A useful handoff brings the next session back to the same canonical artifacts.

## Reader-facing Table
### Restart Packet (Resume Packet) and Its Role

| Artifact | Why it exists | What it stabilizes |
|---|---|---|
| `tasks/FEATURE-001-brief.md` | Restates the issue as an execution contract | scope, inputs, constraints, acceptance criteria, verification |
| `tasks/FEATURE-001-progress.md` | Captures session-local progress | what changed, what was decided, what remains open |
| latest verify result | Re-establishes live state before more edits | whether the repo currently matches the note |
| `Resume Steps` file list | Reduces restart thrash | reading order and first files to reopen |

This packet works because it separates stable task context from mutable session context. If those layers are mixed together, restart becomes guesswork.

## 4. Avoid Summary Drift
Summary drift gets worse every time work crosses a session boundary. The main causes are predictable:

- an unverified hypothesis is written as if it were already decided
- the Progress Note paraphrases the brief and quietly changes the meaning
- pre-verify and post-verify states are mixed into one summary

`FEATURE-001` gives a concrete example. Writing “search and status / assignee filters will be unified” into `Decided` is unsafe. The brief treats that as an open question for later work. If the note upgrades it to a decision too early, the next session may implement new scope that was never approved.

The discipline is simple:

- copy acceptance criteria from the task brief instead of rewording them casually
- keep unresolved points inside `Open Questions`
- record verify results explicitly as pass or fail

Session memory should be short, but it should never compress away the difference between a fact, a guess, and a pending decision.

## 5. Define Minimum Inputs for Session Restart
Restart does not require the full conversation transcript. In most engineering work, the following order is enough:

1. read the task brief to confirm `Goal`, `Constraints`, `Acceptance Criteria`, and `Verification`
2. read the latest Progress Note to check `Decided`, `Open Questions`, and `Next Step`
3. confirm or rerun the latest verify command to restore live context
4. open the files listed in `Resume Steps`

That order matters because it moves from stable artifacts to mutable artifacts and only then to live state. If a session starts from the old chat log or from a stale summary, scope drift becomes likely. If it starts from the brief and verify evidence, the restart stays grounded.

Designing Task Context and Session Memory this way removes one of the most common AI agent failure modes: stopping because the previous conversation is gone.

## Bad / Good Example
Bad:

```text
I read the issue.
The previous session was probably still discussing search behavior,
so I will continue from there.
I will look at the tests only if I need them.
```

This approach fixes nothing. Scope, verification, unresolved questions, and confirmed decisions are all left implicit. Once the session changes, summary drift is almost guaranteed.

Corrected:

```text
Read `sample-repo/tasks/FEATURE-001-brief.md` first and confirm the Goal,
Constraints, Acceptance Criteria, and Verification.
Then read `sample-repo/tasks/FEATURE-001-progress.md` and separate
`Decided` from `Open Questions`.
Finally, rerun the latest verify command and reopen files in `Resume Steps`.
```

This version starts from the canonical task artifact, uses the Progress Note only as session memory, and restores live state before new edits begin.

Comparison points:
- The bad version treats the issue and session memory as the same thing.
- The bad version never fixes verify state or open questions.
- The corrected version separates stable context from mutable context and makes restart reproducible.

## Exercises
1. Convert a GitHub issue into a task brief.
2. Build a `Restart Packet (Resume Packet)` that starts from a `Progress Note` and includes the task brief and latest verify result.

## Referenced Artifacts
- `sample-repo/tasks/FEATURE-001-brief.md`
- `sample-repo/tasks/FEATURE-001-progress.md`
- `docs/en/session-memory-policy.md`
- `.github/ISSUE_TEMPLATE/task.yml`

## Source Notes / Further Reading
- To revisit this chapter quickly, start with `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/tasks/FEATURE-001-progress.md`, and `docs/en/session-memory-policy.md`. These three artifacts show the boundary between stable task context and mutable session context. The policy uses `Restart Packet (Resume Packet)` as the term for this minimal restart artifact, and this chapter uses the same term.
- For the backmatter navigation path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH07 Task Context and Session Memory` and `manuscript-en/backmatter/01-reading-guide.md` under `## Context and Repo Design`.

## Chapter Summary
- A GitHub issue is too coarse to function as task context for a coding agent. It should be normalized into a task brief before execution starts.
- A Progress Note is session memory, not a duplicate of the brief. Its job is to record session-local decisions, open questions, changed files, and verification status.
- A reliable restart begins from the task brief, then the Progress Note, then the latest verify result. The next chapter turns this repeatable task context into reusable skills and context packs.

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch07-task-context-and-memory.md`
- This English draft preserves the same task-brief model, summary-drift controls, and restart order as the Japanese chapter.
