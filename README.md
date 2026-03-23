# AIエージェント実践: Prompt / Context / Harness Engineering

本リポジトリは、書籍原稿 (`manuscript/`)、英語版原稿 (`manuscript-en/`)、サンプル実装 (`sample-repo/`)、および執筆運用系 (`AGENTS.md` / `.agents/skills/` / `scripts/` / `issue-drafts/`) を同居させる構成です。

## 目的

- **Prompt → Context → Harness** の成熟モデルを、章本文だけでなく repo artifact として体現する
- ChatGPT で要件・設計を固め、Codex CLI で repo を読んで変更・検証する実務フローを前提にする
- 章本文とサンプル実装を相互参照しながら執筆できる状態を最初から作る
- 日本語版と英語版の原稿を chapter / appendix / front matter / backmatter / figures 単位で追跡し、英語版の parity と editorial review を issue 単位で進める

## ディレクトリ

```text
manuscript/    # 日本語版原稿と chapter brief
manuscript-en/ # 英語版原稿と parity tracker
sample-repo/   # 書籍全体で使う support-hub サンプル
docs/          # 全体方針と用語
docs/en/       # 英語版 docs
prompts/       # Prompt contract の例
prompts/en/    # 英語版 Prompt artifact
checklists/    # review / verify / hygiene checklist
checklists/en/ # 英語版 checklist
evals/         # Prompt 評価用ファイル
artifacts/     # `artifacts/evidence/` を含む共有 artifact
.agents/       # Codex 向け skills
scripts/       # verify / GitHub bootstrap 用スクリプト
templates/     # 日本語版で参照する再利用テンプレート
templates/en/  # 英語版テンプレート
issue-drafts/  # GitHub issue 作成用の草案と manifest
```

## 推奨の進め方

1. `git pull --ff-only origin main` で canonical source を同期する
2. `./scripts/verify-book.sh` を実行し、`sample-repo/` を触る作業では `./scripts/verify-sample.sh` も実行する
3. GitHub 上で次に扱う 1 issue を選ぶか、新しい issue を作成して作業単位を固定する
4. root `AGENTS.md` と対象ディレクトリ配下の `AGENTS.md`、対応する brief、関連 artifact を読む
5. issue 単位で変更し、verify を通したうえで PR を作成する
6. `scripts/bootstrap-github.sh owner/repo` は、この運用を別 repo に移植するときの再利用用として扱う

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
