# Feature List

## Purpose
`FEATURE-002` を long-running task として管理するための track 一覧。task 全体を 1 回の session で閉じる前提を捨て、workstream ごとに owner、entry criteria、verify signal、exit signal を持たせる。

## Operating Rules
- planner が track 定義と ownership を固定してから coder が着手する。
- 1 回の session で閉じるのは 1 checkpoint までとし、track 全体を一気に終わらせようとしない。
- verify が通ったら progress note と feature list を同じ session で更新する。
- approval 待ち、verify 不明、shared file の衝突がある track は `blocked` または `needs-human-approval` として止める。

## Tracks
### Track A: Assignee Filter Semantics
- Status
  - ready-for-coder-a
- Owner
  - coder-a
- Goal
  - assignee filter の挙動を既存 public contract を壊さずに明文化する
- Entry Criteria
  - planner が scope と non-goals を固定している
  - public contract を変えない前提が確認されている
- Owned Files
  - `src/support_hub/service.py`
  - `tests/test_service.py`
- Verify Signal
  - assignee filter 関連 test が通る
- Exit Signal
  - `Changed Files` / `Verification` / `Remaining Gaps` を説明できる
  - progress note に semantics の決定と latest verify が残っている
- Dependencies
  - none

### Track B: Assignment Change Audit Log
- Status
  - ready-for-coder-b
- Owner
  - coder-b
- Goal
  - assignment change を history / audit log として残す方針を固める
- Entry Criteria
  - planner が audit log の scope と approval 条件を固定している
  - Track A の open question を前提にしない形で着手できる
- Owned Files
  - `src/support_hub/models.py`
  - `src/support_hub/store.py`
- Verify Signal
  - assignment change の履歴が test で確認できる
- Exit Signal
  - data model と store の変更理由を説明できる
  - verify 結果と open question が progress note に残っている
- Dependencies
  - none

### Track C: Verification And Docs Sync
- Status
  - ready-after-a-and-b
- Owner
  - reviewer / verifier
- Goal
  - docs、task artifact、verify 手順を実装差分と同期する
- Entry Criteria
  - Track A と Track B の verify 結果が current-run で残っている
  - planner が merge order を固定している
- Owned Files
  - `tasks/FEATURE-002-plan.md`
  - `docs/harness/restart-protocol.md`
  - `docs/harness/multi-agent-playbook.md`
  - `docs/harness/feature-list.md`
- Verify Signal
  - plan と verify 結果に drift がない
  - reviewer / verifier が current-run evidence を確認できる
- Exit Signal
  - review summary で統合結果を説明できる
  - `Remaining Gaps` に残る事項が短く明示されている
- Dependencies
  - Track A
  - Track B

## Shared File Rule
- `tests/test_service.py` は Track A の owner を優先する。
- Track B で同 file の更新が必要になった場合は、planner が sync window を開いてから着手する。
- `docs/harness/*.md` と `tasks/FEATURE-002-plan.md` は reviewer / verifier の統合フェーズで更新する。

## Stop Instead Of Parallelizing
- owner が未定のまま track を増やそうとしている
- Track A と Track B が同じ file を同時に触ろうとしている
- latest verify が current-run で残っていない
- approval 待ちの論点を抱えたまま coder を前進させようとしている
