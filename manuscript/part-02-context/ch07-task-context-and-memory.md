---
id: ch07
title: Task Context と Session Memory
status: draft
artifacts:
  - sample-repo/tasks/FEATURE-001-brief.md
  - sample-repo/tasks/FEATURE-001-progress.md
  - docs/session-memory-policy.md
  - .github/ISSUE_TEMPLATE/task.yml
dependencies:
  - ch05
  - ch06

---

# Task Context と Session Memory

## この章の位置づけ
issue を reopen した翌朝に「前回どこまで決まっていたか」が読めないなら、repo context が整っていても作業は始められない。CH06 で repo 全体の context を整えた。だが、repo context だけでは「今回の issue で何をやるか」「前回どこまで進んだか」は決まらない。

この章では、issue を task brief に変換する手順、`Progress Note` の書式、handoff と restart の最低入力、summary drift を避ける方法を扱う。対象は `sample-repo` の `FEATURE-001` だが、考え方は原稿作業にもそのまま使える。

## 学習目標
- GitHub issue を task brief に変換できる
- `Progress Note` に最低限必要な項目を理解する
- summary drift を防ぐ手順を設計できる


## 小見出し
### 1. issue を task brief に変換する
GitHub issue は、人間同士でスコープを共有するには十分でも、AI agent に実行させるには粗いことが多い。`.github/ISSUE_TEMPLATE/task.yml` も、Goal、Deliverables、Acceptance Criteria という最低限の入力しか持たない。これをそのまま実装に渡すと、参照すべき artifact、禁止事項、verify、out-of-scope が抜けやすい。

そこで issue を task brief に変換する。`sample-repo/tasks/FEATURE-001-brief.md` は、source、goal、scope、inputs、deliverables、constraints、acceptance criteria、verification、open questions、out of scope を持っている。これは issue を長文化したものではなく、AI agent が work item として扱える形に正規化したものである。

変換時のポイントは 2 つある。第一に、repo context と重複させないこと。architecture や coding standards を task brief に書き直す必要はない。第二に、done と verify を明示すること。task brief は issue の解説ではなく、実行契約である。

### 2. `Progress Note` の書式
task brief が stable な task context だとすると、`Progress Note` は mutable な session context である。`sample-repo/tasks/FEATURE-001-progress.md` と `docs/session-memory-policy.md` では、`Current Goal`、`Completed`、`Decided`、`Open Questions`、`Changed Files`、`Last Verify`、`Resume Steps`、`Next Step` を必須項目としている。`Status` のような短い状態表示を置いてもよいが、それは quick scan 用の補助であり、source of truth ではない。

この書式の狙いは、前回の会話ログを読まなくても再開できることにある。重要なのは、`Progress Note` に全部を書くことではない。brief に既にある Goal や Constraints を重複させず、今回のセッションで新しく確定したことだけを積み上げる。`Decided` は verify または artifact で確認済みの事実、`Open Questions` は未確定の論点、と役割を分けるのが要点である。

`Progress Note` がないと、AI agent は「前回どこまでやったか」を chat history に依存する。これは session を跨いだ瞬間に壊れる。Session Memory は、会話ではなく artifact に残す必要がある。

### 3. handoff と restart の設計
handoff で必要なのは、全文サマリーではなく、再開手順である。`docs/session-memory-policy.md` は「Resume Packet の最低入力」として、task brief、最新 `Progress Note`、最新 verify 結果、再開時に読むべきファイル一覧の 4 点を定義している。本章では、この最小 packet を `Restart Packet（Resume Packet）` と呼ぶ。これは最小だが十分である。

`FEATURE-001` を例にすると、途中で作業者が交代しても、次の担当者は `FEATURE-001-brief.md` を読んで scope を確認し、`FEATURE-001-progress.md` で前回の `Decided` と `Open Questions` を見て、最後に verify を回せば再開できる。逆に「前回はだいたい検索仕様の話をしていた」程度の handoff では、どこまで確定したかが分からず、同じ議論をやり直すことになる。

handoff とは、長い経緯説明ではない。次の AI agent が同じ canonical artifact に戻れるようにすることである。

### 4. summary drift を避ける
summary drift は、セッションを跨ぐほど増える。主な原因は、未検証の仮説が事実として要約に混ざること、task brief の内容を `Progress Note` が勝手に言い換えること、verify 前後の状態を混ぜることである。

たとえば `FEATURE-001` の `Progress Note` に「search と status / assignee filter は統合予定」と書くのは危険である。現時点では open question であり、task brief にも acceptance criteria にもない。これを `Decided` に入れると、次のセッションがそれを実装義務だと誤解する。正しくは `Open Questions` に置き、scope 変更が承認されたら brief と spec を更新してから `Decided` に移すべきである。

summary drift を避けるには、要約より source of truth を優先する。Acceptance Criteria は brief から原文で引用し、verify 結果は pass / fail を明示し、推測は未確定のまま隔離する。Session Memory は短いほどよいが、短ければ何でもよいわけではない。

