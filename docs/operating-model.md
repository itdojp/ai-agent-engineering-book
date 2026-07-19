# Operating Model

## Purpose
AIエージェントをチーム運用へ載せるための最小 operating model。責務分担、review budget、cadence、導入段階、budget 超過時の止め方を固定する。

## Operating Principles
- 1 issue = 1 work package を守る
- Human は責任主体、Agent は実行主体とする
- current-run verify がない差分は review-ready と見なさない
- review budget を超えたら新規着手より queue 解消を優先する
- entropy cleanup を cadence に組み込み、後回しにしない
- review 完了、deployment 承認、production 確認を別の判断として記録する

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

## Runtime-managed loop / repo-owned manual harness の判断

最終 review / merge は常に human-owned であり、source-of-truth artifact も repo-owned のままである。その前提で、runtime-managed loop だけで足りるか、manual harness を厚く残すかを次の表で判断する。

| 判断要因 | runtime-managed loop で足りる条件 | repo-owned manual harness が必要な条件 |
|---|---|---|
| human approval | 最終 review 以外に追加の approval gate がない | 実行前 / 実行中 / 実行後の approval を artifact で管理したい |
| evidence / audit trail | runtime status と verify 結果で十分に説明できる | custom evidence bundle や監査用の記録を残す必要がある |
| stop / resume logic | 線形な run、単純な retry、単純な stop で閉じる | 条件分岐した stop / resume、handoff、retry rule を残したい |
| source-of-truth maintenance | task brief や done criteria が固定済みで run 中に更新しない | artifact sync、refresh policy、owned files を run 中に明示したい |
| review packaging | reviewer が runtime surface をそのまま読めば足りる | `Changed Files`、`Verification`、`Remaining Gaps` を custom に整形したい |

判断基準は「runtime が便利か」ではなく、「custom policy と証跡がどれだけ必要か」である。そこが増えるほど、repo-owned manual harness を薄くしすぎない方が安全になる。

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

### Delivery Owner
- production-ready plan の target、marker、metric、halt / rollback / restart 条件を確定する
- 対象 deployment と production evidence を確認し、`Production Confirmed` または `Halted` を記録する
- rollback と再開の判断、owner、timestamp、evidence location を残す

1人運用では、同じ人が Lead、Operator、Reviewer、Delivery Owner を兼任してよい。ただし、review 完了、deployment 承認、production 確認を1つのチェックで代替してはならない。各判断の時刻、対象SHA、根拠を分けて残す。

## Delivery State Model

merge はcode reviewの終了であり、production成功の証拠ではない。productionへ影響するwork packageは、次の状態を順に通る。

| 状態 | entry condition | owner | 必須 evidence | exit condition |
|---|---|---|---|---|
| `Review Complete` | review body / inline / suggestionを処理し、unresolved thread 0、CI green | Reviewer | review response、thread、CI URL | merge可否を判断した |
| `Production Ready` | 下記production-ready recordが埋まり、rollback可能 | Delivery Owner | target、SHA/version、route/marker、metric、owner、rollback plan | deployment開始を承認した |
| `Deployment Approved` | 必要なenvironment等の保護条件を通過、または適用不要を記録 | 承認者 | approval/deployment recordまたは`N/A`理由 | deployment jobが開始した |
| `Deployed` | 対象artifactのdeployment jobがsuccess | Operator | 対象SHAのdeploymentとworkflow URL | production smokeを開始した |
| `Production Confirmed` | HTTP、semantic marker、代表route、metricが期待値内 | Delivery Owner | owner/timestamp付きconfirmation record | work packageを完了できる |
| `Halted` | deploymentがfailed/unknown、marker不一致、route異常、metric逸脱 | Delivery Owner | halt理由、観測値、影響、次の判断 | rollbackまたは是正を決めた |
| `Rollback in Progress` | 承認済みrollbackを開始 | Operator | revert PR等のrollback change、deployment URL | rollback後のproductionを再確認した |

