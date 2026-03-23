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

## Forbidden Actions

- do not add behavior that is not present in the acceptance criteria
- do not settle ambiguous requirements by guesswork
- do not postpone tests or docs that are required for verify
- do not introduce behavior changes without verification

## Missing Information Policy

- if required inputs are missing, list the missing information and stop
- if you proceed on an assumption, preserve that assumption in `Remaining Gaps`

## Completion Criteria

- the acceptance criteria are satisfied
- tests cover the main happy path and the main edge cases
- you can explain the changed artifacts by code, docs, and tests
- the specified verify commands pass
- if unresolved work remains, record it; otherwise write `none`

## Output Format

1. Implemented Scope
2. Changed Files
3. Verification
4. Remaining Gaps
