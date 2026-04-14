# Context Model

Context Engineering does not mean handing an AI agent everything. It means separating the information the agent sees by role and freshness. A Prompt Contract defines the task boundary. Context defines the decision material. Even with a long context window, this split does not become optional.

## Context Surface

In practice, context does not arrive through one channel. An AI agent receives decision material through multiple surfaces:

- instructions: `AGENTS.md`, repo policy, skill guardrails
- docs and task artifacts: briefs, specs, ADRs, acceptance criteria
- session memory: `Progress Note`, open questions, next step
- tool output: test, lint, verify, and search results
- external data: official docs, runtime status, issue tracker
- persisted note: concise notes kept only to support resume

The goal is not to maximize the number of surfaces. The goal is to avoid mixing canonical sources and live evidence.

## Categories

| Category | Primary Responsibility | Representative Artifacts | Typical Handling | Cache / Refresh Approach |
|---|---|---|---|---|
| Persistent Context | Explain repo invariants | `AGENTS.md`, architecture doc, glossary, coding standards | Keep as persistent artifacts in the repo | Relatively stable. Read at the start of work and refresh only when the source changes. |
| Task Context | Fix scope and done conditions for the current issue | issue, task brief, product spec, ADR, acceptance criteria | Keep verbatim or compact while preserving the contract | Updated per issue. Always refresh when the source artifact changes. |
| Session Context | Make interruption and restart safe | `Progress Note`, open questions, next step, latest verify summary | Keep short as a session summary | Degrades quickly. Update every session and do not keep trusting old verify. |
| Tool Context | Preserve the latest evidence | grep results, test output, verify log, screenshots | Treat as live tool output | Prefer re-fetch over long retention, and split durable evidence out when needed. |

## Responsibility Split

- persistent artifact
  - The source of truth that remains in the repo across sessions, such as `AGENTS.md`, specs, and the glossary.
- session summary
  - The minimum restart information, such as `Decided`, `Open Questions`, and `Next Step`, that preserves the last decisions and next move.
- live tool output
  - The current behavior or exploration result. Grep output, test output, and verify logs should be treated as refreshable evidence, not as permanent resident context.

## Rules

1. Do not use the prompt itself as a substitute for context.
2. Keep invariant information in persistent artifacts instead of pasting it into every task.
3. Push issue-specific decisions into the task brief.
4. Promote only cross-session facts into the session summary.
5. Treat full logs and exploration history as live tool output, and split them into evidence when needed.
6. Do not give the same weight to stable context that can be cached and live context that must be refreshed.
7. Do not copy secrets, credentials, or personal data values into a context pack or `Progress Note`.
8. Keep URLs and versions for external data in task context, but treat time-sensitive responses themselves as live context.

## Telling Stale from Live

- `sample-repo/docs/architecture.md` and `sample-repo/docs/coding-standards.md` are stale-safe persistent context. Read them at the start of the work.
- `sample-repo/tasks/FEATURE-001-brief.md` is task context. It fixes the scope for the current issue.
- `sample-repo/tasks/FEATURE-001-progress.md` is session context. Update it as the work moves.
- Output from `python -m unittest discover -s tests -v` is live context. Keep only the important points in the `Progress Note` and rerun it when needed.

## Resume / Refresh Rule

When resuming work, rebuild context in this order:

1. read persistent context
2. read the task brief and acceptance criteria
3. read the `Progress Note`
4. rerun verify or status commands to refresh live context

Do not resume from the `Progress Note` alone. A summary is a restart aid, not a replacement for the source of truth.

## Secret / Persist Boundary

- keep secret names, environment variable names, vault names, or lookup procedures, not the values
- do not copy raw tokens, cookies, or personal data into a `Progress Note`
- redact screenshots and verify logs if they contain secrets
- what must survive a restart is where to look and what to rerun, not the credential itself

## Ticket Search Example

For `FEATURE-001`, the minimum safe context is:

- persistent: `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`
- task: `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/acceptance-criteria/ticket-search.md`
- session: `sample-repo/tasks/FEATURE-001-progress.md`
- tool: the failure details from `sample-repo/tests/test_ticket_search.py` and the latest verify output

Without this split, the search spec, the previous session's guess, and stale test output all compete as if they had the same authority. That is how context poisoning starts. A long context window increases transport capacity, but the boundary between stable and live context still has to be designed. If the agent trusts an old verify summary without rerunning it, resume drift follows.
