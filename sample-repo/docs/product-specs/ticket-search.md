# Product Spec: Ticket Search

## Status
implementation-ready draft for `FEATURE-001`

## Source Request
「検索を使いやすくしたい」

## Problem
サポート担当者がチケットを探すとき、どの情報が `title`、`description`、`tags` に入っているかを意識しないと検索しづらい。
まずは小さな `sample-repo` の範囲で、単一 query による基本検索を定義し、後続の設計判断と test 追加に使える artifact を作る。

## Objective
サポート担当者が単一の query で候補チケットを絞り込み、詳細確認に進めるようにする。

## Users
- サポート担当者
- 問い合わせ triage を行う開発担当者

## In Scope
- `title` を対象にした部分一致検索
- `description` を対象にした部分一致検索
- `tags` を対象にした部分一致検索
- 大文字小文字を区別しない検索
- 空文字または空白のみの query を入力したときは全件を返す

## Non-goals
- relevance ranking
- typo correction
- 外部検索エンジンの導入
- UI の全面 redesign
- `list_tickets` の既存 filter API の意味変更

## User Scenarios
1. 担当者は `search` で検索し、タイトルに一致するチケット候補を見つけられる。
2. 担当者は `ownership` で検索し、説明文に含まれるチケット候補を見つけられる。
3. 担当者は `ui` で検索し、タグに一致するチケット候補を見つけられる。
4. 担当者は query を空にして一覧全体へ戻れる。

## Requirements
- Query は `title`、`description`、`tags` のいずれかに部分一致したチケットを返す。
- Query の前後空白は無視する。
- Query が空文字または空白のみなら全件を返す。
- 本仕様は検索挙動の定義に集中し、既存の status / assignee filter の挙動は変更しない。

## Open Questions
- none
