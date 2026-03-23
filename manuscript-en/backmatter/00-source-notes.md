# Source Notes

This backmatter gathers the chapter-end `Source Notes / Further Reading` sections so readers can quickly re-find what counts as the source of truth and where to read next. It is not a replacement for exhaustive footnotes or a full bibliography.

## What This Backmatter Does

- Shows which source types should anchor the book's claims: repo artifacts, official docs, and durable engineering references
- Collects next-step reading paths that do not fit cleanly inside each chapter
- Keeps a clear division of labor with the glossary: the glossary defines terms, while source notes define trust and navigation

## Source Policy

Keep the trust order fixed.

1. Canonical artifacts inside this repo
2. Official docs for the tool, platform, or library in use
3. Durable books, handbooks, and public design notes
4. Blog posts, conference talks, and social media

If that order drifts, the manuscript becomes too dependent on fashion, screenshots, or one-off success stories. This is especially important around AI agents, where behavior and product surfaces change quickly. Prefer the official behavior of the tool you are actually using over generalized commentary.

## Chapter-by-Chapter Source Notes

### CH01 Where AI Agents Fail

- Start with `sample-repo/README.md`, `sample-repo/docs/domain-overview.md`, and `sample-repo/docs/seed-issues.md`. The failure model matters only when it stays connected to the recurring cases.
- If you add external sources, prefer official docs for the coding agent, CI, and issue tracker you actually use, plus local postmortems. Do not build the failure model from demos alone.

### CH02 Design Prompts as Contracts

- Start with `prompts/en/bugfix-contract.md`, `prompts/en/feature-contract.md`, and `checklists/en/prompt-contract-review.md`. In this book, a Prompt Contract is a repo artifact rather than a conversational trick.
- If you add external sources, prefer official prompting, structured-output, and tool-use docs for the model you are using. Do not treat generic prompt collections as the source of truth.

### CH03 Use ChatGPT to Shape Requirements and Design

- Start with `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/design-docs/ticket-search-adr.md`, and `sample-repo/docs/acceptance-criteria/ticket-search.md`. Exploratory dialogue does not become the implementation contract by itself.
- If you add external sources, prefer the product-spec, acceptance-criteria, and ADR templates your organization actually uses. For requirement shaping, decision trace matters more than fluent wording.

### CH04 Evaluate Prompts

- Start with `evals/prompt-contract-cases.json`, `evals/rubrics/feature-spec.json`, and `scripts/run-prompt-evals.py`. Prompt quality should be read through reusable cases and rubrics, not through vibes.
- If you add external sources, prefer official docs for the model or eval framework you are using. Screenshots of one-off prompt comparisons are not stable regression evidence.

### CH05 Foundations of Context Engineering

- Start with `docs/en/context-model.md`, `docs/en/context-budget.md`, and `docs/en/context-risk-register.md`. Context Engineering is not about adding more text. It is about managing lifespan, authority, and contamination risk.
- If you add external sources, prefer official docs for context windows, instruction layering, and workspace access in the tools you use. A pile of long prompts is not a context design method.

### CH06 Design Repo Context

- Start with `AGENTS.md`, `manuscript-en/AGENTS.md`, `sample-repo/AGENTS.md`, `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`, and `sample-repo/docs/coding-standards.md`. Read the repo map as the index and the architecture doc as the design rationale.
- If you add external sources, prefer official docs for the VCS, CI, and package manager you use. Repo responsibility boundaries are easier to judge from the concrete repo than from abstractions.

### CH07 Task Context and Session Memory

- Start with `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/tasks/FEATURE-001-progress.md`, `docs/en/session-memory-policy.md`, and `.github/ISSUE_TEMPLATE/task.yml`. Read the restart packet together with the latest verification result.
- If you add external sources, prefer your issue-tracker, handoff, and change-log policies. Do not treat stale chat transcripts as the source of truth for session memory.

### CH08 Reuse Skills and Context Packs

- Start with `.agents/skills/draft-chapter/SKILL.md`, `.agents/skills/review-chapter/SKILL.md`, `sample-repo/.agents/skills/issue-to-plan/SKILL.md`, `sample-repo/.agents/skills/verification/SKILL.md`, and `sample-repo/context-packs/ticket-search.md`. Read a skill as a reusable workflow contract and a context pack as a task-specific minimum input.
- If you add external sources, prefer official skill or instruction docs for the runtime you are using. Do not explain reuse only by naming a framework.

### CH09 Foundations of Harness Engineering

- Start with `scripts/init.sh`, `scripts/verify-sample.sh`, `sample-repo/docs/harness/single-agent-runbook.md`, `sample-repo/docs/harness/permission-policy.md`, and `sample-repo/docs/harness/done-criteria.md`. A single-agent harness is a bundle of start conditions and exit conditions, not a prompt variant.
- If you add external sources, prefer official docs for the shell, CI runner, and permission model you use. Authority boundaries should come from the execution environment, not from intuition.

### CH10 Build a Verification Harness

- Start with `.github/workflows/verify.yml`, `checklists/en/verification.md`, `sample-repo/tests/test_ticket_search.py`, and `artifacts/evidence/README.md`. Read the verification harness as one flow across tests, CI, evidence, and approval.
- If you add external sources, prefer official docs for the test framework, CI system, and coverage tooling you use. A green screenshot alone is not reproducible evidence.

### CH11 Long-running Tasks and Multi-agent Work

- Start with `sample-repo/docs/harness/feature-list.md`, `sample-repo/docs/harness/restart-protocol.md`, `sample-repo/docs/harness/multi-agent-playbook.md`, and `sample-repo/tasks/FEATURE-002-plan.md`. Multi-agent work becomes safe only after the role split and restart packet are concrete.
- If you add external sources, prefer official docs for the orchestration tool or task queue you use. Do not separate the parallelization discussion from write scope and handoff artifacts.

### CH12 Operating Model and Organizational Adoption

- Start with `docs/en/operating-model.md`, `docs/en/metrics.md`, `checklists/en/repo-hygiene.md`, and `.github/pull_request_template.md`. Read the operating model through roles, review budget, cadence, and cleanup rather than through model comparisons alone.
- If you add external sources, prefer official documents for your organization's review policy, release policy, and metric definitions. Do not reduce adoption decisions to model benchmarks.
