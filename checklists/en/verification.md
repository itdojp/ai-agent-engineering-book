# Verification Checklist

## Before Edit
- Have you confirmed which behavior must be preserved in the spec, acceptance criteria, or task brief?
- Have you decided whether a failing test should be added or updated first?
- Have you identified the local verify command and the matching CI job before starting the change?
- If an evidence bundle is required, can you explain that requirement before editing?
- Are you sure that a referenced trace or old log is not being treated as a substitute for current-run verify?

## During Change
- Have you kept the diff inside the smallest practical work package?
- Have you updated docs, the brief, and the `Progress Note` where needed?
- Have you classified verify failures by failure mode?
- Have you recorded the verify command and pass / fail result as current-run information?
- For a long-running task, have you organized the handoff or retry events that should be kept in a trace?
- If you keep a trace, have you recorded the task / work-package id, run timestamp or run id, owner / handoff, and retry / restart reason?

## Before Review
- Have you run local verify?
- Does the verify log preserve the command, timestamp, and pass / fail result?
- Can the same quality bar be enforced in CI, and can you explain any intentional difference?
- If the change is UI-facing or otherwise user-visible, have you preserved an evidence bundle?
- Does the evidence point to the current run?
- Are `Changed Files`, `Verification`, and `Remaining Gaps` consistent with the current diff?
- If a trace is cited in review, are the verify reference and evidence linkage explicit?
- Have you checked whether traces or screenshots need redaction / privacy treatment?
- If evidence is not required, can you explain why?
- Have you called out the points that still require human approval?
- If any check was skipped, is that decision recorded in `Remaining Gaps`?

## Stop Instead Of Merge
- Does an unrelated verify failure remain unresolved?
- Is current-run evidence missing even though the change requires it?
- Do local verify and CI disagree without an explanation?
- Are there changes that require approval before merge?
