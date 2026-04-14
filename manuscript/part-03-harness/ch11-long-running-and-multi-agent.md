---
id: ch11
title: Long-running Task と Multi-agent
status: draft
artifacts:
  - sample-repo/docs/harness/feature-list.md
  - sample-repo/docs/harness/restart-protocol.md
  - sample-repo/docs/harness/multi-agent-playbook.md
  - sample-repo/tasks/FEATURE-002-plan.md
dependencies:
  - ch09
  - ch10

---

# Long-running Task と Multi-agent

## この章の位置づけ
`FEATURE-002` のような長時間タスクを 1 本の prompt で抱えると、verify 状態も判断履歴もすぐに崩れる。CH09 では single-agent harness、CH10 では verification harness を定義した。だが実務では、1 回の session で終わらない task が現れる。ここで必要になるのが long-running task 向けの feature list、restart protocol、役割分離である。

本章の主題は、最初から multi-agent に飛びつくことではない。まず長時間タスクを壊さないための最小構成を設計し、そのうえで必要なときだけ multi-agent に分割することである。題材は `FEATURE-002` とし、assignee filter の振る舞い整理と assignment change の監査ログ強化を、複数 work package にどう分けるかを扱う。

## 学習目標
- 長時間タスクが壊れる理由を説明できる
- restart protocol を設計できる
- single-agent と multi-agent の使い分けを判断できる

## 小見出し
### 1. 長時間タスクで壊れる点
長時間タスクが壊れる主因は、モデルの能力不足より state 管理の崩壊にある。具体的には、scope が広がる、直近の verify 状態が分からなくなる、前の判断と今の判断がずれる、次の 1 手が大きすぎる、の 4 つである。

`FEATURE-002` を 1 本の prompt で「assignee filter と監査ログを全部やる」と渡すと、agent は途中で次のように崩れやすい。

- assignee filter の挙動整理と audit log 拡張が混ざる
- どこまで verify 済みか分からなくなる
- docs / tests / task artifact の更新順が崩れる
- 中断後に何を再開すべきか分からない

この failure mode は CH01 の「忘却」と「停止が早い」の複合形である。long-running task では、context を厚くするだけでは足りない。session を跨いでも state を保てる artifact が必要になる。

### 2. feature list と進捗記録
long-running task の最初の artifact は feature list である。feature list は、最終目標を複数の track に分け、どこまで進んだかを workstream 単位で見える化するための artifact である。`sample-repo/docs/harness/feature-list.md` では、`FEATURE-002` を `Track A: Assignee Filter Semantics`、`Track B: Assignment Change Audit Log`、`Track C: Verification And Docs Sync` の 3 track に分けている。

ここで重要なのは、feature list が backlog の別名ではないことだ。backlog はやることの一覧だが、feature list は long-running task を session またぎで維持するための進行管理 artifact である。各 track に目的、主要ファイル、verify signal、依存関係を持たせることで、「今どの塊を閉じにいくのか」を決めやすくなる。

進捗記録には CH07 の task brief と `Progress Note` が効く。feature list が task 全体の地図なら、`Progress Note` は今の居場所である。両方が揃わないと、中断後に再開しても前回の verify 状態と next step がつながらない。要約だけ残して primary artifact を落とすと、summary drift が起きやすい。

### 3. restart protocol
restart protocol は、中断後に「前回の続きらしいこと」を推測で始めないための手順である。`sample-repo/docs/harness/restart-protocol.md` では、restart packet と restart steps を明示している。

restart packet の最低入力は次の 6 つでよい。

1. `FEATURE-002` plan
2. 最新の `sample-repo/docs/harness/feature-list.md`
3. 現在の owned files と merge order
4. 最新の `Progress Note`
5. 直近の verify 結果
6. 未解決の open question と approval 待ち項目

