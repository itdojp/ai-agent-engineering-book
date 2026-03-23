---
id: ch02
title: プロンプトを契約として設計する
status: draft
artifacts:
  - prompts/bugfix-contract.md
  - prompts/feature-contract.md
  - checklists/prompt-contract-review.md
dependencies:
  - ch01

---

# プロンプトを契約として設計する

## この章の位置づけ
CH01 では、AIエージェントが失敗する理由を誤答、忘却、破壊、停止の 4 類型で整理した。ここから Prompt Engineering に入る。最初の論点は単純である。prompt を「うまい言い回し」ではなく「入出力契約」として扱うことだ。

実務の prompt は、雑談用のメッセージではない。coding agent に単一タスクを実行させるための作業指示であり、目的、入力、制約、禁止事項、完了条件、出力形式を固定する artifact である。これが曖昧だと、AIエージェントはそれらしい説明を返しても、仕事の境界を誤解する。single-task reliability を上げる最初の手段は、prompt を契約として設計することにある。

## 学習目標
- 目的・制約・完了条件・禁止事項を分離して書ける
- bad prompt / good prompt を評価軸付きで比較できる
- feature と bugfix で異なる Prompt Contract を作れる


## 小見出し
### 1. prompt は命令文ではなく入出力契約
「検索を改善して」「バグを直して」のような prompt でも、AIエージェントは何かしら返す。しかし、返答があることと、契約が成立していることは別である。契約としての prompt には、最低でも次の 2 つが必要だ。第一に、何を達成すべきかが明確であること。第二に、何をしてよく、何をしてはいけないかが observable な条件で書かれていることだ。

実務の prompt は、要件書の代用品ではないが、実行境界を決める最小の契約である。たとえば `sample-repo` の `BUG-001` を扱うなら、「既存挙動を壊さずに不具合を修正する」が Objective になり、「public interface を変えない」「failing test を先に追加または更新する」が Constraints になる。ここで重要なのは、モデルにうまく頼むことではなく、作業境界を誤読できないようにすることだ。

この章では prompt を次の 6 要素で扱う。

| 要素 | 役割 | ないと何が起きるか |
|---|---|---|
| Objective | 仕事の目的を 1 文で固定する | 何を優先すべきかぶれる |
| Inputs | 参照すべき artifact と情報源を固定する | 誤答しやすくなる |
| Constraints | 守るべき条件を固定する | 勝手な拡張や破壊が起きる |
| Forbidden Actions | 近道や危険な行動を禁止する | 見かけ上の成功が増える |
| Completion Criteria | 完了判定を固定する | 停止が起きる |
| Output Format | 報告粒度を固定する | レビューと handoff が不安定になる |

この 6 要素が揃って初めて、prompt は「命令文」ではなく「作業契約」になる。

### 2. 目的・制約・完了条件・禁止事項の分離
Prompt Contract の中心は、項目を混ぜないことにある。現場で弱い prompt が壊れやすいのは、Goal、Constraints、Done が一段落に混ざっているからだ。混ざると、AIエージェントは重要度を解釈で補うしかなくなる。

`prompts/bugfix-contract.md` と `prompts/feature-contract.md` は、その分離を示す最小テンプレートである。bugfix では「既存挙動を壊さない」「failing test を先に追加または更新する」が強い制約になる。一方 feature では「仕様外の UI / API 変更をしない」「acceptance criteria を満たす」が中心になる。同じ repo を触る作業でも、契約の重心は異なる。

各項目は次の観点で書くとよい。

| 項目 | 書き方 | 例 |
|---|---|---|
| Objective | 1 文で仕事の目的を書く | `既存仕様を保ったまま、対象不具合の根本原因を特定し、最小差分で修正する。` |
| Inputs | 参照元を列挙する | `対象 issue`, `再現手順`, `関連 test`, `verify コマンド` |
| Constraints | 破ってはいけない条件を書く | `public interface を変更しない` |
| Forbidden Actions | やりがちな危険行動を禁止する | `failing test を削除して green にしない` |
| Completion Criteria | 終了条件を verify 可能に書く | `修正前は失敗し、修正後は成功する test がある` |
| Output Format | 最終報告の形を固定する | `Files Changed`, `Verification`, `Remaining Risk` |

