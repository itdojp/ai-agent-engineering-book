---
id: ch01
title: AIエージェントはどこで失敗するか
status: draft
artifacts:
  - sample-repo/README.md
  - sample-repo/docs/domain-overview.md
  - sample-repo/docs/seed-issues.md
dependencies:
  - none

---

# AIエージェントはどこで失敗するか

## この章の位置づけ
会話では有能に見えるのに、repo を触らせた途端に雑に壊す。この落差が、多くの読者が最初にぶつかる問題である。前付けで、本書の約束、想定読者、3 部構成の読み方を整理した。ここから本文に入る。最初に確認すべきなのは、AIエージェントが実務でどこで失敗するかである。

CH01 の役割は、failure model を定義することにある。誤答、context poisoning、tool misuse、approval 漏れ、verify 不足などを含む 8 類型を起点に、なぜ Prompt Engineering だけでは足りず、Context Engineering と Harness Engineering まで必要になるのかを整理する。以後の章では、この failure model に対して artifact を 1 層ずつ積み上げる。

## 学習目標
- 単発の誤答と、context / permissions / verify / approvals を含む実行失敗の違いを説明できる
- interactive assistant、ローカル CLI coding agent、クラウド / バックグラウンド agent の役割差を理解する
- 後続章で何を artifact として積み上げ、何を verification signal として見るか把握する


## 小見出し
### 1. 単発で当たることと、仕事が完了することは違う
会話の中で良い答えを返すことと、repo 上で仕事を完了することは別問題である。たとえば `sample-repo` の検索改善について AIエージェントに相談すると、「title だけでなく description と tags も見るべきです」と答えるかもしれない。これは方向性としては妥当に見える。しかし、実務ではそこで終わらない。どの issue を対象にするのか、何を変更対象 artifact とみなすのか、verify をどう通すのかが決まっていなければ、仕事は進まない。

`sample-repo` はその差を観察しやすい題材である。`sample-repo/README.md` にはサポートチケット管理の小さな Python ドメインモデルであることが書かれている。ここで必要なのは、単に「良さそうな実装案」を出すことではなく、チケット一覧、検索、ステータス更新といった既存機能を壊さずに改善し、必要な docs や tests も含めて作業を閉じることである。

実務で問われるのは次の差である。

| 観点 | もっともらしい出力 | 完了した仕事 |
|---|---|---|
| 対象 | その場の質問 | issue と変更対象 artifact |
| 成果 | 説明や断片コード | code / docs / tests / verify 結果 |
| 判定 | 読んだ人が納得するか | 変更理由と完了条件を追跡できるか |
| 失敗の出方 | その場では目立たない | 後で誤答、忘却、破壊、停止として表面化する |

### 2. 失敗の 8 類型: 誤答・汚染・誤用・漏れ・停止
AIエージェントの失敗は、2026 年の実務では 4 類型だけでは足りない。少なくとも次の 8 類型を区別しておく必要がある。

1. 誤答
   要件やドメインを取り違えたまま、それらしく答える失敗である。
2. context poisoning
   古い Progress Note、誤った summary、古い spec を正本扱いし、以後の判断全体を汚染する失敗である。
3. stale state
   branch、review 状態、approval pending、runtime 設定などの現在値を見誤る失敗である。
4. tool misuse
   書き込み、外部接続、削除、課金 API 呼び出しなどを、許可境界を超えて実行する失敗である。
5. approval 漏れ
   human approval gate を通すべき操作を自律実行し、監査性を壊す失敗である。
6. verify 不足
   test、lint、docs、policy、evidence の確認が不十分なまま完了扱いする失敗である。
7. background execution の不透明化
   長時間実行や remote / background agent の途中状態が見えず、再開・handoff・rollback が困難になる失敗である。
8. cost / latency の暴走
   無駄な再試行、不要な tool call、過大な context 投入でコストと待ち時間が制御不能になる失敗である。

これらは単独ではなく連鎖する。context poisoning や stale state は誤答を増やし、tool misuse や approval 漏れは破壊と監査不備を生み、verify 不足と background execution の不透明化は停止を見逃しやすくする。

`sample-repo/docs/seed-issues.md` にある貫通ケースに当てはめると、次のように読める。

