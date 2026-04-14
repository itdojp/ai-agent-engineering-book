---
id: ch05
title: Context Engineering の基礎
status: draft
artifacts:
  - docs/context-model.md
  - docs/context-budget.md
  - docs/context-risk-register.md
dependencies:
  - ch01
  - ch02
  - ch03
  - ch04

---

# Context Engineering の基礎

## この章の位置づけ
良い Prompt Contract と eval が揃っていても、古い spec や関係ないログを読ませれば AI agent は外す。CH01-CH04 で、本書は Prompt Engineering を使って single-task reliability を上げるところまで進んだ。だが、それだけでは作業は完了しない。ここから扱う Context Engineering は、prompt を強くする話ではなく、AI agent に何を見せ、何を残し、何を捨てるかを設計する話である。

ここで誤解しやすいのは、context window が長くなれば Context Engineering が不要になるという見方だ。window が広いほど一度に運べる量は増えるが、何を stable artifact として保持し、何を要約・圧縮し、何を再取得前提にするかという設計は残る。長い window は輸送量を増やすが、source of truth、鮮度、責務の設計を代替しない。

2026 年時点の runtime には、prompt caching や server-side compaction / context editing のように context economics を改善する mechanism もある。だが、これらは「何を読むべきか」「何を fresh とみなすか」「何を repo artifact として同期すべきか」を自動で決めてはくれない。本章では、そうした mechanism を vendor 機能の列挙としてではなく、Context Engineering の補助線として位置付ける。

この章では、Prompt Engineering と Context Engineering の境界を明確にし、永続・タスク・セッション・ツールという 4 種類の context を導入する。以後の章では、この基礎の上に repo context、task context、session memory、skill、context pack を積み上げていく。

## 学習目標
- prompt と context の違いを説明できる
- context budget を設計できる
- stale context と live context を分離できる

## 小見出し
### 1. prompt と context の違い
Prompt Contract は、AI agent に「何をするか」「何をしてはいけないか」「何をもって完了とするか」を伝える。CH02 の `prompts/feature-contract.md` や CH04 の eval は、この契約が安定しているかを見ていた。だが契約だけでは、AI agent は repo の現在地を知らない。どの docs が正なのか、どの test が回帰 guard なのか、どの判断が前回確定しているのかは、prompt の外にある。

ここで必要になるのが Context Engineering である。context は、AI agent が契約を実行するための判断材料であり、Prompt Contract の補足ではない。対象になるのは、instructions、repo docs、task artifact、session memory、tool output、external data、persisted note のような「判断に使う材料」全体である。たとえば `FEATURE-001` の Objective が「検索機能を仕様に沿って改善する」でも、`sample-repo/docs/product-specs/ticket-search.md`、`sample-repo/docs/acceptance-criteria/ticket-search.md`、`sample-repo/tests/test_ticket_search.py` を見せなければ、何を仕様とみなすかが曖昧なままになる。

逆に、context だけ厚くして prompt を弱くしても問題は解決しない。大量の docs と test を渡しても、Objective と Completion Criteria がなければ AI agent は止まりどころを失う。Prompt Engineering と Context Engineering は競合ではなく分業である。前者は作業境界を決め、後者は判断材料の優先順位と鮮度を決める。

### 2. 永続・タスク・セッション・ツールコンテキスト
`docs/context-model.md` では、context を 4 種類に分けている。この分類の目的は、情報量を整理することよりも、更新責任と鮮度を分けることにある。

- 永続コンテキスト: `AGENTS.md`、architecture doc、glossary、coding standards のような repo の不変条件
- タスクコンテキスト: issue、task brief、product spec、ADR、acceptance criteria のような issue 固有の判断
- セッションコンテキスト: `Progress Note`、open questions、次の 1 手のような中断と再開のための記録
- ツールコンテキスト: grep 結果、test 出力、verify log のような live な根拠

この 4 分類を artifact に写すと、永続コンテキストは persistent artifact、セッションコンテキストは session summary、ツールコンテキストは live tool output と対応づけやすい。persistent artifact の責務は source of truth を repo に残すこと、session summary の責務は再開時に読む最小情報を残すこと、live tool output の責務はその時点の挙動を示すことである。責務が違うので、同じ window に入る情報でも同じ扱いにしない。

