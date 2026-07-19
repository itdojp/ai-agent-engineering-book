# Verification Checklist

## Before Edit
- Have you confirmed which behavior must be preserved in the spec, acceptance criteria, or task brief?
- Have you decided whether a failing test should be added or updated first?
- Have you identified the local verify command and the matching CI job before starting the change?
- If an evidence bundle is required, can you explain that requirement before editing?
- If the work mentions a model name, API, SDK, or vendor-specific feature, have you chosen where to record the model/runtime profile and official-doc confirmation date?
- If issues, PRs, logs, eval cases, traces, or evidence may enter an AI or external service, have you checked classification, redaction, provider terms, and approval requirements?
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
- If the model/runtime profile changed, did you rerun the eval or smoke check?
- If AI / external-service submission is involved, did you record the submitted data class, redaction, provider terms, and approval decision under `Evidence / Approval`?
- If evidence is not required, can you explain why?
- Have you called out the points that still require human approval?
- Is there a plan to inspect review bodies, inline comments, suggestions, and confirm zero unresolved review threads?
- If any check was skipped, is that decision recorded in `Remaining Gaps`?

## Production Gate (When Applicable)

### Before Merge / Production-ready Plan
- Is the target environment and public URL recorded?
- Is there a location for the post-merge SHA/version and a semantic marker to compare in production?
- Are the deploy owner, production-confirmation owner, and required approver identified?
- Are the root smoke, representative routes, and expected HTTP status / content markers defined?
- Does the metric have a baseline, threshold, window, source, and owner?
- Are halt conditions, rollback method, restart conditions, and evidence location defined?

### After Merge / Production Evidence
- Do the target SHA/version and deployment/workflow run match?
- If a successor run cancelled the target run, are successor inclusion, both run URLs, and successor-deployment checks recorded as `Superseded` evidence?
- Are deployment approval, deployment success, and production confirmation recorded separately?
- Were the root and representative-route HTTP status and semantic markers checked?
- Was the metric checked for the defined window, or recorded as `N/A` with a reason?
- Are owner, UTC timestamp, observed values, and evidence URLs recorded in the PR or linked issue?
- After rollback, were deployment, HTTP, markers, and metrics rechecked for the new main SHA?

## Stop Instead Of Merge
- Does an unrelated verify failure remain unresolved?
- Is current-run evidence missing even though the change requires it?
- Do local verify and CI disagree without an explanation?
- Are there changes that require approval before merge?
- Do review comments, suggestions, or unresolved threads remain while merge is being attempted?
- Did the model/runtime profile change without rerunning evals or smoke checks?
- Is production-affecting work being merged without a completed production-ready plan?
- Is the work being marked complete while deployment is failed/unknown, SHA or marker mismatches, a representative route fails, or a metric exceeds its threshold?
- Is deployment success or approval being used as a substitute for production confirmation?
- Is a `cancelled` run being treated as `Superseded` or successful without successor-SHA inclusion and production confirmation?
