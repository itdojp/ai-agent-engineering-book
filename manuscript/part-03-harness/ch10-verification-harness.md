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

ここで必要になるのが verification harness である。verification harness は、テスト、lint、typecheck、証跡収集、CI、approval gate を束ねた検証系であり、「変更した」ではなく「検証済みで説明可能である」を作るための artifact 群である。本章では support-hub を使い、最小の verification harness をどう設計するかを説明する。特に、verify log、trace、evidence bundle、metrics を別物として扱いながらつなぐことを明確にする。

## 学習目標
- local verify と CI verify の役割を分けられる
- UI 変更時の evidence bundle を設計できる
- human approval をどこに置くか説明できる

## 小見出し
### 1. テストを書いてから触る
verification harness の起点は test である。理由は単純で、test がなければ「何が壊れていたか」「何が直ったか」「何を守りたいか」を機械的に判定できないからだ。特に bugfix と behavior change では、修正前に failing test を作るか、既存 test に不足している回帰 guard を補うことが必要になる。

`sample-repo/tests/test_ticket_search.py` は、`FEATURE-001` の検索仕様を verification artifact として固定する役割を持つ。`title`、`description`、`tags` の検索、空 query の全件返却に加え、query の大文字小文字を区別しないことも test で押さえる。CH03 で acceptance criteria を書くだけでは不十分で、それを regression guard に変換して初めて verification harness の一部になる。

ここでのポイントは、「test は実装の後に添える説明」ではなく「変更可能な仕様の実行形式」だということだ。AI agent に実装を任せるなら、spec と同じくらい test が source of truth になる。だから、変更前に test を確認し、必要なら先に足す。

### 2. verify matrix と実行順序
verification harness は、検証項目を 1 つの塊としてではなく、順序付きの pipeline として設計する。一般には lint、typecheck、unit、integration、e2e の順で重くしていくのがよい。軽い失敗を先に落とすことで、無駄な実行時間を減らせるからだ。

この repo の現状は最小構成なので、実行しているのは主に unit test である。だが CH10 の論点は「今ある検証を厚く見せる」ことではない。将来 lint や typecheck が追加されても壊れない verification harness の考え方を先に定義することである。`checklists/verification.md` では、failing test、local verify、CI 反映、evidence、artifact update、approval を順に確認する checklist として整理した。

ここで重要なのは、この verification pipeline に owner と blocking 条件を持たせることだ。たとえば local verify は agent と開発者が高速に回す。CI verify は branch 上で同じ contract を再実行し、共有 gate にする。evidence review は reviewer が読む。approval は human reviewer が責任を持つ。すべてを 1 回の green に畳み込むのではなく、どの failure をどこで止めるかを分離する。

順序を決めておく利点は、agent が verify failure を分類しやすくなることにある。lint failure を抱えたまま e2e だけ見ても意味が薄い。逆に unit が落ちている段階で evidence bundle を集めても、まだ review-ready ではない。verification harness は、何を確認するかだけでなく、どの順で確認し、誰がその結果を消費するかまで artifact にする。

### 3. verify log、trace、evidence bundle の違い
verification harness では、似た証跡を同じ名前で呼ばないことが重要である。少なくとも次の 3 つは分けて扱う。

- verify log: current-run の command、timestamp、結果を残すログ
- trace: session や run をまたいだ履歴、状態遷移、handoff の記録
- evidence bundle: reviewer が差分を確認できるように束ねた成果物

verify log は freshness が命である。昨日の green log は、今日の current-run verify にはならない。trace は逆に historical artifact であり、長時間タスクや失敗分析で「どう進んだか」を見るためのものだ。evidence bundle は reviewer-facing であり、verify log や trace の抜粋、repro、screenshot を必要な範囲で束ねる。つまり、current-run verify と historical trace は役割が違い、evidence bundle はその両方を review のために整形した artifact である。

