# Multi-agent Playbook

## Roles
- planner
  - brief / plan / scope freeze
  - workstream と ownership を定義する
- coder
  - 実装と test を担当する
  - 他 role の ownership には触らない
- reviewer
  - diff / risk / docs drift / scope逸脱を確認する
- verifier
  - verify 実行、evidence、report を担当する

## Use Multi-agent When
- disjoint な workstream がある
- reviewer / verifier を並列化すると待ち時間が減る
- restart packet と ownership を文章で固定できる

## Do Not Use When
- single-agent で 1 session に閉じられる
- scope が曖昧で planner がまだ固まっていない
- 複数 role が同じ file を同時に触る

## Handoff Contract
- Goal
- Owned Files
- Required Inputs
- Expected Output
- Stop Condition
