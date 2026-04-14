---
id: ch12
title: 運用モデルと組織導入
status: draft
artifacts:
  - docs/operating-model.md
  - docs/metrics.md
  - checklists/repo-hygiene.md
  - .github/pull_request_template.md
dependencies:
  - ch09
  - ch10
  - ch11

---

# 運用モデルと組織導入

## この章の位置づけ
個々の run が成功しても、PR が詰まり、repo が荒れ、誰も最終責任を持たないなら導入は失敗である。CH09-CH11 で、single-agent harness、verification harness、long-running task と multi-agent の設計を見てきた。ここまで来ると、次の問題は技術より運用になる。

CH12 では、AIエージェントをチームへ導入するための operating model を定義する。対象はモデル選定論ではなく、役割分担、review budget、repo hygiene、metrics、導入順序である。ここでの目的は、AIエージェントを「速く動く人手不足の代用品」にすることではない。人間が残す責務を明確にし、artifact-driven な作業をチームで継続できる形にすることだ。

## 学習目標
- 人間が残す責務を明確にできる
- review budget と throughput のトレードオフを説明できる
- repo hygiene と entropy cleanup の運用を設計できる

## 小見出し
### 1. 人間が残す責務
AIエージェントを導入しても、人間の責務は消えない。消えるのは定型作業の一部であり、責務そのものではない。`docs/operating-model.md` では、runtime-managed capability と team-owned duty を分けたうえで、Human / Team と Agent の責務を整理している。

実務で人間側に残すべきなのは、次の 5 点である。

1. 目的と優先順位の決定
2. 破壊的変更と境界条件の承認
3. 設計上の重要判断
4. 最終レビューと merge 判断
5. repo hygiene の維持

一方、AIエージェントに任せやすいのは、既存 repo の探索、定型的な編集、test 追加、docs 草案、差分説明である。`ChatGPT` は要求整理や設計比較に向き、`Codex CLI` は repo を読んで変更し verify する作業に向く。この役割差を混ぜないことが operating model の第一歩になる。

ここでよくある失敗は、「agent がコードを書くなら設計判断も merge 判断も任せてよい」と考えることだ。これは高速化ではなく責任の空洞化である。CH12 の operating model では、AIエージェントは実行主体だが、責任主体ではない。Lead が承認と投入量を決め、Operator が verify と evidence を揃え、Reviewer が merge 可否を判定する。この分離があって初めて、速度を責任へ変換できる。

### 2. review budget と throughput
AIエージェント導入で最初に起きるボトルネックは実装速度ではなく review capacity である。生成速度が上がるほど、人間の review budget が詰まる。これを無視すると、未読 PR が溜まり、浅い review が増え、post-merge regression が増える。

CH12 では throughput を単純な PR 数では見ない。`docs/metrics.md` で扱うように、closed issues / week、PR cycle time、draft-to-merge time に加え、queue 診断や review quality に効く指標を見る。たとえば「1 reviewer が 1 日に深く見られる PR は 2 本まで」「evidence bundle が必要な PR は同時に 1 本まで」「レビュー待ち PR がどこで滞留しているか」といった人的ボトルネックを明示する。

ここでの原則は、agent を速くする前に review を詰まらせないことだ。throughput を上げたいなら、PR を小さくし、work package を issue 単位に分け、PR template で review 入力を標準化する方が効く。`.github/pull_request_template.md` は、そのために `Goal`、`Scope and Non-goals`、`Changed Files`、`Verification`、`Evidence / Approval`、`Remaining Gaps` を固定する。

さらに budget を超えたときの動作も operating model に含めるべきである。`docs/operating-model.md` では、新規 issue 着手を止め、stale draft / blocked PR を棚卸しし、verify 不足と evidence 不足を優先して潰す手順を `Budget Overflow Actions` として定義している。throughput を守るには、止め方まで artifact に落とす必要がある。

### 3. repo hygiene と AI slop 対策
AIエージェント運用では、良い差分だけでなく低品質な差分も高速に増える。この蓄積が AI slop である。AI slop は派手なバグだけではない。stale docs、path 切れ、孤立した task brief、verify script と実態のずれ、表記ゆれ、説明だけ厚いが使われない docs も含む。

`checklists/repo-hygiene.md` は、merge 前の確認項目と、週次の entropy cleanup を分けている。重要なのは「あとでまとめて掃除する」ではなく、普段の cadence に cleanup を組み込むことだ。AIエージェントは差分を増やすので、cleanup を担当する人と時間を決めないと repo はすぐ濁る。

repo hygiene を人間責務として残す理由はここにある。agent は stale docs の候補を見つけられても、どれを source of truth に戻すかは人間の判断が必要なことが多い。CH12 でいう hygiene は美観ではなく、次の agent が壊れずに動ける状態の維持である。`docs/operating-model.md` では、週次の `Weekly Review` に stale docs、orphaned task brief、missing evidence を cleanup backlog へ入れる手順まで含めている。

### 4. metrics と observability
metrics は「AIエージェントが便利か」を測るためではない。運用が健全か、どこが詰まっているかを判断するために使う。`docs/metrics.md` では、Throughput、Quality、Hygiene、Observability の 4 群に分けている。

| 群 | 例 | 見たいこと |
|---|---|---|
| Throughput | closed issues / week、PR cycle time、stale draft count | work package と review queue が適切か |
| Quality | verify failure rate、approval-stop rate、post-merge regression count | review と verification harness が効いているか |
| Hygiene | stale docs count、hygiene backlog age | entropy cleanup が追いついているか |
| Observability | queue wait time、trace coverage、evidence freshness failure | どこで詰まり、どこで説明責任が弱いか |

