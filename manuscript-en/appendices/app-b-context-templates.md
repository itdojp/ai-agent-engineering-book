# Context Templates

## Purpose

The goal of Context Engineering is not to hand the agent a long explanation. It is to deliver only the information required to complete the task, broken down by role. This appendix reorganizes the context artifacts used in CH05 through CH08 into reusable form.

Where the Prompt Contract fixes the input and output contract for one task, context artifacts fix the decision inputs around that task. If those roles are mixed, the prompt grows too large, the Progress Note starts overwriting the source of truth, and the context pack carries stale requirements. That is why the book keeps the task brief, the Progress Note, and the context pack as separate artifacts.

## Included Artifacts

- `templates/task-brief.md`
- `templates/progress-note.md`
- `templates/context-pack.md`
- `templates/en/task-brief.md`
- `templates/en/progress-note.md`
- `templates/en/context-pack.md`

## 1. Task Brief Template

`templates/task-brief.md` defines the canonical task-brief structure, and `templates/en/task-brief.md` provides the English counterpart for English-manuscript work. This is the core artifact of CH07 because it reshapes an issue into a task specification a coding agent can execute.

Each section has a clear role.

- `Source`: identify the issue or starting artifact
- `Goal`: fix the result this task must achieve
- `Scope`: name only the changes included in this run
- `Inputs`: list the specs, ADRs, code, tests, and docs that must be read
- `Deliverables`: make the updated artifacts explicit
- `Constraints`: preserve public contracts, non-functional limits, and update order
- `Acceptance Criteria`: translate the work into verifiable conditions
- `Verification`: lock the commands that must be run
- `Open Questions`: isolate unresolved points without creating a competing source of truth
- `Out of Scope`: stop adjacent work from leaking in

`sample-repo/tasks/FEATURE-001-brief.md` is the worked example. It is short, but it stays reproducible across sessions because the `Goal`, `Inputs`, `Acceptance Criteria`, and `Verification` sections are all present.

## 2. Progress Note Template

`templates/progress-note.md` defines the canonical structure, and `templates/en/progress-note.md` gives the English counterpart. The rule that matters most is this: the Progress Note must not rewrite the task brief. It is a support record that shows current position, not the source of truth itself.

The recommended sections are these.

- `Status`: optional coarse state such as `in-progress`, `blocked`, or `ready-for-handoff`
- `Current Goal`: the one-sentence work package for this session
- `Completed`: what finished in this session
- `Decided`: what was firmly decided during the session
- `Open Questions`: what still needs resolution
- `Last Verify`: the most recent verify command and its result
- `Changed Files`: the diffs a reviewer or handoff owner should track
- `Resume Steps`: the artifact order for the next restart
- `Next Step`: the next single work package

`sample-repo/tasks/FEATURE-001-progress.md` shows the practical target. The note should be short. It does not need to become a diary. It only needs to tell the next worker what changed, what still blocks the task, and what to read first.

## 3. Context Pack Template

`templates/context-pack.md` defines the canonical structure, and `templates/en/context-pack.md` gives the English counterpart. As CH08 explains, a context pack is not a repo summary. It is the smallest reading bundle that lets one task move safely.

The basic structure is:

- `Purpose`: which task this context pack supports
- `Read Order`: the sequence in which artifacts should be read
- `Canonical Facts`: the facts this task must not override
- `Live Checks`: the latest verification, progress note, or state checks that must be refreshed each time
- `Exclusions`: the topics intentionally left out of this task
- `Done Signals`: the conditions that tell the worker the task is actually complete

`sample-repo/context-packs/ticket-search.md` is the worked example for `FEATURE-001`. The key rule is that the context pack must not redefine the specification. The spec still lives in the spec, acceptance criteria, and tests. The context pack only helps the worker reach those sources in a safe reading order.

## 4. Operational Caution

When these context artifacts are used together, keep the priority order stable.

1. task brief
2. spec / ADR / acceptance criteria / tests
3. Progress Note
4. context pack

If the Progress Note or the context pack becomes stronger than the task brief, stale decisions linger too long. In Context Engineering, what matters is not only what to write. It is also what not to over-document.

## Parity Notes

- Japanese source: `manuscript/appendices/app-b-Context-テンプレート集.md`
- Publication target: preserve the Japanese appendix's separation of task brief, Progress Note, and context pack, along with the source-of-truth priority order and the practical warnings against over-documentation.

## Referenced Artifacts

- `templates/task-brief.md`
- `templates/progress-note.md`
- `templates/context-pack.md`
- `templates/en/task-brief.md`
- `templates/en/progress-note.md`
- `templates/en/context-pack.md`
- `sample-repo/tasks/FEATURE-001-brief.md`
- `sample-repo/tasks/FEATURE-001-progress.md`
- `sample-repo/context-packs/ticket-search.md`
