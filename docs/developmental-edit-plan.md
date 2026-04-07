# Developmental Edit Plan

## Goal

CH01-CH12 を、template に従って情報が並ぶ原稿ではなく、読者が「次の failure を減らすためにこの章が要る」と感じながら読み進められる原稿へ寄せる。

## Rewrite Contract (2026)

2026 年版の rewrite では、章本文の言い換えだけでなく、商用運用に耐える判断基準と supporting artifact を揃えることを優先する。具体的には次を固定する。

- Prompt → Context → Harness の成熟モデルを、chapter と appendix を跨いで同じ語彙で運用する
- `support-hub` と recurring case を、全 Part の共通ケースとして維持する
- artifact-driven pedagogy を崩さず、各章で `何を読むか` ではなく `何を残すか` を明確にする
- UI や product 名の一時的な差分より、権限境界、verify、handoff、resume の durable な設計を優先する

## Source Hierarchy

記述が競合したときの優先順位を先に固定する。

1. runtime の挙動、権限、protocol、pricing は official docs と組織ポリシーを優先する
2. recurring case と artifact の責務は、本文と `sample-repo` を source of truth とする
3. 用語と命名は `docs/glossary.md` を正本にする

この方針により、2026 年の product update を追いながらも、本文の設計原則と artifact contract を安定させる。

## Part-level Deliverables

| Part | 章 | 先に固定する artifact | 主に下げる failure |
|---|---|---|---|
| Prompt | CH01-CH04 | Prompt Contract、spec、acceptance criteria、eval case | 曖昧要求の誤読、出力契約の崩壊 |
| Context | CH05-CH08 | repo context、task brief、Progress Note、context pack | 前提喪失、参照迷子、再開失敗 |
| Harness | CH09-CH12 | verify checklist、done criteria、restart protocol、operating model | verify 前停止、越権、handoff 不全 |

## Work Package Tracking

rewrite は章単位ではなく work package 単位で閉じる。現時点の tracking は次のとおり。

| WP | Issue | State | 代表的な deliverable |
|---|---|---|---|
| WP-01 | `#154` | Closed | front matter / glossary / editorial baseline |
| WP-02 | `#155` | Closed | CH01-CH04 と prompt contract / eval artifacts |
| WP-03 | `#156` | Closed | CH05-CH08 と context artifacts |
| WP-04 | `#157` | Closed | CH09-CH12 と harness artifacts |
| WP-05 | `#158` | Open | appendix / backmatter / source notes / figure policy |
| WP-06 | `#159` | Closed | sample-repo / templates / EN parity / verify support |

work package を閉じる判断は、issue コメントだけでなく repo 上の tracking docs でも再確認できるようにする。

## Verification Gate

rewrite 系 PR は、対象範囲に応じて次の検証を通す。

- 章本文、front matter、appendix、backmatter の更新: `./scripts/verify-book.sh`
- `sample-repo/`、`prompts/`、`checklists/`、`evals/` に触れる更新: `./scripts/verify-sample.sh`
- GitHub Pages 公開内容または `docs/` に影響する更新: `./scripts/verify-pages.sh`

verify を通せない場合は、未解決点を issue または PR に明示し、黙って完了扱いにしない。

## Opening 方針

- 冒頭は `CHxx では...` より先に、読者が現場で遭遇する失敗や詰まり方を置く
- hook は大げさな物語ではなく、`sample-repo` と recurring case に接続した実務上の痛みで作る
- 章の technical core は 2 段落目以降で明示し、hook と役割説明を分ける

## Closing / Bridge 方針

- 章末の最後は、内容の再掲ではなく「この章で何が固定され、次にどこが bottleneck になるか」を言い切る
- bridge は Part を跨ぐ境界で特に強く書く。CH04 から CH05、CH08 から CH09 は maturity model の段差を明示する
- CH12 は次章予告で閉じず、Prompt / Context / Harness が team 運用へ閉じるところまで言い切る

## 重複説明の削減方針

- failure model の定義は CH01 に固定し、後続章では必要な failure だけ短く再参照する
- Prompt Engineering の責務説明は CH02-CH04 に閉じ、CH05 以降は境界確認にとどめる
- Context Engineering の責務説明は CH05-CH08 に閉じ、CH09 以降は「何を読むか」より「どう実行と検証を閉じるか」を前面に出す
- artifact の定義は glossary と appendix を正本にし、各章では今回必要な役割だけを再説明する

## Chapter Plan

| 章 | opening で先に置く pain | closing で明示する payoff / bridge |
|---|---|---|
| CH01 | 会話では賢いのに repo 作業で崩れる落差 | 次に fix すべき最初の層は Prompt Contract である |
| CH02 | 1 行の依頼で勝手な拡張や verify 抜けが起きる | 契約の次に詰まるのは要求の曖昧さである |
| CH03 | exploratory dialogue を仕様だと誤認する | 仕様 artifact が揃ったら prompt を評価対象にできる |
| CH04 | 昨日当たった prompt が今日も当たる保証はない | 次に壊れるのは前提保持なので Context へ進む |
| CH05 | 良い prompt と eval があっても古い docs を読むと外す | context の種類が分かったら repo 入口を固定する |
| CH06 | repo に入った直後に agent が迷う | repo context の次は task 単位の context である |
| CH07 | reopen 後に前回の state が読めない | task / session が分かれたら再利用単位へ昇格する |
| CH08 | 同じ workflow を毎回書き直すと再現性が落ちる | 再利用単位が揃ったら Harness へ進む |
| CH09 | brief があっても verify 前停止や越権が起きる | 起動と終了が固まったら verification chain が必要になる |
| CH10 | test が green でも reviewer が信じられない | verify chain の次は長時間タスクの分割である |
| CH11 | 長時間タスクを 1 本で抱えると state が壊れる | 長時間タスクを閉じたら team 運用へ接続する |
| CH12 | 個々の run は成功しても team 運用は崩れる | Prompt / Context / Harness を operating model へ閉じる |