この packet が揃わない状態で再開すると、agent は古い前提で作業を続けやすい。特に summary だけで再開するのは危険である。summary は session summary として必要だが、それ単体では source of truth にならない。再開時には plan、feature list、`Progress Note`、verify、owned files を読み直し、必要なら live verify を取り直す。

### 4. planner / coder / reviewer / verifier の分離
task を multi-agent に分けるとき、最初に分けるべきなのは人数ではなく責務である。`sample-repo/docs/harness/multi-agent-playbook.md` と `sample-repo/tasks/FEATURE-002-plan.md` では、`planner`、`coder`、`reviewer`、`verifier` の 4 役を定義している。

この 4 役の分離が有効なのは、write scope と判断責務が違うからである。

| role | 主な責務 | 触る artifact |
|---|---|---|
| planner | scope freeze、workstream 分解、handoff 定義 | `FEATURE-002-plan.md`、feature list |
| coder | 実装と test 更新 | `src/`、`tests/` |
| reviewer | diff / docs drift / scope逸脱の確認 | docs、task artifact、diff |
| verifier | verify 実行、evidence、report | verify command、evidence bundle |

ここで重要なのは、local multi-agent orchestration は same-repo / same-runtime の role split だという点である。owned files、merge order、exit state が先に決まっているからこそ、local に複数 role を回せる。plan が曖昧なまま agent を増やすと、write scope がぶつかりやすい。まず planner が scope、shared file rule、所有権を固定し、その後に disjoint な workstream だけを parallel にするべきである。

### 5. multi-agent を使う条件、使わない条件
multi-agent は default ではない。使う条件を決めずに導入すると、coordination cost が利益を上回る。CH11 では次の基準で十分である。

| 判断 | 使う条件 | 使わない条件 |
|---|---|---|
| single-agent | scope が狭い、1 session で閉じられる、write scope が 1 か所、verify が 1 本で済む | artifact 同期が多い、長時間化が見えている |
| multi-agent | disjoint な workstream がある、review や verify を並列化できる、restart packet が明確 | plan が曖昧、write scope が重なる、説明コストが高い |

ここで local orchestration と remote interoperability も分けておく。MCP は context / tool connectivity を扱う。つまり agent runtime に tools、resources、prompts を接続するための面である。一方、A2A は agent-to-agent discovery や task handoff のような remote interoperability を扱う。same-repo / same-runtime の sub-agent 分割を設計するときに、MCP と A2A を同一視する必要はない。CH11 の主題は local multi-agent orchestration であり、cross-service / cross-organization の interoperability そのものではない。

実務では「複雑だから multi-agent」ではなく、「分割後に統合コストが下がるから multi-agent」と判断する。`FEATURE-002` なら、assignee filter semantics と audit log は概念的には関連するが、実装 owner と verify checkpoint は分けられる。このように分離可能な task だけを multi-agent に載せるべきである。

## 章で使う bad / good example
bad:

```text
FEATURE-002 を最後まで進める。
必要なら途中で別 agent を増やす。summary だけ残しておけば再開できる。
MCP が使えるので、そのまま A2A 的な分担もできるとみなす。
```

このやり方では、track 分解、restart packet、owned files、role ownership がない。中断や handoff が入った瞬間に state が崩れる。

good:

```text
まず `sample-repo/docs/harness/feature-list.md` で workstream を分ける。
次に `sample-repo/tasks/FEATURE-002-plan.md` で planner / coder / reviewer / verifier の責務を固定する。
`sample-repo/docs/harness/restart-protocol.md` に従い、summary だけでなく plan、feature list、verify、owned files を確認して再開する。
local で閉じる track だけを multi-agent にし、MCP は tool connectivity、A2A は remote handoff として別概念で扱う。
```

この修正版では、long-running task の state 管理、ownership、multi-agent の適用条件が artifact に落ちている。

比較観点:
- bad は session memory を summary だけに依存している
- bad は MCP と A2A を同じ種類の仕組みとして扱っている
- good は feature list、restart packet、owned files、merge order を先に固定している

