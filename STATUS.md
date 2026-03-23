# Repository Status

## Current State

book repo の bootstrap は完了している。

- GitHub repository、labels、milestones、issue / PR 運用は `main` 上で稼働している
- 日本語版は front matter、CH01-CH12、appendices、backmatter、figures を含めて drafted 状態にある
- 英語版は `manuscript-en/STATUS.md` の parity tracker に従って、front matter、CH01-CH12、appendices、backmatter、figures を drafted 状態で保持している
- `sample-repo/`、`prompts/`、`checklists/`、`templates/`、`evals/` は本文参照と整合する状態に保たれている
- `scripts/bootstrap-github.sh`、`scripts/create-issues.py`、`issue-drafts/` は、この運用を別 repo に移植するための reusable setup artifact として残している

## Next Recommended Action
1. `git pull --ff-only origin main` で最新の canonical source を取得する
2. `./scripts/verify-book.sh` を実行し、`sample-repo/` を触る場合は `./scripts/verify-sample.sh` も実行する
3. GitHub 上で次の実行単位になる issue を選ぶか、新規 issue を作成する
4. root `AGENTS.md`、対象ディレクトリの `AGENTS.md`、brief、artifact を読んでから issue 単位で変更する
5. verify を通したら PR を作成し、review と CI を処理する
