# Codex Runbook

## 原則

- 1 issue = 1 work package として扱う
- 入力は **issue body + chapter brief + relevant AGENTS + existing artifacts**
- 出力は **本文 + artifact 更新 + verification result**
- 作業後は changed files / verification / remaining gaps を短く報告する

## 推奨プロンプトの構造

```text
Read AGENTS.md, the relevant local AGENTS.md, the target brief, and the issue body.
Draft the target chapter or artifact.
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

## 避けること

- 本文だけ先に書いて artifact を放置する
- verify なしで「完了」とする
- giant prompt にルールを全部書く
- 同じ指示を毎回コピペする（skills へ昇格させる）

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
