# Context Budget

A context budget is not only a limit on how much text an AI agent reads. It is a design policy for what should stay verbatim, what should be summarized, and what should be dropped.

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

## FEATURE-001 Example

For `FEATURE-001` in `sample-repo`, cut the budget like this:

- keep verbatim: `sample-repo/docs/acceptance-criteria/ticket-search.md`, the decision in `sample-repo/docs/design-docs/ticket-search-adr.md`, and the verify command
- keep summarized: the reason ranking became a non-goal, and why the search abstraction option was rejected
- drop: long lists of trial query strings and full stale failure logs

If the budget is not controlled, old logs become louder than the real constraints and the AI agent starts working from stale context.
