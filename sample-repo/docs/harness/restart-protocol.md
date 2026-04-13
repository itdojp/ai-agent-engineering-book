# Restart Protocol

## Principle
summary は必要だが、それだけで再開してはならない。restart は plan、feature list、`Progress Note`、verify、owned files をそろえてから行う。

## Restart Packet (Canonical Inputs)
- `tasks/FEATURE-002-plan.md`（`FEATURE-002` では task brief 相当として使う）
- 最新の `docs/harness/feature-list.md`
- 現在の owned files と merge order
- 最新の `Progress Note`
- 直近の verify 結果
- open question と approval 待ち項目

## Live Checks
- `Progress Note` だけで再開せず、必要な verify や status command を再実行する
- current track の owner と owned files を feature list で再確認する
- base branch の更新、rebase 必要性、未解決 conflict を確認する
- approval 待ち項目が `needs-human-approval` のまま残っていないか確認する

## Restart Steps
1. restart packet が揃っているか確認する
2. feature list で current track、owner、exit signal を特定する
3. 最新の verify と open question を読み、古い前提を捨てる
4. current-run の verify や status command を再実行し、live context を取り直す
5. owned files と merge order を確認し、衝突があれば planner に戻る
6. 次の 1 手を 1 work package に絞る
7. owner が変わる場合は handoff contract を書いて role を切り替える
8. 作業後に `Progress Note`、feature list、verify 結果を更新する

## Handoff Contract
- Goal
- Owned Files
- Required Inputs
- Expected Output
- Verify
- Stop Condition
- Next Owner

## Restart Output
- Exit State
  - `done` / `blocked` / `needs-human-approval`
- `Changed Files`
- `Verification`
- `Remaining Gaps`
- next session で再開する owner と first step

## Stop Conditions
- 最新の `Progress Note` がない
- verify 状態が不明、または current-run evidence がない
- summary しかなく primary artifact が欠けている
- ownership が曖昧で、他の workstream と衝突しそう
- approval が必要なのに承認がない
- base branch drift や conflict により、今の diff をそのまま前進させるのが危険
