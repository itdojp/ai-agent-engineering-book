---
id: ch11
title: Long-running Tasks and Multi-agent Work
status: drafted
source_ja: manuscript/part-03-harness/ch11-long-running-and-multi-agent.md
artifacts:
  - sample-repo/docs/harness/feature-list.md
  - sample-repo/docs/harness/restart-protocol.md
  - sample-repo/docs/harness/multi-agent-playbook.md
  - sample-repo/tasks/FEATURE-002-plan.md
dependencies:
  - ch09
  - ch10
---

# Long-running Tasks and Multi-agent Work

## Role in This Book
If a long task such as `FEATURE-002` is pushed through one long prompt, verify state and decision history collapse quickly. CH09 defined the single-agent harness. CH10 defined the verification harness. Real work still produces tasks that do not fit inside one session. That is where a feature list, a restart protocol, and explicit role separation become necessary.

The purpose of this chapter is not to jump to multi-agent execution by default. The first step is to design the minimum structure that keeps a long-running task from breaking. Only after that should the work be split across multiple agents. The running example is `FEATURE-002`, where assignee-filter semantics and assignment-change audit logging must be broken into safe work packages.

## Learning Objectives
- Explain why long-running tasks break
- Design a restart protocol
- Decide when to use single-agent versus multi-agent work

## Outline
### 1. Where long-running tasks break
### 2. Feature lists and progress tracking
### 3. Restart protocol
### 4. Separating planner / coder / reviewer / verifier work
### 5. When to use multi-agent and when not to

## 1. Where Long-running Tasks Break
Long-running tasks usually break because state management collapses, not because the model suddenly becomes less capable. In practice, four failure modes appear repeatedly: scope expands, the latest verify state becomes unclear, earlier decisions drift away from current ones, and the next move grows too large for one safe work package.

`FEATURE-002` shows the problem clearly. If the instruction is “handle assignee filters and audit logs end to end,” the agent tends to mix the assignee-filter track and the audit-log track, lose track of what was already verified, update docs, tests, and task artifacts in the wrong order, and restart from guesswork after interruption.

This is a combined form of the CH01 failures of forgetting and stopping early. Long-running work requires more than extra context. It requires artifacts that preserve state across sessions.

## 2. Feature Lists and Progress Tracking
The first long-running-task artifact is the feature list. A feature list is not just another backlog. It exists to split a multi-session task into tracks and make progress visible at the workstream level.

`sample-repo/docs/harness/feature-list.md` splits `FEATURE-002` into three tracks: `Track A: Assignee Filter Semantics`, `Track B: Assignment Change Audit Log`, and `Track C: Verification And Docs Sync`.

The important point is that the feature list is not merely a list of things to do. It is the artifact that keeps a long-running task stable across sessions. Because each track has a goal, major files, a verify signal, and dependencies, the team can decide which chunk is being closed right now.

Progress tracking then connects the feature list to the CH07 artifacts. The feature list is the map of the task. The `Progress Note` is the current location. Without both, a resumed session cannot reconnect the previous verify state to the next safe step. If only a summary survives and the primary artifacts are missing, summary drift follows quickly.

## 3. Restart Protocol
A restart protocol exists so that a resumed session does not begin by guessing what “the previous session was probably doing.” `sample-repo/docs/harness/restart-protocol.md` makes both the restart packet and the restart steps explicit.

The minimum restart packet for this long-running task has six items:

1. the `FEATURE-002` plan
2. the latest `sample-repo/docs/harness/feature-list.md`
3. the current owned files and merge order
4. the latest `Progress Note`
5. the most recent verify result
6. unresolved open questions and pending approvals

If work restarts without that packet, the agent keeps working from stale assumptions. A summary is still necessary as a session summary, but it is not the source of truth on its own. On restart, the operator should reread the plan, feature list, `Progress Note`, verify state, and owned files, then reacquire live verify if needed.

## 4. Separating Planner / Coder / Reviewer / Verifier Work
When a task is split across multiple agents, the first thing to separate is responsibility, not headcount. `sample-repo/docs/harness/multi-agent-playbook.md` and `sample-repo/tasks/FEATURE-002-plan.md` define four roles: `planner`, `coder`, `reviewer`, and `verifier`.

This four-role split works because write scope and decision scope are different.

| Role | Primary responsibility | Main artifacts |
|---|---|---|
| planner | freeze scope, split workstreams, define handoffs | `FEATURE-002-plan.md`, feature list |
| coder | implement and update tests | `src/`, `tests/` |
| reviewer | inspect diff, docs drift, and scope drift | docs, task artifacts, diff |
| verifier | run verify, collect evidence, and prepare the report | verify commands, evidence bundle |

The important point here is that local multi-agent orchestration is a same-repo / same-runtime role split. It becomes safe only after owned files, merge order, and exit states are fixed in advance. If agents are added before the plan is stable, write scopes collide. The planner should fix scope, shared-file rules, and ownership first. Only disjoint workstreams should be parallelized.

## 5. When to Use Multi-agent and When Not To
Multi-agent work is not the default. If the decision rule is unclear, coordination cost can exceed any speed gain.

For this chapter, the following table is enough.