`Deployment Approved` は変更を環境へ送ってよいというcontrol decisionであり、deployment成功やproduction正常性の証明ではない。`Deployed` もartifactが送られたことだけを示し、`Production Confirmed` までは完了扱いにしない。

## Production-ready Gate

merge前にPRまたはlinked Issueへ次を記録する。該当しない変更は `N/A` と理由を残す。

- target environmentと公開URL
- merge後に確定するSHA/versionの記録場所と、productionで照合するsemantic marker
- deploy owner、production confirmation owner、承認者（必要な場合）
- root smokeと代表route、期待するHTTP status / content marker
- metric名、baseline、許容threshold、観測window、取得元
- halt条件、rollback手段、restart条件
- workflow、deployment、HTTP、metric evidenceの保存場所

## Post-deploy Confirmation

Delivery Ownerは、集約statusや「最新らしい」画面だけでなく、対象SHAへ紐づく証拠を確認する。

1. 対象SHA/versionのdeployment statusとworkflow runを照合する。
2. target URLのHTTP smokeと、代表routeのHTTP statusを確認する。
3. titleだけでなく、SHA、version、release固有文言等のsemantic markerを照合する。
4. 事前に定義したmetricを観測window全体で確認する。
5. owner、UTC timestamp、観測値、evidence URLをlinked IssueまたはPRへ記録する。

repository全体の集約statusと対象deploymentが食い違う場合は、食い違い自体を記録し、対象SHAのdeployment、workflow、公開URL/markerを正本として判定する。食い違いを説明できない場合は `Halted` とする。

## Halt, Rollback, and Restart

| trigger | action | completionを止めるevidence | restart condition |
|---|---|---|---|
| deployment `failure` / `cancelled` / 長時間`unknown` | `Halted`、再実行前に原因を分類 | workflow/deployment URL、log、対象SHA | 原因と再試行範囲が承認済み |
| SHA/version/marker不一致 | trafficや追加rolloutを停止 | expected/actual marker、HTTP response | 正しいartifactをdeployして再確認済み |
| 代表route異常 | 影響範囲を記録してrollback判断 | route、status、response marker | rootと代表routeが正常 |
| metricがthreshold超過 | 観測windowを保存してrollback | baseline、threshold、actual、window | rollbackまたは修正後のwindowが正常 |

rollbackは履歴改変ではなく、revert PR等の新しいmain commitを既定とする。source-built Pagesで過去workflowをrerunすると、original runのSHA/refで再実行され、mainと公開物が乖離し得る。そのためhistorical rerunを既定rollbackにしない。restartは、原因、是正、再検証、明示的な再開判断が揃った場合だけ行う。

## Deployment Scenario Walkthrough

### Success
PRのreviewが完了し、production-ready recordを作る。merge後、対象SHAのdeploymentがsuccessで、root/代表routeがHTTP 200、semantic markerが一致し、metricがthreshold内である。Delivery Ownerがowner/timestamp付き証跡を残して `Production Confirmed` とする。

### Deployment Failure or Unknown
deploymentがfailureまたは定義したtimeout後もunknownなら `Halted` とする。CI greenやmerge済みだけを理由に完了させない。run/deployment URL、失敗stage、対象SHA、影響を保存し、原因と再試行範囲を承認してから新しいrunを開始する。

### Marker or Metric Regression and Rollback
deployment自体がsuccessでもmarker不一致またはmetric逸脱なら `Rollback in Progress` とする。revert PRをreview/mergeし、新しいmain SHAのdeploymentを実行する。rollback後も同じHTTP、marker、metric確認を行う。根本原因、是正、再検証、再開判断が揃うまで次のrolloutを開始しない。

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
5. productionへ影響する場合はproduction-ready planを確認してmerge/deployする
6. 対象SHAのproduction evidenceを確認し、metricsとlearningsを記録する
7. 週次で entropy cleanup を行う

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
