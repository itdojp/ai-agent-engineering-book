# Manuscript Layout

## 原稿構成

- `front-matter/`: はじめに、読み方ガイドなどの前付け
- `part-00/`: 本文導入
- `part-01-prompt/`, `part-02-context/`, `part-03-harness/`: 各 Part の opener と章本文
- `appendices/`: テンプレート集と用語集
- `figures/`: reader-facing な図版 source と figure plan

## 標準章構成

1. 章の位置づけ
2. 学習目標
3. 小見出し 1〜5
4. bad / good example
5. 演習 2 問
6. 参照する artifact
7. 章末のまとめ

## 原稿作成ルール

- 各章は **artifact-driven** に書く
- 章本文で言及した path は実在させる
- 前提知識が増える章は dependencies を brief に記録する
- 1 章につき 1 つの中核メッセージに絞る
- 図版 source を追加する場合は `figures/figure-plan.md` と同時に更新する

## front matter / Part opener の扱い

- front matter は読者 promise、対象読者、読み方を reader-facing に整理する
- Part opener は各 Part の役割、増える artifact、章の見取り図、到達点を短く固定する
- front matter と Part opener は章テンプレートをそのまま流用しない
- CH01 の導入は前付けの代替にせず、failure model の定義へ集中させる
