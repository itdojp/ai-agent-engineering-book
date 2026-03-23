# Harness Templates

## Purpose

Harness Engineering is the move from “let the agent do the work” to “let the agent complete, stop, and restart work safely.” Tests alone are not enough. The verify order, permission boundary, and restart conditions also need to be fixed as artifacts.

This appendix reorganizes the harness artifacts reused across CH09 through CH12 into a form that can be applied again. The same foundations support both single-agent work and long-running tasks: define how far autonomy goes, where the worker must stop, and what must be read before work resumes.

## Included Artifacts

- `templates/verify-checklist.md`
- `templates/restart-protocol.md`
- `templates/permission-policy.md`
- `templates/en/verify-checklist.md`
- `templates/en/restart-protocol.md`
- `templates/en/permission-policy.md`

## 1. Verify Checklist Template

`templates/verify-checklist.md` defines the canonical structure, and `templates/en/verify-checklist.md` provides the English counterpart. The goal is to make the verification harness review-ready by keeping the pre-edit, in-change, and pre-review checks in one place.

The recommended flow has three stages.

- `Before Edit`: confirm the behavior that must be preserved, the source of truth, whether a failing test must come first, and which local verify command is required
- `During Change`: keep the diff to one work package, check for missing doc or task-artifact updates, and classify verify failures correctly
- `Before Review`: confirm local verify, CI alignment, evidence-bundle needs, and whether human approval is required

`checklists/verification.md` is the concrete example inside this repo. The checklist becomes more useful when it stays short enough that reviewers actually reread it before merge.

## 2. Restart Protocol Template

`templates/restart-protocol.md` defines the canonical structure, and `templates/en/restart-protocol.md` provides the English counterpart. As CH11 explains, restart is not the act of vaguely continuing from where the last session seemed to stop. It is the act of choosing the next move again from the latest verification state and open questions.

The template has three core parts.

- `Restart Packet`: the minimum input that must exist before restart
- `Restart Steps`: the read order and how to choose the next single work package
- `Stop Conditions`: when missing information or ownership conflict should block restart

`sample-repo/docs/harness/restart-protocol.md` is the concrete example. Without a restart protocol, long-running or multi-agent work loses state before it gains speed.

## 3. Permission Policy Template

`templates/permission-policy.md` defines the canonical structure, and `templates/en/permission-policy.md` provides the English counterpart. In Harness Engineering, permission boundaries are easier to maintain when they live in an explicit artifact instead of being buried inside a long prompt.

The minimum useful sections are these.

- `Purpose`: state which harness uses the policy
- `Agent May Proceed`: list the changes the coding agent may perform autonomously
- `Require Human Approval`: block interface changes, external dependencies, or harness changes that need human signoff
- `Stop And Report`: define the conditions where reporting is safer than continuing
- `Escalation Format`: fix what the agent must report to a human

`sample-repo/docs/harness/permission-policy.md` is the single-agent example in the repo. A vague policy invites accidental interface or CI changes. A clear policy lets the agent stop correctly.

## 4. Operational Caution

Do not collapse these three states into one:

- verify passed
- done criteria met
- human approval not required

A passing test suite is necessary, but it is not sufficient. Evidence may still be missing. Approval may still be required. Task artifacts may still be stale. Harness Engineering exists to name those differences and keep them visible.

## Parity Notes

- Japanese source: `manuscript/appendices/app-c-Harness-テンプレート集.md`
- Publication target: preserve the Japanese appendix's verify / restart / permission structure, along with its operational warning about verify, done, and approval not meaning the same thing.

## Referenced Artifacts

- `templates/verify-checklist.md`
- `templates/restart-protocol.md`
- `templates/permission-policy.md`
- `templates/en/verify-checklist.md`
- `templates/en/restart-protocol.md`
- `templates/en/permission-policy.md`
- `checklists/verification.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/permission-policy.md`
