# Context Pack: Ticket Search

## Purpose
`FEATURE-001` の検索改善を実装またはレビューするときに読む最小 context pack。

## Read Order
1. `docs/domain-overview.md`
2. `docs/repo-map.md`
3. `tasks/FEATURE-001-brief.md`
4. `docs/product-specs/ticket-search.md`
5. `docs/design-docs/ticket-search-adr.md`
6. `docs/acceptance-criteria/ticket-search.md`
7. `src/support_hub/service.py`
8. `tests/test_ticket_search.py`
9. `tasks/FEATURE-001-progress.md`

## Canonical Facts
- 検索対象は `title`、`description`、`tags`
- query は trim 後に比較する
- 大文字小文字は区別しない
- 空文字または空白のみの query は全件を返す
- `list_tickets` の既存 public contract は変更しない

## Source Hierarchy
1. `tasks/FEATURE-001-brief.md`
2. `docs/acceptance-criteria/ticket-search.md`
3. `docs/product-specs/ticket-search.md` と `docs/design-docs/ticket-search-adr.md`
4. 最新の `Progress Note` と verify 出力

`Progress Note` と verify は session memory / live evidence であり、brief や acceptance criteria を上書きしない。

## Live Checks
- 最新の `python -m unittest discover -s tests -v` 結果
- `tests/test_ticket_search.py` の期待値
- 直近の `Progress Note`
- public contract や scope を越える変更が approval boundary に当たらないか

## Approval Boundary
- `list_tickets` の既存 public contract を変える
- relevance ranking や typo correction を今回 scope に追加する
- 外部検索エンジンや新しい依存を導入する

## Exclusions
- relevance ranking
- typo correction
- 外部検索エンジン
- UI redesign

## Done Signals
- docs、tests、実装が同じ挙動を説明している
- verify が通る
- `Progress Note` が更新されている
- unresolved な approval boundary が残っていない
