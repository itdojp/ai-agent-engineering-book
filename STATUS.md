# Repository Status

## Current State

book repo は、2026 年版の日本語 rewrite を主対象としつつ、英語版と supporting artifact を reference として維持する移行段階にある。

- GitHub repository、labels、milestones、issue / PR 運用は `main` 上で稼働している
- 日本語版は front matter、CH01-CH12、appendices、backmatter、figures を起点に、work package 単位で再基準化を進めている
- 英語版は `manuscript-en/STATUS.md` の parity tracker を維持しつつ、現時点では reference / parity backlog として扱う
- `sample-repo/`、`prompts/`、`checklists/`、`templates/`、`evals/`、`artifacts/evidence/`、`artifacts/en/evidence/` は、日本語版 rewrite に追従して整合させる対象である
- 英語版 support artifact として `docs/en/`、`prompts/en/`、`checklists/en/`、`templates/en/`、`artifacts/en/` を保守している
- `scripts/build-pages.py`、`scripts/verify-pages.sh`、`.github/workflows/pages.yml` により、book-formatter shared assets に揃えた book site を GitHub Pages へ公開できる構成を持つ
- `scripts/bootstrap-github.sh`、`scripts/create-issues.py`、`issue-drafts/` は、この運用を別 repo に移植するための reusable setup artifact として残している

## Next Recommended Action
1. `git pull --ff-only origin main` で最新の canonical source を取得する
2. `./scripts/verify-book.sh` を実行し、`sample-repo/` を触る場合は `./scripts/verify-sample.sh`、Pages build を触る場合は `./scripts/verify-pages.sh` も実行する
3. GitHub 上で次の実行単位になる work package issue を選ぶか、新規 issue を作成する
4. root `AGENTS.md`、対象ディレクトリの `AGENTS.md`、brief、artifact を読んでから issue 単位で変更する
5. verify を通したら PR を作成し、review と CI を処理する
