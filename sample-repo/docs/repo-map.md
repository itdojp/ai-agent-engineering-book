# Repo Map

## Read Order
1. `docs/domain-overview.md`
2. `docs/architecture.md`
3. `docs/coding-standards.md`
4. 関連する `tasks/` と `context-packs/`
5. 変更対象コードと tests

## Code
- `src/support_hub/models.py`: Ticket domain object
- `src/support_hub/store.py`: in-memory persistence and seed data
- `src/support_hub/service.py`: application service layer

## Tests
- `tests/test_service.py`: list / update / assignee filter
- `tests/test_ticket_search.py`: search behavior

## Hot Paths
- `src/support_hub/service.py`: 振る舞い変更の入口。多くの issue がここを通る
- `tests/test_service.py`: 既存挙動の回帰 guard
- `tests/test_ticket_search.py`: `FEATURE-001` の verify 起点

## Docs
- `docs/domain-overview.md`: ドメイン概要
- `docs/architecture.md`: 層構成と責務
- `docs/coding-standards.md`: 変更時の規約
- `docs/product-specs/`: 機能仕様
- `docs/design-docs/`: ADR など
- `docs/acceptance-criteria/`: 受け入れ条件
- `docs/harness/`: runbook / permission / done / restart

## Task Artifacts
- `tasks/`: brief / Progress Note / plan
- `context-packs/`: task specific context pack / canonical facts / live checks
- `.agents/skills/`: repeatable workflow

## Update Guide
- 振る舞い変更時は code だけでなく docs / tests / task artifacts を同時に更新する
- 変更対象が `service.py` なら、関連する acceptance criteria と `Progress Note` を確認する
- 中断や handoff がある場合は、task brief、最新 `Progress Note`、最新 verify、再開時に読むファイル一覧が restart packet として揃っている状態にする
- public contract や外部依存を変える場合は approval boundary を越える前に止まる
