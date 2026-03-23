---
id: ch08
title: Skills と Context Pack を再利用する
status: draft
artifacts:
  - .agents/skills/draft-chapter/SKILL.md
  - .agents/skills/review-chapter/SKILL.md
  - sample-repo/.agents/skills/issue-to-plan/SKILL.md
  - sample-repo/.agents/skills/verification/SKILL.md
  - sample-repo/context-packs/ticket-search.md
dependencies:
  - ch05
  - ch06
  - ch07

---

# Skills と Context Pack を再利用する

## この章の位置づけ
CH05-CH07 で、永続コンテキスト、repo context、task brief、session memory を個別に設計してきた。だが実務では、同じ種類の作業を何度も繰り返す。毎回 prompt を書き直し、毎回参照 artifact を列挙し直していると、作業速度も一貫性も落ちる。ここで必要になるのが skill と context pack である。

この章では、repeatable な作業を skill に昇格させる条件、`SKILL.md` の標準構成、repo skill と user skill の分離、context pack の組み立て方、skill versioning と破壊的変更を扱う。目的は instructions を増やすことではなく、再利用可能な作業単位を artifact として管理することである。

## 学習目標
- skill と通常 prompt の境界を説明できる
- SKILL.md の標準構成を定義できる
- context pack を粒度別に設計できる


## 小見出し
### 1. prompt が skill に昇格する条件
単発の prompt と skill の違いは、長さではない。再利用時に同じ inputs、同じ workflow、同じ output contract を繰り返し要求するかどうかで決まる。たとえば chapter 執筆では、brief と AGENTS を読み、artifact を確認し、bad / good example と演習を入れ、verify を回す、という手順が毎回同じである。これは `.agents/skills/draft-chapter/SKILL.md` に切り出す価値がある。

CH02 の Prompt Contract が単一タスクの Objective、Constraints、Completion Criteria を固定する artifact だったのに対し、skill は複数の task で再利用する workflow と output contract を固定する artifact である。この差を意識しないと、長い prompt を skill と呼び替えるだけになりやすい。

一方、「今回だけ `FEATURE-001` の ranking をどうするか考える」のような単発の設計相談は skill にしなくてよい。skill に昇格させるべきなのは、作業境界が安定し、再利用コストより定義コストの方が低いものだけである。

実務では、再利用回数、入力の安定性、出力の安定性、失敗しやすい手順の固定需要を見ると判断しやすい。よくある候補は chapter drafting、issue-to-plan、verification、review である。

### 2. SKILL.md の構成
良い `SKILL.md` は、抽象スローガンではなく作業契約を持つ。`.agents/skills/draft-chapter/SKILL.md`、`.agents/skills/review-chapter/SKILL.md`、`sample-repo/.agents/skills/issue-to-plan/SKILL.md`、`sample-repo/.agents/skills/verification/SKILL.md` は、いずれも Purpose、Use When、Required Inputs または Read First、Workflow または Steps、Output Contract、Guardrails を持っている。

この構成が有効なのは、skill を「便利メモ」ではなく operational artifact にできるからである。Purpose は何のための skill か、Use When は適用範囲、Read First は依存 artifact、Workflow は実行手順、Output Contract は期待成果、Guardrails はスコープ逸脱防止を定義する。どれかが欠けると、skill は長い prompt の別名になりやすい。

特に Output Contract は重要である。skill の出力が曖昧だと、後続の task brief や verify とつながらない。CH02 の Prompt Contract と同じく、skill も入出力契約として設計する必要がある。

### 3. repo skill と user skill の分離
skill には repo に属するものと、個人環境に属するものがある。この区別を曖昧にすると、repo を clone しただけでは再現できない workflow が増える。本 repo では、書籍固有の chapter workflow は `.agents/skills/` に、sample-repo 固有の `issue-to-plan` や `verification` は `sample-repo/.agents/skills/` に置いている。どちらも repo と一緒に version 管理される。

一方、個人の汎用レビュー skill や社内専用の credential を前提にした skill は、この repo には置かない方がよい。repo skill は、clone した他者が同じ artifact と同じ前提で再利用できるものに限定する。user skill は便利でも、repo context の source of truth にはしない。

Context Engineering の観点では、repo skill は永続コンテキストの一部であり、user skill は外部依存である。この線引きをしておくと、作業再現性が上がる。

### 4. context pack の組み立て
skill だけでは、個別タスクの判断材料が足りない。ここで context pack を組み合わせる。`sample-repo/context-packs/ticket-search.md` は、`FEATURE-001` 向けに Purpose、Read Order、Canonical Facts、Live Checks、Exclusions、Done Signals を定義している。

