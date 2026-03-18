# Operating Model

## Purpose
AIエージェントをチーム運用へ載せるための最小 operating model。責務分担、review budget、cadence、導入段階を固定する。

## Responsibilities
### Human
- 目的設定
- 設計上の重要判断
- 破壊的変更の承認
- 最終レビューと merge 判断
- repo hygiene と entropy cleanup

### Agent
- 既存 repo の探索
- 定型編集と scoped implementation
- test / docs / artifact 更新
- verify 実行
- 変更差分の説明

## Review Budget
- reviewer 1 人あたり同時に深く見る PR は 2 本まで
- evidence bundle が必要な PR は reviewer ごとに 1 本まで
- review budget を超えるときは、新規 work package を開く前に既存 PR を閉じる

## Cadence
1. issue を 1 work package に切る
2. task brief と関連 artifact を揃える
3. agent が実装と verify を進める
4. Human が review / approval を行う
5. merge 後に metrics と learnings を記録する

## Rollout Stages
### Pilot
- docs、tests、scoped bugfix に限定する

### Guided Delivery
- issue / brief / verify / PR template を標準化する

### Team Scale
- review budget、metrics、repo hygiene を定例運用に入れる
