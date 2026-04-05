# Source Notes

この後付けは、各章末の `Source Notes / Further Reading` を集約し、読者が「何を正本として信頼するか」と「次にどこを読めばよいか」を短く探し直せるようにするためのものである。本文の全注釈化や脚注の代替ではない。

## この後付けの役割

- 本書の主張を支える source type を、repo artifact、公式 docs、長く残る engineering source に分けて示す
- 章末では収まり切らない next step を、章単位でまとめて示す
- glossary とは役割を分ける。glossary は用語定義、source notes は trust と再参照の導線を扱う

## Source Policy

信頼する順番は固定する。

1. repo 内の canonical artifact
2. 使っている tool、platform、library の公式 docs
3. 長く残る書籍、handbook、public design note
4. ブログ、登壇資料、SNS

この順番を崩すと、本文の主張が流行語や一発成功例に引きずられやすい。特に AI agent 周辺は情報の更新が速いため、一般論より「いま自分が使っている tool の official behavior」を優先する。

## 章別 Source Notes

### CH01 AIエージェントはどこで失敗するか

- 最初に信頼するのは `sample-repo/README.md`、`sample-repo/docs/domain-overview.md`、`sample-repo/docs/seed-issues.md` である。failure mode の説明は recurring case と対応して初めて意味を持つ。
- 外部 source を足すなら、利用中の coding agent、CI、issue tracker の公式 docs と、自分の現場の postmortem を優先する。agent のデモや単発成功例だけで failure model を作らない。

### CH02 プロンプトを契約として設計する

- 最初に信頼するのは `prompts/bugfix-contract.md`、`prompts/feature-contract.md`、`checklists/prompt-contract-review.md` である。Prompt Contract は本文の比喩ではなく、repo に残る contract artifact として読む。
- 外部 source を足すなら、利用中モデルの公式 prompting guide、structured output、tool use の docs を優先する。万能 prompt 集は source of truth にしない。

### CH03 ChatGPTで要件と設計を固める

- 最初に信頼するのは `sample-repo/docs/product-specs/ticket-search.md`、`sample-repo/docs/design-docs/ticket-search-adr.md`、`sample-repo/docs/acceptance-criteria/ticket-search.md` である。exploratory dialogue は、そのまま仕様の正本にならない。
- 外部 source を足すなら、組織で使っている product spec、acceptance criteria、ADR のテンプレートと review record を優先する。要件定義はモデルの流暢さより意思決定の痕跡が重要である。

### CH04 プロンプトを評価する

- 最初に信頼するのは `evals/prompt-contract-cases.json`、`evals/rubrics/feature-spec.json`、`scripts/run-prompt-evals.py` である。prompt の良し悪しは雰囲気ではなく比較可能な case と rubric で読む。
- 外部 source を足すなら、利用中モデルや eval framework の公式 docs を優先する。スクリーンショットだけの prompt comparison は回帰検知の source にならない。

### CH05 Context Engineering の基礎