## Worked Example
`FEATURE-002` を例に、long-running task を 4 つの段階に分ける。

1. planner
   - `FEATURE-002-plan.md` で scope、non-goals、shared file rule を固定する
   - `feature-list.md` に track、owner、verify checkpoint を作る
   - 各 role の owned files と merge order を決める
2. coder
   - assignee filter semantics と audit log を別 workstream として実装する
   - 各 workstream で局所的に verify を回し、`Progress Note` を更新する
3. reviewer
   - docs drift、scope 逸脱、shared-file collision の有無を確認する
4. verifier
   - current-run verify、evidence、`Remaining Gaps` を統合確認する

もし coder が途中で止まったら、再開者は `restart-protocol.md` に従って feature list、`Progress Note`、verify を確認し、次の 1 手を選ぶ。ここで planner の役割に戻るべきか、そのまま coder を継続できるかを判断する。つまり restart protocol は「続きをやるための手順」であると同時に、「役割を戻し直すための手順」でもある。

この worked example が示すのは、multi-agent の本質が同時実行ではなく責務分離だという点である。long-running task を artifact で保てるからこそ、必要なときだけ安全に複数 agent を使える。

## 紙面で押さえる縮約表
### Local Multi-agent / Remote Interoperability 判定カード

| 判定項目 | local multi-agent orchestration | remote interoperability | 主な artifact |
|---|---|---|---|
| 境界 | same-repo / same-runtime の role split | cross-service / cross-organization の handoff | playbook、restart protocol |
| 主な関心 | owned files、merge order、exit state | discovery、task transfer、trust boundary | plan、protocol docs |
| MCP との関係 | tools / resources をつなぐ補助面 | 代替ではない | runtime docs |
| A2A との関係 | 必須ではない | handoff を担う候補 | protocol docs |

このカードで見るべき点は、「複雑だから multi-agent」ではなく、「分割後に統合コストが下がるか」である。feature list と restart packet が弱い状態で agent を増やすと、単に state 崩壊を並列化するだけになる。逆に plan と role split が明確なら、local multi-agent orchestration は long-running task の coordination cost を下げる。

## 演習
1. ケースCを planner / coder / reviewer / verifier に分解する。
2. 途中で失敗した長時間タスクを restart protocol で再開する。

## 参照する artifact
- `sample-repo/docs/harness/feature-list.md`
  long-running task を track に分ける例として読む。backlog ではなく進行管理 artifact である点を確認する。
- `sample-repo/docs/harness/restart-protocol.md`
  restart packet と restart steps を確認する。summary だけで再開しない原則をここで押さえる。
- `sample-repo/docs/harness/multi-agent-playbook.md`
  role ownership、owned files、merge order、exit state を確認する。local multi-agent orchestration を扱う実例である。
- `sample-repo/tasks/FEATURE-002-plan.md`
  planner が scope と checkpoint を固定した例として読む。feature list と playbook をどう task に落としているかを見る。

## Source Notes / Further Reading
- この章を探し直すときは、まず `sample-repo/docs/harness/feature-list.md`、`sample-repo/docs/harness/restart-protocol.md`、`sample-repo/docs/harness/multi-agent-playbook.md`、`sample-repo/tasks/FEATURE-002-plan.md` を正本として見る。multi-agent は default ではなく、local orchestration の owned files と restart packet が揃って初めて使う。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH11 Long-running Task と Multi-agent」と `manuscript/backmatter/01-読書案内.md` の「検証・信頼性・運用」を参照する。

## 章末まとめ
- long-running task を壊さないためには、feature list、`Progress Note`、restart packet が必要である。
- multi-agent は default ではなく、role ownership、owned files、merge order が切れるときだけ使う。
- MCP は context / tool connectivity、A2A は remote interoperability の面であり、same-repo の local orchestration とは別問題である。次章では team 全体の運用設計へつなげる。
