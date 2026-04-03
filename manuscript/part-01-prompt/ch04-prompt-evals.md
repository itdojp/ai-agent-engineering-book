---
id: ch04
title: プロンプトを評価する
status: draft
artifacts:
  - evals/prompt-contract-cases.json
  - evals/rubrics/feature-spec.json
  - scripts/run-prompt-evals.py
dependencies:
  - ch02
  - ch03

---

# プロンプトを評価する

## この章の位置づけ
昨日うまくいった prompt が、今日も同じように当たる保証はない。CH02 で Prompt Contract を定義し、CH03 で曖昧要求を実装準備ができた artifact に変換した。ここで次の問題が出る。どの prompt が本当に良いのかを、どう判断するのか。

Prompt Engineering を実務にするには、prompt quality を評価対象にしなければならない。必要なのは、eval case、rubric、回帰チェック、version comparison である。CH04 では、prompt を folklore ではなく engineering artifact として扱うための最小評価系を説明する。

## 学習目標
- eval case、rubric、judge / human spot-check を分けて設計できる
- prompt の回帰比較に加え、workflow metrics と trace review を評価軸へ入れられる
- モデル更新時の比較観点として品質、tool-call、cost / latency、approval signal を列挙できる


## 小見出し
### 1. 良い prompt / workflow は評価できる
Prompt の品質は、印象ではなく挙動で判断する。たとえば `FEATURE-001` 向けの prompt が 1 回だけうまく動いても、それは prompt が良い証拠にならない。入力がたまたま簡単だっただけかもしれないし、モデルが都合よく補完しただけかもしれない。工学的に見るべきなのは、似た仕事で安定するか、境界条件で壊れないか、更新後に退行しないかである。

2026 年版では、評価対象を prompt 単体に閉じない。Prompt Contract が良くても、tool call の選択、approval 待ちの入り方、trace の残し方、cost / latency の扱いが悪ければ、仕事全体としては壊れる。そこで本章では、prompt-level evaluation を基礎にしつつ、workflow-level evaluation まで射程を広げる。

| 観点 | 見たいもの | この章で扱うか |
|---|---|---|
| Prompt-level evaluation | 目的、制約、完了条件、出力 schema が安定して出るか | 扱う |
| Workflow-level evaluation | tool call、approval、trace、evidence が安定して閉じるか | 扱う |
| Context-level evaluation | 適切な artifact を継続的に参照できるか | 後続章で深掘りする |
| Harness-level evaluation | verify、再試行、再開、evidence capture が機能するか | 後続章で深掘りする |

良い prompt / workflow は評価できる。逆に言えば、評価できない prompt / workflow は改善も version 管理もできない。

### 2. eval set の作り方
eval set は、prompt や workflow を困らせる入力の一覧である。ただし、ランダムに集めればよいわけではない。作るべきなのは、失敗しやすい入力、境界条件、スコープ逸脱、approval 待ち、報告形式崩れ、tool misuse を誘う入力である。

`evals/prompt-contract-cases.json` では、`feature-contract` と `bugfix-contract` に対して複数のケースを定義する。見るべき観点は次のとおりである。

- `FEATURE-001` の scope を保てるか
- 仕様が粗いときに不足情報を明示できるか
- docs / acceptance criteria / ADR まで artifact を同期対象として扱えるか
- structured output と output version を守れるか
- approval が必要な操作で止まれるか
- `BUG-001` で regression guard を維持できるか
- 修正後の報告形式を固定できるか

実務での作り方は次の順でよい。

1. 失敗モードを列挙する
   - scope creep
   - missing information
   - artifact 更新漏れ
   - verify 条件の欠落
   - approval boundary の逸脱
   - tool misuse
   - cost / latency の無駄打ち
2. 各失敗モードに 1 ケース以上割り当てる
3. `must_include` と `must_not_include` を決める
4. prompt 変更時に同じケースを再利用する

失敗が見つかったら、その失敗を再現するケースを追加する。これが prompt / workflow regression check の基本になる。

