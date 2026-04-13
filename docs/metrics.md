# Metrics

## Purpose
throughput の自慢ではなく、どこで運用が詰まり、どの artifact を補強すべきかを判断するための metrics。verification harness の観点では、verify log、trace、evidence bundle が metrics の観測源になる。

## Throughput
- closed issues / week
  - work package が小さく閉じられているかを見る
- PR cycle time
  - review budget が詰まっていないかを見る
- draft-to-merge time
  - verify と review の待ち時間を測る
- queue wait time
  - どの段階で PR が滞留しているかを見る
- stale draft count
  - queue が詰まり始めていないかを見る

## Quality
- verify failure rate
  - brief / prompt / task 分解の質を見る
- post-merge regression count
  - review と verification harness の効き具合を見る
- approval-stop rate
  - approval boundary が曖昧で手戻りしていないかを見る
- artifact drift incidents
  - docs / tests / task artifact の同期漏れを見る
- reviewer re-open rate
  - review で差し戻しが増えていないかを見る

## Hygiene
- stale docs count
  - entropy cleanup が追いついているかを見る
- orphaned task brief count
  - source of truth でない task artifact が溜まっていないかを見る
- missing verification evidence count
  - user-visible change に対する review 根拠不足を検知する
- evidence freshness failures
  - stale な verify や screenshot が review に流れていないかを見る
- hygiene backlog age
  - cleanup backlog が放置されていないかを見る

## Observability Inputs
- trace coverage
  - long-running task や handoff で failure analysis に必要な履歴が残っているかを見る
- current-run verify availability
  - reviewer が最新 run を確認できるかを見る
- retry concentration
  - 同じ段階で failure loop が起きていないかを見る

## Intervention Rules
- PR cycle time や queue wait time が伸びたら
  - work package を小さく切り直し、review budget 超過を疑う
- verify failure rate が高いなら
  - prompt / brief / context pack の不足を先に疑う
- artifact drift incidents が増えたら
  - done criteria と checklist を見直す
- stale docs count、evidence freshness failures、hygiene backlog age が悪化したら
  - cleanup 専用の work package を先に開く

## Review Questions
- throughput は増えているが review budget を超えていないか
- verify failure の主因は prompt / context / harness のどこか
- queue wait time が長いのは reviewer 待ちか、verify 待ちか、approval 待ちか
- trace coverage が不足して failure analysis ができなくなっていないか
- repo hygiene の悪化が次の作業速度を落としていないか
- stale draft と stale docs を同時に増やしていないか
