---
id: ch03
title: Use ChatGPT to Shape Requirements and Design
status: drafted
source_ja: manuscript/part-01-prompt/ch03-requirements-and-design.md
artifacts:
  - sample-repo/docs/product-specs/ticket-search.md
  - sample-repo/docs/design-docs/ticket-search-adr.md
  - sample-repo/docs/acceptance-criteria/ticket-search.md
dependencies:
  - ch01
  - ch02
---

# Use ChatGPT to Shape Requirements and Design

## Role in This Book
“Make search easier to use” is a valid starting point for a conversation, but it is not a valid starting point for implementation. CH02 fixed the task contract. That still leaves another problem: the request itself may be underspecified. If the requirement is vague, even a well-structured Prompt Contract will carry ambiguity into implementation.

This is where ChatGPT is useful. The goal is not to treat the conversation as the deliverable. The goal is to use exploratory dialogue to surface missing decisions and then converge on artifacts that are ready for implementation. In this chapter, those artifacts are a product spec, acceptance criteria, and an ADR. The running example remains `FEATURE-001` in `sample-repo`.

## Learning Objectives
- Turn ambiguous requests into specs with acceptance criteria
- Write an ADR from alternative comparisons
- Separate decisions humans must own from decisions AI can assist

## Outline
### 1. Turn ambiguous requests into specs
### 2. Break work into acceptance criteria
### 3. Compare alternatives and make design decisions
### 4. Explain why ADRs matter
### 5. Mark the decisions humans must stop and own

## 1. Turn Ambiguous Requests into Specs
Ambiguous requests should not be handed directly to a coding agent. For `FEATURE-001`, the starting request is “make search easier to use.” That sentence does not say who is struggling, which fields should be searchable, or what is out of scope. ChatGPT is useful here because it can surface the missing questions quickly and help shape a first pass of the spec.

Exploratory dialogue and a product spec are not the same artifact.

| Type | Purpose | What it can contain | Can it go straight to implementation? |
|---|---|---|---|
| Exploratory dialogue | Expand the problem space | possibilities, hypotheses, unresolved questions | No |
| Product spec | Fix the problem and the scope | Problem, Objective, In Scope, Non-goals, Users, Requirements | Yes |

In `sample-repo/docs/product-specs/ticket-search.md`, the vague request is fixed into a concrete spec:

- Problem: support staff have to guess whether the relevant text lives in `title`, `description`, or `tags`
- Objective: let a support staff member narrow candidate tickets with one query
- In Scope: partial-match search over `title`, `description`, and `tags`
- Non-goals: ranking, typo correction, external search infrastructure

The practical point is not only to define what will be built. It is also to define what will not be built in this issue. ChatGPT can generate many plausible extensions, including ranking, typo tolerance, saved searches, and UI changes. A good product spec cuts those branches off and keeps the issue inside a controlled boundary.

## 2. Break the Spec into Acceptance Criteria
A product spec still does not make the task implementation-ready. Objective and scope statements can be interpreted differently by different readers. Acceptance criteria close that gap by rewriting the spec as observable behavior.

`sample-repo/docs/acceptance-criteria/ticket-search.md` breaks the search requirement into concrete checks:

- return matching tickets when the query is a partial match in `title`
- return matching tickets when the query is a partial match in `description`
- return matching tickets when the query is a partial match in `tags`
- treat upper and lower case as equivalent
- return all tickets when the query is blank or only whitespace

At that point, “make search easier to use” has been reduced to statements that can be tested. The acceptance criteria also add artifact criteria so the repo can enforce synchronization between behavior, docs, and tests. In engineering work, the quality bar is not only runtime behavior. It also includes whether the implementation, the written spec, and the verification artifacts still agree.

ChatGPT can propose many candidate acceptance criteria, but a human still has to decide what belongs in the issue. Too many criteria expand the implementation needlessly. Too few criteria leave completion subjective. The right filter in CH03 is simple: each criterion should be easy to map to a test or a review check later.

## 3. Compare Alternatives and Make Design Decisions
Once the requirement is stable, the next question is design. ChatGPT is useful here too, but again its role is not to choose for you. Its role is to help enumerate options and surface trade-offs.

For `FEATURE-001`, there are at least two reasonable options:

1. implement an in-memory partial-match search in `service.py`
2. add a dedicated search abstraction that leaves room for an external search engine later

ChatGPT can summarize the strengths and weaknesses of both options quickly. The final choice still depends on the current shape of the repo. `sample-repo` is intentionally small, minimizes external dependencies, and uses the service layer as the main entry point. Under those conditions, the first option is the better fit for this chapter. The second option increases future flexibility, but it also increases design cost before the repo has earned that complexity.

The key is to preserve the decision logic, not just the chosen answer. If the repo only records “we picked option A,” later contributors will rediscover the same design question and may reopen it without context. The artifact should show what was compared and why the chosen option was appropriate for the repo at that point.

## 4. Why the ADR Matters
Design decisions should not remain buried in a chat transcript. They need an artifact such as `sample-repo/docs/design-docs/ticket-search-adr.md`.

In this ADR, the repo records Context, Options Considered, Decision, Decision Drivers, Consequences, and Review Trigger. That gives future readers a short route back to the original reasoning:

