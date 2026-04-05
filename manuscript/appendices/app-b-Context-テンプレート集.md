# Context テンプレート集

Context Engineering の目的は、agent に長い説明文を渡すことではない。task を完了するために必要な情報だけを、役割ごとに分解して渡すことである。この appendix では、CH05 から CH08 で使った context artifact を再利用できる形で整理する。

Prompt Contract が単一タスクの入力と出力を固定するのに対し、context artifact は判断材料を固定する。両者を混ぜると、prompt が肥大化し、`Progress Note` が source of truth を上書きし、context pack が古い要件を運ぶ。そこで task brief、`Progress Note`、context pack、persisted note を別 artifact として持つ。

## 1. Task Brief Template

`templates/task-brief.md` は、issue を coding agent 実行向けに構造化するテンプレートである。CH07 の中心 artifact であり、source of truth にもっとも近い。

主要 section の役割は次のとおりである。

- `Source`: issue や起点 artifact を明示する
- `Goal`: この task が達成すべき結果を固定する
- `Scope`: 今回含める変更だけを書く
- `Inputs`: 読むべき spec、ADR、code、tests、docs を列挙する
- `Deliverables`: 更新対象 artifact を明示する
- `Constraints`: 守るべき public contract や非機能制約を書く
- `Acceptance Criteria`: verify 可能な受け入れ条件に変換する
- `Verification`: 実行すべき command を固定する
- `Open Questions`: 推測で確定できない論点を隔離する
- `Out of Scope`: 今回やらないことを止める
- approval boundary や external data がある場合は、その確認先を artifact 側で明示する

`sample-repo/tasks/FEATURE-001-brief.md` は、この template を task 固有に埋めた実例である。短いが、Goal、Inputs、Acceptance Criteria、Verification が揃っているため、次の session でも同じ task を再現できる。

## 2. Progress Note Template

`templates/progress-note.md` は、中断や handoff のための短い進捗記録である。ここで大切なのは、task brief を書き直さないことだ。`Progress Note` は source of truth ではなく、現在位置を示す補助記録である。

推奨 section は次のとおりである。

- `Status`: 任意。`in-progress`、`blocked`、`ready-for-handoff` のような粗い状態だけを書く
- `Current Goal`: 今回の work package を 1 文で書く
- `Completed`: 完了した作業を列挙する
- `Decided`: session 中に確定した判断を残す
- `Open Questions`: 未解決事項を task brief と分けて残す
- `Last Verify`: 直近の verify command と結果を書く
- `Changed Files`: 追跡すべき差分を残す
- `Resume Steps`: 再開時に最初に読む artifact と確認順を書く
- `Next Step`: 次の 1 手を小さく固定する
- persisted note は verified fact と再開手順だけに絞り、secret や raw log を転記しない

`sample-repo/tasks/FEATURE-001-progress.md` では、verify 結果と再開手順が短くまとまっている。長い作業日誌にしないことが重要である。agent が次に読むべき順序が分かればよい。

## 3. Context Pack Template

`templates/context-pack.md` は、特定タスクに必要な参照情報を集約した読み順 artifact である。CH08 で扱ったとおり、context pack は repo 全体を要約する文書ではない。1 つの task を安全に進めるための最小 read set をまとめる。

基本構成は次のとおりである。

- `Purpose`: どの task に使う context pack かを書く
- `Read Order`: 読む順序を固定する
- `Canonical Facts`: task で覆してはいけない事実を書く
- `Live Checks`: 最新 verify や最新 `Progress Note` など、毎回確認すべき live 情報を書く
- `Exclusions`: 今回扱わない論点を明示する
- `Done Signals`: 終了判定に使う条件を書く
- secret は値ではなく参照名だけを残し、必要なら再取得手順を明示する

`sample-repo/context-packs/ticket-search.md` は、`FEATURE-001` の検索改善に必要な最小 read order を定義している。ここで重要なのは、context pack 自体が仕様を再定義しないことだ。仕様は spec や acceptance criteria にあり、context pack はそれらへ安全に到達するための案内である。

## 4. 運用上の注意

Context artifact を運用するときは、次の優先順位を崩さない。

1. task brief
2. spec / ADR / acceptance criteria / tests
3. `Progress Note`
4. context pack
5. persisted note

`Progress Note` や context pack が task brief より強い source of truth になると、古い判断が残りやすい。persisted note は canonical source ではなく、resume の補助として使う。Context Engineering の実務では、「何を書くか」より「何を書きすぎないか」の方が重要である。

## 参照する artifact

- `templates/task-brief.md`
- `templates/progress-note.md`
- `templates/context-pack.md`
- `sample-repo/tasks/FEATURE-001-brief.md`
- `sample-repo/tasks/FEATURE-001-progress.md`
- `sample-repo/context-packs/ticket-search.md`
