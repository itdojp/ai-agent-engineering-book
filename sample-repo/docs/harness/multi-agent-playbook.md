# Multi-agent Playbook

## Purpose
support-hub で local multi-agent orchestration を使うときの entry criteria、role、owned files、merge order、exit state を定義する。対象は same-repo / same-runtime の role split であり、cross-service の remote interoperability 全般を定義する文書ではない。multi-agent を default にせず、ownership、handoff、merge order が明確なときだけ parallelism を使う。

## Entry Criteria
- disjoint な workstream がある
- planner が scope、non-goals、checkpoint、shared file rule を固定している
- role ごとの owned files を文章で定義できる
- restart packet と handoff contract を更新できる

## Roles
- planner
  - brief / plan / scope freeze
  - workstream、ownership、merge order を定義する
- coder
  - 実装と test を担当する
  - 自分の owned files 以外は変更しない
- reviewer
  - diff / risk / docs drift / scope逸脱を確認する
- verifier
  - verify 実行、evidence、report を担当する

## Coordination Rules
- planner が scope を固定する前に coder を parallel にしない
- coder 同士は disjoint な owned files を前提にする
- shared file が必要な場合は planner が sync window を開く
- reviewer と verifier は stale evidence で判断しない
- handoff では canonical report fields を必ず残す

## Owned Files Discipline
- 各 role は着手前に owned files を明示する
- 共有 file に触る必要がある場合は planner に戻して merge order を決める
- reviewer と verifier は原則として docs / artifact / report 側を持ち、実装 file へ直接書き込まない

## Merge Order
1. planner が plan、owned files、checkpoint を固定する
2. coder が disjoint な workstream を進める
3. reviewer が docs drift と scope 逸脱を確認する
4. verifier が verify と evidence を確定する
5. 最後に統合差分をまとめて exit state を判定する

## Use Multi-agent When
- disjoint な workstream があり、owner と owned files を明示できる
- reviewer / verifier を並列化すると待ち時間が減る
- restart packet と handoff contract を文章で固定できる
- merge order を先に決められる

## Do Not Use When
- single-agent で 1 session に閉じられる
- scope が曖昧で planner がまだ固まっていない
- 複数 role が同じ file を同時に触る
- summary だけで handoff しようとしている
- current-run verify や `Progress Note` が欠けている

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
  - checkpoint が閉じ、verify と report が揃っている
- `blocked`
  - ownership 衝突、未解決の verify failure、source conflict がある、または owned files や merge order を組み直さないと進められない
- `needs-human-approval`
  - public contract、approval boundary、merge policy に触れた
