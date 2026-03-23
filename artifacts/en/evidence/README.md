# Evidence Bundle

This directory defines the English counterpart for the evidence-bundle guidance used by the harness chapters. As part of a verification harness, an evidence bundle preserves what changed, what was checked, and what the reviewer should inspect.

## When To Create

- when a UI layout, interaction flow, or visible behavior changes
- when the reviewer cannot judge the change from logs alone
- when a long-running task needs one bundle for verify logs and review notes

## Recommended Layout

```text
artifacts/evidence/<task-id>/<timestamp>/
  summary.md
  verify.log
  repro.md
  before.png
  after.png
```

> Note: Evidence bundles themselves must be created under `artifacts/evidence/...`. The `artifacts/en/evidence/` directory only contains the English guidance for those bundles.

## Minimum Contents

- `summary.md`
  - what changed
  - which verify commands were run
  - what the reviewer should inspect
- `verify.log`
  - the commands that ran and the key output
- `repro.md`
  - the before / after confirmation steps
- `before.png`, `after.png`
  - only when the change is UI-visible

## Notes

- backend-only changes may not need screenshots; `summary.md` and `verify.log` can still be required
- if no bundle is needed, the PR summary should state why
