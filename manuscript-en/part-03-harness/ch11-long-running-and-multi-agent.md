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
When a task like `FEATURE-002` is forced through one long prompt, verification state, ownership, and decision history collapse quickly. CH09 defined the single-agent harness. CH10 defined the verification harness. Real work still produces tasks that do not fit inside one session. That is where feature lists, restart protocols, and role separation become necessary.

The purpose of this chapter is not to jump to multi-agent execution by default. The first step is to design the minimal structure that keeps a long-running task from breaking. Only after that should the work be split across multiple agents. The running example is `FEATURE-002`, which combines assignee-filter semantics with assignment-change audit logging and must be broken into safe work packages.

## Learning Objectives
- Explain why long-running tasks break
- Design a restart protocol
- Decide when to use single-agent versus multi-agent work

## Outline
### 1. Where long-running tasks break
### 2. Feature lists and progress tracking
### 3. Design a restart protocol
### 4. Separate planner, coder, reviewer, and verifier work
### 5. Decide when multi-agent work is justified

## 1. Where Long-running Tasks Break
Long-running tasks usually break because state management collapses, not because the model suddenly becomes less capable. Four failure modes appear repeatedly:

- scope expands without a deliberate decision
- the latest verify state becomes unclear
- previous decisions drift away from current decisions
- the next step grows too large to fit a safe work package

`FEATURE-002` is a clear example. If the instruction is “handle assignee filters and audit logs end to end,” the coding agent tends to mix unrelated tracks, lose track of what was already verified, update docs and tests in the wrong order, and restart from guesswork after interruption.

This is a combined form of the CH01 failures “forgetting” and “stopping early.” Long-running work requires more than extra context. It requires artifacts that preserve state across sessions.

## 2. Feature Lists and Progress Tracking
The first long-running-task artifact is the feature list. A feature list is not just another backlog. It exists to break a multi-session task into tracks and make progress visible at the workstream level.

`sample-repo/docs/harness/feature-list.md` splits `FEATURE-002` into three tracks:

- `Track A`: assignee-filter semantics
- `Track B`: assignment-change audit log
- `Track C`: verification and docs sync

Each track has a goal, primary files, and a verify signal. That matters because the team needs to know which chunk is being closed right now, not just which tickets exist in theory.

Progress tracking then connects the feature list to the existing CH07 artifacts. The feature list is the map of the task. The Progress Note is the current location. Without both, a resumed session cannot reconnect the previous verify state to the next safe step.

CH11 does not add a new Progress Note template. Instead, it connects the existing session-memory policy to long-running task control through the feature list and restart protocol.

## 3. Design a Restart Protocol
A restart protocol exists so that a resumed session does not begin by guessing what “the previous session was probably doing.” `sample-repo/docs/harness/restart-protocol.md` fixes both the restart packet and the restart steps.

The minimum restart packet is five items:

1. the `FEATURE-002` plan
2. the latest feature list
3. the latest Progress Note
4. the most recent verify result
5. unresolved open questions and approval waits

If the session restarts without that packet, the agent keeps working from stale assumptions. For example, the previous session may have finished only the assignee-filter semantics track, but the next session may jump into audit-log design without a verified handoff point.

The most important part of the restart protocol is not “continue the previous plan exactly.” It is “choose the next smallest safe step again.” Restarting a long-running task means re-reading the latest verify state, re-checking open questions, and choosing one work package that still fits the current track.

## 4. Separate Planner, Coder, Reviewer, and Verifier Work
When a task is split across multiple agents, the first thing to separate is responsibility, not headcount. `sample-repo/docs/harness/multi-agent-playbook.md` and `sample-repo/tasks/FEATURE-002-plan.md` define four roles:

| Role | Primary responsibility | Main artifacts |
|---|---|---|
| planner | freeze scope, define workstreams, set handoffs | `FEATURE-002-plan.md`, feature list |
| coder | implement and update tests | `src/`, `tests/` |
| reviewer | inspect diff, risk, docs drift, and scope drift | docs, task artifacts, diff |
| verifier | run verify, collect evidence, report | verify commands, evidence, final report |

This split works because write scope and decision scope are different. The planner should fix scope and ownership before coder work begins. Otherwise, parallelism only makes conflicts happen faster.

`FEATURE-002-plan.md` shows the intended separation: one coding track for assignee-filter semantics, another for assignment-change audit logging, then reviewer and verifier passes to integrate the result. Multi-agent work is useful only when those streams are truly separable.

## 5. When to Use Multi-agent and When Not To
Multi-agent work is not the default. Without an explicit decision rule, coordination cost can exceed any speed gain.

This chapter needs only a simple rule set:

| Decision | Use single-agent when | Use multi-agent when |
|---|---|---|
| task shape | one track can close safely inside one session | two or more disjoint tracks exist |
| restart cost | one person can recover state from the restart packet | handoff is expected and must be explicit |
| write scope | most edits stay in one bounded area | roles can own separate files or phases |
| integration cost | review and verify are simple enough to stay serial | review and verify can run in parallel without collision |

The important idea is not “complex means multi-agent.” The important idea is “split only when the split reduces integration cost.” If the feature list is weak and the restart packet is incomplete, adding more agents only parallelizes confusion.

That is why the prerequisites for multi-agent work are a feature list, a restart protocol, and explicit ownership. When those exist, multi-agent execution becomes a controlled harness choice instead of a reflex.

## Bad / Good Example
Bad:

```text
Finish FEATURE-002.
Add more agents if necessary.
If the work stops, read the old chat and continue.
```

This method has no track split, no restart packet, and no role ownership. The moment interruption or handoff appears, state starts to drift.

Corrected:

```text
First split the workstreams in `sample-repo/docs/harness/feature-list.md`.
Then use `sample-repo/tasks/FEATURE-002-plan.md` to fix planner,
coder, reviewer, and verifier responsibilities.
At interruption, update the restart packet defined in
`sample-repo/docs/harness/restart-protocol.md`.
Keep single-agent execution for tracks that still close safely,
and use multi-agent only for disjoint tracks.
```

This version stores long-running-task state and the conditions for multi-agent use in artifacts before coordination begins.

Comparison points:
- The bad version depends on chat history as session memory.
- The bad version reaches for multi-agent as a reflex.
- The corrected version fixes feature lists, restart packets, and role ownership first.

## Worked Example
Break `FEATURE-002` into three stages.

1. planner
   - fix scope and non-goals in `FEATURE-002-plan.md`
   - create tracks and verify checkpoints in `sample-repo/docs/harness/feature-list.md`
2. coder
   - implement assignee-filter semantics and audit-log behavior as separate workstreams
   - run local verify inside each track
3. reviewer / verifier
   - check docs drift, scope drift, verify results, and final report together

If a coder stops mid-task, the next operator uses `restart-protocol.md` to inspect the latest Progress Note and verify result, then decides whether work should resume in coder mode or return to planner mode first. In other words, the restart protocol is both a continuation mechanism and a role-reset mechanism.

The key lesson from this example is that multi-agent work is not mainly about simultaneous execution. It is about responsibility separation supported by restartable artifacts.

## Reader-facing Table
### Long-running / Multi-agent Decision Card

| Decision point | Continue as single-agent when | Split into multi-agent when | Main artifact |
|---|---|---|---|
| feature list | one track can close directly | multiple disjoint tracks exist | `sample-repo/docs/harness/feature-list.md` |
| restart packet | one person can restore state safely | handoff is expected across sessions or roles | `sample-repo/docs/harness/restart-protocol.md` |
| role split | planner and coder can stay one role safely | planner / coder / reviewer / verifier reduce collisions | `sample-repo/docs/harness/multi-agent-playbook.md` |
| plan | one work package is enough | checkpoints are needed per workstream | `sample-repo/tasks/FEATURE-002-plan.md` |

This card keeps the decision grounded in integration cost instead of surface complexity. Without a strong feature list and restart packet, multi-agent work is just parallelized state loss.

## Exercises
1. Split case C into planner, coder, and reviewer responsibilities.
2. Restart a failed long-running task through a restart protocol.

## Referenced Artifacts
- `sample-repo/docs/harness/feature-list.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/multi-agent-playbook.md`
- `sample-repo/tasks/FEATURE-002-plan.md`

## Source Notes / Further Reading
- To revisit this chapter, start with `sample-repo/docs/harness/feature-list.md`, `sample-repo/docs/harness/restart-protocol.md`, `sample-repo/docs/harness/multi-agent-playbook.md`, and `sample-repo/tasks/FEATURE-002-plan.md`. Read multi-agent work only after the role split and restart packet are concrete.
- For the backmatter path, see `manuscript/backmatter/00-source-notes.md` under `### CH11 Long-running Task と Multi-agent` and `manuscript/backmatter/01-読書案内.md` under `## 検証・信頼性・運用`.

## Chapter Summary
- Long-running tasks need a feature list, a Progress Note, and a restart packet to keep state stable across sessions.
- Multi-agent work is not the default. It becomes useful only when ownership and write scope can be split cleanly.
- Once long-running task control is in place, the remaining problem is team-wide operation. The next chapter moves into roles, review budget, metrics, and repo hygiene.

## Parity Notes
- Japanese source: `manuscript/part-03-harness/ch11-long-running-and-multi-agent.md`
- This English draft preserves the same long-running task model, restart rules, and role-ownership guidance as the Japanese chapter.