重要なのは、指標を増やすことではなく、指標に対する行動を決めることだ。verify failure rate が高ければ prompt や brief の質を疑う。PR cycle time が長ければ review budget を疑う。trace coverage が低ければ failure analysis の材料不足を疑う。evidence freshness failure が多ければ reviewer が current-run verify を確認できていないことを疑う。stale docs count と hygiene backlog age が悪化したら cleanup 専用 work package を先に開く。metrics は throughput 自慢ではなく、queue 診断、failure analysis、review quality 改善に使うべきである。

ここでいう trace coverage は、「trace.md があるか」だけではない。long-running task、handoff、retry、restart のように trace が必要な work package に対して、task / work-package id、run timestamp または run id、owner / handoff、retry / restart reason、verify reference、evidence linkage、redaction note の minimum trace reference contract が揃っているかを見る。これにより、historical trace と current-run verify の混同を避けながら、failure analysis に使える coverage を測れる。

### 5. 導入ロードマップ
AIエージェント導入は、一気に全 repo へ広げるより段階導入が安全である。`docs/operating-model.md` では、導入を 3 段階で考える。

1. Pilot
   - 低リスクな docs / tests / scoped bugfix に限定する
2. Guided Delivery
   - issue、task brief、verify、PR template を標準化する
3. Team Scale
   - review budget、metrics、entropy cleanup を定例運用に入れる

この順に進めると、どの artifact が足りないかを小さく発見できる。いきなり multi-agent や広範囲の実装へ進むと、速度だけ上がってレビューと hygiene が崩れる。本 repo の `docs/release-plan.md` が M0 から M4 へ積み上げているのも同じ発想である。成熟度は機能量ではなく、artifact と運用の安定度で測るべきである。各段階の exit criteria を先に決めることで、「導入したつもり」ではなく「次の段階へ進んでよい状態」を判定できる。

## 章で使う bad / good example
bad:

```text
AIエージェントが速いので、issue の粒度を大きくし、review は人手が空いたときにまとめて行う。
trace や verify log は細かすぎるので見ない。metrics は PR 数だけを見る。
```

この運用では throughput だけが先に増え、review budget、failure analysis、repo hygiene が崩れる。結果として PR は増えるが、merge 後の修正も増える。

good:

```text
1 issue = 1 work package を守る。
PR template で Goal、Scope and Non-goals、Changed Files、Verification、Evidence / Approval、Remaining Gaps を固定する。
人間は目的設定、承認、最終レビュー、entropy cleanup を担当する。
週次で metrics、trace、evidence freshness を見直し、review budget を超える前に投入量を調整する。
```

この運用では、AIエージェントの速度を review と hygiene が支える。速さを成果に変える operating model になっている。

比較観点:
- bad は throughput だけを最適化している
- bad は queue 診断、failure analysis、review quality を見ていない
- good は責務、cadence、metrics、cleanup を artifact 化している

## Worked Example
3 人チームでこの repo を運用する例を考える。役割は次の通りである。

- lead
  - issue 優先順位、破壊的変更の承認、最終 merge 判断を持つ
- operator
  - `ChatGPT` で要件整理、`Codex CLI` で実装・verify を進める
- reviewer
  - PR template と verification を見てレビューする

このチームでは、1 reviewer あたり同時に深く見られる PR を 2 本までとする。evidence bundle が必要な PR は reviewer ごとに 1 本まで、stale draft が 3 本を超えたら新規着手を止める。operator は `.github/pull_request_template.md` に従って PR を作り、verify と evidence を揃える。週次で `docs/metrics.md` の指標を見て、PR cycle time が延びていれば work package をさらに小さく切る。verify failure rate が増えていれば prompt / brief の質を見直す。trace coverage が落ちていれば long-running task の handoff を見直す。`checklists/repo-hygiene.md` は週次 cleanup で使い、stale docs や orphaned artifact を削る。

この例で分かるのは、導入の成否が「どのモデルを使ったか」ではなく、「役割と cadence が artifact で固定されているか」にかかっていることだ。CH12 の operating model は、技術選定ではなく運用設計の章である。

## 演習
1. 3人チーム向けの operating model を定義する。
2. 週次の entropy cleanup checklist を作る。

## 参照する artifact
- `docs/operating-model.md`
- `docs/metrics.md`
- `checklists/repo-hygiene.md`
- `.github/pull_request_template.md`

## Source Notes / Further Reading
- この章を探し直すときは、まず `docs/operating-model.md`、`docs/metrics.md`、`checklists/repo-hygiene.md`、`.github/pull_request_template.md` を正本として見る。導入判断はモデル比較ではなく、役割、review budget、queue 診断、cleanup の設計で読む。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH12 運用モデルと組織導入」と `manuscript/backmatter/01-読書案内.md` の「検証・信頼性・運用」を参照する。

## 章末まとめ
- AIエージェント導入で残る人間責務は、目的設定、承認、最終レビュー、repo hygiene である。
- throughput を上げるには、モデルを速くするより review budget と work package を整える方が先である。
- metrics と observability は throughput 自慢ではなく、queue 診断、failure analysis、review quality 改善のために使う。Prompt、Context、Harness を artifact と operating model に落とすと、AIエージェントは「賢そう」から「完了できる」へ近づく。