`sample-repo` の `FEATURE-001` を例にすると、`sample-repo/docs/architecture.md` は永続コンテキスト、`sample-repo/tasks/FEATURE-001-brief.md` はタスクコンテキスト、`sample-repo/tasks/FEATURE-001-progress.md` はセッションコンテキスト、`python -m unittest discover -s tests -v` の結果はツールコンテキストになる。これらを同じメモ欄に詰め込むと、古い判断と live な失敗ログの区別が消える。

重要なのは、更新速度が違うことだ。architecture doc は毎回変わらないので cache しやすい。一方、`Progress Note` は session ごとに更新が必要であり、verify 結果や grep 結果は数分で無効になる。Context Engineering は、情報の種類ごとに寿命を定義し、AI agent に同じ重みで渡さないようにする。

### 3. context budget の考え方
Context budget は、token 上限の話だけではない。何を原文で残し、何を要約し、何を compact し、何を再取得し、何を persistent artifact に昇格させるかを決める設計方針である。`docs/context-budget.md` では、少なくとも keep verbatim、summarize、compact、re-fetch、persist の 5 操作を使い分ける。

なぜ原文と要約を分けるのか。原文で残すべきものは、後から意味が変わると危険な契約である。`sample-repo/docs/acceptance-criteria/ticket-search.md` の「空文字または空白のみの query は全件を返す」は、要約するとぶれやすい。一方、「ranking を今回の Non-goals にした理由」は、決定自体さえ残っていれば理由の細部は要約で足りる。

compact と summarize も違う。summarize は文章量を減らす操作であり、compact は表や箇条書きへ変換して検索しやすくする操作である。さらに re-fetch を選ぶと、「保持しない代わりに再取得できる」前提を明示できる。長い context window が使えても、live tool output を常駐させるより、再実行で最新化した方が安全な場面は多い。

ここで modern runtime mechanism との境界も明確にしておく。prompt caching は、stable な prefix や繰り返し読む artifact を毎回フル転送しなくて済むようにし、主に cost / latency economics を改善する。だが cache hit は correctness や freshness を保証しない。cached だから source of truth として正しいわけではないし、外部状態や verify 状態の再取得も不要にならない。

server-side compaction / context editing は別の役割を持つ。runtime が古い turn を要約したり、不要な context を server-side で薄くしたりできれば、context pressure は下がる。だが、それは `compact` を runtime 側で補助する mechanism にすぎない。compaction しても、何を re-fetch すべきか、何を redact すべきか、どの artifact を同期すべきかという policy は repo / team 側に残る。つまり、prompt caching は keep / persist を安くする補助であり、compaction / context editing は compact を支える補助であって、どちらも re-fetch、redaction、artifact sync の代替ではない。

persist の観点も同じである。`sample-repo/tasks/FEATURE-001-progress.md` に残してよいのは、verify 済みの決定、未解決点、再開の 1 手である。secret 値そのもの、個人情報を含む raw log、再現可能な terminal 出力全文は、`Progress Note` や context pack に常駐させない方がよい。必要なら secret 名や evidence の保存場所だけを残し、値や全文は別管理にする。

### 4. stale context と live context
stale context と live context を分けないと、AI agent は「昨日は正しかったが今は違う」情報を根拠に使う。`docs/context-model.md` が `sample-repo/docs/architecture.md` を stale-safe、verify 出力を live と分けているのはこのためである。

実務上の見分け方は単純である。repo の設計原則や glossary は stale-safe であり、起動時に読めばよい。task brief や acceptance criteria は今回の issue の canonical artifact であり、変更が入ったときだけ refresh する。`Progress Note` は session summary として使うが、verify 結果が変わった時点で古くなる。test failure や terminal log はその瞬間の live context であり、結論だけを session summary に残し、全文は evidence か再取得前提で扱う。

