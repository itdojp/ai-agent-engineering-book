---
name: verification
description: Use when standardizing post-change verification for support-hub code or docs before handoff.
---

# Verification

## Purpose
support-hub の変更に対する検証を標準化する。

## Use When
- code または docs を変更した後
- handoff 前に verify 証跡を残したいとき

## Read First
- `AGENTS.md`
- `sample-repo/AGENTS.md`
- 対象 task brief
- `sample-repo/docs/harness/single-agent-runbook.md`
- `sample-repo/docs/harness/done-criteria.md`

## Steps
1. impacted tests を確認する
2. `python -m unittest discover -s tests -v` を実行する
3. docs drift がないか確認する
4. current issue に必要な task artifact を更新する
5. `Progress Note` へ残す要点を整理する

## Output Contract
- 実行した verify command
- pass / fail
- docs drift の有無
- `Progress Note` へ残す要点

## Guardrails
- verify 結果だけで issue body / brief / AGENTS を上書きしない
- skill は repeatable verification workflow を定義し、repo 固有の source of truth は task brief と docs に残す
- MCP や外部 tool から得た live 情報は補助として使い、repo artifact の代替にはしない
