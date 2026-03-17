# Draft Chapter

## Purpose
章本文を標準構成で作成または更新する。

## Use When
- chapter brief を publishable draft に変換するとき
- artifact が先にあり、その内容に沿って本文を固めるとき

## Required Inputs
- issue body
- chapter brief
- relevant AGENTS
- already written neighboring chapters
- referenced artifacts

## Workflow
1. brief から Goal / Reader Outcome / Sections / Exercises / Artifacts を読む
2. 章本文の front matter と導入を作る
3. 各小見出しで「何を説明するか」「どの artifact を参照するか」を明確にする
4. bad / good example を最低 1 組入れる
5. 演習を 2 問入れる
6. referenced artifacts がなければ skeleton を作り、drift があれば更新する
7. verify を実行する

## Output Contract
- 章本文
- 変更した artifact
- verify 結果
- verify 失敗時のみ残課題

## Guardrails
- 章本文に `TODO`、`TBA`、メモ書きを残さない
- 未来の章の詳細説明を先取りしない
- artifact が存在しない場合は本文だけで済ませず repo 上に追加する
