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
CH01-CH04 で、本書は Prompt Engineering を使って single-task reliability を上げるところまで進んだ。だが、良い Prompt Contract と eval があっても、AI agent が読む情報が古い、足りない、重すぎる、混ざっている、のいずれかなら作業は完了しない。ここから扱う Context Engineering は、prompt を強くする話ではなく、AI agent に何を見せ、何を残し、何を捨てるかを設計する話である。

この章では、Prompt Engineering と Context Engineering の境界を明確にし、永続・タスク・セッション・ツールという 4 種類の context を導入する。以後の章では、この基礎の上に repo context、task context、session memory、skill、context pack を積み上げていく。

## 学習目標
- prompt と context の違いを説明できる
- context budget を設計できる
- stale context と live context を分離できる


## 小見出し
### 1. prompt と context の違い
Prompt Contract は、AI agent に「何をするか」「何をしてはいけないか」「何をもって完了とするか」を伝える。CH02 の `prompts/feature-contract.md` や CH04 の eval は、この契約が安定しているかを見ていた。だが契約だけでは、AI agent は repo の現在地を知らない。どの docs が正なのか、どの test が回帰 guard なのか、どの判断が前回確定しているのかは、prompt の外にある。

ここで必要になるのが Context Engineering である。context は、AI agent が契約を実行するための判断材料であり、Prompt Contract の補足ではない。たとえば `FEATURE-001` の Objective が「検索機能を仕様に沿って改善する」でも、`sample-repo/docs/product-specs/ticket-search.md`、`sample-repo/docs/acceptance-criteria/ticket-search.md`、`sample-repo/tests/test_ticket_search.py` を見せなければ、何を仕様とみなすかが曖昧なままになる。

逆に、context だけ厚くして prompt を弱くしても問題は解決しない。大量の docs と test を渡しても、Objective と Completion Criteria がなければ AI agent は止まりどころを失う。Prompt Engineering と Context Engineering は競合ではなく分業である。前者は作業境界、後者は判断材料を定義する。

### 2. 永続・タスク・セッション・ツールコンテキスト
`docs/context-model.md` では、context を 4 種類に分けている。この分類の目的は、情報量を整理することよりも、更新責任と鮮度を分けることにある。

- 永続コンテキスト: `AGENTS.md`、architecture doc、glossary、coding standards のような repo の不変条件
- タスクコンテキスト: issue、task brief、product spec、ADR、acceptance criteria のような issue 固有の判断
- セッションコンテキスト: progress note、open questions、次の 1 手のような中断と再開のための記録
- ツールコンテキスト: grep 結果、test 出力、verify log のような live な根拠

`sample-repo` の `FEATURE-001` を例にすると、`sample-repo/docs/architecture.md` は永続コンテキスト、`sample-repo/tasks/FEATURE-001-brief.md` はタスクコンテキスト、`sample-repo/tasks/FEATURE-001-progress.md` はセッションコンテキスト、`python -m unittest discover -s tests -v` の結果はツールコンテキストになる。これらを同じメモ欄に詰め込むと、古い判断と live な失敗ログの区別が消える。

この分離が重要なのは、更新速度が違うからである。architecture doc は毎回変わらないが、progress note はセッションごとに変わる。最新ログは数分で無効になる。Context Engineering は、情報の種類ごとに寿命を定義し、AI agent に同じ重みで渡さないようにする。

### 3. context budget の考え方
Context budget は、token 上限の話だけではない。何を原文で残し、何を要約し、何を捨てるかを決める設計方針である。`docs/context-budget.md` では、Acceptance Criteria、API 契約、verify command、破壊的変更の制約は原文で残し、長い探索ログや比較検討の過程は要約し、古い test 出力全文や失効した仮説は捨てるとしている。

なぜ原文と要約を分けるのか。原文で残すべきものは、後から意味が変わると危険な契約である。`sample-repo/docs/acceptance-criteria/ticket-search.md` の「空文字または空白のみの query は全件を返す」は、要約するとぶれやすい。一方、「ranking を今回の Non-goals にした理由」は、決定自体さえ残っていれば理由の細部は要約で足りる。

