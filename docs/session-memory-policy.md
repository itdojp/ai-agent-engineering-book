# Session Memory Policy

## 目的
セッションを跨いでも、同じ task brief と同じ verify 根拠に戻れるようにする。

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

## Restart Packet（Resume Packet）の最低入力

1. task brief
2. 最新 `Progress Note`
3. 最新 verify 結果
4. 再開時に読むべきファイル一覧

approval boundary で止まったときは、上記に加えて pending な判断、添付済み evidence、再開に必要な human decision を `Blocking / Approval` に残す。

`docs/en/session-memory-policy.md` は本書と整合させる。`Blocking / Approval` を追加・変更した場合は、同等の項目名と説明、関連する `Restart Packet` / Drift Guard / 更新タイミングも英語版へ反映する。

## Drift Guard

- Acceptance Criteria は task brief から原文で引用する
- 未確定事項は `Decided` に入れない
- verify 実行前後で summary を分けて書かない
- open question が解決したら `Progress Note` から消すのではなく `Decided` に昇格させる
- `Progress Note` で Goal や Constraints を言い換えず、stable な task context を上書きしない
- approval boundary で止めた場合は、何を変えると境界を越えるのかを明記する

## 更新タイミング

- 作業を中断するとき
- verify が終わった直後
- handoff 前
- 重要な設計判断を固めたとき
- approval pending で停止するとき
