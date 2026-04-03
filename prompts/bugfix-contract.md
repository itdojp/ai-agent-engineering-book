# Bugfix Prompt Contract

既存挙動を壊さずに、対象不具合を再現・修正・検証するための Prompt Contract。

## Objective
既存仕様を保ったまま、対象不具合の根本原因を特定し、最小差分で修正する。

## Inputs
- 対象 issue または task brief
- 再現手順
- 期待挙動と実際挙動
- 関連ファイル、関連 test、関連 docs
- 実行すべき verify コマンド
- 既知の制約または非対象範囲

## Constraints
- 既存 public interface を変更しない
- failing test を先に追加または更新する
- 変更差分は対象不具合の修正に必要な最小範囲に留める
- 挙動変更がある場合は関連 docs も更新する

## Tool Contract
- 許可された verify / build / test コマンドだけを実行する
- 明示されていない外部接続、依存追加、secret 利用は行わない
- 書き込み対象は task scope に含まれる code / docs / tests / artifact に限定する

## Approval Gate
- 依存追加、破壊的変更、secret 利用、外部課金 API 呼び出し、権限拡張は human approval を待つ
- approval 待ちに入った場合は、未実行のまま判断材料を返す

## Forbidden Actions
- 根拠なく仕様を拡張しない
- failing test を削除して green にしない
- 無関係なリファクタリングや rename をしない
- verify を省略して完了扱いにしない

## Missing Information Policy
- 必須 input が足りない場合は、不足情報を列挙する
- 低リスクの仮定を置いて進める場合は、その仮定を `Remaining Gaps` に残す

## Refusal / Stop Conditions
- 必須 input が足りず、低リスクの仮定も置けない場合は停止する
- approval 必須操作が含まれる場合は、承認なしに続行しない
- source of truth が競合する場合は、競合箇所を列挙して停止する

## Completion Criteria
- 対象不具合の再現条件と根本原因を説明できる
- 修正前は失敗し、修正後は成功する test がある
- 既存 test と指定 verify が通る
- 変更した code / docs / tests を列挙できる
- `Remaining Gaps` フィールドに、未解決の gap があれば明記し、なければ `none` と書ける

## Output Schema
- output_version: `2026-04-01`
- required_sections:
  - Root Cause
  - Changed Files
  - Verification
  - Remaining Gaps

## Output Format
1. output_version
2. Root Cause
3. Changed Files
4. Verification
5. Remaining Gaps
