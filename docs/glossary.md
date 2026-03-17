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
| sample-repo | 本書で継続的に参照する support-hub のサンプル実装 |
| artifact | prompt、doc、script、test、task brief、context pack など repo に残す成果物 |
| task brief | issue を coding agent 実行向けに構造化したタスク仕様 |
| context pack | 特定タスクのために集約した参照情報一式 |
| Session Memory | セッションを跨いで再開するために残す task brief、Progress Note、verify 根拠の組 |
| verification harness | テスト、lint、typecheck、証跡収集、CI を束ねた検証系 |
| Prompt Contract | 目的・制約・完了条件・出力形式を定義した prompt artifact |
| Progress Note | 中断・再開・handoff のための短い進捗記録 |
| Skill | 再利用可能な instructions / resources / scripts の単位 |
| AI Slop | 高スループットな生成で repo に蓄積する質の低い差分や docs |
