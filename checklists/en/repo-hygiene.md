# Repo Hygiene Checklist

## Before Merge

- Have you updated stale docs?
- Are there any broken reference paths?
- Does manuscript or docs still contain absolute-path references?
- Is the verify script aligned with the actual repo state?
- Is wording normalized against `docs/glossary.md` as the source of truth?
- Are the canonical spellings of `Prompt Contract`, `Progress Note`, and `verification harness` stable?
- Does each chapter's `Source Notes / Further Reading` stay aligned with `manuscript/backmatter/00-source-notes.md`?
- Does `manuscript/backmatter/00-source-notes.md` cover CH01 through CH12 without omissions?
- Are output-contract report fields normalized to `Changed Files`, `Verification`, and `Remaining Gaps`?

## Weekly Cleanup

- Are there any orphaned task briefs?
- Are stale Progress Notes still lingering?
- Is `AI slop` accumulating as stale docs or unused artifacts?
- Are multiple artifacts now explaining the same thing under different names?
- Are owners and cadence for `repo hygiene` and `entropy cleanup` still explicit?
- Did only one of source notes, reading guide, or index seed change and create backmatter drift?

## Escalate When

- the source of truth conflicts
- stale artifacts are spreading across multiple chapters or tasks
- cleanup is no longer enough and structural rework is required
