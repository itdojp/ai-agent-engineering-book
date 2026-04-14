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
  - long-running task、handoff、retry、restart がある work package に対して、minimum trace reference contract を満たす trace が残っているかを見る
- current-run verify availability
  - reviewer が最新 run を確認できるかを見る
- retry concentration
  - 同じ段階で failure loop が起きていないかを見る

## Trace Coverage Definition
- 分母
  - long-running task、handoff、retry、restart のいずれかがあり、trace 参照が必要な work package 数
- 分子
  - task / work-package id、run timestamp または run id、owner / handoff、retry / restart reason、verify reference、evidence linkage、redaction note のうち必要項目を満たす trace を残した work package 数

必要項目の判定は次のルールで揃える。
- 常に必須
  - task / work-package id
  - run timestamp または run id（どちらか一方は必須）
  - verify reference
  - evidence linkage
- 条件付き必須
  - owner / handoff: handoff がある work package では必須。handoff がない場合も current owner を書き、owner 概念を置かない運用だけ `N/A` を使う
  - retry / restart reason: retry または restart があれば必須。無ければ `N/A` を明示する
  - redaction note: redact した箇所があれば必須。無ければ `none` または `N/A` を明示する

未該当項目は空欄や省略ではなく、`N/A` や `none` のような非該当表記で残す。分子に数えるには、常に必須の項目が埋まっており、条件付き必須の項目は該当時に埋まっている必要がある。

ここでの trace coverage は trace file の有無だけではない。reviewer が「どの verify とどの task に紐づく trace か」を説明できるかまで含めて測る。

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
- trace coverage の不足は、trace 不在なのか、verify reference 不足なのか、evidence linkage 不足なのか
- repo hygiene の悪化が次の作業速度を落としていないか
- stale draft と stale docs を同時に増やしていないか
