# FEATURE-001 Progress

## Status
ready-for-handoff

## Current Goal
検索仕様、実装、tests、task artifact の同期

## Completed
- product spec、acceptance criteria、ADR の初版を揃えた
- `search_tickets` が `title`、`description`、`tags` を対象にする方針を確定した
- `src/support_hub/service.py` と `tests/test_ticket_search.py` を仕様に同期した
- unittest が通ることを確認した

## Decided
- 初期実装は `src/support_hub/service.py` の in-memory 部分一致検索とする
- query は trim 後に比較し、大文字小文字は区別しない
- ranking と typo correction は今回の scope から外す

## Open Questions
- status / assignee filter を search API に統合するか
- 将来の検索 abstraction 導入を `FEATURE-002` と切り分けるか

## Last Verify
- `python -m unittest discover -s tests -v` : pass

## Changed Files
- `docs/product-specs/ticket-search.md`
- `docs/design-docs/ticket-search-adr.md`
- `docs/acceptance-criteria/ticket-search.md`
- `src/support_hub/service.py`
- `tests/test_ticket_search.py`

## Resume Steps
1. `tasks/FEATURE-001-brief.md` を読む
2. `docs/product-specs/ticket-search.md` と `docs/acceptance-criteria/ticket-search.md` を開く
3. `src/support_hub/service.py` と `tests/test_ticket_search.py` を比較する
4. verify を実行して結果を更新する

## Next Step
- handoff 時は `Open Questions` を確認し、scope 拡張が必要なら follow-up task に切り出す
