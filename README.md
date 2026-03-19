# AIエージェント実践: Prompt / Context / Harness Engineering

本リポジトリは、書籍原稿 (`manuscript/`)、英語版原稿 scaffold (`manuscript-en/`)、サンプル実装 (`sample-repo/`)、および執筆運用系 (`AGENTS.md` / `.agents/skills/` / `scripts/` / `issue-drafts/`) を同居させる構成です。

## 目的

- **Prompt → Context → Harness** の成熟モデルを、章本文だけでなく repo artifact として体現する
- ChatGPT で要件・設計を固め、Codex CLI で repo を読んで変更・検証する実務フローを前提にする
- 章本文とサンプル実装を相互参照しながら執筆できる状態を最初から作る
- 日本語版と英語版の原稿を chapter / appendix 単位で追跡し、英語版を issue 単位で parity へ近づける

## ディレクトリ

```text
manuscript/    # 日本語版原稿と chapter brief
manuscript-en/ # 英語版原稿の scaffold と parity tracker
sample-repo/   # 書籍全体で使う support-hub サンプル
docs/          # 全体方針と用語
docs/en/       # 英語版 docs の scaffold
prompts/       # Prompt contract の例
evals/         # Prompt 評価用ファイル
.agents/       # Codex 向け skills
scripts/       # verify / GitHub bootstrap 用スクリプト
templates/     # 日本語版で参照する再利用テンプレート
templates/en/  # 英語版テンプレートの scaffold
issue-drafts/  # GitHub issue 作成用の草案と manifest
```

## 推奨の進め方

1. `scripts/verify-book.sh` を実行して scaffold の整合性を確認する
2. GitHub 上に空 repo を作成し、この内容を push する
3. `scripts/bootstrap-github.sh owner/repo` で label / milestone / issue を投入する
4. `REPO-01` から順に issue を処理する
5. 章ごとの執筆は `issue-drafts/` 内の body と `manuscript/briefs/` を入力にして Codex に渡す

## Codex 運用原則

- 最初に root `AGENTS.md` と対象ディレクトリ配下の `AGENTS.md` を読む
- 章本文だけでなく、参照する artifact も同時に更新する
- verify が失敗したら未解決点として残し、黙って完了扱いにしない
- repeatable work は `.agents/skills/` に寄せる

## 参照

- `docs/codex-runbook.md`: Codex への投入単位と推奨プロンプト
- `manuscript/README.md`: 原稿構成と標準章テンプレート
- `manuscript-en/README.md`: 英語版原稿の構成と parity ルール
- `sample-repo/README.md`: サンプル実装の前提
