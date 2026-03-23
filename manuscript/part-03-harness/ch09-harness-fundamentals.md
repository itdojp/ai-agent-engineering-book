---
id: ch09
title: Harness Engineering の基礎
status: draft
artifacts:
  - scripts/init.sh
  - scripts/verify-sample.sh
  - sample-repo/docs/harness/single-agent-runbook.md
  - sample-repo/docs/harness/permission-policy.md
  - sample-repo/docs/harness/done-criteria.md
dependencies:
  - ch05
  - ch06
  - ch07
  - ch08

---

# Harness Engineering の基礎

## この章の位置づけ
repo context、task brief、skill が揃っていても、coding agent は verify 前に止まり、approval 境界を越え、同じ失敗を繰り返す。CH05-CH08 では、AI agent に何を見せるかを整えてきた。だが、それだけでは作業は閉じない。

ここから必要になるのが Harness Engineering である。Context Engineering が「何を読むか」を設計するのに対し、Harness Engineering は「どう起動し、どこまで触れ、いつ done と言ってよいか」を設計する。本章では、その最小単位として single-agent harness を定義する。対象は verification harness 全体ではない。まずは 1 つの coding agent を安全に最後まで走らせる土台を固める。

## 学習目標
- single-agent harness の構成要素を説明できる
- permission policy と escalation の必要性を理解する
- done criteria を明文化できる


## 小見出し
### 1. single-agent harness の全体像
single-agent harness は、1 つの coding agent を 1 つの work package に対して動かす実行枠である。ここでいう harness は prompt の別名ではない。prompt や context pack が妥当でも、起動手順、作業境界、権限、verify、完了条件が曖昧なら、agent は plausible output を返しても仕事を完了できない。

この repo では、single-agent harness を次の 6 要素で構成する。

| 要素 | 役割 | この章の artifact |
|---|---|---|
| init | 起動前に読むべき artifact と verify command を固定する | `scripts/init.sh` |
| work boundary | 今回の task で触ってよい範囲を限定する | task brief、`sample-repo/docs/harness/single-agent-runbook.md` |
| permission policy | approval が必要な変更を分離する | `sample-repo/docs/harness/permission-policy.md` |
| done criteria | done / blocked / needs-human-approval を定義する | `sample-repo/docs/harness/done-criteria.md` |
| verify command | local で最低限満たすべき検証を固定する | `scripts/verify-sample.sh` |
| report format | changed files と verification を残す | runbook と done criteria |

`BUG-001` を例にすると違いが見えやすい。「不具合を直して」とだけ渡すと、agent は root cause 仮説だけ返して止まるかもしれない。single-agent harness を通すと、起動時に task brief、permission policy、done criteria、verify command が確定するので、「修正候補を考えた」で止まりにくくなる。

CH08 までで context は十分に揃った。しかし、context が揃っていることと、作業を最後まで完了できることは別問題である。CH09 の対象は後者である。

### 2. init、権限、作業境界
single-agent harness の最初の責務は、起動時点で source of truth を固定することだ。`scripts/init.sh` は、repo root、sample-repo の場所、指定した task brief、先に読むべき docs、verify command を一度に表示する。これにより、agent はセッション開始直後に「何を読むべきか」「どの command で検証するか」を迷わない。

たとえば `BUG-001` を扱うなら、repo root で次のように始める。

```bash
./scripts/init.sh sample-repo/tasks/BUG-001-brief.md
```

出力には `read_first_1` から `read_first_4`、`runbook`、`permission_policy`、`done_criteria`、`verify` が並ぶ。これは単なる案内表示ではない。single-agent harness の起動契約である。

次に必要なのが permission policy である。`sample-repo/docs/harness/permission-policy.md` では、task brief に含まれる範囲の code / docs / tests 更新、failing test 追加、local verify 実行までは agent が自律で進めてよい。一方、public interface の変更、ドメイン前提の変更、verify script や CI の変更、外部 service や secret が絡む操作は approval が必要と定めている。

ここで重要なのは、「agent を信用するか」ではなく「approval の境界を repo artifact に埋め込むか」である。`Codex CLI` のような coding agent は command を実行できる。だからこそ、許可範囲を事前に狭く定義する必要がある。Harness Engineering の権限設計は、LLM の性格診断ではなく実行境界の設計である。

