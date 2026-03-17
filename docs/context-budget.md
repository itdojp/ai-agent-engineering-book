# Context Budget

Context budget は、AI agent に読ませる情報量の上限ではなく、何を原文で保持し、何を要約し、何を捨てるかの設計方針である。

## Budgeting Policy

- root instructions は repo 全体の不変条件だけを書く
- local instructions は対象ディレクトリに閉じた detail だけを書く
- repo map は参照起点と hot path に限定する
- task brief は Goal、Constraints、Acceptance Criteria、Verification を優先する
- progress note は前回の決定、未解決点、再開手順だけを残す

## Keep Verbatim

- acceptance criteria
- API / interface 契約
- verify command
- 破壊的変更の制約
- decision record の結論

## Summarize

- 長い探索ログ
- 試行錯誤の履歴
- 比較検討の過程
- 既に閉じた open question

## Drop

- 同じ意味の重複メモ
- 失効した仮説
- 古い test 出力全文
- 未採用案の細部

## FEATURE-001 Example

`sample-repo` の `FEATURE-001` では、次のように budget を切る。

- 原文で残す: `docs/acceptance-criteria/ticket-search.md`, `docs/design-docs/ticket-search-adr.md` の Decision, verify command
- 要約で残す: ranking を非目標にした理由、検索 abstraction を採用しなかった比較
- 捨てる: 途中で試した query 例の長い列挙、古い失敗ログ全文

budget を切らないと、重要な制約より古いログの方が目立ち、AI agent が stale context に引きずられる。
