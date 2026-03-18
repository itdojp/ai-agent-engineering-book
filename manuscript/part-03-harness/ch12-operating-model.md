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
CH09-CH11 で、single-agent harness、verification harness、long-running task と multi-agent の設計を見てきた。ここまで来ると、次の問題は技術より運用になる。誰が何を決めるのか。review 量をどう抑えるのか。AI slop をどう掃除するのか。どの指標で改善を判断するのか。これらが曖昧だと、個々の chapter や artifact が正しくても、チーム運用としては破綻しやすい。

CH12 では、AIエージェントをチームへ導入するための operating model を定義する。対象はモデル選定論ではなく、役割分担、review budget、repo hygiene、metrics、導入順序である。ここでの目的は、AIエージェントを「速く動く人手不足の代用品」にすることではない。人間が残す責務を明確にし、artifact-driven な作業をチームで継続できる形にすることだ。

## 学習目標
- 人間が残す責務を明確にできる
- review budget と throughput のトレードオフを説明できる
- repo hygiene と entropy cleanup の運用を設計できる


## 小見出し
### 1. 人間が残す責務
AIエージェントを導入しても、人間の責務は消えない。消えるのは定型作業の一部であり、責務そのものではない。`docs/operating-model.md` では、`Responsibilities` の下に `Human` と `Agent` を分けているが、実務で重要なのは次の 5 点を人間側に残すことである。

1. 目的と優先順位の決定
2. 破壊的変更と境界条件の承認
3. 設計上の重要判断
4. 最終レビューと merge 判断
5. repo hygiene の維持

一方、AIエージェントに任せやすいのは、既存 repo の探索、定型的な編集、test 追加、docs 草案、差分説明である。`ChatGPT` は要求整理や設計比較に向き、`Codex CLI` は repo を読んで変更し verify する作業に向く。この役割差を混ぜないことが operating model の第一歩になる。

ここでよくある失敗は、「agent がコードを書くなら設計判断も merge 判断も任せてよい」と考えることだ。これは高速化ではなく責任の空洞化である。CH12 の operating model では、AIエージェントは実行主体だが、責任主体ではない。

### 2. review budget と throughput
AIエージェント導入で最初に起きるボトルネックは実装速度ではなく review capacity である。生成速度が上がるほど、人間の review budget が詰まる。これを無視すると、未読 PR が溜まり、浅い review が増え、post-merge regression が増える。

CH12 では throughput を単純な PR 数では見ない。`docs/metrics.md` で扱うように、closed issues / week、PR cycle time、draft-to-merge time に加え、review budget の利用率を見る。たとえば「1 reviewer が 1 日に深く見られる PR は 2 本まで」「evidence bundle が必要な PR は同時に 1 本まで」のように、人的ボトルネックを明示する。

ここでの原則は、agent を速くする前に review を詰まらせないことだ。throughput を上げたいなら、PR を小さくし、work package を issue 単位に分け、PR template で review 入力を標準化する方が効く。`.github/pull_request_template.md` は、そのために `Goal`、`Changed Files`、`Verification`、`Evidence / Approval`、`Remaining Gaps` を強制する。

### 3. repo hygiene と AI slop 対策
AIエージェント運用では、良い差分だけでなく低品質な差分も高速に増える。この蓄積が AI slop である。AI slop は派手なバグだけではない。stale docs、path 切れ、孤立した task brief、verify script と実態のずれ、表記ゆれ、説明だけ厚いが使われない docs も含む。

`checklists/repo-hygiene.md` は、merge 前の確認項目と、週次の entropy cleanup を分けている。重要なのは「あとでまとめて掃除する」ではなく、普段の cadence に cleanup を組み込むことだ。AIエージェントは差分を増やすので、cleanup を担当する人と時間を決めないと repo はすぐ濁る。

repo hygiene を人間責務として残す理由はここにある。agent は stale docs の候補を見つけられても、どれを source of truth に戻すかは人間の判断が必要なことが多い。CH12 でいう hygiene は美観ではなく、次の agent が壊れずに動ける状態の維持である。

