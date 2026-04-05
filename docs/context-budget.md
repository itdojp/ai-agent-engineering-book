# Context Budget

Context budget は、AI agent に読ませる情報量の上限ではなく、何を原文で保持し、何を要約し、何を捨てるかの設計方針である。
実務ではこれに加えて、何を persist し、何を再取得前提にするかも決める。

## Budgeting Policy

- root instructions は repo 全体の不変条件だけを書く
- local instructions は対象ディレクトリに閉じた detail だけを書く
- repo map は参照起点と hot path に限定する
- task brief は Goal、Constraints、Acceptance Criteria、Verification を優先する
- `Progress Note` は前回の決定、未解決点、再開手順だけを残す

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

## Persist

- task brief の Goal、Constraints、Acceptance Criteria、Verification
- `Progress Note` の `Decided`, `Open Questions`, `Next Step`
- evidence の保存場所
- 再開に必要な command 名、対象ファイル、未完了タスク

## Never Persist As Plain Text

- secret 値、token、cookie、個人情報
- 一時的な本番データの生ログ
- 再実行で得られる terminal 出力全文
- 未検証の推測を事実のように書いた summary

## Refresh Triggers

次の条件では summary を信じる前に live context を取り直す。

- 再開までに時間が空いた
- 依存や branch 先頭が動いた
- verify 結果が session を跨いだ
- approval pending のまま保留した
- external data を根拠にしていた

## FEATURE-001 Example

`sample-repo` の `FEATURE-001` では、次のように budget を切る。

- 原文で残す: `sample-repo/docs/acceptance-criteria/ticket-search.md`, `sample-repo/docs/design-docs/ticket-search-adr.md` の Decision, verify command
- 要約で残す: ranking を非目標にした理由、検索 abstraction を採用しなかった比較
- 捨てる: 途中で試した query 例の長い列挙、古い失敗ログ全文
- persist する: `sample-repo/tasks/FEATURE-001-progress.md` の `Decided`, `Open Questions`, `Next Step`
- persist しない: shell history の全文、secret を含む環境変数 dump、古い verify log の本文

budget を切らないと、重要な制約より古いログの方が目立ち、AI agent が stale context に引きずられる。さらに、persist すべきでない情報まで残ると、resume drift や secret leakage も起こしやすくなる。
