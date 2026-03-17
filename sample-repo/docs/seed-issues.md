# Seed Issues

以下の 4 件は、本書で繰り返し使う貫通ケースです。CH01 では全体像だけを確認し、後続章で prompt artifact、task brief、verification harness などの artifact を追加していきます。

## BUG-001 ステータス更新後の再読み込みで旧状態が見えるケースを再現・修正したい
- 目的: バグ修正の Prompt Contract と verify を説明する題材
- 主な artifact: `tasks/BUG-001-brief.md`, `tests/test_service.py`

## FEATURE-001 チケット検索機能を仕様化し、改善したい
- 目的: product spec / ADR / acceptance criteria を説明する題材
- 主な artifact: `docs/product-specs/ticket-search.md`

## FEATURE-002 assignee フィルタと監査ログを強化したい
- 目的: long-running task と multi-agent 分解の題材
- 主な artifact: `tasks/FEATURE-002-plan.md`

## HARNESS-001 verify と evidence bundle を整備したい
- 目的: verification harness の題材
- 主な artifact: `docs/harness/`, `.github/workflows/verify.yml`
