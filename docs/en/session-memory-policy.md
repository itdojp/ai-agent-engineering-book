# Session Memory Policy

## Purpose

Make it possible to return to the same task brief and the same verification evidence even after the session changes.

## Required Fields for a Progress Note

- `Current Goal`: the current one-task target
- `Completed`: finished changes
- `Decided`: decisions confirmed by verify or artifacts
- `Open Questions`: unresolved points
- `Changed Files`: the main files touched recently
- `Last Verify`: the last verify command and result
- `Resume Steps`: the files to reopen and the reading order
- `Next Step`: the single next action

## Optional Field

- `Status`: a short state label for quick scanning; do not treat it as the source of truth

## What Not to Store

- full redundant exploration logs
- lists of temporary hypotheses
- unverified assertions
- duplicated information that already exists in the task brief

## Minimum Input for a Resume Packet

1. the task brief
2. the latest Progress Note
3. the latest verify result
4. the list of files that should be read first when resuming

## Drift Guard

- quote Acceptance Criteria verbatim from the task brief
- do not put unresolved items into `Decided`
- do not split the summary into separate before-verify and after-verify narratives
- when an open question is resolved, promote it to `Decided` instead of silently deleting it

## Update Timing

- when pausing work
- right after verify finishes
- before handoff
- when an important design decision becomes fixed
