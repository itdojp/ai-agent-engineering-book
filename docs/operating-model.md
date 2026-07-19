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

### Approver
- environment protection 等で必要な deployment 承認を行い、承認記録を残す
- 承認が不要な場合は `N/A` と根拠を記録する
- deployment を開始してよいという control decision と、deployment success / production confirmation を混同しない

### Delivery Owner
- production-ready plan の target、marker、metric、halt / rollback / restart 条件を確定する
- 対象 deployment と production evidence を確認し、`Production Confirmed` または `Halted` を記録する
- rollback と再開の判断、owner、timestamp、evidence location を残す

1 人運用では、同じ人が Lead、Operator、Reviewer、Approver、Delivery Owner を兼任してよい。ただし、review 完了、deployment 承認、production 確認を 1 つのチェックで代替してはならない。各判断の時刻、対象 SHA、根拠を分けて残す。

## Delivery State Model

merge は code review の終了であり、production 成功の証拠ではない。production へ影響する work package は、次の状態を順に通る。

| 状態 | entry condition | owner | 必須 evidence | exit condition |
|---|---|---|---|---|
| `Review Complete` | review body / inline / suggestion を処理し、unresolved thread 0、CI green | Reviewer | review response、thread、CI URL | merge 可否を判断した |
| `Production Ready` | 下記 production-ready plan が埋まり、rollback 可能 | Delivery Owner | target、SHA/version、route/marker、metric、owner、rollback plan | deployment 開始を承認した |
| `Deployment Approved` | 必要な environment 等の保護条件を通過、または適用不要を記録 | Approver | approval/deployment record または `N/A` 理由 | deployment job が開始した |
| `Deployed` | 対象 artifact の deployment job が success | Operator | 対象 SHA の deployment と workflow URL | production smoke を開始した |
| `Superseded` | 対象 run が後続 SHA により `cancelled` となり、後続 SHA が対象 change を含む | Operator | 対象/後続 SHA の包含関係、両 run URL | 後続 deployment で production smoke を開始した |
| `Production Confirmed` | 対象 SHA または適格な後続 SHA で HTTP、semantic marker、代表 route、metric が期待値内 | Delivery Owner | owner/timestamp 付き confirmation record | work package を完了できる |
| `Halted` | deployment が failed/unknown、marker 不一致、route 異常、metric 逸脱 | Delivery Owner | halt 理由、観測値、影響、次の判断 | rollback または是正を決めた |
| `Rollback in Progress` | 承認済み rollback を開始 | Operator | revert PR 等の rollback change、deployment URL | rollback 後の production を再確認した |

`Deployment Approved` は変更を環境へ送ってよいという control decision であり、deployment 成功や production 正常性の証明ではない。`Deployed` も artifact が送られたことだけを示し、`Production Confirmed` までは完了扱いにしない。

## Production-ready Gate

merge 前に PR または linked Issue へ次を記録する。該当しない変更は `N/A` と理由を残す。

- target environment と公開 URL
- merge 後に確定する SHA/version の記録場所と、production で照合する immutable marker。source-built site では build 時に SHA/version を meta tag や `build-revision.txt` へ埋め込み、固定の title や本文だけを marker にしない
- deploy owner、production confirmation owner、承認者（必要な場合）
- root smoke と代表 route、期待する HTTP status / content marker
- metric 名、baseline、許容 threshold、観測 window、取得元
- halt 条件、rollback 手段、restart 条件
- workflow、deployment、HTTP、metric evidence の保存場所

## Post-deploy Confirmation

Delivery Owner は、集約 status や「最新らしい」画面だけでなく、対象 SHA へ紐づく証拠を確認する。

1. 対象 SHA/version の deployment status と workflow run を照合する。対象 run が後続 run により `cancelled` となった場合は、後続 SHA が対象 commit を祖先として含むこと、または対象 change を含むことを確認し、対象/後続の両 SHA と run URL を `Superseded` evidence として残す。
2. target URL の HTTP smoke と、代表 route の HTTP status を確認する。
3. build 時に埋め込んだ SHA/version 等の immutable marker を照合する。固定の title や以前から存在する本文は、stale deployment でも一致するため単独 marker にしない。
4. 事前に定義した metric を観測 window 全体で確認する。
5. owner、UTC timestamp、観測値、evidence URL を linked Issue または PR へ記録する。

repository 全体の集約 status と対象 deployment が食い違う場合は、食い違い自体を記録し、対象 SHA の deployment、workflow、公開 URL/marker を正本として判定する。食い違いを説明できない場合は `Halted` とする。

`cancelled` を自動的に failure または `Superseded` と見なしてはならない。後続 deployment が対象 change を含み、成功し、同じ route/marker/metric 契約を満たした場合だけ、その後続 evidence で元の work package を `Production Confirmed` にできる。後続 SHA が対象 change を含まない、後続 run も失敗した、または包含関係を証明できない場合は `Halted` とする。

## Halt, Rollback, and Restart

| trigger | action | completion を止める evidence | restart condition |
|---|---|---|---|
| deployment `failure` / 長時間 `unknown` / 説明できない `cancelled` | `Halted`、再実行前に原因を分類 | workflow/deployment URL、log、対象 SHA | 原因と再試行範囲が承認済み |
| 後続 SHA による意図的な `cancelled` | 包含関係を確認して `Superseded` | 対象/後続 SHA、両 run URL、commit 包含証拠 | 後続 deployment で route/marker/metric を確認済み |
| SHA/version/marker 不一致 | traffic や追加 rollout を停止 | expected/actual marker、HTTP response | 正しい artifact を deploy して再確認済み |
| 代表 route 異常 | 影響範囲を記録して rollback 判断 | route、status、response marker | root と代表 route が正常 |
| metric が threshold 超過 | 観測 window を保存して rollback | baseline、threshold、actual、window | rollback または修正後の window が正常 |

rollback は履歴改変ではなく、revert PR 等の新しい main commit を既定とする。source-built Pages で過去 workflow を rerun すると、original run の SHA/ref で再実行され、main と公開物が乖離し得る。そのため historical rerun を既定 rollback にしない。restart は、原因、是正、再検証、明示的な再開判断が揃った場合だけ行う。

## Deployment Scenario Walkthrough

### Success
PR の review が完了し、production-ready plan を作る。merge 後、対象 SHA の deployment が success で、root/代表 route が HTTP 200、semantic marker が一致し、metric が threshold 内である。Delivery Owner が owner/timestamp 付き証跡を残して `Production Confirmed` とする。対象 run が後続 SHA により `cancelled` となった場合は、後続 SHA が対象 change を含むことと後続 deployment の同じ確認結果を記録して `Superseded` から `Production Confirmed` へ進める。

### Deployment Failure or Unknown
deployment が failure または定義した timeout 後も unknown なら `Halted` とする。CI green や merge 済みだけを理由に完了させない。run/deployment URL、失敗 stage、対象 SHA、影響を保存し、原因と再試行範囲を承認してから新しい run を開始する。

### Marker or Metric Regression and Rollback
deployment 自体が success でも marker 不一致または metric 逸脱なら `Rollback in Progress` とする。revert PR を review / merge し、新しい main SHA の deployment を実行する。rollback 後も同じ HTTP、marker、metric 確認を行う。根本原因、是正、再検証、再開判断が揃うまで次の rollout を開始しない。

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
5. production へ影響する場合は production-ready plan を確認して merge / deploy する
6. 対象 SHA の production evidence を確認し、metrics と learnings を記録する
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