### 3. rubric・golden・judge・human spot-check の違い
prompt の評価では、golden と rubric を分けて考える必要がある。golden は、期待出力をほぼ固定文字列で持つ方式である。rubric は、満たすべき観点を採点軸として持つ方式である。

| 方式 | 向いている対象 | 弱点 |
|---|---|---|
| golden | 固定フォーマット、固定文言、短い出力 | wording の揺れに弱い |
| rubric | 仕様整理、設計比較、構造化された自由記述 | 人間または採点ロジックの設計が要る |

CH03 で扱った product spec や ADR のような出力は、自由記述を含む。ここで全文一致の golden を使うと、内容が妥当でも言い回しが違うだけで落ちやすい。そこで CH04 では rubric を中心にする。`evals/rubrics/feature-spec.json` には、Objective、Scope、Inputs、Constraints、Completion、Missing Information、Output Format に加え、approval boundary と structured output の観点を定義した。

この rubric が見るのは、「模範解答と同じ文章か」ではない。「実装準備ができた artifact として使える構造になっているか」である。prompt evaluation を engineering discipline に寄せるには、文才ではなく構造と判定可能性を評価する必要がある。

golden が不要という意味ではない。たとえば Output Format の見出し順や固定セクション名は golden に向く。しかし、仕様の妥当性や scope の切り方は rubric の方が扱いやすい。実務では両者を併用するが、CH04 の中心は rubric に置く。

### 4. prompt の回帰テストと trace review
prompt を 1 行変えたら、前に通っていたケースが落ちることがある。だから prompt も回帰テストが必要である。やることはコードの regression check と同じだ。同じ eval set を、prompt の v1 と v2 に当て、差分を見る。

この repo では `scripts/run-prompt-evals.py` を最小実装として置いている。現時点ではモデル呼び出し自体は行わず、次の整合性をチェックする。

- Prompt Contract に必要な見出しが揃っているか
- `evals/prompt-contract-cases.json` のケース定義が壊れていないか
- `evals/rubrics/feature-spec.json` の criterion 定義が壊れていないか

これは full eval runner ではないが、評価資産を repo に乗せて保守する第一歩として有効である。2026 年版では、ここに trace review と workflow metrics を接続する前提を明示する。つまり、prompt regression だけでなく、次のような signal も見る。

- tool call が想定どおりの境界に収まっているか
- approval 待ちに入るべき run が自律実行されていないか
- cost / latency が異常に増えていないか
- evidence と trace が reviewer に再確認可能な形で残っているか

実際の regression check は、同じ suite を v1 と v2 に流す形で行う。たとえば `feature-contract` の v1 が不足情報への扱いを書いていなかったとする。v2 で `Missing Information Policy` を追加したら、`feature-001-missing-info` ケースで改善し、他のケースが落ちていないかを見る。trace review は、その回帰差分を evidence として読むための補助線である。

### 5. versioning と比較運用
prompt の version comparison では、「どちらが好きか」を議論しない。同じ cases、同じ rubric、できれば同じモデル条件で比較する。比較時に見るべき観点は 5 つである。

1. pass 数が増えたか
2. 重大な fail の種類が減ったか
3. structured output と approval boundary が安定したか
4. tool-call / trace の振る舞いが改善したか
5. cost / latency のばらつきが減ったか

ここで重要なのは、総合点だけで判断しないことだ。平均点が少し上がっても、approval gate を飛ばすようになったら採用すべきではない。逆に latency が少し増えても、重大 fail が減るなら受け入れる価値がある。

比較記録には、少なくとも次を残す。

- prompt version
- model / runtime version
- eval suite version
- rubric version
- tool / approval policy version

これができると、「なぜ先週は通って今週は落ちたか」を説明できる。versioning の対象は prompt だけではなく、workflow contract 全体である。

## 章で使う bad / good example
bad:

```text
この prompt は昨日 1 回うまくいった。だから十分に良い prompt だ。
```