task brief が「何をやるか」を定義するのに対し、context pack は「どの artifact をどの順で読むか」を定義する。`ticket-search` pack では、domain overview、task brief、product spec、ADR、acceptance criteria、`service.py`、`test_ticket_search.py`、progress note の順で読むようにしている。さらに、検索対象、case-insensitive、blank query、非目標といった canonical fact を明示し、ranking や外部検索エンジンを exclusion に入れている。

良い context pack は、artifact の束であって雑多なリンク集ではない。Read Order、Canonical Facts、Live Checks、Exclusions、Done Signals の 5 点があると、AI agent は task brief を補強するために何を読むべきかを迷いにくい。

### 5. skill versioning と破壊的変更
skill や context pack も artifact である以上、変更管理が必要である。破壊的変更になるのは、Required Inputs が変わる、Output Contract の見出しが変わる、verify 手順が増減する、Read Order の前提 artifact が変わる、といった場合である。たとえば `verification` skill が unittest だけでなく evidence bundle 収集まで必須に変わるなら、後続の章や task brief の記述も更新しなければならない。

小さな repo では専用 version field がなくても運用できるが、「何が契約で、何が実装詳細か」は明示する必要がある。Purpose、Output Contract、Guardrails が変わる変更は、実質的に skill version の更新である。逆に wording の調整や説明追加は非破壊変更として扱える。

重要なのは、skill を増やすことではなく、壊れたまま放置しないことだ。skill と context pack は再利用のための artifact なので、古い手順を保存する場所ではない。



## 紙面で押さえるポイント
### Prompt / Skill / Context Pack の境界表

| artifact | 主目的 | 入力の安定性 | 出力契約 | 典型例 |
|---|---|---|---|---|
| Prompt Contract | 単一 task の objective と completion criteria を固定する | 低から中 | その task の完了条件 | bugfix prompt、feature prompt |
| skill | 再利用する workflow を固定する | 中から高 | 毎回そろえるべき steps と report format | `issue-to-plan`、`verification` |
| context pack | task 固有の読み順と canonical fact を固定する | 中 | 読む順序、除外事項、done signal | `ticket-search` pack |

この 3 つを混ぜると、長い prompt に workflow と参照ファイル一覧を全部押し込みやすい。CH08 のポイントは、Prompt Contract は単発 task の契約、skill は再利用 workflow の契約、context pack は task 固有の読み込み束だと切り分けることである。3 者を分離すると、同じ planning や verify を何度も書き直さずに済む。

## 章で使う bad / good example
bad:

```text
issue ごとに毎回、同じ planning 手順、同じ verify 手順、同じ参照ファイル一覧を
チャットに貼り直す。検索系タスクでも review タスクでも、長い自由文 prompt で済ませる。
```

このやり方では、再利用回数が増えるほど drift が増える。どの手順が必須か、どの artifact が canonical かが task ごとに微妙に変わってしまう。

good:

```text
plan 化は `sample-repo/.agents/skills/issue-to-plan/SKILL.md` に固定する。
verify は `sample-repo/.agents/skills/verification/SKILL.md` に固定する。
`FEATURE-001` では `sample-repo/context-packs/ticket-search.md` を読み順と
canonical fact の source of truth として使う。
```

この修正版では、繰り返し出る workflow を skill に、task 固有の読み込みセットを context pack に分離している。

比較観点:
- bad は再利用される手順が artifact 化されていない
- bad は task 固有情報と汎用 workflow を同じ prompt に混ぜている
- good は workflow は skill、task 固有情報は context pack として分離している

## 演習
1. issue → plan 変換 skill を作る。
2. PR review skill を作り、チェック観点を固定する。

## 参照する artifact
- `.agents/skills/draft-chapter/SKILL.md`
  chapter drafting を再利用 workflow として固定した例として読む。Purpose、Read First、Output Contract の関係を見る。
- `.agents/skills/review-chapter/SKILL.md`
  review 系 skill の例として読む。chapter drafting と比較し、workflow 差分がどこに出るかを確認する。
- `sample-repo/.agents/skills/issue-to-plan/SKILL.md`
  issue を plan に落とす repo skill の例として読む。Prompt Contract ではなく workflow 契約である点を押さえる。
- `sample-repo/.agents/skills/verification/SKILL.md`
  verify を毎回書き直さないための skill として読む。CH10 の verification harness への橋渡しになる。
- `sample-repo/context-packs/ticket-search.md`
  task 固有の読み順と canonical fact を束ねた例として読む。skill ではなく context pack で持つ理由を確認する。


## 章末まとめ
- skill は長い prompt の別名ではなく、再利用可能な workflow と output contract を持つ artifact である。
- context pack は task brief を置き換えるものではなく、読む順序と canonical fact を束ねる task-specific context である。
- repo skill と user skill を分け、破壊的変更を契約変更として扱うと再利用しやすい。次章からは Harness Engineering に入り、こうして整えた context を安全に実行し、verify する仕組みを扱う。
