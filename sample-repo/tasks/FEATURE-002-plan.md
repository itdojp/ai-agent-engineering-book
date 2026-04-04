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

## Planner Responsibilities
- scope、non-goals、approval gate、merge order を固定する
- `docs/harness/feature-list.md` で owner と shared file rule を確定する
- coder が迷わず着手できる状態を作ってから parallelism を許可する

## Workstreams
| Track | Owner | Goal | Owned Files | Verify | Exit Signal |
|---|---|---|---|---|---|
| A | coder-a | assignee filter semantics を固定する | `src/support_hub/service.py`, `tests/test_service.py` | assignee filter 関連 test | semantics の決定と verify が `Progress Note` に残る |
| B | coder-b | assignment change audit log を固定する | `src/support_hub/models.py`, `src/support_hub/store.py` | audit log 関連 test | audit 方針と verify が `Progress Note` に残る |
| C | reviewer / verifier | docs、artifact、verify summary を統合する | `docs/harness/*.md`, `tasks/FEATURE-002-plan.md` | `./scripts/verify-sample.sh` と review | `Changed Files` / `Verification` / `Remaining Gaps` を説明できる |

## Shared File Rule
- `tests/test_service.py` は assignee filter workstream の owner（`coder-a`）を優先する。
- audit log workstream で同 file の更新が必要になった場合は、Track A 完了後に planner が sync window を開く。
- docs と task artifact の更新は Track C でまとめる。

## Merge Order
1. planner が Track A / B / C、owner、shared file rule を固定する
2. `coder-a` と `coder-b` は shared file rule を守って並列化する
3. reviewer が docs drift と scope 逸脱を確認する
4. verifier が current-run verify と report contract を閉じる

## Approval Gates
- public contract を変える
- audit retention policy を変える
- verify script や CI を変える
- shared file を無計画に同時更新する

## Handoff Contract
- Goal
- Owned Files
- Required Inputs
- Expected Output
- Verify
- Stop Condition
- Next Owner

## Checkpoints
- Checkpoint 1: planner が scope、Track A / B / C、shared file rule を固定した
- Checkpoint 2: Track A の verify が通った
- Checkpoint 3: Track B の verify が通った
- Checkpoint 4: Track C で reviewer / verifier が current-run evidence を確認した

## Restart Anchor
- read `docs/harness/restart-protocol.md`
- read latest `docs/harness/feature-list.md`
- read latest `Progress Note`
- read latest verify result
- confirm current track, owner, and next work package before resuming
