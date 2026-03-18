# Feature List

## Purpose
`FEATURE-002` を long-running task として管理するための track 一覧。task 全体を 1 回の session で閉じる前提を捨て、workstream ごとに進行と verify checkpoint を持つ。

## Tracks
### Track A: Assignee Filter Semantics
- Goal
  - assignee filter の挙動を既存 public contract を壊さずに明文化する
- Primary Files
  - `src/support_hub/service.py`
  - `tests/test_service.py`
- Verify Signal
  - assignee filter 関連 test が通る

### Track B: Assignment Change Audit Log
- Goal
  - assignment change を history / audit log として残す方針を固める
- Primary Files
  - `src/support_hub/models.py`
  - `src/support_hub/store.py`
  - `tests/test_service.py`
- Verify Signal
  - assignment change の履歴が test で確認できる

### Track C: Verification And Docs Sync
- Goal
  - docs、task artifact、verify 手順を実装差分と同期する
- Primary Files
  - `tasks/FEATURE-002-plan.md`
  - `docs/harness/restart-protocol.md`
  - `docs/harness/multi-agent-playbook.md`
- Verify Signal
  - plan と verify 結果に drift がない

## Shared Constraints
- `list_tickets` と search の既存 contract を壊さない
- unrelated な artifact を巻き込まない
- verify と docs 更新を後回しにしない
