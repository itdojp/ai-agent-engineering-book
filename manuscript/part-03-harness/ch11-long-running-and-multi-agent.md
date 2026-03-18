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
CH09 では single-agent harness、CH10 では verification harness を定義した。だが実務では、1 回の session で終わらない task が現れる。artifact が増え、verify が複数回に分かれ、途中で handoff や再開が入ると、単一 session 前提の運用は崩れやすい。ここで必要なのが long-running task 向けの feature list、restart protocol、役割分離である。

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
long-running task の最初の artifact は feature list である。feature list は、最終目標を複数の track に分け、どこまで進んだかを workstream 単位で見える化するための artifact である。`sample-repo/docs/harness/feature-list.md` では、`FEATURE-002` を `assignee filter semantics`、`assignment change audit log`、`verification and docs sync` の 3 track に分けている。

ここで重要なのは、feature list が backlog の別名ではないことだ。backlog はやることの一覧だが、feature list は long-running task を session またぎで維持するための進行管理 artifact である。各 track に目的、主要ファイル、verify signal、依存関係を持たせることで、「今どの塊を閉じにいくのか」を決めやすくなる。

進捗記録には CH07 の task brief と Progress Note、そして `docs/session-memory-policy.md` が効く。feature list が task 全体の地図なら、Progress Note は今の居場所である。両方が揃わないと、中断後に再開しても前回の verify 状態と next step がつながらない。

CH11 では Progress Note の新規テンプレートを増やさない。その代わり、既存の Session Memory Policy を前提に、feature list と restart protocol を接続する。

### 3. restart protocol
restart protocol は、中断後に「前回の続きらしいこと」を推測で始めないための手順である。`sample-repo/docs/harness/restart-protocol.md` では、restart packet と restart steps を明示している。

restart packet の最低入力は次の 5 つでよい。

1. `FEATURE-002` plan
2. 最新の feature list
3. 最新の Progress Note
4. 直近の verify 結果
5. 未解決の open question

この packet が揃わない状態で再開すると、agent は古い前提で作業を続けやすい。たとえば前回は assignee filter の semantics だけ決めたのに、再開時に audit log の設計へ飛ぶと、verify も review もつながらない。

restart protocol で大切なのは、再開時に「次の 1 手」を小さく選び直すことだ。前回の計画をそのまま丸ごと再実行するのではない。最新の verify と open question を見て、今もっとも安全な 1 手を選ぶ。これが long-running harness における retry であり、CH09 の session 内 retry を session 間へ拡張したものと考えればよい。

### 4. planner / coder / reviewer の分離
task を multi-agent に分けるとき、最初に分けるべきなのは人数ではなく責務である。`sample-repo/docs/harness/multi-agent-playbook.md` と `sample-repo/tasks/FEATURE-002-plan.md` では、`planner`、`coder`、`reviewer`、`verifier` の 4 役を定義している。

この分離が有効なのは、write scope と判断責務が違うからである。

| role | 主な責務 | 触る artifact |
|---|---|---|
| planner | scope freeze、workstream 分解、handoff 定義 | `FEATURE-002-plan.md`、feature list |
| coder | 実装と test 更新 | `src/`、`tests/` |
| reviewer | diff / docs drift / scope逸脱の確認 | docs、task artifact、diff |
| verifier | verify 実行、evidence、report | verify command、evidence bundle |

ここで重要なのは、multi-agent は parallelism の道具であって、曖昧な task を丸投げする仕組みではないという点だ。plan が曖昧なまま `planner` と `coder` を同時に走らせると、write scope がぶつかりやすい。まず planner が scope と所有権を固定し、その後に disjoint な workstream だけを parallel にするべきである。

`FEATURE-002-plan.md` では、assignee filter track と audit log track を別 workstream として扱い、最後に reviewer と verifier が統合確認する構成にしている。これにより、multi-agent を使う場合でも merge 点が見える。

### 5. multi-agent を使う条件、使わない条件
multi-agent は default ではない。使う条件を決めずに導入すると、coordination cost が利益を上回る。CH11 では次の基準で十分である。

| 判断 | 使う条件 | 使わない条件 |
|---|---|---|
| single-agent | scope が狭い、1 session で閉じられる、write scope が 1 か所、verify が 1 本で済む | artifact 同期が多い、長時間化が見えている |
| multi-agent | disjoint な workstream がある、review や verify を並列化できる、restart packet が明確 | plan が曖昧、write scope が重なる、説明コストが高い |

つまり、multi-agent の前提は feature list と restart protocol である。これらがない状態で agent を増やしても、単に混乱を並列化するだけになる。

実務では「複雑だから multi-agent」ではなく、「workstream を分けても統合コストが下がるから multi-agent」と判断する。`FEATURE-002` なら、assignee filter semantics と audit log は概念的には関連するが、実装と review の観点は分けられる。このように分離可能な task だけを multi-agent に載せるべきである。



## 章で使う bad / good example
bad:

```text
FEATURE-002 を最後まで進める。
必要なら途中で別 agent を増やす。
止まったら前の会話を見て再開する。
```

このやり方では、track 分解、restart packet、role ownership がない。中断や handoff が入った瞬間に state が崩れる。

good:

```text
まず `sample-repo/docs/harness/feature-list.md` で workstream を分ける。
次に `sample-repo/tasks/FEATURE-002-plan.md` で planner / coder / reviewer / verifier の責務を固定する。
中断時は `sample-repo/docs/harness/restart-protocol.md` の restart packet を更新する。
single-agent で閉じられる track は分割せず、disjoint な track だけ multi-agent にする。
```

この修正版では、long-running task の state 管理と multi-agent の適用条件が artifact に落ちている。

比較観点:
- bad は session memory を会話履歴に依存している
- bad は multi-agent を手段ではなく反射で使っている
- good は feature list、restart packet、role ownership を先に固定している

## Worked Example
`FEATURE-002` を例に、long-running task を 3 つの段階に分ける。

1. planner
   - `FEATURE-002-plan.md` で scope と non-goals を固定する
   - `feature-list.md` に track と verify checkpoint を作る
2. coder
   - assignee filter semantics と audit log を別 workstream として実装する
   - 各 workstream で局所的に verify を回す
3. reviewer / verifier
   - docs drift、scope 逸脱、verify 結果、evidence を統合確認する

もし coder が途中で止まったら、再開者は `restart-protocol.md` に従って最新 Progress Note と verify を確認し、次の 1 手を選ぶ。ここで planner の役割に戻るべきか、そのまま coder を継続できるかを判断する。つまり restart protocol は「続きをやるための手順」であると同時に、「役割を戻し直すための手順」でもある。

この worked example が示すのは、multi-agent の本質が同時実行ではなく責務分離だという点である。long-running task を artifact で保てるからこそ、必要なときだけ安全に複数 agent を使える。

## 演習
1. ケースCを planner / coder / reviewer に分解する。
2. 途中で失敗した長時間タスクを restart protocol で再開する。

## 参照する artifact
- `sample-repo/docs/harness/feature-list.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/multi-agent-playbook.md`
- `sample-repo/tasks/FEATURE-002-plan.md`


## 章末まとめ
- long-running task を壊さないためには、feature list、Progress Note、restart packet が必要である。
- multi-agent は default ではなく、role ownership と write scope が切れるときだけ使う。
- CH11 では task を長時間に耐える形へ分解した。次章では、こうした harness を team 運用と metrics にどう載せるかを扱う。
