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
AIエージェントは、数ターンの会話では非常に有能に見える。質問に答え、設計案を出し、コードの断片もそれらしく書ける。しかし、実務で必要なのは「もっともらしい出力」ではなく「仕事が完了した状態」を作ることだ。repo を読み、必要な artifact を見つけ、変更し、verify し、必要なら docs も更新して初めて、作業は完了と言える。

本書は、AIエージェントを賢く見せる本ではない。ChatGPT で要件と設計を整理し、Codex CLI で repo を読みながら変更と verify を進め、最終的に仕事を最後までやり切らせるための本である。そのために、Prompt Engineering、Context Engineering、Harness Engineering という 3 段階の成熟モデルを使う。CH01 では、この成熟モデルがなぜ必要なのかを、失敗パターンと `sample-repo` の貫通ケースから整理する。

## 学習目標
- 単発の誤答と長時間タスク失敗の違いを説明できる
- 本書の sample-repo、ChatGPT、Codex CLI の役割分担を理解する
- 後続章で何を artifact として積み上げるか把握する


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

### 2. 失敗の4類型: 誤答・忘却・破壊・停止
AIエージェントの失敗は、多くの場合 4 類型に収まる。

1. 誤答
   要件やドメインを取り違えたまま、それらしく答える失敗である。`sample-repo/docs/domain-overview.md` を読まずに検索改善を始めると、現行機能や制約を外した提案をしやすい。
2. 忘却
   途中で前提、制約、作業履歴を落とす失敗である。最初は `FEATURE-001` を見ていたのに、途中から別の前提で話し始めると、後半の変更が前半の意図とつながらなくなる。
3. 破壊
   一部を直した結果、別の動作や artifact を壊す失敗である。検索を改善したつもりでも、既存の assignee フィルタや docs の説明がずれれば、その変更は壊れている。
4. 停止
   途中まで進めて「終わった」と判断する失敗である。コードだけ変えて verify をしていない、docs を更新していない、影響範囲の確認が抜けている、という形で現れる。

この 4 類型は、単独ではなく連鎖する。誤答したまま進めば忘却が起きやすくなり、忘却したまま変更すると破壊し、破壊を見つける前に停止してしまう。AIエージェントが有能に見えるほど、この連鎖は見逃されやすい。

`sample-repo/docs/seed-issues.md` にある貫通ケースに当てはめると、次のように読める。

| 失敗類型 | `sample-repo` での典型例 | 最初に疑うべき不足 |
|---|---|---|
| 誤答 | `FEATURE-001` で検索要件を早合点する | 対象 issue とドメイン理解 |
| 忘却 | `FEATURE-002` で途中の判断や前提を落とす | task brief と progress note |
| 破壊 | `BUG-001` 修正で別の動作や docs を壊す | tests と変更影響範囲の確認 |
| 停止 | `HARNESS-001` で verify 前に完了扱いする | verification harness と done criteria |

### 3. Prompt Engineering / Context Engineering / Harness Engineering の対応表
4 類型の失敗を、気合いで減らすことはできない。必要なのは、どの失敗に対して何を設計するかを分けることである。本書ではそれを 3 段階の成熟モデルとして扱う。

| 成熟段階 | 主に減らす失敗 | 何を設計するか | この本で増やす代表 artifact |
|---|---|---|---|
| Prompt Engineering | 誤答 | 目的、制約、完了条件、出力期待 | prompt artifact、review checklist |
| Context Engineering | 忘却 | repo、task、session にまたがる前提情報 | task brief、context pack、AGENTS.md |
| Harness Engineering | 破壊・停止 | 実行境界、verify、再試行、証跡 | verify script、runbook、verification harness |

重要なのは、後ろの段階が前の段階を置き換えるのではなく、積み重なることだ。Prompt Engineering だけでは、うまい依頼は作れても、長時間の作業で前提を保持できない。Context Engineering を足しても、verify や停止条件がなければ、壊れた変更を「完了」と誤認する。だから本書は Prompt Engineering から始めて、Context Engineering、Harness Engineering へ進む。

この順番は、学習順でもあり、実務で事故率を下げる順でもある。まず「何をやらせるか」を決め、次に「何を見せ続けるか」を決め、最後に「どう実行と検証を閉じるか」を決める。

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

この依頼では、対象 issue、変更対象 artifact、完了条件、verify が抜けている。AIエージェントはもっともらしい提案や部分実装を返せるが、誤答、忘却、破壊、停止のどれも防げない。

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


## 章末まとめ
- AIエージェントは、会話で賢く見えても、誤答・忘却・破壊・停止で簡単に失敗する。
- 本書の対象は「もっともらしい出力」ではなく「artifact と verify を伴って仕事を完了させること」である。
- そのために Prompt Engineering、Context Engineering、Harness Engineering を順に積み上げる。次章ではまず Prompt Engineering から始める。