### 4. metrics とふりかえり
metrics は「AIエージェントが便利か」を測るためではない。運用が健全か、どこが詰まっているかを判断するために使う。`docs/metrics.md` では、Throughput、Quality、Hygiene の 3 群に分けている。

| 群 | 例 | 見たいこと |
|---|---|---|
| Throughput | closed issues / week、PR cycle time | work package が適切に小さいか |
| Quality | verify failure rate、post-merge regression count | review と verify が効いているか |
| Hygiene | stale docs count、orphaned task brief count | entropy cleanup が追いついているか |

重要なのは、指標を増やすことではなく、指標に対する行動を決めることだ。たとえば verify failure rate が高ければ prompt や brief の質を疑う。PR cycle time が長ければ review budget を疑う。stale docs count が増えれば hygiene cadence を疑う。metrics は責任追及ではなく、operating model の調整に使うべきである。

### 5. 導入ロードマップ
AIエージェント導入は、一気に全 repo へ広げるより段階導入が安全である。`docs/operating-model.md` では、導入を 3 段階で考える。

1. Pilot
   - 低リスクな docs / tests / scoped bugfix に限定する
2. Guided Delivery
   - issue、task brief、verify、PR template を標準化する
3. Team Scale
   - review budget、metrics、entropy cleanup を定例運用に入れる

この順に進めると、どの artifact が足りないかを小さく発見できる。いきなり multi-agent や広範囲の実装へ進むと、速度だけ上がってレビューと hygiene が崩れる。本 repo の `docs/release-plan.md` が M0 から M4 へ積み上げているのも同じ発想である。成熟度は機能量ではなく、artifact と運用の安定度で測るべきである。



## 章で使う bad / good example
bad:

```text
AIエージェントが速いので、issue の粒度を大きくし、review は人手が空いたときにまとめて行う。
docs の古さや表記ゆれは大きな問題ではないので後回しにする。
```

この運用では throughput だけが先に増え、review budget、repo hygiene、責務分担が崩れる。結果として PR は増えるが、merge 後の修正も増える。

good:

```text
1 issue = 1 work package を守る。
PR template で Goal / Changed Files / Verification / Evidence / Remaining Gaps を固定する。
人間は目的設定、承認、最終レビュー、entropy cleanup を担当する。
週次で metrics と repo hygiene を見直し、review budget を超える前に投入量を調整する。
```

この運用では、AIエージェントの速度を review と hygiene が支える。速さを成果に変える operating model になっている。

比較観点:
- bad は throughput だけを最適化している
- bad は review capacity と hygiene cost を無視している
- good は責務、cadence、metrics、cleanup を artifact 化している

## Worked Example
3 人チームでこの repo を運用する例を考える。役割は次の通りである。

- lead
  - issue 優先順位、破壊的変更の承認、最終 merge 判断を持つ
- operator
  - `ChatGPT` で要件整理、`Codex CLI` で実装・verify を進める
- reviewer
  - PR template と verification を見てレビューする

このチームでは、1 reviewer あたり同時に深く見られる PR を 2 本までとする。operator は `.github/pull_request_template.md` に従って PR を作り、verify と evidence を揃える。週次で `docs/metrics.md` の指標を見て、PR cycle time が延びていれば work package をさらに小さく切る。`checklists/repo-hygiene.md` は週次 cleanup で使い、stale docs や orphaned artifact を削る。

この例で分かるのは、導入の成否が「どのモデルを使ったか」ではなく、「役割と cadence が artifact で固定されているか」にかかっていることだ。CH12 の operating model は、技術選定ではなく運用設計の章である。

## 演習
1. 3人チーム向けの operating model を定義する。
2. 週次の entropy cleanup checklist を作る。

## 参照する artifact
- `docs/operating-model.md`
- `docs/metrics.md`
- `checklists/repo-hygiene.md`
- `.github/pull_request_template.md`


## 章末まとめ
- AIエージェント導入で残る人間責務は、目的設定、承認、最終レビュー、repo hygiene である。
- throughput を上げるには、モデルを速くするより review budget と work package を整える方が先である。
- operating model、metrics、repo hygiene、PR template を artifact にすると、Harness Engineering をチーム運用へ接続できる。
