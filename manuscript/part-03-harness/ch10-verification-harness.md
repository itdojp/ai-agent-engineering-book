---
id: ch10
title: Verification Harness を作る
status: draft
artifacts:
  - .github/workflows/verify.yml
  - checklists/verification.md
  - sample-repo/tests/test_ticket_search.py
  - artifacts/evidence/README.md
dependencies:
  - ch09

---

# Verification Harness を作る

## この章の位置づけ
test が green でも、reviewer が「何を確認すればよいか分からない」なら verify は閉じていない。CH09 では、single-agent harness の start condition、permission boundary、done criteria を定義した。だが `./scripts/verify-sample.sh` のような 1 本の verify command だけでは、まだ十分ではない。

ここで必要になるのが verification harness である。verification harness は、テスト、lint、typecheck、証跡収集、CI、approval gate を束ねた検証系であり、「変更した」ではなく「検証済みで説明可能である」を作るための artifact 群である。本章では support-hub を使い、最小の verification harness をどう設計するかを説明する。

## 学習目標
- local verify と CI verify の役割を分けられる
- verify matrix と evidence freshness の考え方を説明できる
- UI 変更時の evidence bundle を設計できる
- human approval をどこに置くか説明できる

## 小見出し
### 1. テストを書いてから触る
verification harness の起点は test である。理由は単純で、test がなければ「何が壊れていたか」「何が直ったか」「何を守りたいか」を機械的に判定できないからだ。特に bugfix と behavior change では、修正前に failing test を作るか、既存 test に不足している回帰 guard を補うことが必要になる。

`sample-repo/tests/test_ticket_search.py` は、`FEATURE-001` の検索仕様を verification artifact として固定する役割を持つ。`title`、`description`、`tags` の検索、空 query の全件返却に加え、query の大文字小文字を区別しないことも test で押さえる。CH03 で acceptance criteria を書くだけでは不十分で、それを regression guard に変換して初めて verification harness の一部になる。

ここでのポイントは、「test は実装の後に添える説明」ではなく「変更可能な仕様の実行形式」だということだ。AI agent に実装を任せるなら、spec と同じくらい test が source of truth になる。だから、変更前に test を確認し、必要なら先に足す。

### 2. verify matrix と実行順序
verification harness は、検証項目を 1 つの塊としてではなく、順序付きの matrix として設計する。一般には lint、typecheck、unit、integration、e2e の順で重くしていくのがよい。軽い失敗を先に落とすことで、無駄な実行時間を減らせるからだ。

この repo の現状は最小構成なので、実行しているのは主に unit test である。だが CH10 の論点は「今ある検証を厚く見せる」ことではない。将来 lint や typecheck が追加されても壊れない verification harness の考え方を先に定義することである。`checklists/verification.md` では、failing test、local verify、CI 反映、evidence、artifact update、approval を順に確認する checklist として整理した。

ここで重要なのは、verify matrix に owner と blocking 条件を持たせることだ。たとえば local verify は agent と開発者が高速に回す。CI verify は branch 上で同じ contract を再実行し、共有 gate にする。evidence review は reviewer が読む。approval は human reviewer が責任を持つ。すべてを 1 回の green に畳み込むのではなく、どの failure をどこで止めるかを分離する。

順序を決めておく利点は、agent が verify failure を分類しやすくなることにある。lint failure を抱えたまま e2e だけ見ても意味が薄い。逆に unit が落ちている段階で evidence bundle を集めても、まだ review-ready ではない。verification harness は、何を確認するかだけでなく、どの順で確認し、誰がその結果を消費するかまで artifact にする。

### 3. UI 変更の証跡と freshness
test が通っても、人間の reviewer が diff の妥当性を理解できるとは限らない。特に UI 変更では、見た目、操作順、before / after の差が log だけでは伝わらない。そこで verification harness には evidence bundle が必要になる。

