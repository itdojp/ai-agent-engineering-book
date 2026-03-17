---
id: ch03
title: ChatGPTで要件と設計を固める
status: draft
artifacts:
  - sample-repo/docs/product-specs/ticket-search.md
  - sample-repo/docs/design-docs/ticket-search-adr.md
  - sample-repo/docs/acceptance-criteria/ticket-search.md
dependencies:
  - ch01
  - ch02

---

# ChatGPTで要件と設計を固める

## この章の位置づけ
CH02 では、single-task reliability のために Prompt Contract を定義した。だが、契約がしっかりしていても、対象の要求そのものが曖昧なら、AIエージェントは正しく実装できない。CH03 の役割はそこにある。ChatGPT を使って、曖昧な依頼を product spec、acceptance criteria、design decision に変換する。

ここで重要なのは、ChatGPT との対話そのものを成果物と勘違いしないことだ。探索的な会話は有用だが、実装準備ができた状態とは別である。実装準備ができた状態とは、repo に product spec、acceptance criteria、ADR が残り、人間が最終判断を説明できる状態を指す。この章では `sample-repo` の `FEATURE-001` を題材に、その変換過程を具体化する。

## 学習目標
- 曖昧な依頼を acceptance criteria 付き仕様に変換できる
- 代替案比較から ADR を書ける
- 人間が残す判断点と AI に委ねる判断点を分けられる


## 小見出し
### 1. 曖昧要求を仕様に変える
曖昧な要求は、そのままでは coding agent に渡せない。たとえば `FEATURE-001` の起点は「検索を使いやすくしたい」である。この文には、誰が困っているのか、どのフィールドを検索対象にするのか、非目標は何かが入っていない。ここで ChatGPT を使う価値は、足りない論点を洗い出し、仕様の骨格を短時間で作ることにある。

ただし、探索会話と product spec は別物である。探索会話は発散してよいが、product spec は収束していなければならない。

| 種類 | 目的 | 書いてよいこと | そのまま実装に渡せるか |
|---|---|---|---|
| 探索会話 | 論点を増やす | 可能性、仮説、未確定事項 | できない |
| product spec | 問題設定とスコープを固定する | Problem、Objective、In Scope、Non-goals、Users、Requirements | できる |

`sample-repo/docs/product-specs/ticket-search.md` では、曖昧な要求を次の形に固定した。

- Problem: サポート担当者が検索対象フィールドを意識しないと探しづらい
- Objective: 単一 query で候補チケットを絞り込めるようにする
- In Scope: `title`、`description`、`tags` の部分一致検索
- Non-goals: ranking、typo correction、外部検索エンジン導入

この段階で大切なのは、「何を作るか」だけでなく「今回は何を作らないか」を決めることだ。ChatGPT は論点を出すのが得意だが、どこで切るかは人間が決める必要がある。検索を使いやすくする議論は、ranking、typo correction、保存済み検索、UI 変更へ簡単に広がる。product spec の価値は、広がる論点を現在の issue のスコープに閉じ込めることにある。

### 2. 受け入れ条件の分解
product spec ができても、まだ実装準備は終わらない。Objective や In Scope は、読む人によって解釈がぶれるからだ。そこで必要になるのが acceptance criteria である。acceptance criteria は、仕様を verify 可能な文へ落とし直した artifact であり、「何ができたら完了か」を固定する。

`sample-repo/docs/acceptance-criteria/ticket-search.md` では、仕様を次の単位へ分解している。

- `title` に部分一致する query で該当チケットを返す
- `description` に部分一致する query で該当チケットを返す
- `tags` に部分一致する query で該当チケットを返す
- 大文字小文字を区別しない
- 空文字または空白のみの query は全件を返す

この分解により、product spec の「検索を使いやすくする」が、test と結びつく粒度まで下りてくる。さらに、artifact criteria を別に置くことで、「docs と tests が同期しているか」も acceptance の一部として扱える。実務では機能の挙動だけでなく、仕様・設計・検証 artifact の同期も品質条件に含めるべきだ。

ChatGPT は acceptance criteria の候補を大量に出せるが、最終的に残す条件は人間が絞り込む必要がある。条件が多すぎると実装範囲が膨らみ、少なすぎると完成判定が曖昧になる。CH03 の時点で重要なのは、「あとで test に落とせる文になっているか」を基準にすることだ。

### 3. 代替案比較と設計判断
要求が固定されたら、次は設計判断である。ここでも ChatGPT は有用だが、役割は「正解を決めること」ではなく、「選択肢とトレードオフを整理すること」にある。

`FEATURE-001` では、少なくとも 2 つの案が考えられる。

1. `service.py` で in-memory の部分一致検索を行う
2. 検索専用 abstraction を追加し、将来の外部検索エンジンを見据える

ChatGPT にこの比較をさせると、長所短所はすぐ出る。しかし、どちらを採用するかは repo の現在地に依存する。`sample-repo` は例示用で、外部依存を増やさず、service layer 経由の変更を原則としている。この前提を踏まえると、Chapter 3 の目的には 1 が適切である。2 は将来の柔軟性を増やすが、現在の repo 規模では設計コストが先行する。

