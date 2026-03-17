# AGENTS.md

## Scope
このファイルは repo 全体の不変条件を定義する。詳細ルールは対象ディレクトリ配下の `AGENTS.md` を読むこと。

## Core Rules
- 作業は **issue 単位** で行う。issue の Goal / Deliverables / Acceptance Criteria を満たすこと。
- 変更前に、対象ディレクトリの `AGENTS.md`、対応する chapter brief、関連 artifact を読むこと。
- **章本文だけ更新して終わりにしない**。本文が参照する artifact が存在しなければ作成し、drift していれば更新する。
- verify を実行せずに完了扱いにしない。verify に失敗した場合は failure mode と残課題を明記する。
- 破壊的な rename や構成変更を行う場合、影響範囲を brief / issue / docs に反映すること。
- 文章は日本語で書く。用語表記は `docs/glossary.md` に合わせる。

## Done Means
- 変更ファイルが issue の Deliverables に含まれている
- bad / good example、演習、artifact 参照が章の標準構成に従っている
- `scripts/verify-book.sh [chapter-id]` が通る
- `sample-repo/` を触った場合は `scripts/verify-sample.sh` も通る

## Escalation
次の条件では勝手に確定しない。
- 書籍全体の用語定義が変わる
- part を跨いだ再編が必要
- sample-repo のドメイン前提が変わる
- verify を修正してまで通す必要がある

## Suggested Workflow
1. Read issue body and chapter brief
2. Read relevant `AGENTS.md`
3. Draft changes
4. Update referenced artifacts
5. Run verify
6. Summarize changed files / verification / remaining gaps