作業境界も同じだ。`BUG-001` の work package なら、まず `sample-repo/tasks/BUG-001-brief.md`、`sample-repo/docs/repo-map.md`、`sample-repo/docs/architecture.md`、関連 test を読む。CH09 の時点では、ここで repo 全体を自由探索しない。work package を小さく保つほど、verify と rollback の単位も小さくなる。

### 3. completion criteria と exit rule
Harness Engineering の中心は、start より exit にある。多くの agent は「何か書いたら完了」と誤認する。だが実務で必要なのは「done の条件を満たしたか」である。`sample-repo/docs/harness/done-criteria.md` では、done を 3 つの exit state に分ける。

- `done`
- `blocked`
- `needs-human-approval`

`done` と言ってよいのは、task brief の Goal と Acceptance Criteria を満たし、変更ファイルが scope に収まり、code / docs / tests / task artifact の drift がなく、`./scripts/verify-sample.sh` が通ったときだけである。つまり、single-agent harness における完了とは「変更を出したこと」ではなく「verify 済みの work package を閉じたこと」である。

`scripts/verify-sample.sh` は、この exit rule を mechanical に支える。現時点では sample-repo の必須 docs、harness docs、task brief、tests の存在を確認し、unit test を実行するだけである。まだ lint や typecheck、evidence bundle は入っていない。そこは CH10 で verification harness として拡張する。CH09 で必要なのは、「完了前に最低限これを通す」という 1 本の verify command を固定することだ。

この区別は重要である。CH09 の harness は verify を呼び出す枠組みを定義する。verify の中身を厚くするのは CH10 の仕事である。

### 4. 安全な retry と rollback
retry は回数ではなく条件で設計する。single-agent harness がないと、agent は verify failure のたびに同じ操作を繰り返しやすい。これは進捗ではなく、failure loop である。

`sample-repo/docs/harness/single-agent-runbook.md` では、retry の前に failure mode を 4 種類に分類する。

| failure mode | 何が足りないか | 取るべき行動 |
|---|---|---|
| missing-context | 読むべき artifact が足りない | 追加で読む artifact を明示し、scope を言い直す |
| verify-failure | 変更仮説が外れている | 現在の diff を見直し、最小差分で修正する |
| permission-boundary | approval が必要 | 変更を止めて escalate する |
| environment-failure | command / path / tool が壊れている | 実行コマンドと stderr を報告する |

特に rollback の考え方が重要である。CH09 でいう rollback は、「repo 全体を危険に戻すこと」ではない。現在の work package 内で、自分が入れた tentative diff を捨てて last known-good state に戻すことだ。ユーザーの未理解な差分や unrelated file を巻き戻してはいけない。これは coding agent の安全制約であり、単なる git 操作の話ではない。

安全な retry は、failure mode の再分類と work package の縮小を伴う。新しい情報も新しい仮説もないまま同じ verify を繰り返しても、Harness Engineering としては失敗である。

### 5. agent に仕事を最後までさせる条件
coding agent に仕事を最後までさせるには、次の 5 条件が要る。

1. start condition が 1 command で明確である
2. work boundary と permission boundary が artifact 化されている
3. done / blocked / needs-human-approval の exit state が決まっている
4. verify command が固定されている
5. retry と rollback の単位が小さい

この 5 条件がないと、agent は途中で止まるか、逆に止まるべき場所で止まれない。前者は「停止が早い」失敗であり、後者は「壊す」失敗である。CH01 の failure model を、Harness Engineering の側から防いでいると考えるとよい。

逆に、task brief、context pack、skill が揃っていても、start / permission / exit / retry が曖昧なら、agent は最後の 10% で崩れる。実務で問題になるのはこの最後の 10% である。Harness Engineering は、その 10% を偶然ではなく artifact で支える。



## 紙面で押さえるポイント
### Single-Agent Harness フロー

| 段階 | 何を固定するか | 主な artifact / command | ここで防ぐ failure |
|---|---|---|---|
| init | 読む順番と verify command | `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md` | 開始直後の迷走 |
| boundary | task scope と更新可能範囲 | task brief、runbook | 触る範囲の肥大化 |
| permission | approval が必要な変更 | `sample-repo/docs/harness/permission-policy.md` | 勝手な public contract 変更 |
| verify | 最低限の合格ライン | `./scripts/verify-sample.sh` | verify 前の早すぎる停止 |
| exit | `done / blocked / needs-human-approval` | `sample-repo/docs/harness/done-criteria.md` | 終了条件の曖昧さ |
| report | changed files と remaining gaps | runbook、done criteria | review-ready でない報告 |