制約と禁止事項を分けるのも重要である。制約は「守るべき条件」、禁止事項は「やってはいけない近道」を書く。たとえば「仕様外の UI / API 変更をしない」は制約であり、「曖昧な要件を推測で確定しない」は禁止事項である。前者は境界、後者は failure mode を防ぐための明示的なガードだ。

### 3. 仮定の置き方と不足情報の扱い
良い Prompt Contract は、すべての情報を持っている必要はない。重要なのは、不足情報があるときの振る舞いを曖昧にしないことだ。弱い prompt は、情報が足りないと AIエージェントに「よしなに補完」させる。これが誤答の入り口になる。

たとえば `FEATURE-001` の検索改善で product spec がまだ粗い場合、feature prompt に書くべきなのは「不足情報は仮定として列挙し、仕様を確定した事実として扱わない」である。ここでやりたいのは Context Engineering ではなく、単一タスクの中で危険な推測を防ぐことだ。

single-task reliability の観点では、不足情報への対処は次の 3 パターンに分けるとよい。

1. 既存 artifact から解決できる
   `sample-repo` の docs や test を読めば分かるなら、その artifact を Inputs に入れる。
2. 仮定を置いて進められる
   仮定を箇条書きにし、Output Format に含める。
3. 仮定を置くと危険
   その場で止まり、不足情報として報告する。

ここで大切なのは、「分からない場合の正しい挙動」も Prompt Contract に含めることだ。AIエージェントは止まるべき場面を与えられないと、埋め草の説明で穴をふさぎやすい。後続章では task brief や context pack で情報不足を減らすが、CH02 の段階ではまず、prompt 自体に推測の扱いを埋め込む。

### 4. bad prompt / good prompt の比較
弱い prompt と operational prompt の差は、文体ではなく契約密度にある。次の bad prompt を見る。

```text
sample-repo の検索を改善して。使いやすくして、必要ならテストも追加して。
```

この依頼は一見自然だが、契約としては弱い。何が Objective なのか曖昧で、何を Inputs として読むべきか分からず、Constraints と Completion Criteria がない。そのため、AIエージェントは「検索しやすくする」という抽象語を自分なりに解釈し、仕様外の変更や中途半端な停止に向かいやすい。

これを operational prompt にすると、次のようになる。

```text
対象は `sample-repo/docs/seed-issues.md` の `FEATURE-001` とする。
Objective: 既存 public contract を保ったまま、チケット検索機能を仕様に沿って改善する。
Inputs:
- `sample-repo/docs/product-specs/ticket-search.md`
- `sample-repo/docs/acceptance-criteria/ticket-search.md`
- `sample-repo/docs/design-docs/ticket-search-adr.md`
- `sample-repo/tests/test_ticket_search.py`
Constraints:
- 仕様外の UI / API 変更をしない
- docs と tests を同時に更新する
Forbidden Actions:
- acceptance criteria にない機能追加をしない
- 曖昧な要件を推測で確定しない
Completion Criteria:
- acceptance criteria を満たす
- 主要 happy path と edge case の test がある
- 指定 verify が通る
Output Format:
1. Implemented Scope
2. Files Changed
3. Verification
4. Open Questions
```

この prompt は、まだ十分に短い。しかし、single-task reliability に必要な骨格は揃っている。読み手が人間でも AIエージェントでも、何をすべきか、どこまでがスコープか、何をもって完了とするかが分かる。

つまり、弱い prompt は「何かをやってくれ」と頼む文であり、operational prompt は「何を、何で、どこまで、どう報告するか」を固定する文である。

