# Operating Model

## Purpose
AIエージェントをチーム運用へ載せるための最小 operating model。責務分担、review budget、cadence、導入段階、budget 超過時の止め方を固定する。

## Operating Principles
- 1 issue = 1 work package を守る
- Human は責任主体、Agent は実行主体とする
- current-run verify がない差分は review-ready と見なさない
- review budget を超えたら新規着手より queue 解消を優先する
- entropy cleanup を cadence に組み込み、後回しにしない

## Runtime-managed capability と team-owned duty

runtime は background execution、hosted tools、managed context のような mechanism を提供できる。一方で、次の責務は repo / team 側で定義し続ける必要がある。

| 領域 | runtime が提供しうるもの | repo / team が持つべき責務 |
|---|---|---|
| execution | background execution、job status、再接続 | issue 単位の work package、stop condition、retry 条件 |
| capability | hosted tools、外部接続、resource access | permission boundary、approval rule、secret 取扱い |
| context | managed context、session storage | source of truth、artifact sync、refresh policy |
| verification | verify job の実行や表示 | どの verify を必須とするか、evidence の基準 |
| review | status surface、diff 表示 | 最終レビュー、承認、merge 判断 |

runtime は mechanism の提供者であり、policy の決定者ではない。この区別を曖昧にすると、便利機能が増えるほど責務の所在が見えなくなる。

## Responsibilities
### Human / Team
- 目的設定と優先順位の決定
- 設計上の重要判断
- 破壊的変更と approval boundary の承認
- artifact sync と source of truth の維持
- 最終レビューと merge 判断
- repo hygiene と entropy cleanup の維持

### Agent
- 既存 repo の探索
- 定型編集と scoped implementation
- test / docs / artifact 更新
- verify 実行
- 変更差分の説明

## Human Role Split
### Lead
- issue 優先順位と work package の粒度を決める
- 破壊的変更、public contract、運用ポリシー変更を承認する
- review budget を超えた場合の投入量調整を判断する

### Operator
- brief、artifact、verify を揃えて agent 実行を進める
- current-run verify と evidence を PR に残す
- `Remaining Gaps` を明示し、曖昧な completion を避ける

### Reviewer
- `Goal`、`Changed Files`、`Scope and Non-goals`、`Verification`、`Evidence / Approval`、`Remaining Gaps` を確認する
- docs drift、artifact drift、scope 逸脱を確認する
- merge 可能か、追加 verify が必要かを判定する

## Review Budget
- reviewer 1 人あたり同時に深く見る PR は 2 本まで
- evidence bundle が必要な PR は reviewer ごとに 1 本まで
- stale draft が 3 本を超えたら、新規 work package を開く前に queue を減らす
- review budget を超えるときは、新規 work package を開く前に既存 PR を閉じる

## Budget Overflow Actions
1. 新規 issue 着手を止める
2. stale draft / blocked PR を棚卸しする
3. work package をさらに小さく切る
4. verify 不足と evidence 不足を優先して潰す

## Cadence
1. issue を 1 work package に切る
2. task brief と関連 artifact を揃える
3. agent が実装と verify を進める
4. Human が review / approval を行う
5. merge 後に metrics と learnings を記録する
6. 週次で entropy cleanup を行う

## Weekly Review
- PR cycle time と stale draft 数を確認する
- verify failure の主因が prompt / context / harness のどこかを分類する
- stale docs、orphaned task brief、missing evidence を cleanup backlog に入れる

## Rollout Stages
### Pilot
- docs、tests、scoped bugfix に限定する
- Exit Criteria
  - verify と PR summary が毎回揃う
  - review budget を超えずに回る

### Guided Delivery
- issue / brief / verify / PR template を標準化する
- Exit Criteria
  - current-run verify と evidence の書式が揃う
  - repo hygiene の週次運用が始まる

### Team Scale
- review budget、metrics、repo hygiene を定例運用に入れる
- Exit Criteria
  - throughput / quality / hygiene の指標で投入量調整ができる
  - cleanup と導入判断が担当者依存で止まらない
