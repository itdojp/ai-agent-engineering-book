# Multi-agent Playbook

## Purpose
multi-agent を default にせず、ownership、handoff、merge order が明確なときだけ parallelism を使うための playbook。

## Entry Criteria
- planner が goal、non-goals、workstream、merge order を固定している
- 各 workstream に owner、owned files、verify signal、exit signal がある
- restart packet が current-run の verify と open question を含んでいる
- shared file rule が feature list か plan に明示されている

## Roles
### planner
- scope freeze、workstream 分解、handoff 定義
- output
  - `tasks/FEATURE-002-plan.md`
  - `docs/harness/feature-list.md`

### coder
- 実装と test 更新
- output
  - code diff
  - local verify result
  - progress note の更新案

### reviewer
- diff / docs drift / scope 逸脱 / shared-file 衝突の確認
- output
  - review findings
  - docs / artifact update の要求

### verifier
- verify 実行、evidence、report
- output
  - current-run verify evidence
  - `Changed Files` / `Verification` / `Remaining Gaps`

## Coordination Rules
- planner が scope を固定する前に coder を parallel にしない
- coder 同士は disjoint な owned files を前提にする
- shared file が必要な場合は planner が sync window を開く
- reviewer と verifier は stale evidence で判断しない
- handoff では canonical report fields を必ず残す

## Use Multi-agent When
- disjoint な workstream があり、owner と owned files を明示できる
- reviewer / verifier を並列化すると待ち時間が減る
- restart packet と handoff contract を文章で固定できる
- merge order を先に決められる

## Do Not Use When
- single-agent で 1 session に閉じられる
- scope が曖昧で planner がまだ固まっていない
- 複数 role が同じ file を同時に触る
- current-run verify や progress note が欠けている

## Handoff Contract
- Goal
- Owned Files
- Required Inputs
- Expected Output
- Verify
- Stop Condition
- Next Owner

## Exit States
- `done`
  - owner の workstream が exit signal を満たした
- `blocked`
  - verify 不明、input 不足、shared-file 衝突などで前進不能
- `needs-human-approval`
  - public contract、approval boundary、merge policy に触れた
