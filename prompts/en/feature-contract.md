# Feature Prompt Contract

Prompt Contract for implementing a feature according to the written spec and preserving the reason for the change and the verification trail.

## Objective

Implement the target feature according to the defined spec and acceptance criteria, and update the required artifacts.

## Inputs

- the product spec
- acceptance criteria
- relevant architecture docs
- the target issue or task brief
- related code and existing tests
- the verify commands that must be run

## Constraints

- do not change UI or API behavior outside the written spec
- follow the existing naming, style, and public contract
- update docs and tests together
- do not mix in changes outside the scope of the target issue

## Tool Contract

- run only the verify, build, and test commands that are explicitly allowed
- do not use external connections, new dependencies, or secrets unless they are explicitly approved
- limit write targets to the code, docs, tests, and artifacts that are inside the task scope

## Approval Gate

- wait for human approval before adding dependencies, making breaking changes, using secrets, calling paid external APIs, or expanding permissions
- if the run enters an approval wait, stop and return the decision inputs without performing the blocked action

## Forbidden Actions

- do not add behavior that is not present in the acceptance criteria
- do not settle ambiguous requirements by guesswork
- do not postpone tests or docs that are required for verify
- do not introduce behavior changes without verification

## Missing Information Policy

- if required inputs are missing, list the missing information
- if you proceed on a low-risk assumption, preserve that assumption in `Remaining Gaps`

## Refusal / Stop Conditions

- stop if required inputs are missing and no low-risk assumption is acceptable
- stop if an approval-required action is in scope and approval has not been granted
- stop if the sources of truth conflict and the conflict cannot be resolved safely

## Completion Criteria

- the acceptance criteria are satisfied
- tests cover the main happy path and the main edge cases
- you can explain the changed artifacts by code, docs, and tests
- the specified verify commands pass
- if unresolved work remains, record it; otherwise write `none`

## Output Schema

- output_version: `2026-04-01`
- required_sections:
  - Implemented Scope
  - Changed Files
  - Verification
  - Remaining Gaps

## Output Format

1. output_version
2. Implemented Scope
3. Changed Files
4. Verification
5. Remaining Gaps