### 5. セッション再開時の最低入力
再開時に必要なのは、前回会話の全文ではない。順序を付けるなら次の 4 つで十分である。

1. task brief で Goal、Constraints、Acceptance Criteria、Verification を確認する
2. `Progress Note` で前回の `Decided`、`Open Questions`、`Next Step` を確認する
3. 最新 verify 結果を確認し、必要なら再実行して live context を取り直す
4. `Resume Steps` に従って対象ファイルを開く

この順序が有効なのは、stable な task context から mutable な session context へ降りる構造になっているからである。いきなり `Progress Note` や chat history から入ると、scope の土台が抜けやすい。CH05 の原則どおり、stale-safe な artifact を先に読み、live context を後から取りにいく。

Task Context と Session Memory の設計ができると、AI agent は「前回の会話が見えないから止まる」という failure mode をかなり減らせる。



## 紙面で押さえるポイント
### Restart Packet 最小形

| issue 側の入力 | task brief / session memory で増やすもの | 再開時に確認する要点 |
|---|---|---|
| `Goal` | `Goal` と `Scope` | そもそも何を終わらせる task か |
| `Deliverables` | `Deliverables` と `Inputs` | どの artifact が完了物で、何を読むか |
| `Acceptance Criteria` | `Acceptance Criteria`、`Verification`、`Out of Scope` | 何を満たせば done で、何はやらないか |
| 会話で決まった追加事項 | `Decided`、`Open Questions`、`Next Step` | 前回の session で何が確定し、何が未決か |

再開時の最小 packet は 4 点でよい。ここではこれを `Restart Packet（Resume Packet）` と呼ぶ。`task brief`、最新 `Progress Note`、最新 `verify`、再開時に開くファイル一覧である。これが揃っていれば、前回の会話全文を読まなくても scope と次の 1 手を復元できる。逆にこの 4 点が欠けると、AI agent は chat history を source of truth と誤認しやすい。

## 章で使う bad / good example
bad:

```text
Issue の本文は読んだ。
前回は検索の話をしていたはずなので、その続きとして実装を進める。
必要になったら test を見る。
```

このやり方では、scope、verify、未解決点、前回の確定事項がどこにも固定されていない。セッションを跨いだ瞬間に summary drift が起きる。

good:

```text
まず `sample-repo/tasks/FEATURE-001-brief.md` を読み、Goal、Constraints、
Acceptance Criteria、Verification を確認する。
次に `sample-repo/tasks/FEATURE-001-progress.md` を読み、
`Decided` と `Open Questions` を分けて確認する。
最後に最新 verify を取り直し、`Resume Steps` の順でファイルを開く。
```

この修正版では、issue から task brief へ変換された canonical artifact を起点にし、`Progress Note` は session memory として限定的に使っている。

比較観点:
- bad は issue と session memory の差を潰している
- bad は verify と open question を固定していない
- good は stable な brief と mutable な `Progress Note` を役割分担している

## 演習
1. GitHub issue を task brief に変換する。
2. 中断した作業に対して、`Progress Note` を起点に task brief と verify 結果を含む `Restart Packet（Resume Packet）` を作りなさい。読む順番も書くこと。

## 参照する artifact
- `sample-repo/tasks/FEATURE-001-brief.md`
  issue を task brief に正規化した実例として読む。CH07 では Scope、Inputs、Verification の増分を見る。
- `sample-repo/tasks/FEATURE-001-progress.md`
  session memory の実例として読む。`Decided` と `Open Questions` をどう分離しているかを確認する。
- `docs/session-memory-policy.md`
  `Progress Note` の必須項目と `Resume Packet` の最低入力を確認する。本章ではこれを `Restart Packet（Resume Packet）` として扱い、本文の再開手順と照らし合わせて読む。
- `.github/ISSUE_TEMPLATE/task.yml`
  GitHub issue 側の最小入力を確認する。brief で何を補っているかを比較する起点になる。


## Source Notes / Further Reading
- この章を探し直すときは、まず `sample-repo/tasks/FEATURE-001-brief.md`、`sample-repo/tasks/FEATURE-001-progress.md`、`docs/session-memory-policy.md` を正本として見る。ポリシーでは `Resume Packet` と呼ぶ最小 packet を、本章では `Restart Packet（Resume Packet）` として扱う。summary だけでなく最新 verify とセットで読む。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH07 Task Context と Session Memory」と `manuscript/backmatter/01-読書案内.md` の「Context と repo 設計」を参照する。

## 章末まとめ
- issue はそのままでは task context として粗い。AI agent に渡す前に task brief へ正規化する必要がある。
- session memory は chat history ではなく `Progress Note` と verify 証跡で管理する。
- task と session の state を分けられると、次はそれを毎回書き直さず再利用する段階になる。次章では skill と context pack を扱う。