| Decision | Use it when | Do not use it when |
|---|---|---|
| single-agent | scope is narrow, the work can close in one session, write scope stays in one area, and one verify path is enough | artifact synchronization is already heavy or long-running work is visible from the start |
| multi-agent | disjoint workstreams exist, review or verify can run in parallel, and the restart packet is explicit | the plan is unclear, write scopes overlap, or explanation cost is too high |

Local orchestration and remote interoperability also need to be separated. MCP covers context and tool connectivity: it connects tools, resources, and prompts to a runtime. A2A covers remote interoperability such as agent discovery and task handoff. When designing same-repo / same-runtime sub-agent work, MCP and A2A do not need to be treated as the same thing. The subject of this chapter is local multi-agent orchestration, not cross-service or cross-organization interoperability itself.

In practice, the decision should not be “complex means multi-agent.” It should be “split only when the split reduces integration cost.” In `FEATURE-002`, assignee-filter semantics and audit logging are related, but their owners and verify checkpoints can still be separated. Only tasks that can be separated that way should be moved into multi-agent work.

## Bad / Good Example
Bad:

```text
Finish FEATURE-002 end to end.
Add more agents if necessary.
Keep only a summary and resume from that.
Because MCP is available, treat it as if A2A-style role splitting is already covered.
```

This method has no track split, no restart packet, no owned files, and no role ownership. The moment interruption or handoff appears, state starts to drift.

good:

```text
First split the workstreams in `sample-repo/docs/harness/feature-list.md`.
Then use `sample-repo/tasks/FEATURE-002-plan.md` to fix planner / coder / reviewer / verifier responsibilities.
Follow `sample-repo/docs/harness/restart-protocol.md` and restart only after checking the plan, feature list, verify state, and owned files, not a summary alone.
Use multi-agent only for tracks that stay local, and keep MCP as tool connectivity and A2A as remote handoff as separate concepts.
```

This corrected version stores long-running-task state, ownership, and the conditions for multi-agent use in artifacts before coordination begins.

Comparison points:
- the bad version depends on summary alone as session memory
- the bad version treats MCP and A2A as the same kind of mechanism
- the good version fixes the feature list, restart packet, owned files, and merge order first

## Worked Example
Break `FEATURE-002` into four stages.

1. planner
   - fix scope, non-goals, and shared-file rules in `FEATURE-002-plan.md`
   - create tracks, owners, and verify checkpoints in `feature-list.md`
   - define owned files and merge order for each role
2. coder
   - implement assignee-filter semantics and audit logging as separate workstreams
   - run local verify in each workstream and update the `Progress Note`
3. reviewer
   - inspect docs drift, scope drift, and shared-file collisions
4. verifier
   - confirm current-run verify, evidence, and the final `Remaining Gaps`

If a coder stops mid-task, the next operator follows `restart-protocol.md`, checks the feature list, `Progress Note`, and verify state, and decides whether the work can continue in coder mode or must return to planner mode first. The restart protocol is therefore both a continuation procedure and a role-reset procedure.

The key lesson from this worked example is that the essence of multi-agent work is not simultaneity. It is responsibility separation supported by restartable artifacts.

## Reader-facing Table
### Local Multi-agent / Remote Interoperability Decision Card

| Decision point | local multi-agent orchestration | remote interoperability | Main artifact |
|---|---|---|---|
| boundary | same-repo / same-runtime role split | cross-service / cross-organization handoff | playbook, restart protocol |
| main concern | owned files, merge order, exit state | discovery, task transfer, trust boundary | plan, protocol docs |
| relationship to MCP | a supporting layer for tools and resources | not a substitute | runtime docs |
| relationship to A2A | not required | one possible handoff layer | protocol docs |

This card keeps the decision grounded in integration cost instead of surface complexity. Without a strong feature list and restart packet, multi-agent work only parallelizes state loss. If the plan and role split are clear, local multi-agent orchestration can reduce the coordination cost of long-running work.

## Exercises
1. Split case C into planner / coder / reviewer / verifier responsibilities.
2. Restart a failed long-running task through a restart protocol.

## Referenced Artifacts
- `sample-repo/docs/harness/feature-list.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/multi-agent-playbook.md`
- `sample-repo/tasks/FEATURE-002-plan.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `sample-repo/docs/harness/feature-list.md`, `sample-repo/docs/harness/restart-protocol.md`, `sample-repo/docs/harness/multi-agent-playbook.md`, and `sample-repo/tasks/FEATURE-002-plan.md`. Read multi-agent work only after owned files and the restart packet are concrete.
- For the backmatter path, see `manuscript-en/backmatter/00-source-notes.md` under `### CH11 Long-running Tasks and Multi-agent Work` and `manuscript-en/backmatter/01-reading-guide.md` under `## Verification, Reliability, and Operations`.

## Chapter Summary
- Long-running tasks need a feature list, a `Progress Note`, and a restart packet to keep state stable across sessions.
- Multi-agent work is not the default. It becomes useful only when role ownership, owned files, and merge order can be split cleanly.
- MCP is about context and tool connectivity, while A2A is about remote interoperability. Same-repo local orchestration is a different design problem. The next chapter moves from that boundary into the team-wide operating model.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch11-long-running-and-multi-agent.md`
- This English chapter preserves the same long-running-task model, restart rules, local-orchestration framing, and MCP / A2A distinction as the Japanese chapter.
