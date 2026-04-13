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
同じ verification prompt や issue-to-plan prompt を毎回貼り直していると、速くなるどころか再現性が落ちる。CH05-CH07 で、永続コンテキスト、repo context、task brief、session memory を個別に設計してきた。だが実務では、同じ種類の作業を何度も繰り返す。ここで必要になるのが skill と context pack である。

この章では、repeatable な作業を skill に昇格させる条件、`SKILL.md` の標準構成、repo skill と user skill の分離、context pack の組み立て方、skill versioning と破壊的変更を扱う。目的は instructions を増やすことではなく、再利用可能な作業単位を artifact として管理することである。長い prompt を skill と呼び替えるだけでも、MCP をつなげたから repo artifact が不要になると考えることでもない。

## 学習目標
- skill と通常 prompt の境界を説明できる
- SKILL.md の標準構成を定義できる
- context pack を粒度別に設計できる


## 小見出し
### 1. prompt が skill に昇格する条件
単発の prompt と skill の違いは、長さではない。再利用時に同じ inputs、同じ workflow、同じ output contract を繰り返し要求するかどうかで決まる。たとえば chapter 執筆では、brief と AGENTS を読み、artifact を確認し、bad / good example と演習を入れ、verify を回す、という手順が毎回同じである。これは `.agents/skills/draft-chapter/SKILL.md` に切り出す価値がある。

CH02 の Prompt Contract が単一タスクの Objective、Constraints、Completion Criteria を固定する artifact だったのに対し、skill は複数の task で再利用する workflow と output contract を固定する artifact である。この差を意識しないと、長い prompt を skill と呼び替えるだけになりやすい。skill に昇格させるべきなのは、作業境界が安定し、再利用コストより定義コストの方が低いものだけである。

一方、「今回だけ `FEATURE-001` の ranking をどうするか考える」のような単発の設計相談は skill にしなくてよい。実務では、再利用回数、入力の安定性、出力の安定性、失敗しやすい手順の固定需要を見ると判断しやすい。よくある候補は chapter drafting、issue-to-plan、verification、review である。

### 2. SKILL.md の構成
良い `SKILL.md` は、抽象スローガンではなく作業契約を持つ。`.agents/skills/draft-chapter/SKILL.md`、`.agents/skills/review-chapter/SKILL.md`、`sample-repo/.agents/skills/issue-to-plan/SKILL.md`、`sample-repo/.agents/skills/verification/SKILL.md` は、いずれも Purpose、Use When、Read First または Required Inputs、Workflow または Steps、Output Contract、Guardrails を持っている。

この構成が有効なのは、skill を「便利メモ」ではなく operational artifact にできるからである。Purpose は何のための skill か、Use When は適用範囲、Read First は依存 artifact、Workflow は実行手順、Output Contract は期待成果、Guardrails はスコープ逸脱防止を定義する。どれかが欠けると、skill は長い prompt の別名になりやすい。

ここで `AGENTS.md` との違いを明確にしておく。`AGENTS.md` は repo entrypoint であり、その領域で外してはいけない不変条件と、次に開くべき artifact への入口を定義する。`SKILL.md` は repeatable work unit であり、同じ作業を何度も安全に回すための workflow と output contract を定義する。repo 全体の不変条件は `AGENTS.md` に置き、repeatable な手順は `SKILL.md` に置く。これを混ぜると、root instructions が肥大化し、skill が repo 固有知識を抱え込みすぎる。

### 3. repo skill と user skill の分離
skill には repo に属するものと、個人環境に属するものがある。この区別を曖昧にすると、repo を clone しただけでは再現できない workflow が増える。本 repo では、書籍固有の chapter workflow は `.agents/skills/` に、sample-repo 固有の `issue-to-plan` や `verification` は `sample-repo/.agents/skills/` に置いている。どちらも repo と一緒に version 管理される。

一方、個人の汎用レビュー skill や社内専用の credential を前提にした skill は、この repo には置かない方がよい。repo skill は、clone した他者が同じ artifact と同じ前提で再利用できるものに限定する。user skill は便利でも、repo context の source of truth にはしない。

また、repo skill は small に保つ必要がある。skill に domain の全文説明、repo map、過去の issue 履歴まで詰め込むと、再利用 workflow と repo 固有 knowledge が分離できなくなる。skill は「何を入力にし、どう進め、どう返すか」を中心に保ち、詳細な設計理由や source of truth は AGENTS、brief、spec、docs へ委譲する。

### 4. context pack の組み立て
skill だけでは、個別タスクの判断材料が足りない。ここで context pack を組み合わせる。`sample-repo/context-packs/ticket-search.md` は、`FEATURE-001` 向けに Purpose、Read Order、Canonical Facts、Live Checks、Exclusions、Done Signals を定義している。

task brief が「何をやるか」を定義するのに対し、context pack は「どの artifact をどの順で読むか」を定義する。`ticket-search` pack では、domain overview、task brief、product spec、ADR、acceptance criteria、`service.py`、`test_ticket_search.py`、`Progress Note` の順で読むようにしている。さらに、検索対象、case-insensitive、blank query、非目標といった canonical fact を明示し、ranking や外部検索エンジンを exclusion に入れている。

