# 用語集

| 用語 | 定義 |
|---|---|
| Prompt Engineering | ChatGPT などに渡す prompt artifact を設計し、目的・制約・完了条件を固定する工程 |
| Context Engineering | AI agent や coding agent に見せる repo・task・session 情報を設計・維持する工程 |
| Harness Engineering | coding agent の実行境界、権限、verification harness、再試行、回復を設計する工程 |
| AI agent | 複数 step の判断とツール利用で作業を進める主体。本書の日本語本文では「AIエージェント」とも表記する |
| coding agent | repo を読み、コード・docs・tests・artifact を変更し verify する AI agent |
| ChatGPT | 要件整理、設計検討、比較、レビュー観点の洗い出しに使う対話インターフェース |
| Codex CLI | repo を読んで変更し、コマンド実行と verify を行う coding agent 実行環境 |
| `AGENTS.md` | repo entrypoint。対象領域で外してはいけない不変条件と、次に読むべき artifact への入口を定義する |
| sample-repo | 本書で継続的に参照する support-hub のサンプル実装 |
| recurring case | 章を跨いで同じ repo / issue / failure mode を追跡するための継続ケース。本書では `BUG-001`、`FEATURE-001`、`FEATURE-002`、`HARNESS-001` を指す |
| artifact | prompt、doc、script、test、task brief、context pack など repo に残す成果物 |
| acceptance criteria | 機能または変更が満たすべき受け入れ条件。spec と tests の橋渡しに使う |
| task brief | issue を coding agent 実行向けに構造化したタスク仕様 |
| context pack | 特定タスクに必要な参照情報一式。task-specific な読み順と canonical fact を束ねる |
| persistent artifact | repo をまたいで残す source of truth。spec、glossary、architecture doc のような stable な artifact を指す |
| session memory | セッションを跨いで再開するために残す task brief、Progress Note、verify 根拠の組。章タイトルや doc title では `Session Memory` と表記することがある |
| session summary | 再開時に読む最小情報。`Decided`、`Open Questions`、`Next Step` のように、前回判断を短く残した summary を指す |
| source of truth | もっとも優先される正本の artifact。矛盾時の判断基準になる |
| source hierarchy | 本文、repo artifact、official docs、組織ポリシーのどれを何の判断で優先するかを定めた優先順位 |
| source notes | 章末または後付けで、何を正本として信頼するかと次の一歩を短く示す案内 |
| further reading | 章の理解を深めるために official docs、書籍、handbook へつなぐ導線 |
| backmatter | source notes、読書案内、索引、図表一覧など、通読後の再参照装置 |
| verification harness | テスト、lint、typecheck、証跡収集、CI を束ねた検証系 |
| done criteria | harness 上で完了扱いにする条件。verify、artifact 更新、approval の要否を含む |
| verify log | current-run の command、timestamp、pass / fail を残すログ。historical trace とは分けて扱う |
| trace | run、retry、handoff、状態遷移を示す履歴。current-run verify の代わりではなく、failure analysis の材料になる |
| evidence bundle | reviewer が変更を検証できるように残す verify log、repro 手順、画像、summary の組 |
| provenance | prompt、context、artifact、evidence がどの source から生成・更新されたかを追跡するための来歴情報 |
| observability | queue 診断、failure analysis、review quality 改善のために verify log、trace、metrics を観測可能にする考え方 |
| Changed Files | 最終報告で使う canonical な出力項目。変更した code、docs、tests、artifact を reviewer が追跡できる粒度で列挙する |
| Remaining Gaps | 最終報告で使う canonical な出力項目。verify 後も残る未解決事項、human follow-up、completion を妨げる差分を短く記す |
| Prompt Contract | 目的・制約・完了条件・出力形式を定義した prompt artifact |
| Progress Note | 中断・再開・handoff のための短い進捗記録 |
| live tool output | grep 結果、test 出力、verify log のような、その時点でしか有効でない live な根拠 |
| repo context | repo 全体で比較的安定している構造、規約、entry point、ownership 情報 |
| MCP (Model Context Protocol) | tool / resource / prompt などの context source を統一的に接続するための protocol。runtime ごとに実装差分があるため、実運用時は仕様と official docs を併読する |
| MCP-connected capability | runtime に tools、resources、prompts などの追加 capability を接続する面。repo skill や context pack の代替ではない |
| A2A (Agent2Agent) | agent-to-agent discovery や task handoff のような remote interoperability を扱う protocol 群。本書では same-repo の local orchestration と分けて扱う |
| tool drift | UI、CLI、API、tool capability が時間経過で変わり、本文や手順の記述とズレる現象 |
| human approval gate | 高リスク操作の前に human reviewer の確認を必須にする承認境界 |
| approval boundary | 破壊的変更、public contract 変更、運用ポリシー変更の前に human approval が必要になる境界 |
| operating model | AIエージェント運用の責務分担、review budget、cadence、導入段階を定義する運用設計 |
| Lead | issue 優先順位、work package の粒度、破壊的変更や public contract 変更の承認を担う human role |
| Operator | brief、artifact、verify、evidence を揃えて agent 実行を進め、`Remaining Gaps` を明示する human role |
| Reviewer | `Goal`、`Changed Files`、`Scope and Non-goals`、`Verification`、`Evidence / Approval`、`Remaining Gaps` を確認して merge 可否を判断する human role |
| throughput | 一定期間に処理できる issue、PR、work package の量 |
| stale draft count | review budget の窓で進行が止まっている draft PR の数。queue 解消を優先する signal に使う |
| approval-stop rate | approval boundary や permission policy によって run や PR が停止した比率 |
| repo hygiene | 次の作業を壊さないために repo の整合性と可読性を保つ運用 |
| hygiene backlog age | cleanup backlog のうち最も古い未処理項目の経過時間 |
| entropy cleanup | stale docs、孤立 artifact、表記ゆれ、不要差分を定期的に整理する運用 |
| restart packet | 中断後の再開に必要な canonical input。plan、feature list、最新 `Progress Note`、verify evidence、open questions の組 |
| permission policy | coding agent が自律で進めてよい変更と human approval が必要な変更を分ける規則 |
| skill | 再利用可能な workflow / output contract を持つ instructions / resources / scripts の単位。章タイトルや file 名では `Skills` や `SKILL.md` と表記することがある |
| runtime-managed capability | background execution、hosted tools、managed context のように runtime が mechanism を肩代わりする機能 |
| harness-owned duty | approval boundary、artifact sync、verify、review のように repo / team 側で定義と運用が必要な責務 |
| work package | 1 回の session または 1 人の担当で安全に進められる最小作業単位 |
| review budget | reviewer が一定期間に深く確認できる変更量の上限 |
| owned files | role や workstream ごとに責任を持って変更してよい file 範囲。multi-agent の衝突防止に使う |
| AI slop | 高スループットな生成で repo に蓄積する質の低い差分や docs |
