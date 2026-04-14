# Context Budget

A context budget is not just a limit on how much text an AI agent reads. It is the design policy that decides what should stay verbatim, what should be summarized, what should be compacted, what should be reacquired, and what should be promoted into a persistent artifact. A long context window does not remove the need for a budget.

## Budgeting Policy

- root instructions should contain only repo-wide invariants
- local instructions should contain only details closed over the target directory
- the repo map should stay limited to entry points and hot paths
- the task brief should prioritize Goal, Constraints, Acceptance Criteria, and Verification
- the `Progress Note` should keep only the last decisions, open questions, and resume steps
- when live tool output can be reacquired safely, prefer re-fetch over retention

## Decision Matrix

| Operation | Purpose | Typical Example | Storage Guidance |
|---|---|---|---|
| keep verbatim | Preserve contracts whose meaning must not drift | acceptance criteria, API or interface contracts, verify commands, destructive-change constraints | Refer to the source-of-truth artifact as-is |
| summarize | Leave a short record of long history | comparison history, closed open questions, conclusions from exploration | Keep a short note in the `Progress Note` or another summary artifact |
| compact | Compress while preserving structure | read-order guides, file lists, checkpoint lists, risk tables | Convert to tables or bullets that are easy to search again |
| re-fetch | Refresh information that goes stale quickly | test output, grep results, external search results, terminal logs | Prefer rerunning over keeping it resident in chat |
| persist | Carry conclusions into the next session | task-brief decisions, `Next Step`, ADR conclusions | Promote to a repo artifact and avoid dependence on chat history |

## Keep Verbatim

- acceptance criteria
- API or interface contracts
- verify commands
- destructive-change constraints
- decision-record conclusions

## Summarize or Compact

- long exploration logs
- trial-and-error history
- comparison process
- open questions that are already closed
- read order for referenced files
- checkpoint and ownership lists

## Re-fetch

- full stale test output
- transient grep or search results
- full stdout or stderr from tool runs
- live status that goes stale quickly

## Persist

- the Goal, Constraints, Acceptance Criteria, and Verification from the task brief
- the `Decided`, `Open Questions`, and `Next Step` sections in the `Progress Note`
- conclusions fixed by review or verify
- where evidence is stored
- the command names, target files, and unfinished tasks needed to resume

## Never Persist As Plain Text

- secret values, tokens, cookies, or personal data
- raw logs from temporary production inspection
- full terminal output that can be regenerated
- unverified guesses written as if they were facts

## Refresh Triggers

Refresh live context before trusting a summary when:

- substantial time has passed since the last run
- dependencies or the branch head moved
- verify results came from an earlier session
- the task stopped at an approval boundary
- the prior reasoning depended on external data

## Drop

- duplicate notes with the same meaning
- expired hypotheses
- details from rejected options
- full logs that were already split into evidence

## FEATURE-001 Example

For `FEATURE-001` in `sample-repo`, cut the budget like this:

- keep verbatim: `sample-repo/docs/acceptance-criteria/ticket-search.md`, the Decision section in `sample-repo/docs/design-docs/ticket-search-adr.md`, and the verify command
- summarize: why ranking became a non-goal, and why the search-abstraction option was rejected
- compact: the read order for the relevant artifacts and the checkpoints that must be checked
- re-fetch: the latest result from `python -m unittest discover -s tests -v` and the latest grep output
- promote to a persistent artifact: the verified decisions, `Next Step`, and the evidence references needed by a reviewer
- persist: the `Decided`, `Open Questions`, and `Next Step` sections in `sample-repo/tasks/FEATURE-001-progress.md`
- do not persist: full shell history, environment dumps containing secrets, or stale verify-log bodies
- drop: long lists of trial query strings and full stale failure logs

If the budget is not controlled, old logs become louder than the real constraints and the AI agent starts working from stale context. If persistence boundaries are also loose, resume drift and secret leakage become much more likely.
