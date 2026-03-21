# Seed Issues

以下の 4 件は、本書で繰り返し使う貫通ケースです。4 件は別々の小ネタではなく、同じ support-hub の現場を異なる失敗類型と設計レイヤーから見るためのケース群です。CH01 では全体像だけを確認し、後続章で prompt artifact、task brief、context pack、verification harness などの artifact を追加していきます。

## Case Portfolio

| ケース | 現場で起きている痛み | 主に使う章 | 主な artifact | 読者 payoff |
|---|---|---|---|---|
| `BUG-001` | status 更新後に旧状態が見え、二重対応や誤った handoff が起きうる | CH01, CH02, CH09 | `tasks/BUG-001-brief.md`, `tests/test_service.py`, `docs/harness/single-agent-runbook.md` | 範囲を閉じた bugfix を prompt と harness で閉じる考え方が分かる |
| `FEATURE-001` | 類似 ticket を見つけにくく、要求も「検索を良くしたい」で止まりやすい | CH01, CH03, CH04, CH05, CH06, CH07, CH08, CH10 | `docs/product-specs/ticket-search.md`, `docs/design-docs/ticket-search-adr.md`, `docs/acceptance-criteria/ticket-search.md`, `context-packs/ticket-search.md`, `tests/test_ticket_search.py` | 曖昧要求を spec、context、verify へ変換する流れが追える |
| `FEATURE-002` | assignee の意味と監査ログの扱いが長時間タスク化しやすい | CH01, CH07, CH11, CH12 | `tasks/FEATURE-002-plan.md`, `docs/harness/feature-list.md`, `docs/harness/restart-protocol.md`, `docs/harness/multi-agent-playbook.md` | long-running task を plan、restart packet、role 分担で扱う理由が分かる |
| `HARNESS-001` | verify と証跡が弱く、変更を安心して review できない | CH01, CH09, CH10, CH12 | `docs/harness/done-criteria.md`, `docs/harness/permission-policy.md`, `.github/workflows/verify.yml`, `artifacts/evidence/README.md` | verification harness と operating model の必要性が分かる |

## Chapter Guide

| 章 | 主なケース | 今回このケースで何を学ぶか |
|---|---|---|
| CH01 | 4 件すべて | 失敗類型と成熟モデルを、support-hub 全体の現場像に結びつける |
| CH02 | `BUG-001` | bugfix を vague な依頼ではなく Prompt Contract として定義する |
| CH03 | `FEATURE-001` | 曖昧な検索改善要求を spec、acceptance criteria、ADR に変える |
| CH04 | `FEATURE-001` | prompt の良し悪しを eval case と rubric で比較する |
| CH05 | `FEATURE-001` | prompt だけでなく context classes と context budget が必要な理由を理解する |
| CH06 | `FEATURE-001` | repo context と read order を使って参照起点を設計する |
| CH07 | `FEATURE-001`, `FEATURE-002` | issue を task brief に変換し、session を跨ぐ progress を保つ |
| CH08 | `FEATURE-001` | skill と context pack へ再利用可能な workflow を昇格させる |
| CH09 | `BUG-001`, `HARNESS-001` | single-agent harness で開始条件、権限、done criteria を固定する |
| CH10 | `FEATURE-001`, `HARNESS-001` | failing test、local verify、CI、evidence、approval を 1 本の verification harness にまとめる |
| CH11 | `FEATURE-002` | long-running task を feature list、restart packet、role 分担で壊れにくくする |
| CH12 | `FEATURE-002`, `HARNESS-001` | harness を team 運用、review budget、metrics に載せる |

## BUG-001 ステータス更新後の再読み込みで旧状態が見えるケースを再現・修正したい
- 現場の状況: 更新したはずの status が再読み込み後に古く見えると、別担当が未対応と誤認しやすい
- 目的: バグ修正の Prompt Contract と harness を説明する題材
- 主な artifact: `tasks/BUG-001-brief.md`, `tests/test_service.py`, `docs/harness/single-agent-runbook.md`

## FEATURE-001 チケット検索機能を仕様化し、改善したい
- 現場の状況: 類似 ticket を見つけにくいと、再発問い合わせの対応速度が落ちる
- 目的: product spec / ADR / acceptance criteria / context pack を説明する題材
- 主な artifact: `docs/product-specs/ticket-search.md`, `docs/design-docs/ticket-search-adr.md`, `docs/acceptance-criteria/ticket-search.md`, `context-packs/ticket-search.md`

## FEATURE-002 assignee フィルタと監査ログを強化したい
- 現場の状況: assignee の意味が曖昧だと handoff が崩れ、監査ログが弱いと変更理由を追えない
- 目的: long-running task と multi-agent 分解の題材
- 主な artifact: `tasks/FEATURE-002-plan.md`, `docs/harness/feature-list.md`, `docs/harness/restart-protocol.md`, `docs/harness/multi-agent-playbook.md`

## HARNESS-001 verify と evidence bundle を整備したい
- 現場の状況: verify と証跡が弱いと、直した変更を reviewer が信頼できない
- 目的: verification harness と operating model の題材
- 主な artifact: `docs/harness/`, `.github/workflows/verify.yml`, `artifacts/evidence/README.md`
