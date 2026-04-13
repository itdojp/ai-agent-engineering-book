# Context Model

Context Engineering では、AI agent に見せる情報を「何でも渡す」のではなく、役割と鮮度で分ける。Prompt Contract が作業境界を決めるのに対し、context は判断材料を決める。context window が長くても、この分解は不要にならない。

## Context Surface

実務上の context surface は 1 つではない。AI agent は次のような面から判断材料を受け取る。

- instructions: `AGENTS.md`、repo policy、skill guardrail
- docs / task artifact: brief、spec、ADR、acceptance criteria
- session memory: `Progress Note`、open questions、next step
- tool output: test、lint、verify、search 結果
- external data: official docs、runtime status、issue tracker
- persisted note: 再開用に残した要点メモ

重要なのは、surface を増やすことではなく、どの surface が canonical で、どれが live evidence かを混ぜないことである。

## Categories

| 種類 | 主責務 | 代表 artifact | 典型的な扱い | Cache / Refresh の考え方 |
|---|---|---|---|---|
| 永続コンテキスト | repo の不変条件を伝える | `AGENTS.md`, architecture doc, glossary, coding standards | persistent artifact として repo に残す | 比較的 stable。作業開始時に読み、対応ファイルが変わったときだけ refresh する |
| タスクコンテキスト | 今回の issue の scope と done を固定する | issue, task brief, product spec, ADR, acceptance criteria | 原文保持または compact して参照する | issue 単位で更新。source artifact が変われば必ず refresh する |
| セッションコンテキスト | 中断と再開を可能にする | `Progress Note`, open questions, next step, latest verify summary | session summary として短く残す | 劣化しやすい。session ごとに更新し、古い verify は参照し続けない |
| ツールコンテキスト | 直近の根拠を示す | grep 結果, test 出力, verify log, screenshot | live tool output として扱う | live。長く保持するより再取得を優先し、必要なら evidence に分離する |

## Responsibility Split

- persistent artifact
  - repo をまたいで残す source of truth。`AGENTS.md`、spec、glossary のように、意味が安定しているものを置く。
- session summary
  - 再開時に必要な最小情報。`Decided`、`Open Questions`、`Next Step` のように、前回の判断と次の 1 手を短く残す。
- live tool output
  - 現時点の挙動や探索結果。grep、test 出力、verify log は refresh 前提で扱い、常駐させすぎない。

## Rules
1. prompt 自体を context の代わりにしない。
2. 不変情報は persistent artifact に置き、毎回貼り直さない。
3. issue 固有の判断は task brief に寄せる。
4. セッションを跨いで必要な事実だけを session summary に昇格させる。
5. ログ全文や探索履歴は live tool output として扱い、必要なら evidence に分離する。
6. cache できる stable context と refresh が必要な live context を同じ重みで扱わない。
7. secret、credential、個人情報は context pack や `Progress Note` に値そのものを残さない。
8. external data は URL や version を task context に残し、時点依存の応答そのものは live context として扱う。

## Stale と Live の見分け方

- `sample-repo/docs/architecture.md` や `sample-repo/docs/coding-standards.md` は stale-safe な永続コンテキストである。作業開始時に読めばよい。
- `sample-repo/tasks/FEATURE-001-brief.md` は issue 単位で固定したタスクコンテキストである。今回の作業範囲を示す。
- `sample-repo/tasks/FEATURE-001-progress.md` はセッションコンテキストであり、作業が進むたびに更新が必要である。
- `python -m unittest discover -s tests -v` の出力は live context であり、要点だけを `Progress Note` に残し、必要なら再実行する。

## Resume / Refresh Rule

再開時は次の順で context を復元する。

1. 永続コンテキストを読む
2. task brief と acceptance criteria を読む
3. `Progress Note` を読む
4. verify や status command を再実行して live context を取り直す

`Progress Note` だけで再開しない。summary は再開の起点であり、source of truth の置き換えではない。

## Secret / Persist Boundary

- secret は値ではなく、環境変数名、vault 名、参照手順だけを残す
- token、cookie、個人情報を raw log のまま `Progress Note` に転記しない
- screenshot や verify log に secret が含まれる場合は redact する
- 再開に必要なのは「どこで読むか」と「何を再実行するか」であり、credential そのものではない

## Ticket Search Example

`FEATURE-001` で検索挙動を確認するとき、AI agent に見せるべき最小構成は次の通りである。

- 永続: `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`
- タスク: `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/acceptance-criteria/ticket-search.md`
- セッション: `sample-repo/tasks/FEATURE-001-progress.md`
- ツール: `sample-repo/tests/test_ticket_search.py` の失敗内容、最新の verify 出力

この分離がないと、検索仕様、前回の推測、古い test 出力が同じ重みで混ざり、context poisoning を起こしやすい。長い context window は輸送量を増やすが、stable と live の境界は設計し続ける必要がある。前回の verify 結果だけを信じて再実行しないと、resume drift も起こりやすい。
