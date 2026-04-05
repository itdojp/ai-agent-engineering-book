# 索引 seed

このファイルは、組版時に索引へ展開するための seed である。現段階ではページ番号の代わりに、主に戻る章と primary artifact を固定する。

## 使い方

- glossary は語義を引くために使う
- この索引 seed は「どの章と artifact に戻るか」を引くために使う
- 組版時には、ここを起点に page 参照と see / see also を付ける

## 索引 seed

| 見出し語 | 主に戻る章 | primary artifact / 補助参照 |
|---|---|---|
| acceptance criteria | CH03, CH10 | `sample-repo/docs/acceptance-criteria/ticket-search.md`, `sample-repo/tests/test_ticket_search.py` |
| A2A | Appendix D | `docs/glossary.md` |
| approval boundary | CH09, CH12 | `sample-repo/docs/harness/permission-policy.md`, `docs/operating-model.md` |
| ADR | CH03 | `sample-repo/docs/design-docs/ticket-search-adr.md` |
| AGENTS.md | CH06 | `AGENTS.md`, `manuscript/AGENTS.md`, `sample-repo/AGENTS.md` |
| AI agent | CH01, CH12 | `docs/glossary.md`, `docs/operating-model.md` |
| artifact | CH01, Appendix D | `docs/glossary.md` |
| bad / good example | CH01-CH12 | 各章の `## 章で使う bad / good example` |
| ChatGPT | CH03 | `docs/glossary.md` |
| coding agent | CH01, CH12 | `docs/glossary.md`, `docs/operating-model.md` |
| Codex CLI | CH06, CH12 | `docs/glossary.md`, `.github/pull_request_template.md` |
| context pack | CH08 | `sample-repo/context-packs/ticket-search.md` |
| Context Engineering | CH01, CH05 | `docs/context-model.md` |
| done criteria | CH09 | `sample-repo/docs/harness/done-criteria.md` |
| evidence bundle | CH10 | `artifacts/evidence/README.md` |
| hygiene backlog age | CH12 | `docs/metrics.md` |
| Lead / Operator / Reviewer | CH12 | `docs/operating-model.md`, `.github/pull_request_template.md` |
| MCP | Appendix D | `docs/glossary.md` |
| feature list | CH11 | `sample-repo/docs/harness/feature-list.md` |
| Harness Engineering | CH01, CH09 | `sample-repo/docs/harness/single-agent-runbook.md` |
| operating model | CH12 | `docs/operating-model.md` |
| approval-stop rate | CH12 | `docs/metrics.md` |
| permission policy | CH09 | `sample-repo/docs/harness/permission-policy.md` |
| Progress Note | CH07 | `sample-repo/tasks/FEATURE-001-progress.md` |
| Prompt Contract | CH02 | `prompts/bugfix-contract.md`, `prompts/feature-contract.md` |
| Prompt Engineering | CH01, CH02 | `checklists/prompt-contract-review.md` |
| repo context | CH06 | `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md` |
| repo hygiene | CH12 | `checklists/repo-hygiene.md` |
| restart packet | CH11 | `sample-repo/docs/harness/restart-protocol.md` |
| review budget | CH12 | `docs/operating-model.md`, `docs/metrics.md` |
| rubrics | CH04 | `evals/rubrics/feature-spec.json` |
| provenance | Appendix D | `docs/glossary.md`, `artifacts/evidence/README.md` |
| sample-repo | CH01 | `sample-repo/README.md`, `sample-repo/docs/domain-overview.md` |
| session memory | CH07 | `docs/session-memory-policy.md` |
| skill | CH08 | `.agents/skills/draft-chapter/SKILL.md`, `sample-repo/.agents/skills/verification/SKILL.md` |
| source notes | この後付け | `manuscript/backmatter/00-source-notes.md` |
| source hierarchy | Appendix D | `docs/glossary.md`, `manuscript/backmatter/00-source-notes.md` |
| stale draft count | CH12 | `docs/metrics.md` |
| task brief | CH07 | `sample-repo/tasks/FEATURE-001-brief.md` |
| verification harness | CH10 | `.github/workflows/verify.yml`, `checklists/verification.md` |
| work package | CH11, CH12 | `sample-repo/tasks/FEATURE-002-plan.md`, `docs/operating-model.md` |
