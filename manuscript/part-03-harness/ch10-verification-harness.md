---
id: ch10
title: Verification Harness を作る
status: draft-outline
artifacts:
  - .github/workflows/verify.yml
  - checklists/verification.md
  - sample-repo/tests/test_ticket_search.py
  - artifacts/evidence/README.md
dependencies:
  - ch09

---

# Verification Harness を作る

## この章の位置づけ
テスト・lint・typecheck・証跡収集・CI をまとめて verification harness として設計する。

## 学習目標
- local verify と CI verify の役割を分けられる
- UI 変更時の evidence bundle を設計できる
- human approval をどこに置くか説明できる


## 小見出し
### 1. テストを書いてから触る
- 狙い:
- 扱う artifact:
- bad example:
- good example:
- 本文メモ:

### 2. lint / typecheck / unit / e2e の順序
- 狙い:
- 扱う artifact:
- bad example:
- good example:
- 本文メモ:

### 3. UI 変更の証跡
- 狙い:
- 扱う artifact:
- bad example:
- good example:
- 本文メモ:

### 4. CI と local verify の分担
- 狙い:
- 扱う artifact:
- bad example:
- good example:
- 本文メモ:

### 5. human approval の位置
- 狙い:
- 扱う artifact:
- bad example:
- good example:
- 本文メモ:



## 章で使う bad / good example
- bad:
- good:
- 比較観点:

## 演習
1. failing test を先に足してから修正する。
2. UI変更に対する evidence bundle を作る。

## 参照する artifact
- `.github/workflows/verify.yml`
- `checklists/verification.md`
- `sample-repo/tests/test_ticket_search.py`
- `artifacts/evidence/README.md`


## 章末まとめ
- この章の core message:
- 次章への橋渡し:
