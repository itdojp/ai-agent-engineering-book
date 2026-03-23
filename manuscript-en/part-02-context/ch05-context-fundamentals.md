---
id: ch05
title: Foundations of Context Engineering
status: drafted
source_ja: manuscript/part-02-context/ch05-context-fundamentals.md
artifacts:
  - docs/context-model.md
  - docs/context-budget.md
  - docs/context-risk-register.md
dependencies:
  - ch01
  - ch02
  - ch03
  - ch04
---

# Foundations of Context Engineering

## Role in This Book
Good Prompt Contracts and prompt evals are not enough on their own. An AI agent can still miss the target if it reads the wrong spec, follows stale notes, or gives too much weight to irrelevant logs. CH01 through CH04 established Prompt Engineering as the way to improve single-task reliability. This chapter starts the next layer: Context Engineering.

Context Engineering is not about writing a better prompt. It is about deciding what the agent should see, what should be preserved, and what should be discarded. This chapter draws the boundary between Prompt Engineering and Context Engineering, then introduces four context types: persistent, task, session, and tool context. Later chapters build repo context, task context, session memory, skills, and context packs on top of that model.

## Learning Objectives
- Explain the difference between Prompt Engineering and Context Engineering
- Design a context budget
- Separate stale context from live context

## Outline
### 1. Prompt Engineering versus Context Engineering
### 2. Persistent, task, session, and tool context
### 3. Think in context budgets
### 4. Separate stale context from live context
### 5. Prevent context poisoning and drift

## 1. Prompt Engineering Versus Context Engineering
Prompt Contracts tell the AI agent what to do, what not to do, and what counts as done. CH02 examined `prompts/feature-contract.md`, and CH04 showed how to evaluate whether that contract behaves consistently. A strong contract still does not tell the agent where the current truth lives in the repo. It does not answer which spec is canonical, which test is the regression guard, or which previous decision is already fixed.

That is the job of Context Engineering. Context is the decision material an AI agent needs in order to execute the contract. It is not a decorative appendix to the prompt. For `FEATURE-001`, even if the objective says “improve ticket search according to the spec,” the agent still needs `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/acceptance-criteria/ticket-search.md`, and `sample-repo/tests/test_ticket_search.py` in view. Without those artifacts, the word “spec” remains too vague to execute.

The opposite mistake also fails. A large pile of docs and tests cannot compensate for a weak prompt. If the objective and completion criteria are missing, the agent has no clear stopping condition. Prompt Engineering and Context Engineering are not competing techniques. Prompt Engineering defines the work boundary. Context Engineering defines the decision material inside that boundary.

## 2. Persistent, Task, Session, and Tool Context
`docs/context-model.md` divides context into four types. The value of this model is not taxonomy for its own sake. The real value is that each type has a different update rate, owner, and freshness requirement.

- Persistent context: relatively stable repo rules such as `AGENTS.md`, architecture docs, glossary entries, and coding standards
- Task context: issue-specific scope and done conditions such as the issue, task brief, product spec, ADR, and acceptance criteria
- Session context: restart-oriented records such as progress notes, open questions, the latest decision summary, and the next step
- Tool context: live evidence such as grep output, test results, verify logs, and screenshots

For `FEATURE-001`, `sample-repo/docs/architecture.md` is persistent context. `sample-repo/tasks/FEATURE-001-brief.md` is task context. `sample-repo/tasks/FEATURE-001-progress.md` is session context. The latest `python -m unittest discover -s tests -v` output is tool context. If these all get dumped into one memo, old decisions and live failures start to look equally authoritative.

The separation matters because the update speed is different. Architecture docs do not change every session. Progress notes do. Verify output can become obsolete within minutes. Context Engineering treats those differences as design constraints rather than accidents.

## 3. Think in Context Budgets
A context budget is not only about token limits. It is a design policy for what should stay verbatim, what should be summarized, and what should be dropped. `docs/context-budget.md` gives that policy explicitly: keep acceptance criteria, interface contracts, verify commands, and destructive-change constraints verbatim; summarize exploratory logs and comparison history; drop stale test output and expired hypotheses.

The reason for that split is practical. Anything that becomes dangerous when paraphrased should stay in its original wording. In `sample-repo/docs/acceptance-criteria/ticket-search.md`, the rule “return all tickets when the query is blank or only whitespace” should remain verbatim. By contrast, the historical reason why ranking became a non-goal can usually be summarized as long as the decision itself remains intact.

Without a context budget, noisy artifacts pull attention away from the real contract. Long terminal logs and exploratory notes can overshadow current acceptance criteria simply because they are larger or more vivid. In practice, Context Engineering is less about accumulating information and more about declaring information priority.

