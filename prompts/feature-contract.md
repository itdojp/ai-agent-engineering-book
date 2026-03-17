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

## Forbidden Actions
- acceptance criteria にない機能追加をしない
- 曖昧な要件を推測で確定しない
- verify に必要な test や docs 更新を後回しにしない
- 既存挙動を壊す変更を無検証で入れない

## Missing Information Policy
- 必須 input が足りない場合は、不足情報を列挙して停止する
- 仮定を置いて進める場合は、その仮定を `Open Questions` に残す

## Completion Criteria
- acceptance criteria を満たす
- 主要 happy path と主要 edge case の test がある
- 変更した artifact を code / docs / tests 単位で説明できる
- 指定 verify が通る
- 未解決事項があれば明記し、なければ `none` と書ける

## Output Format
1. Implemented Scope
2. Files Changed
3. Verification
4. Open Questions
