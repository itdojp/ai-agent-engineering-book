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
CH02 で Prompt Contract を定義し、CH03 で曖昧要求を実装準備ができた artifact に変換した。ここで次の問題が出る。どの prompt が本当に良いのかを、どう判断するのか。1 回うまくいった prompt を「完成」とみなすのは、工学ではなく偶然に依存した運用である。

Prompt Engineering を実務にするには、prompt quality を評価対象にしなければならない。必要なのは、eval case、rubric、回帰チェック、version comparison である。CH04 では、prompt を folklore ではなく engineering artifact として扱うための最小評価系を説明する。

## 学習目標
- eval case と rubric を分けて設計できる
- prompt の回帰テストを自動実行できる
- モデル更新時の比較観点を列挙できる


## 小見出し
### 1. 良い prompt は評価できる
Prompt の品質は、印象ではなく挙動で判断する。たとえば `FEATURE-001` 向けの prompt が 1 回だけうまく動いても、それは prompt が良い証拠にならない。入力がたまたま簡単だっただけかもしれないし、モデルが都合よく補完しただけかもしれない。工学的に見るべきなのは、似た仕事で安定するか、境界条件で壊れないか、更新後に退行しないかである。

この章でいう評価は、prompt-level evaluation に限定する。つまり、Prompt Contract や要件整理 prompt に対して、どの入力で、どの観点を満たすべきかを定義する。Context Engineering や Harness Engineering の評価は後続章で扱う。

評価対象を分けると、Prompt Engineering の責務が明確になる。

| 観点 | 見たいもの | この章で扱うか |
|---|---|---|
| Prompt-level evaluation | 目的、制約、完了条件、出力形式が安定して出るか | 扱う |
| Context-level evaluation | 適切な artifact を継続的に参照できるか | まだ扱わない |
| Harness-level evaluation | verify、再試行、証跡収集が機能するか | まだ扱わない |

良い prompt は評価できる。逆に言えば、評価できない prompt は改善も version 管理もできない。

### 2. eval set の作り方
eval set は、prompt を困らせる入力の一覧である。ただし、ランダムに集めればよいわけではない。作るべきなのは、失敗しやすい入力、境界条件、スコープ逸脱を誘う入力、報告形式が崩れやすい入力である。

`evals/prompt-contract-cases.json` では、`feature-contract` と `bugfix-contract` に対して 5 件のケースを定義した。たとえば次の観点が入っている。

- `FEATURE-001` の scope を保てるか
- 仕様が粗いときに不足情報を明示できるか
- docs / acceptance criteria / ADR まで artifact を同期対象として扱えるか
- `BUG-001` で regression guard を維持できるか
- 修正後の報告形式を固定できるか

eval case は、理想入力ではなく壊れやすい入力から作る方が有効である。理由は簡単で、単純なケースだけで評価すると、prompt の弱さが見えないからだ。`feature-contract` なら「検索を使いやすくしたい」のような曖昧依頼だけでなく、「仕様はまだ粗い」「ついでに ranking も欲しい」といった scope creep や missing information を含むケースを入れるべきである。

実務での作り方は次の順でよい。

1. 失敗モードを列挙する
   - scope creep
   - missing information
   - artifact 更新漏れ
   - verify 条件の欠落
2. 各失敗モードに 1 ケース以上割り当てる
3. `must_include` と `must_not_include` を決める
4. prompt 変更時に同じケースを再利用する

eval set は一度作って終わりではない。失敗が見つかったら、その失敗を再現するケースを追加する。これが prompt regression check の基本になる。

### 3. rubric と golden の違い
prompt の評価では、golden と rubric を分けて考える必要がある。golden は、期待出力をほぼ固定文字列で持つ方式である。rubric は、満たすべき観点を採点軸として持つ方式である。

| 方式 | 向いている対象 | 弱点 |
|---|---|---|
| golden | 固定フォーマット、固定文言、短い出力 | wording の揺れに弱い |
| rubric | 仕様整理、設計比較、構造化された自由記述 | 人間または採点ロジックの設計が要る |

CH03 で扱った product spec や ADR のような出力は、自由記述を含む。ここで全文一致の golden を使うと、内容が妥当でも言い回しが違うだけで落ちやすい。そこで CH04 では rubric を中心にする。`evals/rubrics/feature-spec.json` には、Objective、Scope、Inputs、Constraints、Completion、Missing Information、Output Format という観点を定義した。

この rubric が見るのは、「模範解答と同じ文章か」ではない。「実装準備ができた artifact として使える構造になっているか」である。prompt evaluation を engineering discipline に寄せるには、文才ではなく構造と判定可能性を評価する必要がある。