## 4. Separate Stale Context from Live Context
If stale context and live context are mixed together, the agent will use “correct yesterday, wrong today” information as if it were current evidence. `docs/context-model.md` treats architecture guidance as stale-safe and verify output as live for exactly this reason.

The operational rule is straightforward:

- repo principles such as `sample-repo/docs/architecture.md` and `sample-repo/docs/coding-standards.md` are stale-safe starting points
- task artifacts such as a task brief or acceptance criteria must be reread for the current issue
- progress notes are useful session memory, but they become stale as soon as verify results change
- terminal output and failing test logs are live context and should be refreshed rather than trusted from memory

In `FEATURE-001`, `sample-repo/docs/repo-map.md` and `sample-repo/docs/architecture.md` are safe entry points. `sample-repo/tasks/FEATURE-001-progress.md` is less stable. If the progress note says the last verify passed, that statement may already be obsolete by the next session. Restarting from the note alone is not enough. The safe action is to reread the note, then rerun verify if the current task depends on it.

## 5. Prevent Context Poisoning and Drift
Context Engineering fails not only when information is missing, but also when the wrong information keeps circulating. `docs/context-risk-register.md` lists the main risks: stale docs, summary drift, instruction bloat, context poisoning, hidden done criteria, and tool spam.

Three failure patterns appear often:

1. docs and tests drift apart, so implementation follows an obsolete spec
2. a progress note writes an unverified guess under `Decided`, and the next session treats it as fact
3. `AGENTS.md` or handoff notes grow until the important constraints are buried

The countermeasures are structural. Keep canonical artifacts in the task brief and acceptance criteria. Separate `Decided` from `Open Questions` in the progress note. Move long logs out of the standing context and keep them as evidence instead. When live evidence can be rerun, rerun it before trusting an old summary.

Context Engineering is not only a technique for adding information. It is also a technique for preventing broken information from surviving too long.

## Bad / Good Example
Bad:

```text
This is `FEATURE-001`, so give the agent the previous chat summary, the full old test log, the whole repo tree, and a stack of old notes.
The prompt only says: “Fix search and continue from last time.”
```

This fails twice. The Prompt Contract is weak, and the context has no freshness or priority model. Old logs and unverified guesses are treated as if they were equal to acceptance criteria.

Corrected:

```text
Keep the Prompt Contract focused on Objective, Constraints, and Completion Criteria.
Then provide context in this order:
1. `sample-repo/docs/repo-map.md`
2. `sample-repo/tasks/FEATURE-001-brief.md`
3. `sample-repo/docs/acceptance-criteria/ticket-search.md`
4. `sample-repo/tasks/FEATURE-001-progress.md`
5. the latest verify result
Do not keep full historical logs in the standing context. Promote only the conclusions that must survive into the progress note.
```

This version separates the contract from the decision material and also separates stale-safe docs from live verify evidence.

Comparison points:
- The bad version mixes prompt and context responsibilities.
- The bad version gives stale context and live context the same weight.
- The corrected version fixes canonical artifacts first and treats logs as live evidence instead of standing truth.

## Exercises
1. Sort 15 information fragments into the four context types: persistent, task, session, and tool context.
2. Write a policy that decides what to summarize and what to keep verbatim for a task like `FEATURE-001`.

## Referenced Artifacts
- `docs/context-model.md`
- `docs/context-budget.md`
- `docs/context-risk-register.md`

## Source Notes / Further Reading
- When you need to revisit this chapter, treat `docs/context-model.md`, `docs/context-budget.md`, and `docs/context-risk-register.md` as the source of truth. Context Engineering is not a method for adding more text. It is a method for separating lifespan, authority, and refresh policy.
- For the next navigation step, see `manuscript-en/backmatter/00-source-notes.md` under `### CH05 Foundations of Context Engineering` and `manuscript-en/backmatter/01-reading-guide.md` under `## Context and Repo Design`.

## Chapter Summary
- Prompt Engineering defines the work boundary. Context Engineering defines the type, freshness, and priority of the decision material inside that boundary.
- Context becomes easier to design when it is separated into persistent, task, session, and tool context.
- Once those types are visible, the next requirement is a stable repo entry point. The next chapter covers the role split among `AGENTS.md`, `sample-repo/docs/repo-map.md`, and `sample-repo/docs/architecture.md`.

## Parity Notes
- Japanese source: `manuscript/part-02-context/ch05-context-fundamentals.md`
- This English draft preserves the same Prompt-versus-Context boundary, the same four-context model, and the same failure-mode framing as the Japanese chapter.
