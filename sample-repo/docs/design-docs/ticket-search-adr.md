# ADR: Ticket Search

## Status
accepted

## Context
`FEATURE-001` の要求は「検索を使いやすくしたい」という曖昧な依頼から始まった。
この要求を `sample-repo` で扱うにあたり、次の前提がある。

- repo は例示用であり、外部依存は極力増やさない
- 主要な学習対象は要件整理、artifact 設計、tests の接続である
- 既存の service layer を入口とする構成は維持したい
- 検索対象は `title`、`description`、`tags` に限定する

## Options Considered
### Option A: `service.py` で in-memory の部分一致検索を行う
- 長所:
  - 既存 architecture にそのまま乗る
  - unit test を小さく保てる
  - Chapter 3 の主題である spec / ADR / acceptance criteria に集中できる
- 短所:
  - ranking や typo correction は扱えない
  - データ件数が増えると伸びしろが小さい

### Option B: 検索専用 abstraction を追加して将来の外部検索エンジンに備える
- 長所:
  - 将来の拡張余地を先に作れる
  - ranking や indexing の議論に進みやすい
- 短所:
  - 現時点の repo 規模に対して設計が重い
  - Chapter 3 の範囲を超えて infrastructure の話に寄りやすい

## Decision
初期実装は Option A を採用し、`service.py` で `title`、`description`、`tags` を対象にした in-memory の部分一致検索を行う。
空文字または空白のみの query は全件を返す。

## Decision Drivers
- 曖昧要求を実装準備可能な artifact に落とすことが主目的である
- `sample-repo` の現在規模では外部依存や新 abstraction は過剰である
- tests と docs を同期させやすい
- 非目標を明示しやすい

## Consequences
- 実装と verify は小さく保てる
- ranking、typo correction、検索専用 index は扱わない
- 将来、検索要件が増えた場合は新しい ADR を追加して設計を見直す

## Review Trigger
- 検索対象フィールドが増える
- ranking や typo correction が要求される
- 外部検索エンジンの導入がスコープに入る
