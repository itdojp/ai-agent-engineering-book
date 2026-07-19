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
- review completion rate
  - review body、inline comment、suggestion への応答と未解決 thread 0 が merge 前に揃った比率を見る
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
- unresolved review thread residual count
  - merge 前に未解決 thread が残っていないかを見る
- eval rerun coverage
  - prompt、model/runtime profile、tool policy 変更時に eval / smoke check が再実行されているかを見る

## Production Delivery

productionへ影響するwork packageだけを分母にし、Delivery Ownerが週次またはrelease単位で記録する。`N/A`を0件として扱わず、対象外理由を残す。

| 指標 | 定義 | window / owner | 介入の目安 |
|---|---|---|---|
| production confirmation latency | merge timestampから`Production Confirmed` timestampまでの時間 | work package単位 / Delivery Owner | 定義したSLO超過でdeploy、smoke、metric待ちのどこかを分類する |
| production confirmation rate | window内にproductionへ影響したmerged work packageを分母、期限内に`Production Confirmed`となった件数を分子とする | 週次またはrelease単位 / Delivery Owner | 100%未満なら未確認案件を完了扱いにせず棚卸しする |
| deployment failure / unknown count | 対象SHAのdeploymentがfailure、説明できない`cancelled`、または定義したtimeout後もunknownだった件数。対象changeを含む後続deploymentで確認済みの`Superseded`は除く | 週次 / Operator | 1件以上でcauseとretry scopeを記録する |
| marker mismatch count | expected SHA/version/semantic markerとproduction responseが不一致だった件数 | deployment単位 / Delivery Owner | 1件以上でrolloutをhaltする |
| post-deploy metric regression count | 事前定義したbaseline/threshold/windowを逸脱したdeployment件数 | deploymentの観測window / Delivery Owner | 1件以上でrollback判断を行う |
| rollback rate | productionへ影響したdeploymentを分母、rollback開始件数を分子とする | release単位 / Lead | 上昇時はproduction-ready gateとchange sizeを見直す |
| rollback recovery time | `Rollback in Progress`開始からrollback後の`Production Confirmed`までの時間 | rollback単位 / Delivery Owner | 目標超過時はrollback手順とevidence取得を改善する |

metricは、名前だけでなくbaseline、threshold、window、source、ownerが揃った場合だけ判定に使う。trafficが少なく数値metricを判定できない場合も、HTTPとsemantic markerを省略せず、metricを `N/A: low traffic` のように理由付きで記録する。

## Hygiene
- stale docs count
  - entropy cleanup が追いついているかを見る
- orphaned task brief count
  - source of truth でない task artifact が溜まっていないかを見る
- missing verification evidence count
  - user-visible change に対する review 根拠不足を検知する
- evidence freshness failures
  - stale な verify や screenshot が review に流れていないかを見る
- model/runtime profile drift count
  - model、API、SDK、runtime、tool set の変更が確認日と eval 再実行なしに入っていないかを見る
- external-input exception count
  - AI / 外部サービス投入で redaction、provider 条件、approval の例外が増えていないかを見る
- hygiene backlog age
  - cleanup backlog が放置されていないかを見る

## Observability Inputs
- trace coverage
  - long-running task、handoff、retry、restart がある work package に対して、minimum trace reference contract を満たす trace が残っているかを見る
- current-run verify availability
  - reviewer が最新 run を確認できるかを見る
- review-response evidence availability
  - review body / inline comment / suggestion への応答と thread 解決の証跡を reviewer が確認できるかを見る
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
- review completion rate が低い、または unresolved review thread residual が残るなら
  - PR template、review-response 手順、merge 前 gate を見直す
- artifact drift incidents が増えたら
  - done criteria と checklist を見直す
- model/runtime profile drift count や eval rerun coverage が悪化したら
  - model / API / SDK 変更時の確認日記録と eval 再実行を merge 前 gate に戻す
- external-input exception count が増えたら
  - redaction policy、provider 条件確認、approval boundary を見直す
- production confirmation rate が100%未満、またはproduction confirmation latencyがSLOを超えたら
  - merge済みを完了扱いにせず、deploy、HTTP/marker、metricのどこで待っているか分類する
- deployment failure / unknown、marker mismatch、post-deploy metric regression が1件以上なら
  - rolloutをhaltし、対象SHAのevidenceを保存してrollbackまたは是正を判断する
- rollback rateまたはrollback recovery timeが悪化したら
  - production-ready gate、change size、revert手順、確認ownerを見直す
- stale docs count、evidence freshness failures、hygiene backlog age が悪化したら
  - cleanup 専用の work package を先に開く

## Review Questions
- throughput は増えているが review budget を超えていないか
- verify failure の主因は prompt / context / harness のどこか
- queue wait time が長いのは reviewer 待ちか、verify 待ちか、approval 待ちか
- trace coverage が不足して failure analysis ができなくなっていないか
- trace coverage の不足は、trace 不在なのか、verify reference 不足なのか、evidence linkage 不足なのか
- review completion rate が低い原因は、コメント未返信なのか、suggestion 未処理なのか、thread 解決漏れなのか
- model/runtime profile 変更時に eval rerun が抜けていないか
- AI / 外部サービス投入の例外が redaction / approval / provider 条件のどこで増えているか
- mergeからproduction confirmationまでの遅延を、deploy、HTTP/marker、metricのどこで説明できるか
- deployment成功だけでproduction confirmationを代替していないか
- rollback後に新しいmain SHAとproduction markerを再確認したか
- repo hygiene の悪化が次の作業速度を落としていないか
- stale draft と stale docs を同時に増やしていないか
