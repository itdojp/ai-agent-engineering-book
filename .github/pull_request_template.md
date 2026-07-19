## Goal
- What outcome this PR is trying to achieve

## Scope and Non-goals
- Included scope
- Explicit non-goals / deferred work

## Changed Files
- Key files or artifacts changed

## Verification
- [ ] Current-run commands executed for this PR
- [ ] CI-equivalent local checks or documented differences
- [ ] If the model/runtime profile changed: eval or smoke check rerun, with profile and confirmation date recorded

Current-run command list:
- `TODO: ./scripts/verify-book.sh`
- `TODO: ./scripts/verify-pages.sh`
- `TODO: ./scripts/verify-sample.sh`
- `TODO: <additional command or reason omitted>`

## AI / External Service Boundary
- [ ] No secrets, credentials, personal data, unreleased specs, vulnerability details, or sensitive logs are pasted into AI / external services without classification and redaction
- [ ] Provider retention / training-use / logging terms are acceptable, or no external submission occurred
- [ ] Approval owner and decision are recorded when external input or high-risk tool use is involved

## Evidence / Approval
- Evidence bundle, approval boundary touched, or explicit approval still needed

## Review Completion Gate
- [ ] GitHub Copilot review requested when required for the issue
- [ ] Review body, inline comments, and suggestions checked
- [ ] Required fixes applied, or non-action reasons replied in the PR
- [ ] Unresolved review threads: 0
- [ ] CI green before merge
- [ ] Post-merge main checks / public-site reflection confirmed when applicable

## Production Gate (When Applicable)

Before merge / production-ready plan:
- Target environment and public URL: `N/A — reason`
- SHA/version record and semantic marker: `N/A — reason`
- Deploy owner / production-confirmation owner / approver: `N/A — reason`
- Root smoke, representative routes, and expected HTTP/content markers: `N/A — reason`
- Metric baseline / threshold / window / source / owner: `N/A — reason`
- Halt condition / rollback method / restart condition / evidence location: `N/A — reason`

After merge / production evidence (update the merged PR body or linked issue):
- Target SHA and deployment/workflow: `N/A — reason`
- HTTP/semantic-marker observations: `N/A — reason`
- Metric observation and window: `N/A — reason`
- Production confirmation or halt decision / owner / UTC timestamp: `N/A — reason`
- Rollback evidence and post-rollback reconfirmation when used: `N/A — reason`

Deployment approval, deployment success, and production confirmation are separate decisions. Keep the linked source issue open until production confirmation, or record why the production gate does not apply.

## Remaining Gaps
- Known follow-ups, risks, or deferred checks

## Notes for Review
- Reviewer should confirm Goal / Changed Files / Scope and Non-goals / Verification / AI / External Service Boundary / Evidence / Approval / Review Completion Gate / Production Gate
