# Issue to Plan

## Purpose
sample-repo 向け issue / brief を実装計画に変換する。

## Use When
- issue を着手可能な plan に分解したいとき
- code / docs / tests / task artifact の更新範囲を先に固定したいとき

## Read First
- `docs/repo-map.md`
- `docs/architecture.md`
- `docs/coding-standards.md`
- 関連する `tasks/` と `context-packs/`

## Required Output
- scope
- files to read
- files to change
- tests to add / update
- docs to update
- verify command

## Guardrails
- plan に issue 外の拡張を入れない
- verify と docs 更新を省略しない
- public behavior を変える場合は tests を先に挙げる