| 失敗類型 | `sample-repo` での典型例 | 最初に疑うべき不足 |
|---|---|---|
| 誤答 | `FEATURE-001` で検索要件を早合点する | 対象 issue とドメイン理解 |
| context poisoning / stale state | `FEATURE-002` で古い Progress Note を正本扱いする | source hierarchy と `restart packet（Resume Packet）` |
| tool misuse / approval 漏れ | verify 前に危険操作や外部接続を走らせる | permission policy と approval gate |
| verify 不足 / 停止 | `HARNESS-001` で evidence を残さず完了扱いする | verification harness と done criteria |
| cost / latency の暴走 | context を過投入し、長時間 run を無制御に回す | context budget と operating model |

### 3. Failure を減らす設計面と agent 類型
8 類型の失敗を、気合いで減らすことはできない。必要なのは、どの failure に対して何を設計するかを分けることである。本書ではそれを Prompt / Context / Harness の 3 面で扱う。

| 設計面 | 主に減らす failure | 何を設計するか | 代表 artifact |
|---|---|---|---|
| Prompt Engineering | 誤答、scope drift、出力契約崩れ | task の目的、制約、tool contract、done criteria、output schema | prompt artifact、review checklist、eval cases |
| Context Engineering | context poisoning、stale state、前提喪失 | repo / task / session / memory / context pack の正本と優先順位 | task brief、Progress Note、context pack、repo map |
| Harness Engineering | tool misuse、approval 漏れ、verify 不足、停止 | 実行境界、permission policy、verify、resume、evidence、approval | verify checklist、runbook、restart packet、operating model |

さらに、agent の種類ごとに設計責務も異なる。

| agent 類型 | 主な役割 | 先に固定すべき境界 |
|---|---|---|
| interactive assistant | 要件整理、比較、論点抽出 | exploratory dialogue を正本にしないこと |
| ローカル CLI coding agent | repo を読んで変更し、local verify を回す | write scope、shell 権限、verify 手順 |
| クラウド / バックグラウンド coding agent | 長時間 task、remote 実行、非同期再開 | approval、polling / notification、restart packet |
| API / managed runtime agent | product workflow への組み込み | tool policy、observability、auditability、cost / latency |

重要なのは、後ろの設計面が前を置き換えるのではなく積み重なることだ。Prompt が弱ければ、良い harness を作っても誤った task を丁寧に完遂するだけになる。Context が弱ければ、良い prompt を与えても session を跨いだ時点で前提が壊れる。Harness が弱ければ、良い prompt と context があっても verify と approval が閉じない。

### 4. 本書の貫通ケースと sample-repo の概要
本書では、`support-hub` という小さなサポートチケット管理システムを `sample-repo` として使う。これは単なる toy app ではない。一次受け担当が ticket を triage し、当番リードが assignee と backlog を見て、実装担当や運用担当が再発問い合わせの検索と運用変更を判断する、という現場を簡略化した題材である。`sample-repo/docs/domain-overview.md` にある通り、中核は `Ticket`、`InMemoryTicketStore`（概念として `TicketStore` と総称する）、`SupportHubService` であり、一覧取得、ステータス更新、キーワード検索、assignee での絞り込みが入っている。規模は小さいが、status の不整合、検索の弱さ、ownership の曖昧さ、verify 不足といった実務の痛みを一通り載せられる。

さらに、本書では `sample-repo/docs/seed-issues.md` の 4 件を貫通ケースとして使う。

| ケース | 現場の痛み | 何が増えるか | 代表的な失敗 |
|---|---|---|---|
| `BUG-001` | 旧 status が見え、二重対応が起きうる | bugfix brief、test、single-agent harness | 破壊、停止 |
| `FEATURE-001` | 類似 ticket を見つけにくく、要求も曖昧 | spec、ADR、acceptance criteria、context pack、verify guard | 誤答 |
| `FEATURE-002` | assignee と監査ログの扱いが長時間化しやすい | plan、feature list、restart packet、role 分担 | 忘却、停止 |
| `HARNESS-001` | verify と証跡が弱く、review で説明しにくい | done criteria、CI、evidence bundle、operating model | 停止、破壊 |