golden が不要という意味ではない。たとえば Output Format の見出し順や固定セクション名は golden に向く。しかし、仕様の妥当性や scope の切り方は rubric の方が扱いやすい。実務では両者を併用するが、CH04 の中心は rubric に置く。

### 4. prompt の回帰テスト
prompt を 1 行変えたら、前に通っていたケースが落ちることがある。だから prompt も回帰テストが必要である。やることはコードの regression check と同じだ。同じ eval set を、prompt の v1 と v2 に当て、差分を見る。

この repo では `scripts/run-prompt-evals.py` を最小実装として置いている。現時点ではモデル呼び出し自体は行わず、次の整合性をチェックする。

- Prompt Contract に必要な見出しが揃っているか
- `evals/prompt-contract-cases.json` のケース定義が壊れていないか
- `evals/rubrics/feature-spec.json` の criterion 定義が壊れていないか

これは full eval runner ではないが、評価資産を repo に乗せて保守する第一歩として有効である。prompt evaluation を運用に乗せるには、まず cases と rubric が壊れていない状態を保つ必要があるからだ。

実際の regression check は、同じ suite を v1 と v2 に流す形で行う。たとえば `feature-contract` の v1 が不足情報への扱いを書いていなかったとする。v2 で `Missing Information Policy` を追加したら、`feature-001-missing-info` ケースで改善し、他のケースが落ちていないかを見る。この考え方が prompt versioning の核になる。

### 5. versioning と比較運用
prompt の version comparison では、「どちらが好きか」を議論しない。同じ cases、同じ rubric、できれば同じモデル条件で比較する。比較時に見るべき観点は 3 つである。

1. pass 数が増えたか
2. 重大な fail の種類が減ったか
3. 出力のばらつきが減ったか

ここで重要なのは、総合点だけで判断しないことだ。総合点が同じでも、scope creep を防げる prompt の方が実務では安全な場合がある。逆に、平均点が少し上がっても、`BUG-001` の regression guard を落とすなら採用すべきではない。

運用としては、次の単位で比較すると扱いやすい。

- prompt v1 vs v2
- 同一 prompt + model update 前後
- 同一 prompt + rubric 更新前後

つまり、比較対象は prompt だけではない。モデルが変われば prompt の出方も変わるし、rubric を厳しくすれば pass/fail も変わる。だから比較記録には、prompt version、model version、eval suite version、rubric version を残すべきである。これができると、「なぜ先週は通って今週は落ちたか」を説明できる。



## 章で使う bad / good example
bad:

```text
この prompt は昨日 1 回うまくいった。だから十分に良い prompt だ。
```

この判断は folklore であり、評価ではない。ケースの偏り、モデルの偶然、入力の簡単さを区別できず、prompt 変更後の退行も検出できない。

good:

```text
`evals/prompt-contract-cases.json` にある 5 件を固定の eval set とする。
`evals/rubrics/feature-spec.json` の rubric で v1 と v2 を比較する。
`feature-001-missing-info` と `bugfix-001-regression-guard` を重要ケースとして、改善と退行を個別に記録する。
```

この進め方は、prompt を engineering artifact として扱っている。同じ入力集合と同じ評価軸を使うため、変更の良し悪しを再現可能に比較できる。

比較観点:
- bad は単発成功を品質と取り違えている
- good は eval case、rubric、重点ケースを固定している
- good は回帰と version comparison を前提にしている

## Worked Example
`sample-repo` の `FEATURE-001` を題材に、feature prompt の v1 と v2 を比較する。v1 は次の弱さを持つとする。

- 仕様が粗いときの扱いが曖昧
- artifact 同期の指示が弱い
- scope creep を防ぐ非目標が弱い

そこで v2 では、`Missing Information Policy`、`docs と tests を同時に更新する`、`仕様外の UI / API 変更をしない` を明示した。この変更を評価するために、`evals/prompt-contract-cases.json` のうち次の 3 ケースを見る。

1. `feature-001-scope`
   - ranking や typo correction を今回の必須要件にしないか
2. `feature-001-missing-info`
   - 不足情報を列挙して停止または `Open Questions` に残せるか
3. `feature-001-artifact-sync`
   - product spec、acceptance criteria、ADR を同期対象として扱えるか

採点には `evals/rubrics/feature-spec.json` を使う。期待する改善は次の通りである。

| 観点 | v1 で起きやすい失敗 | v2 で見たい改善 |
|---|---|---|
| Scope | ranking を勝手に追加する | Non-goals を保つ |
| Missing Information | 曖昧な要件を補完してしまう | 不足情報を明示する |
| Artifacts | docs 更新が抜ける | spec / acceptance / ADR を列挙する |

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
- この章では prompt-level evaluation までを扱った。次章からは Context Engineering に入り、prompt だけでは足りない情報設計を扱う。