`artifacts/evidence/README.md` では、evidence bundle を保存する目的、適用場面、推奨ディレクトリ構成、最低限の内容を定義した。基本は `summary.md`、`verify.log`、`repro.md`、必要なら `before.png` と `after.png` でよい。重要なのは豪華な資料を作ることではなく、「何を確認し、どの command を実行し、どの差分が user-visible だったか」を review 可能な単位で残すことだ。

2026 年の運用で特に重要なのは freshness である。evidence は存在するだけでは不十分で、current run の verify と結び付いていなければならない。古い screenshot、古い verify.log、別 branch の summary を流用すると、green check が付いていても reviewer は現行 diff を信じられない。evidence bundle は archive ではなく、現在の PR と verify chain を結び付ける artifact である。

support-hub は現時点で UI repo ではないため、CH10 の worked example では screenshot は使わない。しかし、HARNESS-001 や将来の UI 変更では、この evidence bundle が verify の一部になる。ここで先に場所と形式を決めておくことで、UI を触る段階で「どの証跡を残すべきか」が曖昧にならない。

### 4. CI と local verify の分担
local verify と CI verify は同じものではない。local verify は、agent や開発者が変更前後に高速に回す検証であり、CI verify は branch や PR に対して同じ検証を再現し、共有の合格ラインにする仕組みである。前者は iteration speed、後者は reproducibility を担当する。

`.github/workflows/verify.yml` では、book 側と sample-repo 側の検証を別 job に分けている。これは「どちらかが落ちた」ではなく、「どの harness が壊れたか」を CI で判別しやすくするためである。book manuscript の path 整合性と prompt eval artifact の整合確認と、sample-repo の test 実行は、どちらも verify だが failure mode は異なる。job を分けると、review も retry も速くなる。

ここで重要なのは、CI が local verify を置き換えるわけではないという点である。agent はまず local で `./scripts/verify-book.sh` や `./scripts/verify-sample.sh` を回す。その後、CI が同じ合格ラインを branch 上で再実行する。local と CI の command が意図的に違うなら、その差は checklist や PR summary で説明されなければならない。この二段構えが verification harness の基本になる。

### 5. human approval の位置
verification harness は完全自動化の話ではない。human approval をどこに置くかも設計対象である。approval が必要なのは、verify の成否だけでは決められない変更、または人間が責任を持つべき変更である。

CH10 の範囲では、approval を 3 箇所に置くと整理しやすい。

1. verify 前
   - public contract を変えるか
   - CI や verify script を変えるか
2. verify 後
   - evidence bundle が review に十分か
   - scope 外の影響が残っていないか
3. merge 前
   - PR summary、verification、`Remaining Gaps` が説明可能か

`checklists/verification.md` には、この approval 観点も含めてある。重要なのは「すべて人間確認に戻す」ことではない。機械で判定できる部分は harness に寄せ、人間が判断すべき部分だけを明示的に残すことだ。これにより、AI agent は verify をやり切りつつ、approval が必要な地点では止まれる。

## 章で使う bad / good example
bad:

```text
検索の修正を入れて `python -m unittest` が 1 回通った。
CI は後で見る。UI は触っていないつもりなので、証跡も不要とする。
```

この進め方では、どの test が回帰 guard なのか、CI で同じ検証が再現されるのか、evidence が本当に不要なのかが曖昧である。verify を「一度 green だった」という思い出にしてしまっている。

good:

```text
まず `sample-repo/tests/test_ticket_search.py` に回帰 guard を追加する。
次に `./scripts/verify-sample.sh` を local で回す。
CI は `.github/workflows/verify.yml` で同じ verify を再実行する。
UI 変更なら `artifacts/evidence/README.md` の形式で evidence bundle を残す。
approval が必要な変更は `checklists/verification.md` で分離する。
```

この進め方では、test、local verify、CI、evidence、approval が 1 つの harness としてつながっている。

