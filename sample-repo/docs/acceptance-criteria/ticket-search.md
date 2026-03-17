# Acceptance Criteria: Ticket Search

## Functional Criteria
- AC-1: `title` に部分一致する query で該当チケットを返す
- AC-2: `description` に部分一致する query で該当チケットを返す
- AC-3: `tags` に部分一致する query で該当チケットを返す
- AC-4: query の大文字小文字は区別しない
- AC-5: 空文字または空白のみの query は全件を返す

## Artifact Criteria
- AC-6: `docs/product-specs/ticket-search.md` と `docs/design-docs/ticket-search-adr.md` が更新されている
- AC-7: `tests/test_ticket_search.py` が `title`、`description`、`tags`、空 query を検証している

## Out of Scope Checks
- relevance ranking は必須ではない
- typo correction は必須ではない
- 外部検索エンジンの導入は必須ではない
