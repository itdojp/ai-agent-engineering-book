# English Glossary

This file is the English counterpart of the repo-wide glossary and is used by the English manuscript. It must stay in sync with, and be derived from, [`docs/glossary.md`](../glossary.md), which remains the single source of truth for terminology.

| Term | Definition |
|---|---|
| Prompt Engineering | The stage that designs prompt artifacts and fixes objective, constraints, completion criteria, and output format for one task. |
| Context Engineering | The stage that designs and maintains the repo, task, session, and tool context shown to an AI agent or coding agent. |
| Harness Engineering | The stage that designs execution boundaries, permission rules, verification harnesses, retries, and recovery paths for coding-agent work. |
| AI agent | An actor that advances work through multi-step decisions and tool use. In the Japanese manuscript this may also appear as `AIエージェント`. |
| coding agent | An AI agent that reads a repo, changes code, docs, tests, and artifacts, and runs verify steps. |
| ChatGPT | A conversational interface used for requirements shaping, design exploration, comparison, and review-angle discovery. |
| Codex CLI | A coding-agent execution environment that reads the repo, applies changes, runs commands, and gathers verification evidence. |
| `AGENTS.md` | The repo entrypoint that defines local invariants and points to the next artifacts that must be read. |
| sample-repo | The `support-hub` sample implementation used as the recurring case throughout the book. |
| recurring case | A continuing case tracked across chapters through the same repo, issue shape, or failure mode. In this book it refers to `BUG-001`, `FEATURE-001`, `FEATURE-002`, and `HARNESS-001`. |
| artifact | A concrete repo asset such as a prompt, doc, script, test, task brief, or context pack. |
| acceptance criteria | The conditions a feature or change must satisfy. They bridge the specification and the tests. |
| task brief | A task specification that restructures an issue for coding-agent execution. |
| context pack | The task-specific bundle of reference material that fixes read order and canonical facts for one task. |
| persistent artifact | A source-of-truth artifact that stays in the repo across sessions, such as a spec, glossary, or architecture doc. |
| session memory | The combination of task brief, `Progress Note`, and verification evidence used to resume work across sessions. Chapter or document titles may also use `Session Memory`. |
| session summary | The minimum restart summary that preserves the last decisions and next move, such as `Decided`, `Open Questions`, and `Next Step`. |
| source of truth | The highest-priority artifact used to resolve contradictions. |
| source hierarchy | The priority order that decides whether the manuscript, repo artifact, official docs, or organization policy wins when they conflict. |
| source notes | Short chapter-end or backmatter notes that identify trusted sources and the next step for deeper reading. |
| further reading | The reading path that points the reader to official docs, books, or handbooks after a chapter. |
| backmatter | The re-reference apparatus after the main text, including source notes, reading guide, index seed, and figure/list policies. |
| verification harness | The verification system that bundles tests, lint, typecheck, evidence capture, and CI. |
| done criteria | The operational conditions required to treat work as complete, including verify state, artifact updates, and approval requirements. |
| verify log | The current-run log that records commands, timestamps, and pass/fail state. It is distinct from a historical trace. |
| trace | The history of runs, retries, handoffs, and state transitions. It supports failure analysis and does not replace current-run verify. |
| evidence bundle | The set of verify logs, repro steps, screenshots, and summaries that lets a reviewer confirm the result. |
| provenance | The lineage information that tracks which source produced or updated a prompt, context, artifact, or evidence item. |
| observability | The practice of making verify logs, traces, and metrics visible for queue diagnosis, failure analysis, and review-quality improvement. |
| Changed Files | The canonical final-report label that lists the code, docs, tests, and artifacts changed in a reviewable unit. |
| Remaining Gaps | The canonical final-report label for unresolved issues, human follow-up, or gaps that remain after verify. |
| Prompt Contract | A prompt artifact that defines objective, constraints, completion criteria, and output format. |
| Progress Note | A short progress record used for interruption, restart, and handoff. |
| live tool output | Evidence that is valid only at the moment it was collected, such as grep results, test output, or a verify log. |
| repo context | The relatively stable repo-wide information about structure, conventions, entry points, and ownership. |
| MCP (Model Context Protocol) | The protocol for connecting context sources such as tools, resources, and prompts in a uniform way. Because runtime implementations differ, read the spec and official docs together in practice. |
| MCP-connected capability | The runtime layer that attaches extra tools, resources, or prompts. It is not a substitute for repo skills or context packs. |
| A2A (Agent2Agent) | A family of protocols for remote interoperability such as agent discovery and task handoff. In this book it is treated separately from same-repo local orchestration. |
| tool drift | The drift that appears when a UI, CLI, API, or tool capability changes over time and the manuscript or procedure no longer matches it. |
| human approval gate | The approval boundary that requires human review before a high-risk operation. |
| approval boundary | The boundary beyond which destructive changes, public contract changes, or policy changes require human approval. |
| operating model | The operating design that defines role boundaries, review budget, cadence, and rollout stages for AI-agent use. |
| Lead | The human role that sets issue priority, work-package size, and approves destructive or public-contract changes. |
| Operator | The human role that prepares briefs, artifacts, verify evidence, and explicit `Remaining Gaps` before or during agent execution. |
| Reviewer | The human role that inspects `Goal`, `Changed Files`, `Scope and Non-goals`, `Verification`, `Evidence / Approval`, and `Remaining Gaps` before deciding mergeability. |
| throughput | The amount of issue, PR, or work-package volume a team can process within a period. |
| stale draft count | The number of draft PRs that have stalled within the review-budget window. It signals when queue reduction should be prioritized. |
| approval-stop rate | The rate at which runs or PRs are intentionally stopped by approval boundaries or permission policy. |
| repo hygiene | The practice of preserving repo consistency and readability so the next task is not made harder. |
| hygiene backlog age | The age of the oldest unresolved item in the cleanup backlog. |
| entropy cleanup | The recurring cleanup work that removes stale docs, orphaned artifacts, naming drift, and unnecessary diffs. |
| restart packet | The canonical input needed to resume work after interruption: the plan, feature list, owned files, merge order, latest `Progress Note`, verify evidence, and open questions. |
| permission policy | The rule set that separates work a coding agent may perform autonomously from work that requires human approval. |
| skill | A reusable unit of instructions, resources, and scripts with a repeatable workflow and output contract. Chapter titles and file names may also use `Skills` or `SKILL.md`. |
| runtime-managed capability | A mechanism the runtime can provide directly, such as background execution, hosted tools, or managed context. |
| harness-owned duty | A duty the repo or team must still define and operate, such as approval boundaries, artifact sync, verify rules, or review. |
| work package | The smallest unit of work that can be completed safely in one session or by one owner. |
| review budget | The upper bound on how much change a reviewer can inspect deeply within a period. |
| owned files | The file set a role or workstream may edit without conflict. It is used to prevent collisions in multi-agent work. |
| AI slop | Low-quality diffs or docs that accumulate in a repo when high-throughput generation is left unchecked. |
