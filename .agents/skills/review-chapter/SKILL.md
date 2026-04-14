---
name: review-chapter
description: Use when reviewing a chapter for redundancy, terminology drift, artifact consistency, and brief alignment before finalization.
---

# Review Chapter

## Purpose
章本文の冗長性、用語揺れ、artifact 参照の整合性をレビューする。

## Use When
- 完成稿前に章の重複と表記 drift を詰めたいとき
- artifact と prose の対応を確認したいとき

## Read First
- `AGENTS.md`
- `manuscript/AGENTS.md`
- 対象 chapter brief
- issue body
- 章本文と referenced artifacts

## Checks
- glossary と表記が一致するか
- 前後章と重複しすぎていないか
- 参照 artifact が存在するか
- `AGENTS.md` が定義する不変条件と矛盾しないか
- `SKILL.md` が repeatable workflow にとどまり、repo 固有知識を抱え込みすぎていないか
- context pack や MCP-connected capability を source of truth と誤認していないか
- small heading と exercises が brief に沿っているか
- 局所的な example が本文主張と一致するか

## Output Contract
- 修正が必要な箇所
- 局所 edit で済むか、artifact 更新が必要か
- verify の要否

## Guardrails
- review 結果を issue body / brief / AGENTS より強い source of truth にしない
- 外部 tool の取得結果だけで repo artifact の正否を確定しない
