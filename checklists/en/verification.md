# Verification Checklist

## Before Edit

- Have you confirmed which behavior must be preserved in the spec, acceptance criteria, or task brief?
- Have you decided whether a failing test should be added or updated first?
- Have you identified the local verify command and the matching CI job before starting the change?
- If an evidence bundle is required, can you state that requirement before editing?

## During Change

- Have you kept the diff inside the smallest practical work package?
- Have you updated docs, brief, and Progress Note where needed?
- Have you classified verify failures by failure mode?
- Are the command and pass/fail result recorded as current-run evidence rather than remembered from an earlier run?

## Before Review

- Have you run local verify?
- Can the same quality bar be enforced in CI, and can you explain any intentional difference?
- If the change is UI-facing or user-visible, have you preserved an evidence bundle?
- If evidence is not required, can you explain why?
- Are `Changed Files`, `Verification`, and `Remaining Gaps` consistent with the current diff?
- Have you called out the points that still require human approval?
- If any check was skipped, is that decision recorded in `Remaining Gaps`?

## Stop Instead Of Merge

- Does an unrelated verify failure remain unresolved?
- Is required evidence missing for the current run?
- Do local verify and CI disagree without an explanation?
- Are there changes that need approval before merge?
