---
name: draft-chapter
description: Use when drafting or revising a chapter from a chapter brief, issue body, neighboring chapters, and referenced artifacts.
---

# Draft Chapter

## Purpose
章本文を標準構成で作成または更新する。

## Use When
- chapter brief を publishable draft に変換するとき
- artifact が先にあり、その内容に沿って本文を固めるとき

## Read First
- `AGENTS.md`
- `manuscript/AGENTS.md`
- 対象 chapter brief
- issue body
- referenced artifacts

## Workflow
1. brief から Goal / Reader Outcome / Sections / Exercises / Artifacts を読む
2. `AGENTS.md` で repo 全体の不変条件、`manuscript/AGENTS.md` で章構成と文体ルールを確認する
3. 章本文の front matter と導入を作る
4. 各小見出しで「何を説明するか」「どの artifact を参照するか」を明確にする
5. bad / good example を最低 1 組入れる
6. 演習を 2 問入れる
7. referenced artifacts がなければ skeleton を作り、drift があれば更新する
8. verify を実行する

## Output Contract
- 章本文
- 変更した artifact
- verify 結果
- verify 失敗時のみ残課題

## Guardrails
- `AGENTS.md` が定義する repo 不変条件をこの file に再定義しない
- skill は repeatable workflow を定義し、repo 固有の source of truth は brief / docs / artifact を参照する
- MCP や外部 tool は補助的に使えても、issue body + brief + AGENTS + artifact を置き換えない
- 章本文に `TODO`、`TBA`、メモ書きを残さない
- 未来の章の詳細説明を先取りしない
- artifact が存在しない場合は本文だけで済ませず repo 上に追加する
