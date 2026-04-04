# Prompt テンプレート集

本書の Prompt Engineering は、気の利いた言い回しを探す作業ではない。単一タスクを安定して完了させるために、入力、制約、完了条件、出力形式を固定する作業である。この appendix では、そのために使う最小テンプレートをまとめる。

Prompt テンプレートは、実装や review を始める前の作業境界を決めるために使う。長い説明を書くことが目的ではない。曖昧さを残さず、verify 可能な単位で task を切ることが目的である。

## 1. Prompt Contract Template

`templates/prompt-contract.md` は、単一タスク向けの Prompt Contract の骨格である。CH02 で扱ったとおり、ここで大切なのは「何をしてほしいか」より、「何を入力として使い、何をしてはいけず、どこまで終われば完了か」を固定することである。

Template の各 section は次の役割を持つ。

- `Objective`: 達成すべき結果を 1 文で固定する
- `Inputs`: 参照すべき issue、spec、test、verify command を列挙する
- `Constraints`: 既存契約、scope、更新必須 artifact を制限する
- `Tool Contract`: 実行してよい command と外部接続の境界を固定する
- `Approval Gate`: human approval が必要な操作を明示する
- `Forbidden Actions`: 推測でやってはいけない変更を先に止める
- `Missing Information Policy`: input 不足時に止まる条件と、仮定を置く条件を分ける
- `Refusal / Stop Conditions`: 続行せず停止すべき条件を定義する
- `Completion Criteria`: 完了判定を verify 可能な言葉で書く
- `Output Schema`: output version と必須 section を固定する
- `Output Format`: 最終報告の見出しを固定する

たとえば bugfix なら `prompts/bugfix-contract.md`、feature なら `prompts/feature-contract.md` が実例になる。どちらも `Objective` と `Completion Criteria` は異なるが、`Tool Contract`、`Approval Gate`、`Refusal / Stop Conditions`、`Output Schema` を含む構造は同じである。まず構造を固定し、その後に task 固有の差分だけを入れる。

最小の埋め方は次のようになる。

```md
## Objective
既存仕様を保ったまま、対象不具合の根本原因を特定し、最小差分で修正する。

## Inputs
- issue または task brief
- 再現手順
- 関連 test
- verify command

## Constraints
- public interface を変更しない
- failing test を先に追加または更新する

## Tool Contract
- 許可された verify / build / test コマンドだけを実行する
- 明示されていない外部接続、依存追加、secret 利用は行わない

## Approval Gate
- 依存追加、破壊的変更、secret 利用、権限拡張は human approval を待つ

## Forbidden Actions
- 無関係な refactor を混ぜない
- verify を省略しない

## Refusal / Stop Conditions
- 必須 input が足りず、低リスクの仮定も置けない場合は停止する
- source of truth が競合する場合は競合箇所を列挙して停止する

## Completion Criteria
- 修正前は失敗し、修正後は成功する test がある
- 指定 verify が通る

## Output Schema
- output_version: `2026-04-01`
- required_sections:
  - Root Cause
  - Changed Files
  - Verification
  - Remaining Gaps
```

Prompt Contract を書くときは、「実行前に agent を止める条件」と「実行後に完了を判断する条件」の両方を書く。片方しかない prompt は、指示としては読めても契約としては弱い。

## 2. Prompt Rubric Template

`templates/prompt-rubric.md` は、prompt の良し悪しを比較するための rubric である。Prompt Engineering を偶然や好みに戻さないために使う。CH04 で扱ったように、prompt を改善したかどうかは、eval case と rubric で判断する。

rubric では、`checklists/prompt-contract-review.md` と同じ観点を最低限そろえるとよい。

- `Goal clarity`: 何を達成する prompt かが明確か
- `Input completeness`: 必要 artifact や source of truth が不足していないか
- `Constraint clarity`: 守るべき境界が書かれているか
- `Forbidden action clarity`: 壊れやすい逸脱を明示的に禁止しているか
- `Verifiability`: 完了条件が verify 可能か
- `Output format specificity`: 最終出力が review しやすい形に固定されているか
- `Approval gate clarity`: human approval が必要な操作が明示されているか
- `Stop condition clarity`: 止まるべき条件が先に定義されているか

実務では 0 から 2 の三段階で十分なことが多い。重要なのは細かい採点ではなく、「前の prompt より何が改善したか」を case ごとに説明できることだ。rubric がないと、出力がたまたま良かった prompt を保存してしまい、次回の regression に気づけない。

## 3. 実務での使い分け

Prompt Contract と Prompt Rubric は役割が違う。

- Prompt Contract は task を実行させるための artifact
- Prompt Rubric は prompt を評価し比較するための artifact

先に Contract を作り、次に Rubric で評価する順にすると、目的と評価軸がずれにくい。逆に rubric だけ先に作ると、「何の task を安定化したいのか」が曖昧なまま採点だけが増えやすい。

本書の流れでは、Prompt Contract は Prompt Engineering の中核であり、Context Engineering ではない。task を取り巻く repo 情報や session 情報は後続の appendix と chapter で扱う。appendix A の範囲では、単一タスクを安定して遂行する prompt artifact に集中すればよい。

## 参照する artifact

- `templates/prompt-contract.md`
- `templates/prompt-rubric.md`
- `prompts/bugfix-contract.md`
- `prompts/feature-contract.md`