`artifacts/evidence/README.md` では、evidence bundle を保存する目的、適用場面、推奨ディレクトリ構成、最低限の内容を定義した。2026 年の運用で特に重要なのは freshness である。evidence は存在するだけでは不十分で、current run の verify と結び付いていなければならない。古い screenshot、古い verify.log、別 branch の summary を流用すると、green check が付いていても reviewer は現行 diff を信じられない。evidence bundle は archive ではなく、現在の PR と verify chain を結び付ける artifact である。

trace coverage を metrics に使うなら、trace も自由記述のメモでは足りない。少なくとも review で trace を参照するときは、minimum trace reference contract を満たしている必要がある。必要なのは複雑な tracing system ではなく、次の 7 項目で十分である。

| 項目 | 役割 |
|---|---|
| task / work-package identifier | どの task を指す trace かを識別する |
| run timestamp または run identifier | どの実行の trace かを current-run verify と結び付ける |
| owner / handoff | 誰が実行し、handoff があれば誰へ渡したかを示す |
| retry / restart reason | なぜ再試行や再開が発生したかを示す |
| verify reference | どの current-run verify に対応する trace かを示す |
| evidence linkage | review でどの evidence bundle から参照されているかを示す |
| redaction / privacy note | 秘匿化や省略がある場合に、その影響を説明する |

この contract があれば、reviewer は「この trace が何を指しているか」を判断できる。逆に、run id も verify 参照もない trace は historical memo にはなっても、trace coverage を測る対象にはしにくい。CH10 の範囲では、trace は current-run verify を置き換えず、verify を説明しやすくする参照 artifact として扱う。

### 4. CI と local verify の分担
local verify と CI verify は同じものではない。local verify は、agent や開発者が変更前後に高速に回す検証であり、CI verify は branch や PR に対して同じ検証を再現し、共有の合格ラインにする仕組みである。前者は iteration speed、後者は reproducibility を担当する。

`.github/workflows/verify.yml` では、book 側と sample-repo 側の検証を別 job に分けている。これは「どちらかが落ちた」ではなく、「どの harness が壊れたか」を CI で判別しやすくするためである。book manuscript の path 整合性と prompt eval artifact の整合確認と、sample-repo の test 実行は、どちらも verify だが failure mode は異なる。job を分けると、review も retry も速くなる。

observability はここで verification harness に接続される。CI job の成否、verify log の freshness、trace 上の retry 回数、evidence bundle の有無は、すべて後の failure analysis や review quality の材料になる。observability は別チームの監視機能ではなく、verification harness の一部である。

### 5. human approval の位置
verification harness は完全自動化の話ではない。human approval をどこに置くかも設計対象である。approval が必要なのは、verify の成否だけでは決められない変更、または人間が責任を持つべき変更である。

CH10 の範囲では、approval を 3 箇所に置くと整理しやすい。

1. verify 前
   - public contract を変えるか
   - CI や verify script を変えるか
2. verify 後
   - evidence bundle が review に十分か
   - verify log が current-run のものか
   - trace や screenshot に redaction / privacy consideration が必要か
3. merge 前
   - PR summary、Verification、`Remaining Gaps` が説明可能か

`checklists/verification.md` には、この approval 観点も含めてある。重要なのは「すべて人間確認に戻す」ことではない。機械で判定できる部分は harness に寄せ、人間が判断すべき部分だけを明示的に残すことだ。これにより、AI agent は verify をやり切りつつ、approval が必要な地点では止まれる。

## 章で使う bad / good example
bad:

```text
検索の修正を入れて `python -m unittest` が 1 回通った。
昨日の verify log も残っているので、だいたい安全と判断する。
trace と evidence は同じものとして扱い、必要になったら後で探す。
```

この進め方では、current-run verify と historical artifact の境界が曖昧である。reviewer は、何が今の結果で、何が過去の履歴かを判断できない。

good:

