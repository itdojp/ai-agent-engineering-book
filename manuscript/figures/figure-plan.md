# Figure Plan

本書の主要概念を reader-facing な図版として固定するための plan。図番号そのものは組版工程で確定するが、ここでは source file と chapter progression を正本として管理する。

| 図 ID | 対象章 | 挿入候補 | Caption | 読者価値 | Source |
|---|---|---|---|---|---|
| `fig-01` | CH01 | 「Prompt Engineering / Context Engineering / Harness Engineering の対応表」の直後 | Prompt / Context / Harness は、誤答・忘却・破壊/停止という failure mode を減らす順に積み上がる。 | 書店での立ち読みでも本書の promise と progression が 1 枚で伝わる。 | `fig-01-maturity-model.mmd` |
| `fig-02` | CH05 | 「永続・タスク・セッション・ツールコンテキスト」の直後 | Context は永続、タスク、セッション、ツールの 4 種類に分かれ、鮮度と更新責任が異なる。 | Context Engineering を「情報を増やす話」ではなく「寿命を分ける話」として理解しやすくする。 | `fig-02-context-classes.mmd` |
| `fig-03` | CH07 | 「セッション再開時の最低入力」の直後 | 再開時は repo context から task brief、session memory、live verify へ降りる順で読むと drift が減る。 | repo / task / session の関係と `restart packet` の読み順を 1 枚で再確認できる。 | `fig-03-resume-packet.mmd` |
| `fig-04` | CH09 | 「single-agent harness の全体像」の直後 | single-agent harness は init、boundary、permission、verify、exit、report を 1 つの実行枠にまとめる。 | Harness Engineering が prompt の言い換えではなく、開始条件と終了条件の設計だと分かる。 | `fig-04-single-agent-harness.mmd` |
| `fig-05` | CH10 | 「lint / typecheck / unit / e2e の順序」の直後 | verification harness は failing test、local verify、CI、evidence、approval を順序付きでつなぐ。 | verify を単発コマンドではなく review-ready に向かう pipeline として読める。 | `fig-05-verification-pipeline.mmd` |
| `fig-06` | CH11 | 「planner / coder / reviewer の分離」の直後 | long-running task は feature list、`restart packet`、`approval boundary`、role 分担が揃って初めて安全に multi-agent へ分割できる。 | long-running task と multi-agent の関係を責務図として再参照できる。 | `fig-06-long-running-multi-agent.mmd` |
| `fig-07` | CH12 | 「人間が残す責務」の直後 | operating model は Human と Agent の責務、review budget、metrics、cleanup cadence を循環させて保つ。 | チーム導入を「モデル選定」ではなく「責務と cadence の設計」として理解しやすくする。 | `fig-07-operating-model.mmd` |