この判断は folklore であり、評価ではない。ケースの偏り、モデルの偶然、入力の簡単さを区別できず、prompt 変更後の退行も検出できない。

good:

```text
`evals/prompt-contract-cases.json` にある 6 件を固定の eval set とする。
`evals/rubrics/feature-spec.json` の rubric で v1 と v2 を比較する。
`feature-001-missing-info`、`feature-001-approval-boundary`、`bugfix-001-regression-guard` を重要ケースとして、改善と退行を個別に記録する。
```

この進め方は、prompt を engineering artifact として扱っている。同じ入力集合と同じ評価軸を使うため、変更の良し悪しを再現可能に比較できる。

比較観点:
- bad は単発成功を品質と取り違えている
- good は eval case、rubric、approval boundary を固定している
- good は回帰、trace review、version comparison を前提にしている

## Worked Example
`sample-repo` の `FEATURE-001` を題材に、feature prompt の v1 と v2 を比較する。v1 は次の弱さを持つとする。

- 仕様が粗いときの扱いが曖昧
- artifact 同期の指示が弱い
- scope creep を防ぐ非目標が弱い

そこで v2 では、`Missing Information Policy`、`docs と tests を同時に更新する`、`仕様外の UI / API 変更をしない`、`Approval Gate` を明示した。この変更を評価するために、`evals/prompt-contract-cases.json` のうち次の 4 ケースを見る。

1. `feature-001-scope`
   - ranking や typo correction を今回の必須要件にしないか
2. `feature-001-missing-info`
   - 不足情報を列挙して停止または `Open Questions` に残せるか
3. `feature-001-artifact-sync`
   - product spec、acceptance criteria、ADR を同期対象として扱えるか
4. `feature-001-approval-boundary`
   - approval 必須操作で止まり、承認なしに外部接続や依存追加へ進まないか

採点には `evals/rubrics/feature-spec.json` を使う。期待する改善は次の通りである。

| 観点 | v1 で起きやすい失敗 | v2 で見たい改善 |
|---|---|---|
| Scope | ranking を勝手に追加する | Non-goals を保つ |
| Missing Information | 曖昧な要件を補完してしまう | 不足情報を明示する |
| Artifacts | docs 更新が抜ける | spec / acceptance / ADR を列挙する |
| Approval Boundary | 承認が必要な操作へ自律実行で進む | approval gate と停止条件を返す |

この worked example で重要なのは、prompt の良さを文章の雰囲気で語らないことだ。同じケースで比較し、何が改善し、何が未解決かを観点ごとに記録する。これが prompt evaluation を engineering discipline に変える。

## 演習
1. `feature-contract` 向けに 5 件の eval case を作りなさい。少なくとも `scope creep`、`missing information`、`artifact sync` を 1 件ずつ含めること。
2. 同じ feature task に対して prompt v1 / v2 を比較する記録テンプレートを作りなさい。case ごとの pass/fail、重大 fail、観察メモを残せる形にすること。

## 参照する artifact
- `evals/prompt-contract-cases.json`
- `evals/rubrics/feature-spec.json`
- `scripts/run-prompt-evals.py`


## Source Notes / Further Reading
- この章を探し直すときは、まず `evals/prompt-contract-cases.json`、`evals/rubrics/feature-spec.json`、`scripts/run-prompt-evals.py` を正本として見る。prompt の良し悪しは雰囲気ではなく、case と rubric の差分で判断する。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH04 プロンプトを評価する」と `manuscript/backmatter/01-読書案内.md` の「Prompt と要求定義」を参照する。

## 章末まとめ
- 良い prompt は、単発の成功ではなく eval case、rubric、回帰チェックで判断する。
- prompt evaluation の中心は、再現可能な入力集合と、構造を判定する評価軸を持つことにある。
- prompt / workflow が評価できるようになると、次に壊れるのは前提保持である。次章からは Context Engineering に入り、何を見せ続けるかを設計する。