```text
まず `sample-repo/tests/test_ticket_search.py` に回帰 guard を追加する。
次に `./scripts/verify-sample.sh` を local で回し、current-run の verify log を残す。
必要なら trace に retry や handoff の履歴を残す。
review 用には `artifacts/evidence/README.md` の形式で evidence bundle を作り、
verify log と trace 参照を整理する。
redaction / privacy consideration が必要な情報は bundle 化の前に除く。
```

この進め方では、test、current-run verify、historical trace、review 証跡が 1 つの harness としてつながっている。

比較観点:
- bad は current-run verify と historical trace を混同している
- bad は evidence の freshness と redaction を管理していない
- good は verify log、trace、evidence bundle を役割ごとに分離している

## Worked Example
`FEATURE-001` の ticket search を verification harness の題材にする。既存 spec では AC-4 として「query の大文字小文字は区別しない」と定義しているが、test 側にその guard が薄いと、将来の refactor で退行しやすい。

そこでまず `sample-repo/tests/test_ticket_search.py` に case-insensitive の test を追加する。これは新機能ではなく verification harness の強化である。次に local で `./scripts/verify-sample.sh` を実行し、search regression が守られていることを確認する。この current-run の結果は verify log として残す。さらに CI では `.github/workflows/verify.yml` が book 側と sample 側を別 job で再実行し、branch 上でも同じ合格ラインを共有する。

この変更では UI は触っていないため screenshot は不要である。ただし reviewer に対しては、「どの acceptance criteria を test に落とし込んだか」「どの verify を回したか」を PR summary で説明する。長時間タスクや flaky な再現手順が絡むなら、trace で retry や handoff を残し、必要な抜粋だけを evidence bundle に入れる。

この worked example で重要なのは、verification harness が test だけでも CI だけでもないことだ。仕様の guard、current-run verify、historical trace、review 証跡、approval をまとめて設計して初めて、変更が review-ready になる。

## 紙面で押さえるポイント
### Verification Artifact Matrix

| artifact | 主な役割 | 鮮度 | 主な利用者 |
|---|---|---|---|
| verify log | current-run の command と結果を示す | もっとも短い | agent、reviewer |
| trace | run / handoff / retry の履歴を示す | 長めに保持する | reviewer、運用者 |
| evidence bundle | reviewer が差分を再確認できるように束ねる | review 時点で fresh である必要がある | reviewer |
| metrics | queue 診断、failure analysis、review quality を見る | 集計周期ごと | team lead、運用者 |

この表の狙いは、verification artifact を「全部 log」として扱わないことである。verify log は current-run の真偽、trace は履歴、evidence bundle は review-ready な束、metrics は運用診断の集計というように分担させる。

## 演習
1. failing test を先に足してから修正する。
2. UI 変更に対する evidence bundle を作る。

## 参照する artifact
- `.github/workflows/verify.yml`
  book 側と sample 側の job 分離を見る。CI が local verify をどう共有合格ラインに変えるかを確認する。
- `checklists/verification.md`
  current-run verify、trace、evidence、approval をどう分離しているかを見る。CH10 の最終段に対応する。
- `sample-repo/tests/test_ticket_search.py`
  acceptance criteria を regression guard に変換した例として読む。worked example の起点になる。
- `artifacts/evidence/README.md`
  evidence bundle の最低構成と freshness、redaction の考え方を確認する。

## Source Notes / Further Reading
- この章を探し直すときは、まず `.github/workflows/verify.yml`、`checklists/verification.md`、`sample-repo/tests/test_ticket_search.py`、`artifacts/evidence/README.md` を正本として見る。verification harness は test、verify log、trace、evidence、approval の流れで読む。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH10 Verification Harness を作る」と `manuscript/backmatter/01-読書案内.md` の「検証・信頼性・運用」を参照する。

## 章末まとめ
- verification harness は、test、実行順序、verify log、trace、evidence、CI、approval gate を束ねた検証系である。
- local verify は iteration speed、CI verify は reproducibility を担当し、どちらも必要である。
- verify chain ができると、次に壊れるのは 1 session では閉じない仕事である。次章では long-running task と multi-agent の分割条件を扱う。
