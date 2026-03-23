# English Glossary

This file is the English counterpart of the repo-wide glossary and is used by the English manuscript. It must stay in sync with, and be derived from, [`docs/glossary.md`](../glossary.md), which remains the single source of truth for terminology.

| Term | Definition |
|---|---|
| Prompt Engineering | The stage that designs prompt artifacts and fixes objective, constraints, completion criteria, and output format for a single task. |
| Context Engineering | The stage that selects and maintains the repo, task, session, and tool context shown to an AI agent or coding agent. |
| Harness Engineering | The stage that designs execution boundaries, permission rules, verification harnesses, retries, and recovery paths for coding-agent work. |
| AI agent | An actor that advances work through multi-step decisions and tool use. In the Japanese manuscript this may also appear as `AIエージェント`. |
| coding agent | An AI agent that reads a repo, changes code, docs, tests, and artifacts, and runs verify steps. |
| ChatGPT | A conversational interface used for requirements shaping, design exploration, comparison, and review-angle discovery. |
| Codex CLI | A coding-agent execution environment that reads the repo, applies changes, runs commands, and gathers verification evidence. |
| sample-repo | The `support-hub` sample implementation used as the running case study throughout the book. |
| artifact | A concrete repo asset such as a prompt, doc, script, test, task brief, or context pack. |
| acceptance criteria | The conditions a feature or change must satisfy from the specification side. |
| task brief | A task specification that restructures an issue for coding-agent execution. |
| context pack | The bundle of reference material collected for one specific task. |
| session memory | The combination of task brief, `Progress Note`, and verification evidence used to resume work across sessions. Chapter or document titles may use `Session Memory`. |
| source of truth | The highest-priority artifact used to resolve contradictions. |
| source notes | Short chapter-end or backmatter notes that identify trusted sources and the next step for deeper reading. |
| further reading | The reading path that points the reader to official docs, books, or handbooks after a chapter. |
| backmatter | The re-reference apparatus after the main text, including source notes, reading guide, index seed, and figure/list policies. |
| verification harness | The verification system that bundles tests, lint, typecheck, evidence capture, and CI. |
| done criteria | The operational conditions required to treat work as complete, including verify state, artifact updates, and approval requirements. |
| evidence bundle | The set of verify logs, repro steps, screenshots, and summaries that lets a reviewer confirm the result. |
| Remaining Gaps | The canonical final-report label for unresolved issues, human follow-up, or gaps that remain after verify. |
| Prompt Contract | A prompt artifact that defines objective, constraints, completion criteria, and output format. |
| Progress Note | A short progress record used for interruption, restart, and handoff. |
| repo context | The relatively stable repo-wide information about structure, conventions, entry points, and ownership. |
| operating model | The operating design that defines role boundaries, review budget, cadence, and rollout stages for AI-agent use. |
| throughput | The amount of issue, PR, or work-package volume a team can process within a period. |
| repo hygiene | The practice of preserving repo consistency and readability so the next task is not made harder. |
| entropy cleanup | The recurring cleanup work that removes stale docs, orphaned artifacts, naming drift, and unnecessary diffs. |
| restart packet | The minimum input required to resume work after interruption, typically a plan, the latest `Progress Note`, verify evidence, and open questions. |
| permission policy | The rule set that separates work a coding agent may perform autonomously from work that requires human approval. |
| skill | A reusable unit of instructions, resources, and scripts. Chapter titles and file names may also use `Skills` or `SKILL.md`. |
| work package | The smallest unit of work that can be completed safely in one session or by one owner. |
| review budget | The upper bound on how much change a reviewer can inspect deeply within a period. |
| AI slop | Low-quality diffs or docs that accumulate in a repo when high-throughput generation is left unchecked. |
