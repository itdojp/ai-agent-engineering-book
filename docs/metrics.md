# Metrics

## Throughput
- closed issues / week
  - work package が小さく閉じられているかを見る
- PR cycle time
  - review budget が詰まっていないかを見る
- draft-to-merge time
  - verify と review の待ち時間を測る

## Quality
- verify failure rate
  - brief / prompt / task 分解の質を見る
- post-merge regression count
  - review と verification harness の効き具合を見る
- artifact drift incidents
  - docs / tests / task artifact の同期漏れを見る

## Hygiene
- stale docs count
  - entropy cleanup が追いついているかを見る
- orphaned task brief count
  - source of truth でない task artifact が溜まっていないかを見る
- missing verification evidence count
  - user-visible change に対する review 根拠不足を検知する

## Review Questions
- throughput は増えているが review budget を超えていないか
- verify failure の主因は prompt / context / harness のどこか
- repo hygiene の悪化が次の作業速度を落としていないか
