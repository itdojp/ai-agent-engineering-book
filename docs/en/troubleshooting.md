# Safety-First Troubleshooting Flow

When an AI-agent task does not behave as expected, prioritize containing impact and preserving decision evidence over fixing it quickly. This reader-facing flow isolates Prompt, Context, and Harness failure modes with the smallest safe action.

## 0. Stop Immediately and Protect the Boundary

Do not retry or take additional action when any of the following applies:

- production, customer data, credentials, public exposure, billing, or destructive commands may be affected
- the Permission Policy, Tool Contract, or Approval Gate boundary is unclear
- the failure has produced unexpected file changes, external submission, privilege escalation, or missing data

Stopping is not a failure. It preserves the safety boundary so that the next owner can make an informed decision.

## 1. Record the Symptoms

First, record the expected behavior separately from the actual Symptoms. Preserve the task, run timestamp or run ID, inputs, executed command, error, changed files, and whether an external operation occurred. Do not treat an old log or trace as a substitute for current-run verification.

## 2. Reproduce with the Smallest Input

Reproduce the same Symptoms with a read-only or isolated minimum input. If the failure does not Reproduce, state which input, environment, permission, or timing condition differs from the original run. Do not use production data or an unapproved external operation to reproduce it.

## 3. Perform a Minimum Safe Check

Before making a change, confirm the target repository, branch, working tree, allowed tools and commands, network access, and approval requirement. If a safe check cannot establish the scope, Stop rather than expanding the hypothesis.

## 4. Diagnose the Prompt

Check whether the Objective, Inputs, Constraints, Tool Contract, Completion Criteria, and Refusal / Stop Conditions are present as observable conditions. Ambiguous requests, conflicting constraints, and a missing output contract are Prompt failure modes. When changing a Prompt, define the expected output first with the minimum reproduction input.

## 5. Diagnose the Context

Check whether the required artifacts, target files, terminology, existing decisions, and current state are in Context. Stale information, irrelevant bulk input, swapped JA/EN counterparts, and absolute paths are Context failure modes. Identify one source of truth at a time before adding more Context.

## 6. Diagnose the Harness

Check execution order, tool permissions, timeouts, retries, the verification command, divergence from CI, and evidence preservation. Even with a correct Prompt and Context, do not call work safely complete when the Harness boundary or verification is missing. Isolate a Harness failure through commands and outcomes, not retry count.

## 7. Decide When to Stop and Escalate

Stop and Escalate to the appropriate owner or approver when:

- a decision would cross a safety boundary, Permission Policy, or Approval Gate
- the minimum reproduction still leaves possible data loss, security, privacy, or external impact
- no single Prompt, Context, or Harness failure mode explains the result and sources of truth conflict
- current-run verification cannot run or its failure mode cannot be explained

Include the Symptoms, reproduction conditions, reason for stopping, minimum safe checks attempted, and decision needed in the escalation.

## 8. Preserve Evidence

Under Evidence / Approval, preserve the executed command, run timestamp or run ID, pass or fail result, relevant diff, trace, redaction requirement, approver, and decision inputs. Evidence prevents the next retry, review, or handoff from repeating the same risky operation.
