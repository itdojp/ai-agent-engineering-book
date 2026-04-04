# Context Budget

A context budget is not only a limit on how much text an AI agent reads. It is a design policy for what should stay verbatim, what should be summarized, and what should be dropped.
In practice, that policy also has to decide what should persist across sessions and what must be reacquired.

## Budgeting Policy

- root instructions should contain only repo-wide invariants
- local instructions should contain only details closed over the target directory
- the repo map should stay limited to entry points and hot paths
- the task brief should prioritize Goal, Constraints, Acceptance Criteria, and Verification
- the Progress Note should keep only the last decisions, open questions, and resume steps

## Keep Verbatim

- acceptance criteria
- API or interface contracts
- verify commands
- constraints on destructive changes
- the conclusion of a decision record

## Summarize

- long exploration logs
- trial-and-error history
- comparison process
- open questions that are already closed

## Drop

- duplicate notes with the same meaning
- expired hypotheses
- full old test output
- details from rejected options

## Persist

- the Goal, Constraints, Acceptance Criteria, and Verification from the task brief
- the `Decided`, `Open Questions`, and `Next Step` sections in the Progress Note
- the storage location of evidence
- the command names, target files, and unfinished tasks needed to resume

## Never Persist As Plain Text

- secret values, tokens, cookies, or personal data
- raw production logs captured for one-off inspection
- full terminal output that can be regenerated
- unverified guesses written as if they were facts

## Refresh Triggers

Refresh live context before trusting a summary when:

- substantial time has passed since the last run
- dependencies or the branch head moved
- verify results came from an earlier session
- the task stopped at an approval boundary
- the prior reasoning depended on external data

## FEATURE-001 Example

For `FEATURE-001` in `sample-repo`, cut the budget like this:

- keep verbatim: `sample-repo/docs/acceptance-criteria/ticket-search.md`, the decision in `sample-repo/docs/design-docs/ticket-search-adr.md`, and the verify command
- keep summarized: the reason ranking became a non-goal, and why the search abstraction option was rejected
- drop: long lists of trial query strings and full stale failure logs
- persist: the `Decided`, `Open Questions`, and `Next Step` sections in `sample-repo/tasks/FEATURE-001-progress.md`
- do not persist: full shell history, environment dumps containing secrets, or stale verify logs

If the budget is not controlled, old logs become louder than the real constraints and the AI agent starts working from stale context. If persistence boundaries are also loose, resume drift and secret leakage become much more likely.
