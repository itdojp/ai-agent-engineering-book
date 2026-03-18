# Restart Protocol

## Restart Packet
- `tasks/FEATURE-002-plan.md`
- 最新の feature list
- 最新の Progress Note
- 直近の verify 結果
- open question と approval 待ち項目

## Restart Steps
1. restart packet が揃っているか確認する
2. feature list で現在の track を特定する
3. 最新の verify と open question を読み、古い前提を捨てる
4. 次の 1 手を 1 work package に絞る
5. 役割が変わる場合は planner / coder / reviewer / verifier のどこに戻るかを明示する
6. 作業後に Progress Note と verify 結果を更新する

## Stop Conditions
- 最新の Progress Note がない
- verify 状態が不明
- ownership が曖昧で、他の workstream と衝突しそう
- approval が必要なのに承認がない
