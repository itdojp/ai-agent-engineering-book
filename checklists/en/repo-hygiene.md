# Repo Hygiene Checklist

## Before Merge

- Have you updated stale docs?
- Are there any broken reference paths?
- Does manuscript or docs still contain absolute-path references?
- Is the verify script aligned with the actual repo state?
- Is wording normalized against `docs/glossary.md` as the source of truth?
- Are the canonical spellings of `Prompt Contract`, `Progress Note`, and `verification harness` stable?
- If the diff touches an approval boundary, does `Evidence / Approval` name the approver and the decision inputs?
- Is the `needs-human-approval` wording aligned with `sample-repo/docs/harness/done-criteria.md`?
- Are `verify log`, `trace`, and `evidence bundle` used as separate terms rather than mixed together?
- Have you confirmed that the evidence used in review comes from the current run?
- Have you avoided leaving artifacts that still require redaction or privacy handling untouched?
- Does each chapter's `Source Notes / Further Reading` stay aligned with `manuscript-en/backmatter/00-source-notes.md`?
- Does `manuscript-en/backmatter/00-source-notes.md` cover CH01 through CH12 without omissions?
- Are `Output Contract` report fields normalized to `Goal`, `Scope and Non-goals`, `Changed Files`, `Verification`, `Evidence / Approval`, and `Remaining Gaps`?
- Are local verify, CI, and evidence terms consistent across chapters and checklists?

## Weekly Cleanup

- Are there any orphaned task briefs?
- Are stale Progress Notes still lingering?
- Is `AI slop` accumulating as stale docs or unused artifacts?
- Are trace or evidence references left stale or expired?
- Are multiple artifacts now explaining the same thing under different names?
- Are owners and cadence for `repo hygiene` and `entropy cleanup` still explicit?
- Did only one of source notes, reading guide, or index seed change and create backmatter drift?

## Escalate When

- the source of truth conflicts
- stale artifacts are spreading across multiple chapters or tasks
- cleanup is no longer enough and structural rework is required