比較観点:
- bad は verify を単発コマンドとして扱っている
- bad は CI と evidence の責務が曖昧である
- good は regression guard、共有 verify、review 証跡、approval gate を分離している

## Worked Example
`FEATURE-001` の ticket search を verification harness の題材にする。既存 spec では AC-4 として「query の大文字小文字は区別しない」と定義しているが、test 側にその guard が薄いと、将来の refactor で退行しやすい。

そこでまず `sample-repo/tests/test_ticket_search.py` に case-insensitive の test を追加する。これは新機能ではなく verification harness の強化である。次に local で `./scripts/verify-sample.sh` を実行し、search regression が守られていることを確認する。さらに CI では `.github/workflows/verify.yml` が book 側と sample 側を別 job で再実行し、branch 上でも同じ合格ラインを共有する。

この変更では UI は触っていないため screenshot は不要である。ただし reviewer に対しては、「どの acceptance criteria を test に落とし込んだか」「どの verify を回したか」を PR summary で説明する。もし今後 search UI を追加するなら、`artifacts/evidence/README.md` の形式に従い、before / after screenshot と verify log を束ねて evidence bundle を作る。

この worked example で重要なのは、verification harness が test だけでも CI だけでもないことだ。仕様の guard、実行順序、証跡、approval をまとめて設計して初めて、変更が review-ready になる。

## 紙面で押さえるポイント
### Verification Pipeline

| 段階 | 何を確認するか | 主な artifact / command | 読者が見るべきポイント |
|---|---|---|---|
| failing test | 壊れている仕様を executable にしたか | `sample-repo/tests/test_ticket_search.py` | acceptance criteria が regression guard に変わっているか |
| local verify | 手元で再現可能な最小合格ラインを満たすか | `./scripts/verify-sample.sh` | 変更直後に高速で回せるか |
| CI | branch 上で同じ検証を再実行できるか | `.github/workflows/verify.yml` | local と共有合格ラインがずれていないか |
| evidence | reviewer が差分を再確認できるか | `artifacts/evidence/README.md` | 何を確認し、何を残すかが明示されているか |
| approval | 人間が判断すべき論点だけ残っているか | `checklists/verification.md` | verify で自動化しない判断が分離されているか |

この表の狙いは、verification harness を「test の話」だけに縮めないことである。`failing test` で仕様 guard を作り、`local verify` と `CI` で再現性を担保し、最後に `evidence` と `approval` で review-ready にする。読者はこの 5 段階を紙面上で追えば、repo を開かなくても harness の全体像を把握できる。

## 演習
1. failing test を先に足してから修正する。
2. UI 変更に対する evidence bundle を作る。

## 参照する artifact
- `.github/workflows/verify.yml`
  book 側と sample 側の job 分離を見る。CI が local verify をどう共有合格ラインに変えるかを確認する。
- `checklists/verification.md`
  verify と approval を同じ checklist 上でどう分離しているかを見る。CH10 の最終段に対応する。
- `sample-repo/tests/test_ticket_search.py`
  acceptance criteria を regression guard に変換した例として読む。worked example の起点になる。
- `artifacts/evidence/README.md`
  evidence bundle の最低構成を確認する。UI 変更時に何を残すべきかの参照先である。

## Source Notes / Further Reading
- この章を探し直すときは、まず `.github/workflows/verify.yml`、`checklists/verification.md`、`sample-repo/tests/test_ticket_search.py`、`artifacts/evidence/README.md` を正本として見る。verification harness は test、CI、evidence、approval の流れで読む。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH10 Verification Harness を作る」と `manuscript/backmatter/01-読書案内.md` の「検証・信頼性・運用」を参照する。

## 章末まとめ
- verification harness は、test、実行順序、evidence、CI、approval gate を束ねた検証系である。
- local verify は iteration speed、CI verify は reproducibility を担当し、どちらも必要である。
- verify chain ができると、次に壊れるのは 1 session では閉じない仕事である。次章では long-running task と multi-agent の分割条件を扱う。