この順番で並べると、single-agent harness は高度な自動化ではなく、開始条件と終了条件の固定だと見える。特に `verify` と `exit` を分けることが重要である。verify が通っただけでは、scope 外変更や approval 境界を越えた変更は still open のまま残りうる。

## 章で使う bad / good example
bad:

```text
BUG-001 を直す。
必要なら test を見て、終わったと思ったら報告する。
```

この指示では、start condition、approval 境界、verify command、done criteria がない。agent はもっともらしい修正案を返せても、どこで止まるべきか分からない。

good:

```text
Task は `sample-repo/tasks/BUG-001-brief.md` を source of truth とする。
開始時に `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md` を実行する。
`sample-repo/docs/harness/permission-policy.md` を超える変更は approval を求める。
done と言ってよいのは `sample-repo/docs/harness/done-criteria.md` を満たし、
`./scripts/verify-sample.sh` が通ったときだけとする。
返答は Changed Files / Verification / Remaining Gaps を含める。
```

この修正版では、single-agent harness の start、boundary、exit が artifact と command で固定されている。

比較観点:
- bad は prompt だけで agent を動かそうとしている
- bad は verify 前に停止する余地が大きい
- good は init、permission policy、done criteria、verify を 1 つの実行枠として定義している

## Worked Example
`BUG-001` の「ステータス更新後の再読み込みで旧状態が見える」ケースを single-agent harness で進める。

1. 起動
   - `./scripts/init.sh sample-repo/tasks/BUG-001-brief.md`
2. 読み込み
   - `AGENTS.md`
   - `sample-repo/AGENTS.md`
   - `sample-repo/tasks/BUG-001-brief.md`
   - `sample-repo/docs/repo-map.md`
   - `sample-repo/docs/architecture.md`
   - `sample-repo/tests/test_service.py`
3. 境界確認
   - public interface を変えない
   - verify script を変えない
   - bugfix と test に必要な最小差分に限定する
4. 実行
   - failing behavior を再現する test を追加または既存 test の不足を補う
   - 根本原因を仮説化し、scope 内で修正する
   - `./scripts/verify-sample.sh` を実行する
5. 終了判定
   - verify が通り、Root Cause を説明でき、Remaining Gaps を短く言えるなら `done`
   - approval 境界を越えるなら `needs-human-approval`
   - task brief と test が矛盾して判断できないなら `blocked`

この例で見えるのは、Harness Engineering が高度な自動化ではなく、開始条件と終了条件の固定だという点である。agent を賢く見せるのではなく、仕事を閉じられるようにする。それが CH09 の主題である。

## 演習
1. バグ修正タスク向けの single-agent runbook を設計する。
2. permission policy と escalation rule を定義する。

## 参照する artifact
- `scripts/init.sh`
  起動契約として読む。何を先に読み、どの verify command を使うかを固定している。
- `scripts/verify-sample.sh`
  single-agent harness が呼び出す最低限の verify として読む。CH10 ではこれを verification harness へ拡張する。
- `sample-repo/docs/harness/single-agent-runbook.md`
  failure mode の分類と retry rule を確認する。verify failure をどう扱うかの本文対応箇所で使う。
- `sample-repo/docs/harness/permission-policy.md`
  approval が必要な変更を確認する。権限設計を prompt ではなく artifact に置く例である。
- `sample-repo/docs/harness/done-criteria.md`
  `done / blocked / needs-human-approval` の exit state を確認する。報告フォーマットとのつながりもここで押さえる。


## Source Notes / Further Reading
- この章を探し直すときは、まず `scripts/init.sh`、`sample-repo/docs/harness/single-agent-runbook.md`、`sample-repo/docs/harness/permission-policy.md`、`sample-repo/docs/harness/done-criteria.md` を正本として見る。single-agent harness は prompt の言い換えではなく、開始条件と終了条件の束である。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH09 Harness Engineering の基礎」と `manuscript/backmatter/01-読書案内.md` の「検証・信頼性・運用」を参照する。

## 章末まとめ
- Context Engineering が「何を見せるか」を決めるのに対し、Harness Engineering は「どう始め、どこで止まり、いつ done と言えるか」を決める。
- single-agent harness の最小構成は、init、work boundary、permission policy、done criteria、verify command、retry rule である。
- 起動と終了条件が固まると、次に不足するのは reviewer が信じられる verify chain である。次章では test、CI、evidence を束ねる verification harness を扱う。