- what problem the repo was solving
- which options were considered
- why one option was selected
- which conditions would justify revisiting the decision

The `Review Trigger` section is especially important. In-memory search is enough for the current scope, but that should change if more searchable fields are added, if ranking becomes required, or if an external search engine enters scope. An ADR does not exist to freeze the design forever. It exists to make later re-evaluation explicit and cheap.

If the design choice lives only in a conversation log, the repo accumulates undocumented intent. If it lives in an ADR, the repo accumulates traceable engineering decisions.

## 5. Decisions Humans Must Still Own
ChatGPT is useful for decomposing vague requests, proposing candidate specs, and organizing trade-offs. It should not silently own the decisions that carry scope, complexity, or accountability.

At least four decisions must stay with humans:

1. which requirements belong inside the current issue
2. which non-goals are acceptable for now
3. which trade-offs are worth paying for this repo at this stage
4. who owns the failure if the decision turns out to be wrong

For example, ChatGPT can easily suggest ranking and typo correction when it sees “make search easier to use.” A human still has to decide whether those belong in `FEATURE-001`, given the issue scope, the teaching goal of the repo, and the acceptable implementation cost. AI can accelerate option generation. It should not silently absorb responsibility for the final call.

That boundary makes exploratory work faster. Humans use ChatGPT to find the questions and compare options, then convert only the approved decisions into repo artifacts. The next coding agent should receive the product spec, acceptance criteria, and ADR, not the full exploratory transcript.

## Bad / Good Example
Bad:

```text
We want search to be easier to use. Ask ChatGPT to define the spec, then move straight to implementation.
```

This mixes exploration and commitment. ChatGPT can generate ranking, typo correction, UI changes, and several other possibilities, but the repo still does not know which of those belong in the current issue.

Corrected:

```text
Scope this work to `FEATURE-001` in `sample-repo/docs/seed-issues.md`.
Use ChatGPT first to surface the user, the problem, the in-scope behavior, the non-goals, and the unresolved questions.
Then copy only the approved decisions into `sample-repo/docs/product-specs/ticket-search.md`.
Break that spec into verifiable statements in `sample-repo/docs/acceptance-criteria/ticket-search.md`.
Compare two design options and preserve the selected option with rationale in `sample-repo/docs/design-docs/ticket-search-adr.md`.
```

The corrected version separates exploration from convergence. ChatGPT is used to accelerate thinking, but the implementation-ready artifacts are the repo files, not the conversation itself.

Comparison points:
- The bad version treats the chat log as if it were the spec.
- The corrected version gives the product spec, acceptance criteria, and ADR separate roles.
- The corrected version also shows where human approval enters the flow.

## Worked Example
Take the original request for `FEATURE-001`: “make search easier to use.” Use ChatGPT to converge in the following order.

1. Explore the problem
   - Who is doing the search?
   - Which fields should count as searchable?
   - What is explicitly out of scope for this issue?
   - What is the minimum condition for saying the feature is done?
2. Fix the product spec
   - make `title`, `description`, and `tags` searchable
   - treat ranking, typo correction, and external search infrastructure as non-goals
3. Rewrite the spec as acceptance criteria
   - partial matches should work
   - matching should be case-insensitive
   - a blank query should return all tickets
4. Record the design decision in the ADR
   - use in-memory search in `service.py`
   - keep future search infrastructure as a review trigger rather than part of the initial implementation

The important point in this worked example is that ChatGPT does not directly decide the implementation. It accelerates question discovery and alternative comparison. Humans still approve the artifacts that define the work.

## Exercises
1. Use “make search easier to use” as the starting request and write a product spec for `sample-repo`. Include Problem, Objective, In Scope, Non-goals, and User Scenarios.
2. Compare two implementation options for `ticket-search` and write one ADR. Include Decision Drivers and Review Trigger.

## Referenced Artifacts
- `sample-repo/docs/product-specs/ticket-search.md`
- `sample-repo/docs/design-docs/ticket-search-adr.md`
- `sample-repo/docs/acceptance-criteria/ticket-search.md`

## Source Notes / Further Reading
- When you need to revisit this chapter, treat `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/design-docs/ticket-search-adr.md`, and `sample-repo/docs/acceptance-criteria/ticket-search.md` as the source of truth. Do not treat exploratory dialogue as the implementation contract.
- For the next navigation step, see `manuscript-en/backmatter/00-source-notes.md` under `### CH03 Use ChatGPT to Shape Requirements and Design` and `manuscript-en/backmatter/01-reading-guide.md` under `## Prompts and Requirements Shaping`.

## Chapter Summary
- ChatGPT is most useful when it turns ambiguous requests into product specs, acceptance criteria, and ADRs rather than trying to implement directly from a vague request.
- Exploratory dialogue and implementation-ready artifacts are different things. The coding agent should receive the final artifacts, not the full conversation.
- Once the spec artifacts are stable, the next question is whether the same prompt produces stable quality repeatedly. CH04 addresses that with prompt evaluation, cases, and rubrics.

## Parity Notes
- Japanese source: `manuscript/part-01-prompt/ch03-requirements-and-design.md`
- This English draft preserves the same `FEATURE-001` worked example, the same artifact set, and the same human-judgment boundary as the Japanese chapter.
