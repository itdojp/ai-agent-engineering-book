# Bugfix Prompt Contract

Prompt Contract for reproducing, fixing, and verifying a bug without breaking existing behavior.

## Objective

Identify the root cause of the target bug and fix it with the smallest possible diff while preserving existing behavior.

## Inputs

- the target issue or task brief
- reproduction steps
- expected behavior and actual behavior
- related files, related tests, and related docs
- the verify commands that must be run
- known constraints or explicitly out-of-scope areas

## Constraints

- do not change the existing public interface
- add or update the failing test first
- keep the diff limited to the smallest range required to fix the target bug
- update related docs when behavior changes

## Forbidden Actions

- do not extend the spec without evidence
- do not delete a failing test just to get green
- do not mix in unrelated refactors or renames
- do not treat the task as complete without running verify

## Missing Information Policy

- if required inputs are missing, list the missing information and stop
- if you proceed with a low-risk assumption, record that assumption in the final report

## Completion Criteria

- you can explain the reproduction condition and the root cause
- a test fails before the fix and passes after the fix
- the existing tests and the specified verify commands pass
- you can enumerate the changed code, docs, and tests
- if unresolved work remains, record it in `Remaining Gaps`; otherwise write `none`

## Output Format

1. Root Cause
2. Changed Files
3. Verification
4. Remaining Gaps
