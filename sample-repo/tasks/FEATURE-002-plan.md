# FEATURE-002 Plan

## Goal
assignee filter の振る舞い整理と assignment change の監査ログ強化を、long-running task として安全に分割する。

## Scope
- assignee filter semantics を既存 contract と矛盾しない形で固定する
- assignment change を history / audit log に残す方針を定義する
- verify、docs、task artifact の更新順を plan に含める

## Non-goals
- search contract の変更
- unrelated な repo 再編
- multi-agent を使うこと自体の最適化

## Work Breakdown
1. planner
   - `docs/harness/feature-list.md` を track 単位に整理する
   - scope、non-goals、ownership を固定する
2. coder-a
   - assignee filter semantics を担当する
   - 主な対象: `src/support_hub/service.py`, `tests/test_service.py`
3. coder-b
   - assignment change audit log を担当する
   - 主な対象: `src/support_hub/models.py`, `src/support_hub/store.py`, `tests/test_service.py`
4. reviewer
   - docs drift、scope 逸脱、role 間衝突を確認する
5. verifier
   - `./scripts/verify-sample.sh` と evidence / report を担当する

## Checkpoints
- Checkpoint 1: planner が scope と ownership を固定した
- Checkpoint 2: assignee filter track の verify が通った
- Checkpoint 3: audit log track の verify が通った
- Checkpoint 4: reviewer / verifier が統合結果を確認した

## Restart Anchor
- read `docs/harness/restart-protocol.md`
- read latest progress note
- read latest verify result
- confirm current track and owner before resuming
