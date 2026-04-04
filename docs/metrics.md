# Metrics

## Purpose
throughput の自慢ではなく、どこで運用が詰まり、どの artifact を補強すべきかを判断するための metrics。

## Throughput
- closed issues / week
  - work package が小さく閉じられているかを見る
- PR cycle time
  - review budget が詰まっていないかを見る
- draft-to-merge time
  - verify と review の待ち時間を測る
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

## Hygiene
- stale docs count
  - entropy cleanup が追いついているかを見る
- orphaned task brief count
  - source of truth でない task artifact が溜まっていないかを見る
- missing verification evidence count
  - user-visible change に対する review 根拠不足を検知する
- hygiene backlog age
  - cleanup backlog が放置されていないかを見る

## Intervention Rules
- PR cycle time が伸びたら
  - work package を小さく切り直し、review budget 超過を疑う
- verify failure rate が高いなら
  - prompt / brief / context pack の不足を先に疑う
- artifact drift incidents が増えたら
  - done criteria と checklist を見直す
- stale docs count と hygiene backlog age が悪化したら
  - cleanup 専用の work package を先に開く

## Review Questions
- throughput は増えているが review budget を超えていないか
- verify failure の主因は prompt / context / harness のどこか
- repo hygiene の悪化が次の作業速度を落としていないか
- stale draft と stale docs を同時に増やしていないか
