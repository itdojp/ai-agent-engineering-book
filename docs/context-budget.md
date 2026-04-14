# Context Budget

Context budget は、AI agent に読ませる情報量の上限ではなく、何を原文で保持し、何を要約し、何を compact し、何を再取得し、何を persistent artifact に昇格させるかの設計方針である。長い context window は budget を不要にしない。

## Budgeting Policy

- root instructions は repo 全体の不変条件だけを書く
- local instructions は対象ディレクトリに閉じた detail だけを書く
- repo map は参照起点と hot path に限定する
- task brief は Goal、Constraints、Acceptance Criteria、Verification を優先する
- `Progress Note` は前回の決定、未解決点、再開手順だけを残す
- live tool output は再取得可能なら re-fetch を優先する

## Decision Matrix

| 操作 | 目的 | 典型例 | 保存先の考え方 |
|---|---|---|---|
| keep verbatim | 意味変化が危険な契約を守る | acceptance criteria、API / interface 契約、verify command、破壊的変更の制約 | source of truth の artifact をそのまま参照する |
| summarize | 長い経緯を短く残す | 比較検討の過程、閉じた open question、探索の結論 | `Progress Note` や summary へ短く残す |
| compact | 構造を保ったまま圧縮する | 読み順表、ファイル一覧、checkpoint 一覧、risk table | 表や箇条書きに変換し、再検索しやすくする |
| re-fetch | stale になりやすい情報を最新化する | test 出力、grep 結果、外部検索結果、terminal log | chat に保持するより再実行で取り直す |
| persist | 次 session で引き継ぐべき結論を残す | task brief の決定、`Progress Note` の `Next Step`、ADR の結論 | repo artifact に昇格させ、会話履歴依存を避ける |

## Runtime Economics Notes

- prompt caching
  - stable な prefix や繰り返し参照する artifact の転送コストと待ち時間を下げる補助である
  - cache hit は correctness や freshness の保証ではないため、source of truth、verify、external data の refresh 判断は別途必要である
- server-side compaction / context editing
  - 古い turn や低優先度 context を server-side で薄くし、context pressure を下げる補助である
  - runtime 側で `compact` を助けても、`re-fetch`、redaction、artifact sync の policy は消えない

この 2 つは context economics を改善する mechanism だが、keep verbatim / summarize / compact / re-fetch / persist の設計を置き換えない。長い context window と同様に、輸送量や常駐量を楽にしても source-of-truth 設計そのものは残る。

## Keep Verbatim

- acceptance criteria
- API / interface 契約
- verify command
- 破壊的変更の制約
- decision record の結論

## Summarize Or Compact

- 長い探索ログ
- 試行錯誤の履歴
- 比較検討の過程
- 既に閉じた open question
- 参照ファイルの読み順
- checkpoint と ownership の一覧

## Re-fetch

- 古い test 出力全文
- grep や search の transient な結果
- tool 実行の stderr / stdout 全文
- stale になりやすい live status

## Persist

- task brief の Goal、Constraints、Acceptance Criteria、Verification
- `Progress Note` の `Decided`、`Open Questions`、`Next Step`
- review や verify で確定した結論
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
- prompt caching や compaction が効いていても、freshness を runtime に委ねられない

## Drop

- 同じ意味の重複メモ
- 失効した仮説
- 未採用案の細部
- 既に evidence に切り出したログ全文

## FEATURE-001 Example

`sample-repo` の `FEATURE-001` では、次のように budget を切る。

- 原文で残す: `sample-repo/docs/acceptance-criteria/ticket-search.md`, `sample-repo/docs/design-docs/ticket-search-adr.md` の Decision, verify command
- 要約で残す: ranking を非目標にした理由、検索 abstraction を採用しなかった比較
- compact する: 読むべき artifact の順序、確認すべき checkpoint
- 再取得する: `python -m unittest discover -s tests -v` の最新結果、grep 結果
- persistent artifact に昇格する: `Next Step`、検証済みの決定、reviewer 向け evidence 参照
- persist する: `sample-repo/tasks/FEATURE-001-progress.md` の `Decided`, `Open Questions`, `Next Step`
- persist しない: shell history の全文、secret を含む環境変数 dump、古い verify log の本文
- 捨てる: 途中で試した query 例の長い列挙、古い失敗ログ全文

budget を切らないと、重要な制約より古いログの方が目立ち、AI agent が stale context に引きずられる。さらに、persist すべきでない情報まで残ると、resume drift や secret leakage も起こしやすくなる。
