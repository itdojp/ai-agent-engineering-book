# FEATURE-001 Brief

## Source
- `docs/seed-issues.md` の `FEATURE-001`
- `.github/ISSUE_TEMPLATE/task.yml`

## Goal
チケット検索機能を仕様に沿って明文化し、現行実装と docs と tests を同期する。

## Scope
- `search_tickets` の検索挙動を `title`、`description`、`tags` の部分一致に揃える
- product spec、acceptance criteria、ADR を現行挙動と同期する
- progress note に判断と verify 結果を残す

## Inputs
- `docs/product-specs/ticket-search.md`
- `docs/design-docs/ticket-search-adr.md`
- `docs/acceptance-criteria/ticket-search.md`
- `src/support_hub/service.py`
- `tests/test_ticket_search.py`

## Deliverables
- 検索関連 docs の更新
- 必要なら code / tests の更新
- progress note の更新

## Constraints
- `list_tickets` の既存 public contract は変更しない
- ranking、typo correction、外部検索エンジンは今回扱わない
- docs、tests、task artifact を同時に更新する

## Acceptance Criteria
- title / description / tags の部分一致
- 空 query で全件返却
- 大文字小文字を区別しない
- docs と tests が一致

## Verification
`python -m unittest discover -s tests -v`

## Open Questions
- search と status / assignee filter の組み合わせは `FEATURE-002` で扱うか、別 issue に切り出すか

## Out of Scope
- UI 層の実装
- relevance ranking
- typo correction