再開時の運用もここに含まれる。resume では、まず stale-safe な root / repo / task artifact に戻り、その後に `Progress Note` を読む。最後に verify や status command を再実行して live context を取り直す。前回セッションの summary だけで再開すると、`Last Verify` や依存状態が既に失効していても気づきにくい。再開手順まで含めて Context Engineering の責務である。

### 5. context poisoning と drift
Context Engineering の失敗は、情報不足だけではない。間違った context が残ることも同じくらい危険である。`docs/context-risk-register.md` では、stable/live confusion、summary drift、instruction bloat、context poisoning、hidden done criteria、tool spam、secret leakage、resume drift を主要リスクとして整理している。

典型例は 4 つある。第一に、docs と tests がずれたまま放置され、古い仕様を正として実装してしまうこと。第二に、`Progress Note` の `Decided` に未検証の推測を書き、次セッションがそれを事実として引き継ぐこと。第三に、長い context window を理由にログ全文を保持し続け、live output を stale なまま信じること。第四に、verify でしか分からない情報を persistent artifact に早すぎる形で昇格させることだ。

対策も構造的に考える。canonical artifact を task brief と acceptance criteria に固定し、`Progress Note` では `Decided` と `Open Questions` を分ける。長いログは evidence として切り離す。secret は値ではなく参照名だけを残す。verify を再実行できるなら、要約を信じる前に live context を取り直す。Context Engineering は「情報を増やす技術」ではなく、「壊れた情報を残さない技術」でもある。

## 章で使う bad / good example
bad:

```text
`FEATURE-001` の作業なので、前回のチャット要約、長い test ログ全文、repo tree 全体、古いメモ、
一時的に確認した credential 断片までまとめて渡す。
prompt には「検索を直して。前回の流れを踏まえて進めて」とだけ書く。
```

このやり方では、Prompt Contract が弱いだけでなく、context の鮮度も重みも区別されない。古いログや未検証の推測が、acceptance criteria と同じ扱いになる。しかも secret や一時的な live output を persisted note と同列に扱うため、漏洩と resume drift まで起こしやすい。

good:

```text
Prompt Contract では Objective、Constraints、Completion Criteria を固定する。
context は次の順に渡す。
1. `sample-repo/docs/repo-map.md`
2. `sample-repo/tasks/FEATURE-001-brief.md`
3. `sample-repo/docs/acceptance-criteria/ticket-search.md`
4. `sample-repo/tasks/FEATURE-001-progress.md`
5. 最新の verify 結果
古いログ全文は残さず、必要な結論だけを `Progress Note` に昇格させる。
secret は値を残さず、環境変数名や参照先だけを記録する。
```

この修正版では、契約と判断材料が分離され、さらに stale-safe な docs と live な verify 結果、persist してよい情報と残してはいけない情報も分けて扱われている。

比較観点:
- bad は prompt と context の役割を混ぜている
- bad は stale context と live context の重みを分けていない
- good は canonical artifact を先に固定し、ログは live evidence として扱っている

## 演習
1. 15 個の情報片を 4 種類の context に分類する。
2. 何を要約し、何を原文で残し、何を persist せず再取得前提にするかポリシーを作る。

## 参照する artifact
- `docs/context-model.md`
- `docs/context-budget.md`
- `docs/context-risk-register.md`

## Source Notes / Further Reading
- この章を探し直すときは、まず `docs/context-model.md`、`docs/context-budget.md`、`docs/context-risk-register.md` を正本として見る。Context Engineering は情報を増やす話ではなく、source of truth、鮮度、保持期間、更新責任を分ける設計である。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH05 Context Engineering の基礎」と `manuscript/backmatter/01-読書案内.md` の「Context と repo 設計」を参照する。

## 章末まとめ
- Prompt Engineering が作業境界を決めるのに対し、Context Engineering は判断材料の種類、鮮度、優先順位を決める。
- context window が長くなっても、keep verbatim、summarize、compact、re-fetch、persist の設計は残る。
- context は永続、タスク、セッション、ツールに分け、さらに persist / refresh の境界を決めると設計しやすい。次章では `AGENTS.md`、`sample-repo/docs/repo-map.md`、`sample-repo/docs/architecture.md` の役割分担を扱う。