- 最初に信頼するのは `docs/context-model.md`、`docs/context-budget.md`、`docs/context-risk-register.md` である。Context Engineering は情報量ではなく、寿命、更新責任、毒性の管理として読む。
- 外部 source を足すなら、[OpenAI Codex: AGENTS.md](https://developers.openai.com/codex/guides/agents-md)、[OpenAI Codex: Skills](https://developers.openai.com/codex/skills)、[Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) を優先する。長い prompt の寄せ集めや context window の広さだけで context design を説明しない。

### CH06 Repo Context を設計する

- 最初に信頼するのは `AGENTS.md`、`manuscript/AGENTS.md`、`sample-repo/AGENTS.md`、`sample-repo/docs/repo-map.md`、`sample-repo/docs/architecture.md`、`sample-repo/docs/coding-standards.md` である。repo-map は索引、architecture は設計理由として分けて読む。
- 外部 source を足すなら、[OpenAI Codex: AGENTS.md](https://developers.openai.com/codex/guides/agents-md)、[OpenAI Codex: Hooks](https://developers.openai.com/codex/hooks)、[GitHub Coding Agent: Create custom agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents) を優先する。repo の責務分離は一般論より、instruction layering と managed policy の実運用で判断する方が速い。

### CH07 Task Context と Session Memory

- 最初に信頼するのは `sample-repo/tasks/FEATURE-001-brief.md`、`sample-repo/tasks/FEATURE-001-progress.md`、`docs/session-memory-policy.md`、`.github/ISSUE_TEMPLATE/task.yml` である。ポリシーで `Resume Packet` と呼ぶ最小 packet を、本書では `Restart Packet（Resume Packet）` として扱い、最新 verify とセットで読む。
- 外部 source を足すなら、[OpenAI Codex: AGENTS.md](https://developers.openai.com/codex/guides/agents-md) を先に見て、[Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) は補助線として使う。組織の issue tracker / handoff / change log ルールを優先し、古い summary や chat log を session memory の正本にしない。

### CH08 Skills と Context Pack を再利用する

- 最初に信頼するのは `.agents/skills/draft-chapter/SKILL.md`、`.agents/skills/review-chapter/SKILL.md`、`sample-repo/.agents/skills/issue-to-plan/SKILL.md`、`sample-repo/.agents/skills/verification/SKILL.md`、`sample-repo/context-packs/ticket-search.md` である。skill は再利用 workflow の契約、context pack は task ごとの最小入力として読む。
- 外部 source を足すなら、[OpenAI Codex: Skills](https://developers.openai.com/codex/skills)、[OpenAI Codex: Subagents](https://developers.openai.com/codex/subagents)、[Google ADK: Skills](https://adk.dev/skills/) を優先する。フレームワーク名だけで再利用設計を説明しない。

### CH09 Harness Engineering の基礎

- 最初に信頼するのは `scripts/init.sh`、`scripts/verify-sample.sh`、`sample-repo/docs/harness/single-agent-runbook.md`、`sample-repo/docs/harness/permission-policy.md`、`sample-repo/docs/harness/done-criteria.md` である。single-agent harness は prompt の言い換えではなく、開始条件と終了条件の束である。
- 外部 source を足すなら、[OpenAI Codex: Hooks](https://developers.openai.com/codex/hooks)、[OpenAI: New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)、[Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) を優先する。権限境界は agent の印象論ではなく、実行環境の仕様で決める。

### CH10 Verification Harness を作る

- 最初に信頼するのは `.github/workflows/verify.yml`、`checklists/verification.md`、`sample-repo/tests/test_ticket_search.py`、`artifacts/evidence/README.md` である。verification harness は test、CI、evidence、approval の流れで読む。
- 外部 source を足すなら、[OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-python/tracing/)、[OpenAI Agents SDK: Guardrails](https://openai.github.io/openai-agents-python/guardrails/)、[OpenAI Agents SDK: Human in the Loop](https://openai.github.io/openai-agents-python/human_in_the_loop/) を優先する。green screenshot だけでは reviewer が再検証できない。

### CH11 Long-running Task と Multi-agent

- 最初に信頼するのは `sample-repo/docs/harness/feature-list.md`、`sample-repo/docs/harness/restart-protocol.md`、`sample-repo/docs/harness/multi-agent-playbook.md`、`sample-repo/tasks/FEATURE-002-plan.md` である。multi-agent は role split と restart packet（canonical inputs）が揃って初めて扱う。
- 外部 source を足すなら、[OpenAI Codex: Subagents](https://developers.openai.com/codex/subagents)、[A2A Protocol specification](https://a2a-protocol.org/latest/specification/)、[Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) を優先する。並列化の議論を、write scope と handoff artifact から切り離さない。

### CH12 運用モデルと組織導入

- 最初に信頼するのは `docs/operating-model.md`、`docs/metrics.md`、`checklists/repo-hygiene.md`、`.github/pull_request_template.md` である。運用モデルは Lead / Operator / Reviewer、approval boundary、review budget、cadence、cleanup の組で読む。
- 外部 source を足すなら、[OpenAI Agents SDK: Human in the Loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)、[OpenAI Agents SDK: Guardrails](https://openai.github.io/openai-agents-python/guardrails/)、[GitHub Coding Agent: About coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent) を優先する。導入判断をモデル比較だけで閉じない。
