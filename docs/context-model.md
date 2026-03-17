# Context Model

Context Engineering では、AI agent に見せる情報を「何でも渡す」のではなく、役割と鮮度で分ける。
Prompt Contract が作業境界を決めるのに対し、context は判断材料を決める。

## Categories

| 種類 | 目的 | 代表 artifact | 鮮度 | 置き場 |
|---|---|---|---|---|
| 永続コンテキスト | repo の不変条件を伝える | `AGENTS.md`, architecture doc, glossary, coding standards | 比較的 stable | `docs/`, root |
| タスクコンテキスト | 今回の issue の scope と done を固定する | issue, task brief, product spec, ADR, acceptance criteria | issue ごとに更新 | `tasks/`, `docs/` |
| セッションコンテキスト | 中断と再開を可能にする | progress note, open questions, next step, latest verify result | もっとも劣化しやすい | `tasks/`, summary |
| ツールコンテキスト | 直近の根拠を示す | grep 結果, test 出力, verify log, screenshot | live | terminal, evidence |

## Rules
1. prompt 自体を context の代わりにしない。
2. 不変情報は docs に置き、毎回貼り直さない。
3. issue 固有の判断は task brief に寄せる。
4. セッションを跨いで必要な事実だけを progress note に昇格させる。
5. ログ全文や探索履歴は live context として扱い、常駐させない。

## Stale と Live の見分け方

- `sample-repo/docs/architecture.md` や `sample-repo/docs/coding-standards.md` は stale-safe な永続コンテキストである。作業開始時に読めばよい。
- `sample-repo/tasks/FEATURE-001-brief.md` は issue 単位で固定したタスクコンテキストである。今回の作業範囲を示す。
- `sample-repo/tasks/FEATURE-001-progress.md` はセッションコンテキストであり、作業が進むたびに更新が必要である。
- `python -m unittest discover -s tests -v` の出力は live context であり、要点だけを progress note に残す。

## Ticket Search Example

`FEATURE-001` で検索挙動を確認するとき、AI agent に見せるべき最小構成は次の通りである。

- 永続: `sample-repo/docs/repo-map.md`, `sample-repo/docs/architecture.md`
- タスク: `sample-repo/tasks/FEATURE-001-brief.md`, `sample-repo/docs/product-specs/ticket-search.md`, `sample-repo/docs/acceptance-criteria/ticket-search.md`
- セッション: `sample-repo/tasks/FEATURE-001-progress.md`
- ツール: `sample-repo/tests/test_ticket_search.py` の失敗内容、最新の verify 出力

この分離がないと、検索仕様、前回の推測、古い test 出力が同じ重みで混ざり、context poisoning を起こしやすい。
