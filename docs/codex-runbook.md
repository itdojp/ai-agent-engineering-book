# Codex Runbook

## 原則

- 1 issue = 1 work package として扱う
- 入力は **issue body + chapter brief + relevant AGENTS + existing artifacts** を基本とする
- 出力は **本文 + artifact 更新 + verification result** とする
- 作業後は changed files / verification / remaining gaps を短く報告する
- 外部 capability を使っても、repo の source of truth は repo artifact に残す

## Input Layering

| 層 | 役割 | 典型 artifact |
|---|---|---|
| Prompt Contract | 単一 task の目的と完了条件を固定する | chapter fix prompt、feature prompt |
| `AGENTS.md` | repo entrypoint と不変条件を示す | root / local `AGENTS.md` |
| skill | 再利用 workflow を固定する | `SKILL.md` |
| context pack | task 固有の読み順と canonical fact を束ねる | `context-packs/*.md` |
| MCP-connected capability | runtime に追加能力を接続する | tool / resource / prompt access |

`AGENTS.md` は repo entrypoint、`SKILL.md` は repeatable work unit、context pack は task-specific read set である。MCP-connected capability は追加能力の接続面であり、repo artifact の代替ではない。

## 推奨プロンプトの構造

```text
Read AGENTS.md, the relevant local AGENTS.md, the target brief, and the issue body.
Review the existing artifacts that define the source of truth for this task.
Draft or revise the target chapter or artifact.
Then update every referenced artifact if the text would otherwise drift.
Run the required verify scripts.
Return only:
- changed files
- verification results
- remaining gaps (only if verification failed)
```

## 推奨 work package

### Chapter drafting
- 章本文
- 章が参照する artifact
- chapter-level verify

### Consistency pass
- 用語統一
- cross-reference
- 参照パスの存在確認
- glossary との整合性

### Sample repo implementation
- issue brief
- code change
- test change
- docs / `Progress Note` 更新

## Skill を small に保つルール

- repo 全体の不変条件は `AGENTS.md` に置く
- skill には repeatable workflow と output contract だけを書く
- task-specific read order は context pack に置く
- live な外部取得結果は repo artifact に昇格するまで source of truth にしない

## 避けること

- 本文だけ先に書いて artifact を放置する
- verify なしで「完了」とする
- giant prompt にルールを全部書く
- 同じ指示を毎回コピペする（skills へ昇格させる）
- MCP や tool 接続があることを理由に brief / AGENTS / spec を省略する

## 章執筆の recommended order

1. CH01
2. CH02
3. CH03
4. CH04
5. CH05
6. CH06
7. CH07
8. CH08
9. CH09
10. CH10
11. CH11
12. CH12
13. Appendices
14. Polish / consistency pass