ここでのポイントは、「ChatGPT が提案した案」ではなく、「人間がどの判断軸で選んだか」を残すことだ。判断軸が曖昧なままだと、後で別の担当者が同じ論点を再発見し、設計がぶれやすい。

### 4. ADR を残す理由
設計判断は、会話ログの中に埋めない。`sample-repo/docs/design-docs/ticket-search-adr.md` のような ADR として残す。ADR の役割は、未来の自分や別の担当者に「なぜこの設計を選んだのか」を短時間で伝えることにある。

今回の ADR では、Context、Options Considered、Decision、Decision Drivers、Consequences、Review Trigger を残した。これにより、次の点が明確になる。

- 何が問題設定だったか
- どの案を比較したか
- なぜその案を選んだか
- どの条件が変わったら再判断すべきか

特に Review Trigger は重要である。今は in-memory 検索で十分でも、検索対象フィールドが増える、ranking が必要になる、外部検索エンジンが要求される、といった条件が出れば見直しが必要になる。ADR は過去の判断を固定化するためではなく、再判断の条件を明示するために書く。

設計判断を会話だけで済ませると、「たしかこういう理由だったはずだ」が増える。ADR を残すと、「この repo の今の前提での判断」が artifact として追跡できる。

### 5. 人間が止めるべき判断点
ChatGPT は、曖昧要求を分解し、仕様候補や設計案を出すのに向く。しかし、次の判断は人間が残すべきである。

1. どの要求を今の issue のスコープに入れるか
2. どの非目標を受け入れるか
3. どのトレードオフを許容するか
4. 失敗時の責任を誰が持つか

たとえば「検索を使いやすくしたい」に対して、ChatGPT は ranking や typo correction も提案できる。だが、それを今回の `FEATURE-001` に入れるかは、優先度、工数、教育目的、repo の複雑性を踏まえて人間が決めるべきである。AI に委ねてよいのは論点の発見と比較表のたたき台までであり、採否の責任までではない。

この線引きができると、探索会話は速くなる。人間は「何を決めるべきか」を知った上で ChatGPT を使い、決めた内容だけを artifact に落とせばよい。次の coding agent に渡すべきものは、会話の全文ではなく、確定した product spec、acceptance criteria、ADR である。



## 章で使う bad / good example
bad:

```text
検索を使いやすくしたい。ChatGPT に仕様を考えさせて、そのまま実装に進める。
```

この進め方では、探索会話と確定仕様が混ざる。ChatGPT は ranking、typo correction、UI 変更などを次々と提案できるが、どれが今回の issue のスコープか分からないまま artifact を作ることになる。

good:

```text
対象は `sample-repo/docs/seed-issues.md` の `FEATURE-001` とする。
まず ChatGPT で、ユーザー、問題、In Scope、Non-goals、未確定点を洗い出す。
次に、人間が採否を決めた内容だけを `docs/product-specs/ticket-search.md` にまとめる。
その仕様を verify 可能な文へ分解し、`docs/acceptance-criteria/ticket-search.md` に落とす。
設計案は 2 案比較し、採用理由を `docs/design-docs/ticket-search-adr.md` に残す。
```

この修正版は、探索と収束を分けている。ChatGPT は論点整理に使い、実装準備に必要な artifact は repo に確定形で残す。

比較観点:
- bad は会話ログを仕様の代わりにしている
- good は product spec、acceptance criteria、ADR に役割を分けている
- good は人間が採否を決める位置を明示している

## Worked Example
`FEATURE-001` の元要求を「検索を使いやすくしたい」とする。ここから ChatGPT を使って次の順に収束させる。

1. 探索会話で確認する
   - 誰が検索するのか
   - どのフィールドを対象にするのか
   - 今回扱わないことは何か
   - 完了したと言える最低条件は何か
2. product spec に固定する
   - `title`、`description`、`tags` を検索対象にする
   - ranking、typo correction、外部検索エンジンは非目標とする
3. acceptance criteria に分解する
   - 部分一致
   - 大文字小文字を区別しない
   - 空 query は全件
4. ADR に設計判断を残す
   - `service.py` で in-memory 検索
   - 将来の検索基盤追加は review trigger に回す

この worked example で重要なのは、ChatGPT が直接実装を決めたわけではない点である。ChatGPT は論点の抽出と比較の高速化に使い、最終的な artifact の確定と責任は人間が持つ。

## 演習
1. 「検索を使いやすくしたい」を題材に、`sample-repo` 向けの product spec を書きなさい。Problem、Objective、In Scope、Non-goals、User Scenarios を必ず含めること。
2. `ticket-search` の設計案を 2 案比較し、ADR を 1 本書きなさい。Decision Drivers と Review Trigger を必ず含めること。

## 参照する artifact
- `sample-repo/docs/product-specs/ticket-search.md`
- `sample-repo/docs/design-docs/ticket-search-adr.md`
- `sample-repo/docs/acceptance-criteria/ticket-search.md`


## 章末まとめ
- ChatGPT の価値は、曖昧要求をそのまま実装させることではなく、論点を洗い出して product spec、acceptance criteria、ADR に収束させることにある。
- 探索会話と実装準備ができた artifact は別であり、実装に渡すべきなのは確定した artifact である。
- 人間はスコープ、非目標、設計トレードオフの採否を残す必要がある。次章では、この仕様と設計 artifact を prompt 評価へつなげる。