`FEATURE-001` は本書の spine であり、曖昧要求を spec、context、verify に変えていく流れを通して追う。`BUG-001` は bounded な bugfix を確実に閉じる題材であり、`FEATURE-002` は session を跨ぐ task を壊さない題材であり、`HARNESS-001` は verify と証跡を team 運用へ接続する題材である。`sample-repo/docs/seed-issues.md` には、各ケースがどの chapter / artifact / payoff に接続するかの対応表も置いてある。後続章では毎回ケースを最初から説明し直すのではなく、「今回このケースで何を学ぶか」だけを再確認しながら進める。

ChatGPT と Codex CLI の役割も分ける。ChatGPT は曖昧要求の整理、代替案比較、レビュー観点の洗い出しに向く。Codex CLI は repo を読み、変更し、verify を回し、artifact を更新する実行側に向く。CH01 の時点では、この役割分担だけ押さえればよい。詳細な prompt 設計や task brief の書式は後続章で扱う。

### 5. 理論ではなく artifact を積む本として読む
この本では、各章で概念を説明するだけで終わらない。概念を repo 上の artifact に落とす。Prompt Engineering の章では prompt artifact を作り、Context Engineering の章では task brief や context pack を整え、Harness Engineering の章では verify script や runbook を整える。読者は説明を読むだけでなく、「その章の終わりに repo に何が増えるか」を追うべきである。

この読み方には利点がある。第一に、AIエージェントの良し悪しを主観で語らずに済む。artifact が増え、verify が通り、変更理由が説明できれば前進である。第二に、途中で失敗しても戻りやすい。どこまで artifact が整っているかを見れば、次の一手が分かる。第三に、後続章の内容が独立した小技ではなく、同じ仕事を完了に近づけるための層だと理解できる。

CH01 の結論は単純である。AIエージェントが失敗するのは、能力が低いからではない。完了までの道具立てが足りないからである。次章からは、その道具立てを Prompt Engineering から順に積み上げる。



## 章で使う bad / good example
bad:

```text
sample-repo の検索を改善して。いい感じに直しておいて。
```

この依頼では、対象 issue、変更対象 artifact、完了条件、verify が抜けている。AIエージェントはもっともらしい提案や部分実装を返せるが、誤答、approval 漏れ、verify 不足、停止のどれも防げない。

good:

```text
まず `sample-repo/docs/seed-issues.md` の `FEATURE-001` を読み、何を決めずに着手すると失敗するかを整理する。
今回は実装前の準備として、目的、変更対象 artifact、verify 方法を箇条書きでまとめる。
完了条件は、次の作業者が同じ前提で着手できること。
```

この修正版は、まだ詳細な Prompt Contract ではないが、「何を終わりとみなすか」「どの artifact を見るか」を先に固定している。CH02 以降で扱う設計の必要性を、実務的な形で示す最小の例である。

比較観点:
- bad は出力の見た目しか管理していない
- good は対象 issue、artifact、完了条件を先に固定している
- good は次の verify と handoff を前提にしている

## 演習
1. `sample-repo/docs/seed-issues.md` の 4 件を見て、それぞれが主にどの失敗類型を扱う題材かを分類しなさい。1 件につき 1 行で理由も書くこと。
2. 次の依頼文を読み、起きやすい失敗類型を 2 つ選びなさい。さらに、完了に近づけるために最初に追加すべき artifact を 2 つ挙げなさい。依頼文: 「support-hub の使い勝手を上げたい。必要ならコードも docs も直して。」。

## 参照する artifact
- `sample-repo/README.md`
- `sample-repo/docs/domain-overview.md`
- `sample-repo/docs/seed-issues.md`


## Source Notes / Further Reading
- この章を探し直すときは、まず `sample-repo/README.md`、`sample-repo/docs/domain-overview.md`、`sample-repo/docs/seed-issues.md` を正本として見る。failure model は recurring case と切り離して一般論だけで理解しない。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH01 AIエージェントはどこで失敗するか」と `manuscript/backmatter/01-読書案内.md` の「Prompt と要求定義」「検証・信頼性・運用」を参照する。

## 章末まとめ
- AIエージェントは、誤答だけでなく context poisoning、tool misuse、approval 漏れ、verify 不足、cost / latency の暴走でも失敗する。
- 本書の対象は「もっともらしい出力」ではなく、artifact・permissions・verify・evidence を伴って仕事を完了させることである。
- failure model が見えれば、次に最初に固定すべきは単一 task の契約である。次章では Prompt Engineering の入口として、prompt を入出力契約として扱う。
