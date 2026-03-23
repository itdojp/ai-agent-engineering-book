# 用語集

本書では、似た概念を意図的に分けて扱う。Prompt Engineering、Context Engineering、Harness Engineering は近いが別工程であり、task brief、Progress Note、context pack も役割が異なる。用語が揃っていないと、artifact の境界も壊れやすい。

定義の source of truth は `docs/glossary.md` である。この appendix では、読み進めるうえで混同しやすい語をまとまりごとに整理する。後付けの source notes、読書案内、索引 seed は探し直しの装置であり、この appendix は語義と表記を固定する装置に集中する。

## 1. 成熟モデルの語

本書の流れは次の 3 段階である。

- Prompt Engineering: 単一タスクの入力と出力を Prompt Contract で固定する
- Context Engineering: task に必要な repo・task・session 情報を選び、保守する
- Harness Engineering: 実行境界、verification harness、再開、approval を設計する

この順序には意味がある。prompt が弱いまま context を足しても、単一タスクの失敗を大きな文脈で包むだけになる。context が弱いまま harness を足しても、間違った前提を丁寧に検証するだけになる。

## 2. 主体と道具の語

AI agent、coding agent、ChatGPT、Codex CLI は同じではない。

- `AI agent`: 複数 step の判断とツール利用で作業を進める主体
- `coding agent`: repo を読み、code / docs / tests / artifact を変更し verify する AI agent
- `ChatGPT`: 要件整理、比較、レビュー観点の洗い出しに向く対話環境
- `Codex CLI`: repo に対して実際の変更と verify を行う実行環境

この区別を曖昧にすると、「会話でうまく説明できた」ことと「repo で仕事が完了した」ことを混同しやすい。本書は後者を扱う。

## 3. 作業 artifact の語

本書で頻出する artifact は次のとおりである。

- `Prompt Contract`: 単一タスクの目的、制約、完了条件、出力形式を定義する prompt artifact
- `task brief`: issue を coding agent 実行向けに構造化した task 仕様
- `Progress Note`: 中断、handoff、再開のための短い進捗記録
- `context pack`: 特定タスクで読む最小参照情報の束
- `verification harness`: test、lint、typecheck、evidence、CI、approval を束ねた検証系

ここで重要なのは、どの artifact も「説明文」ではなく「運用のための入力」であることだ。artifact は人が読むだけでは不十分で、agent が使っても誤解しにくい形でなければならない。

## 4. Harness 運用の語

後半で重要になる語も先に揃えておく。

- `acceptance criteria`: 機能または変更が満たすべき受け入れ条件
- `done criteria`: harness 上で完了扱いにする条件
- `evidence bundle`: reviewer が変更を検証できるように残す証跡一式
- `restart packet`: 再開時に読む最小入力の組
- `permission policy`: 自律実行と human approval の境界を定義する規則
- `work package`: 1 回の session または 1 人の担当で安全に進められる最小単位

これらの語は近いが役割が違う。たとえば `acceptance criteria` は仕様側の条件であり、`done criteria` は運用側の条件である。前者を満たしても verify 未実行なら完了ではないし、後者だけ満たしても仕様を外していれば意味がない。

## 5. 表記ルール

表記の揺れを減らすため、本文では次を優先する。

- repo や artifact 名は code と同じ綴りを使う
- `sample-repo` はハイフン付きで固定する
- `ChatGPT`、`Codex CLI`、`Prompt Contract`、`Progress Note` は固有の綴りを維持する
- 日本語本文では `AIエージェント` と書いてよいが、glossary の基準語は `AI agent` とする

新しい章や artifact を追加するときは、まず `docs/glossary.md` に合わせる。用語の drift を後から直すより、最初に命名を揃える方が安い。

## 参照する artifact

- `docs/glossary.md`
