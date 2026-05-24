# Session Memory Policy

## 目的
セッションを跨いでも、同じ task brief と同じ verify 根拠に戻れるようにする。

## 方針決定

Issue #228 の方針として、session memory policy では **Resume Packet** を正規名称にする。章本文では読者向けの再開手順として `restart packet（Resume Packet）` と呼んでよいが、policy artifact での正規名称は Resume Packet である。

- `Blocking / Approval` は必須項目ではなく、approval boundary で停止した場合だけ使う任意項目として維持する。
- `Progress Note` は stable な task context を上書きしない。Goal、Constraints、Acceptance Criteria は task brief を正本とし、`Progress Note` では言い換えない。
- approval pending で停止するときは、通常の中断と同じく更新タイミングに含める。

## Progress Note の必須項目

- `Current Goal`: 今の 1 タスク
- `Completed`: 完了した変更
- `Decided`: verify または artifact で確定した判断
- `Open Questions`: 未確定の論点
- `Changed Files`: 直近で触った主要ファイル
- `Last Verify`: 最後に実行した verify と結果
- `Resume Steps`: 再開時に開くファイルと順序
- `Next Step`: 次にやる 1 手

## 任意項目

- `Status`: quick scan 用の短い状態表示。source of truth にはしない
- `Blocking / Approval`: approval boundary で停止した場合だけ、止まる理由、必要な判断、再開条件を残す

## 保存しないもの

- 冗長な探索ログ全文
- 一時的な仮説の羅列
- 未検証の断定
- 既に task brief にある情報の重複

## Resume Packet の最低入力

1. task brief
2. 最新 `Progress Note`
3. 最新 verify 結果
4. 再開時に読むべきファイル一覧

approval boundary で止まったときは、上記に加えて pending な判断、添付済み evidence、再開に必要な human decision を `Blocking / Approval` に残す。章本文で `restart packet（Resume Packet）` と書く場合も、この最低入力セットを指す。

`docs/en/session-memory-policy.md` は本書と整合させる。`Blocking / Approval` を追加・変更した場合は、同等の項目名と説明、関連する `Resume Packet` / Drift Guard / 更新タイミングも英語版へ反映する。

## Drift Guard

- Acceptance Criteria は task brief から原文で引用する
- 未確定事項は `Decided` に入れない
- verify 実行前後で summary を分けて書かない
- open question が解決したら `Progress Note` から消すのではなく `Decided` に昇格させる
- `Progress Note` で Goal、Constraints、Acceptance Criteria を言い換えず、stable な task context を上書きしない
- approval boundary で止めた場合は、何を変えると境界を越えるのかを明記する

## 更新タイミング

- 作業を中断するとき
- verify が終わった直後
- handoff 前
- 重要な設計判断を固めたとき
- approval pending で停止するとき