ここで MCP-connected capability との違いも押さえる必要がある。MCP や tool 接続は、runtime に新しい tool、resource、prompt surface を足す接続面である。これは live に情報を取得したり、外部機能を呼び出したりする能力であって、repo skill や context pack の代替ではない。task brief、AGENTS、spec、tests が repo 上の source of truth であることは変わらない。MCP-connected capability はそれらへ到達する能力を増やすが、「何を信頼し、どの順で読むか」を決めるのは依然として context pack 側の仕事である。

### 5. skill versioning と破壊的変更
skill や context pack も artifact である以上、変更管理が必要である。破壊的変更になるのは、Required Inputs が変わる、Output Contract の見出しが変わる、verify 手順が増減する、Read Order の前提 artifact が変わる、といった場合である。たとえば `verification` skill が unittest だけでなく evidence bundle 収集まで必須に変わるなら、後続の章や task brief の記述も更新しなければならない。

小さな repo では専用 version field がなくても運用できるが、「何が契約で、何が実装詳細か」は明示する必要がある。Purpose、Output Contract、Guardrails が変わる変更は、実質的に skill version の更新である。逆に wording の調整や説明追加は非破壊変更として扱える。

重要なのは、skill を増やすことではなく、壊れたまま放置しないことだ。skill と context pack は再利用のための artifact なので、古い手順を保存する場所ではない。



## 紙面で押さえるポイント
### Prompt / AGENTS / Skill / Context Pack / MCP の境界表

| artifact | 主目的 | 何を固定するか | 典型例 |
|---|---|---|---|
| Prompt Contract | 単一 task の objective と completion criteria を固定する | その task の入出力契約 | bugfix prompt、feature prompt |
| `AGENTS.md` | repo entrypoint と不変条件を示す | まず読む入口、verify 義務、更新境界 | root / local `AGENTS.md` |
| skill | 再利用する workflow を固定する | inputs、steps、output contract | `issue-to-plan`、`verification` |
| context pack | task 固有の読み順と canonical fact を固定する | 読む順序、除外事項、done signal | `ticket-search` pack |
| MCP-connected capability | runtime に新しい capability を接続する | tool / resource / prompt surface | 外部検索、DB 参照、remote tool |

この 5 つを混ぜると、長い prompt に workflow と参照ファイル一覧を全部押し込みやすい。CH08 のポイントは、Prompt Contract は単発 task の契約、`AGENTS.md` は repo 入口、skill は再利用 workflow、context pack は task 固有の読み込み束、MCP-connected capability は追加能力の接続面だと切り分けることである。

## 章で使う bad / good example
bad:

```text
issue ごとに毎回、同じ planning 手順、同じ verify 手順、同じ参照ファイル一覧を
長い自由文 prompt に貼り込む。MCP で外部検索が使えるので、repo の AGENTS や spec は
都度読まなくてもよいと判断する。
```

このやり方では、再利用回数が増えるほど drift が増える。どの手順が必須か、どの artifact が canonical かが task ごとに微妙に変わってしまう。

good:

```text
repo entrypoint は `AGENTS.md` と local `AGENTS.md` に固定する。
plan 化は `sample-repo/.agents/skills/issue-to-plan/SKILL.md` に固定する。
verify は `sample-repo/.agents/skills/verification/SKILL.md` に固定する。
`FEATURE-001` では `sample-repo/context-packs/ticket-search.md` を読み順と
canonical fact の source of truth として使う。
MCP-connected capability は live な追加調査に使うが、repo artifact の代替にはしない。
```

この修正版では、repo 入口、再利用 workflow、task 固有情報、追加 capability の境界が分離されている。

比較観点:
- bad は長い prompt を skill と呼び替えている
- bad は AGENTS と context pack を省略し、MCP を source of truth と誤認している
- good は repo entrypoint、workflow、task-specific context、runtime capability を分離している

## 演習
1. issue → plan 変換 skill を作る。
2. PR review skill を作り、チェック観点を固定する。

## 参照する artifact
- `.agents/skills/draft-chapter/SKILL.md`
  chapter drafting を再利用 workflow として固定した例として読む。Purpose、Read First、Output Contract の関係を見る。
- `.agents/skills/review-chapter/SKILL.md`
  review 系 skill の例として読む。`AGENTS.md` の不変条件を写し込まずに workflow を保つ点を確認する。
- `sample-repo/.agents/skills/issue-to-plan/SKILL.md`
  issue を plan に落とす repo skill の例として読む。Prompt Contract ではなく workflow 契約である点を押さえる。
- `sample-repo/.agents/skills/verification/SKILL.md`
  verify を毎回書き直さないための skill として読む。CH10 の verification harness への橋渡しになる。
- `sample-repo/context-packs/ticket-search.md`
  task 固有の読み順と canonical fact を束ねた例として読む。skill ではなく context pack で持つ理由を確認する。


## Source Notes / Further Reading
- この章を探し直すときは、まず `SKILL.md` 群と `sample-repo/context-packs/ticket-search.md` を正本として見る。skill は再利用 workflow の契約、context pack は task ごとの最小入力であり、MCP-connected capability の代替ではない。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH08 Skills と Context Pack を再利用する」と `manuscript/backmatter/01-読書案内.md` の「Context と repo 設計」を参照する。

## 章末まとめ
- skill は長い prompt の別名ではなく、再利用可能な workflow と output contract を持つ artifact である。
- `AGENTS.md` は repo entrypoint、`SKILL.md` は repeatable work unit、context pack は task-specific read set として分ける。
- MCP-connected capability は追加能力の接続面であり、repo skill や context pack の代替ではない。次章からは Harness Engineering に入り、single-agent harness を扱う。