context budget を切らないと、AI agent は重要な契約よりも目立つ情報に引きずられる。長いログ全文や古い探索メモが残っていると、最新の Acceptance Criteria よりそちらを優先してしまう。Context Engineering の実務では、たくさん集めることより、優先順位を明示することの方が重要である。

### 4. stale context と live context
stale context と live context を分けないと、AI agent は「昨日は正しかったが今は違う」情報を根拠に使う。`docs/context-model.md` が `sample-repo/docs/architecture.md` を stale-safe、verify 出力を live と分けているのはこのためである。

実務上の見分け方は単純である。repo の設計原則や glossary は stale-safe であり、起動時に読めばよい。task brief や acceptance criteria は今回の issue の canonical artifact であり、実装前に必ず読む。progress note は session memory として使うが、verify 結果が変わった時点で古くなる。test failure や terminal log はその瞬間の live context であり、結論だけを progress note に残し、全文は常駐させない。

`FEATURE-001` であれば、`sample-repo/docs/repo-map.md` と `sample-repo/docs/architecture.md` は stale-safe な参照起点である。一方、`sample-repo/tasks/FEATURE-001-progress.md` の `Last Verify` は stale になりやすい。だから再開時には progress note を読むだけで終わらせず、必要なら verify を再実行して live context を取り直す。

### 5. context poisoning と drift
Context Engineering の失敗は、情報不足だけではない。間違った context が残ることも同じくらい危険である。`docs/context-risk-register.md` では、stale docs、summary drift、instruction bloat、context poisoning、hidden done criteria、tool spam を主要リスクとして整理している。

典型例は 3 つある。第一に、docs と tests がずれたまま放置され、古い仕様を正として実装してしまうこと。第二に、progress note の `Decided` に未検証の推測を書き、次セッションがそれを事実として引き継ぐこと。第三に、`AGENTS.md` や handoff メモが肥大化し、重要な制約が埋もれることである。

対策も構造的に考える。canonical artifact を task brief と acceptance criteria に固定し、progress note では `Decided` と `Open Questions` を分ける。長いログは evidence として切り離す。verify を再実行できるなら、要約を信じる前に live context を取り直す。Context Engineering は「情報を増やす技術」ではなく、「壊れた情報を残さない技術」でもある。



## 章で使う bad / good example
bad:

```text
`FEATURE-001` の作業なので、前回のチャット要約、長い test ログ全文、repo tree 全体、古いメモをまとめて渡す。
prompt には「検索を直して。前回の流れを踏まえて進めて」とだけ書く。
```

このやり方では、Prompt Contract が弱いだけでなく、context の鮮度も重みも区別されない。古いログや未検証の推測が、acceptance criteria と同じ扱いになる。

good:

```text
Prompt Contract では Objective、Constraints、Completion Criteria を固定する。
context は次の順に渡す。
1. `sample-repo/docs/repo-map.md`
2. `sample-repo/tasks/FEATURE-001-brief.md`
3. `sample-repo/docs/acceptance-criteria/ticket-search.md`
4. `sample-repo/tasks/FEATURE-001-progress.md`
5. 最新の verify 結果
古いログ全文は残さず、必要な結論だけを progress note に昇格させる。
```

この修正版では、契約と判断材料が分離され、さらに stale-safe な docs と live な verify 結果も分けて扱われている。

比較観点:
- bad は prompt と context の役割を混ぜている
- bad は stale context と live context の重みを分けていない
- good は canonical artifact を先に固定し、ログは live evidence として扱っている

## 演習
1. 15 個の情報片を 4 種類の context に分類する。
2. 何を要約し、何を原文で残すかポリシーを作る。

## 参照する artifact
- `docs/context-model.md`
- `docs/context-budget.md`
- `docs/context-risk-register.md`


## 章末まとめ
- Prompt Engineering が作業境界を決めるのに対し、Context Engineering は判断材料の種類、鮮度、優先順位を決める。
- context は永続、タスク、セッション、ツールに分けて扱うと設計しやすい。
- context budget を切り、stale context と live context を分離しないと、情報量が多いほど失敗しやすくなる。次章では、この考え方を repo 全体の instruction と docs に落とし込む。