### 5. プロンプトレビューの観点
Prompt Contract は、書いただけでは不十分である。実行前にレビューし、弱い箇所を潰す必要がある。`checklists/prompt-contract-review.md` は、そのための最小チェックリストである。

レビューでは、文の美しさより failure mode を見つける。観点は多くない。

1. Objective が 1 文で定義されているか
2. Inputs が artifact レベルで特定されているか
3. Constraints が observable か
4. Forbidden Actions が危険な近道を塞いでいるか
5. Completion Criteria が verify 可能か
6. Output Format がレビューしやすいか

この観点で見ると、weak prompt はすぐに見抜ける。たとえば「必要なら docs も直して」は Constraints ではなく裁量の押し付けである。「うまくやって」「いい感じに」も同様で、レビュー不能な語を残している。逆に、Objective、Inputs、Completion Criteria が固定されていれば、多少文体が素朴でも operational prompt として機能する。

Prompt Engineering の第一歩は、名文を書くことではない。レビュー可能な Prompt Contract を作り、single-task reliability を上げることだ。次章では、この契約を前提にして、ChatGPT を使った要件整理と設計判断に進む。



## 章で使う bad / good example
bad:

```text
BUG-001 を直して。既存挙動は壊さないように、必要ならテストも見て対応して。
```

この prompt は対象 issue しか固定していない。再現条件、関連 artifact、禁止事項、完了条件、出力形式がなく、作業境界を AIエージェント側の解釈に委ねている。

good:

```text
対象は `sample-repo/docs/seed-issues.md` の `BUG-001` とする。
Objective: 既存 public interface を変えずに不具合を再現・修正する。
Inputs:
- 再現条件
- 関連ファイル
- `sample-repo/tests/test_service.py`
- verify コマンド
Constraints:
- failing test を先に追加または更新する
- 影響範囲は最小にする
Forbidden Actions:
- 無関係なリファクタリングをしない
- failing test を削除して green にしない
Completion Criteria:
- 修正前は失敗し、修正後は成功する test がある
- 既存 test と指定 verify が通る
Output Format:
1. Root Cause
2. Files Changed
3. Verification
4. Remaining Risk
```

この修正版は、bugfix の境界を契約として明示している。Prompt Contract は長文化のためではなく、失敗しやすい判断点を先回りして固定するために書く。

比較観点:
- bad は「どう直したら完了か」が書かれていない
- good は Inputs、Forbidden Actions、Completion Criteria が明示されている
- good は single-task reliability を上げるための報告形式まで固定している

## 演習
1. `sample-repo` の検索改善を題材に、「検索を追加して」という依頼文を Prompt Contract に書き換えなさい。Objective、Inputs、Constraints、Forbidden Actions、Completion Criteria、Output Format を必ず含めること。
2. `BUG-001` を題材に、Completion Criteria だけを 5 項目で書きなさい。各項目は verify 可能な文にすること。

## 参照する artifact
- `prompts/bugfix-contract.md`
- `prompts/feature-contract.md`
- `checklists/prompt-contract-review.md`


## Source Notes / Further Reading
- この章を探し直すときは、まず `prompts/bugfix-contract.md`、`prompts/feature-contract.md`、`checklists/prompt-contract-review.md` を正本として見る。Prompt Contract は会話のコツではなく repo に残す contract artifact である。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH02 プロンプトを契約として設計する」と `manuscript/backmatter/01-読書案内.md` の「Prompt と要求定義」を参照する。

## 章末まとめ
- Prompt Engineering の出発点は、prompt を曖昧な命令文ではなく入出力契約として設計することにある。
- single-task reliability を上げるには、Objective、Inputs、Constraints、Forbidden Actions、Completion Criteria、Output Format を分けて書く必要がある。
- weak prompt と operational prompt の差は文才ではなく契約密度で決まる。次章では、この Prompt Contract を前提に ChatGPT で要件と設計を固める。
