# Feature Prompt Contract

仕様に沿って新機能を追加し、変更理由と verify を残すための Prompt Contract。

## Objective
定義済みの仕様と acceptance criteria に沿って、対象機能を実装し、必要な artifact を更新する。

## Inputs
- product spec
- acceptance criteria
- relevant architecture docs
- 対象 issue または task brief
- 関連コードと既存 test
- 実行すべき verify コマンド

## Constraints
- 仕様外の UI / API 変更をしない
- 既存 naming / style / public contract に従う
- docs と tests を同時に更新する
- 対象 issue のスコープから外れる変更を混ぜない

## Tool Contract
- 許可された verify / build / test コマンドだけを実行する
- 明示されていない外部接続、依存追加、secret 利用は行わない
- 書き込み対象は task scope に含まれる code / docs / tests / artifact に限定する

## Approval Gate
- 依存追加、破壊的変更、secret 利用、外部課金 API 呼び出し、権限拡張は human approval を待つ
- approval 待ちに入った場合は、未実行のまま判断材料を返す

## Forbidden Actions
- acceptance criteria にない機能追加をしない
- 曖昧な要件を推測で確定しない
- verify に必要な test や docs 更新を後回しにしない
- 既存挙動を壊す変更を無検証で入れない

## Missing Information Policy
- 必須 input が足りない場合は、不足情報を列挙して停止する
- 仮定を置いて進める場合は、その仮定を `Remaining Gaps` に残す

## Refusal / Stop Conditions
- 必須 input が足りず、低リスクの仮定も置けない場合は停止する
- approval 必須操作が含まれる場合は、承認なしに続行しない
- source of truth が競合する場合は、競合箇所を列挙して停止する

## Completion Criteria
- acceptance criteria を満たす
- 主要 happy path と主要 edge case の test がある
- 変更した artifact を code / docs / tests 単位で説明できる
- 指定 verify が通る
- 未解決事項があれば明記し、なければ `none` と書ける

## Output Schema
- output_version: `2026-04-01`
- required_sections:
  - Implemented Scope
  - Changed Files
  - Verification
  - Remaining Gaps

## Output Format
1. Implemented Scope
2. Changed Files
3. Verification
4. Remaining Gaps
