# Evidence Bundle

The place to preserve verification results for UI changes and other user-visible changes. As part of the verification harness, an evidence bundle keeps review material in a form that lets reviewers see what changed and what was checked.

## Related Artifacts
- verify log
  - the log that shows the current-run command, timestamp, and result
- trace
  - the history that shows handoff, retry, and state transitions
- evidence bundle
  - the review-ready bundle that combines verify-log references, trace references, repro steps, and images

Verify logs and traces may be included in an evidence bundle, but they are not the same thing. The bundle is the artifact formatted for review.

## When To Create
- when a UI appearance or interaction flow changes
- when the reviewer cannot judge the diff without shared repro steps
- when a long-running task needs verify-log and trace references bundled for review

## Recommended Layout
```text
artifacts/evidence/<task-id>/<timestamp>/
  summary.md
  verify.log
  repro.md
  trace.md        # only when needed
  before.png
  after.png
```

> Note: actual evidence bundles still live under `artifacts/evidence/...`. `artifacts/en/evidence/` holds the English guidance only.

## Minimum Trace Reference Contract
When a trace is cited in review or metrics, it must at least be possible to connect the following items.

- task / work-package identifier
- run timestamp or run identifier
- owner / handoff information (when relevant)
- retry / restart reason (when relevant)
- verify reference (which current-run verify this trace belongs to)
- evidence linkage (which bundle or PR summary cites it)
- redaction / privacy note (when relevant)

This contract does not exist to replace current-run verify with trace. It is the minimum reference information that lets a reviewer identify what the trace refers to.

## Minimum Contents
- `summary.md`
  - what changed
  - which verify steps were run
  - what the reviewer should look at
  - the evidence timestamp
- `verify.log`
  - the current-run command and the key log lines
- `repro.md`
  - the before / after confirmation steps
- `trace.md`
  - only when handoff, retry, or failure analysis history is needed
  - if it is cited, it must satisfy the minimum trace reference contract
- `before.png`, `after.png`
  - only when the change is UI-visible

## Freshness Rule
- the evidence bundle must point to current-run verify at review time
- if an older verify log is reused, `summary.md` must explain why rerun was impossible and what the impact is
- do not keep only stale screenshots or stale traces while skipping current-run verify
- do not mistake a trace with no verify reference for current-run evidence

## Redaction / Privacy
- remove secrets, credentials, personal data, or internal identifiers before bundling
- do not share raw logs that the reviewer does not need
- if redaction affects judgment, explain that impact in `summary.md`

## Notes
- backend-only changes may not need screenshots; `summary.md` and `verify.log` can still be required
- when no bundle is needed, state the reason briefly in the PR summary
