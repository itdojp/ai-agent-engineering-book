# Context Model

Context Engineering does not mean handing an AI agent everything. It means separating the information the agent sees by role and freshness. A Prompt Contract defines the boundary of the task. Context defines the decision material.

## Context Surface

In practice, context does not arrive through one channel. An AI agent receives decision material through multiple surfaces:

- instructions: `AGENTS.md`, repo policy, skill guardrails
- docs and task artifacts: briefs, specs, ADRs, acceptance criteria
- session memory: Progress Note, open questions, next step
- tool output: test, lint, verify, and search results
- external data: official docs, runtime status, issue tracker
- persisted note: concise notes kept only to support resume

The point is not to maximize the number of surfaces. The point is to keep canonical sources separate from live evidence.

## Categories

| Category | Purpose | Typical Artifacts | Freshness | Persistence Policy | Location |
|---|---|---|---|---|---|
| Persistent Context | Explain repo-level invariants | `AGENTS.md`, architecture doc, glossary, coding standards | relatively stable | safe to keep in the repo | `docs/`, root |
| Task Context | Fix the scope and done condition for the current issue | issue, task brief, product spec, ADR, acceptance criteria | updated per issue | safe to keep in the repo | `tasks/`, `docs/` |
| Session Context | Make interruption and restart safe | Progress Note, open questions, next step, summarized verify status | degrades fastest | keep only verified facts and restart cues | `tasks/`, summary |
| Tool Context | Preserve the latest evidence | grep results, test output, verify log, screenshot | live | do not keep the full output resident; move it into evidence | terminal, evidence |

## Rules

1. Do not use the prompt itself as a substitute for context.
2. Keep invariant information in docs instead of pasting it into every task.
3. Push issue-specific decisions into the task brief.
4. Promote only cross-session facts into the Progress Note.
5. Treat full logs and exploration history as live context, not as permanent context.
6. Do not copy raw secrets, credentials, or personal data into a context pack or Progress Note.
7. Keep URLs and versions for external data in task context, but treat time-sensitive responses themselves as live context.

## Telling Stale from Live

- `sample-repo/docs/architecture.md` and `sample-repo/docs/coding-standards.md` are stale-safe persistent context. Read them at the start of the work.
- `sample-repo/tasks/FEATURE-001-brief.md` is task context. It fixes the scope for the current issue.
- `sample-repo/tasks/FEATURE-001-progress.md` is session context. Update it as the work moves.
- Output from `python -m unittest discover -s tests -v` is tool context. Preserve only the important points in the Progress Note.

## Resume / Refresh Rule

When resuming work, rebuild context in this order:

1. read persistent context
2. read the task brief and acceptance criteria
3. read the Progress Note
4. rerun verify or status commands to refresh live context

Do not resume from the Progress Note alone. A summary is a restart aid, not a replacement for the source of truth.

## Secret / Persist Boundary

- keep secret names, environment variable names, or vault references, not the values
- do not copy raw tokens, cookies, or personal data into a Progress Note
- redact screenshots and verify logs if they contain secrets
- what must survive a restart is where to look and what to rerun, not the credential itself

## Ticket Search Example

For `FEATURE-001`, the minimum safe context is:

- persistent: `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`
- task: `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/acceptance-criteria/ticket-search.md`
- session: `sample-repo/tasks/FEATURE-001-progress.md`
- tool: the failure details from `sample-repo/tests/test_ticket_search.py` and the latest verify output

Without this split, the search spec, the previous session's guess, and stale test output all compete as if they had the same authority. That is how context poisoning starts. If the agent also trusts an old verify summary without rerunning it, resume drift follows.
