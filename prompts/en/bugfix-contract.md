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

## Tool Contract

- run only the verify, build, and test commands that are explicitly allowed
- do not use external connections, new dependencies, or secrets unless they are explicitly approved
- limit write targets to the code, docs, tests, and artifacts that are inside the task scope

## Approval Gate

- wait for human approval before adding dependencies, making breaking changes, using secrets, calling paid external APIs, or expanding permissions
- if the run enters an approval wait, stop and return the decision inputs without performing the blocked action

## Forbidden Actions

- do not extend the spec without evidence
- do not delete a failing test just to get green
- do not mix in unrelated refactors or renames
- do not treat the task as complete without running verify

## Missing Information Policy

- if required inputs are missing, list the missing information
- if you proceed with a low-risk assumption, record that assumption in `Remaining Gaps`

## Refusal / Stop Conditions

- stop if required inputs are missing and no low-risk assumption is acceptable
- stop if an approval-required action is in scope and approval has not been granted
- stop if the sources of truth conflict and the conflict cannot be resolved safely

## Completion Criteria

- you can explain the reproduction condition and the root cause
- a test fails before the fix and passes after the fix
- the existing tests and the specified verify commands pass
- you can enumerate the changed code, docs, and tests
- if unresolved work remains, record it in `Remaining Gaps`; otherwise write `none`

## Output Schema

- output_version: `2026-04-01`
- required_sections:
  - Root Cause
  - Changed Files
  - Verification
  - Remaining Gaps

## Output Format

1. output_version
2. Root Cause
3. Changed Files
4. Verification
5. Remaining Gaps
