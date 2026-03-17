# Context Pack: Ticket Search

## Purpose
`FEATURE-001` の検索改善を実装またはレビューするときに読む最小 context pack。

## Read Order
1. `docs/domain-overview.md`
2. `tasks/FEATURE-001-brief.md`
3. `docs/product-specs/ticket-search.md`
4. `docs/design-docs/ticket-search-adr.md`
5. `docs/acceptance-criteria/ticket-search.md`
6. `src/support_hub/service.py`
7. `tests/test_ticket_search.py`
8. `tasks/FEATURE-001-progress.md`

## Canonical Facts
- 検索対象は `title`、`description`、`tags`
- query は trim 後に比較する
- 大文字小文字は区別しない
- 空文字または空白のみの query は全件を返す
- `list_tickets` の既存 public contract は変更しない

## Live Checks
- 最新の `python -m unittest discover -s tests -v` 結果
- `tests/test_ticket_search.py` の期待値
- 直近の progress note

## Exclusions
- relevance ranking
- typo correction
- 外部検索エンジン
- UI redesign

## Done Signals
- docs、tests、実装が同じ挙動を説明している
- verify が通る
- progress note が更新されている
