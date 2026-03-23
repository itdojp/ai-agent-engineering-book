# Part III Harness Engineering

Even when Prompt and Context are stable, an AI agent can still fail. It can stop before verification, cross a permission boundary, repeat the same failed move, or lose state in long-running work. Harness Engineering is the work of designing execution boundaries, verification, restart, and operating rules so the work can be closed safely.

## Role of This Part

This part mainly targets breakage and early stopping. Without a designed execution flow, verification harness, restart protocol, and review budget, the AI agent produces many partial diffs but does not reliably finish the job.

Harness Engineering builds in this order.

1. Fix start conditions, permissions, and done criteria with a single-agent harness
2. Bundle tests, CI, evidence, and approval into a verification harness
3. Split long-running and multi-agent work into restartable units
4. Move the whole system into a team operating model

## Artifacts Added in This Part

By the end of this part, the reader will have at least the following artifacts.

- runbook
- permission policy
- done criteria
- verification checklist
- evidence bundle
- restart protocol
- feature list
- operating model
- metrics

The goal of this part is not raw speed. It is to let the AI agent work without breaking the repo, stopping in the wrong place, or handing off an unreadable partial state.

## Chapter Map

- CH09: define the single-agent harness
- CH10: build the verification harness
- CH11: handle long-running tasks and multi-agent work
- CH12: define the operating model and organizational adoption path

The first two chapters focus on execution and verification. The last two chapters focus on restart and operation. Only at this point do Prompt and Context turn into work that can close safely in practice.

## What You Should Be Able to Do by the End of This Part

By the end of this part, the reader should be able not only to start AI-agent work, but also to verify it, stop it at the correct boundary, and finish it in a handoff-ready form. The appendices and backmatter then collect the templates, glossary, and re-reference artifacts needed to reuse that system.
