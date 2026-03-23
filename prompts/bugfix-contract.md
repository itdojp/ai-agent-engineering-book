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

## Forbidden Actions
- 根拠なく仕様を拡張しない
- failing test を削除して green にしない
- 無関係なリファクタリングや rename をしない
- verify を省略して完了扱いにしない

## Missing Information Policy
- 必須 input が足りない場合は、不足情報を列挙して停止する
- 低リスクの仮定を置く場合は、その仮定を最終報告に明記する

## Completion Criteria
- 対象不具合の再現条件と根本原因を説明できる
- 修正前は失敗し、修正後は成功する test がある
- 既存 test と指定 verify が通る
- 変更した code / docs / tests を列挙できる
- `Remaining Gaps` フィールドに、未解決の gap があれば明記し、なければ `none` と書ける

## Output Format
1. Root Cause
2. Changed Files
3. Verification
4. Remaining Gaps
