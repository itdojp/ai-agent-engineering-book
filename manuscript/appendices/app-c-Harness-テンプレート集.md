# Harness テンプレート集

Harness Engineering は、「agent に作業させる」段階から「安全に完了・停止・再開させる」段階へ進むための設計である。ここで必要になるのは、test だけではない。verify の順序、権限境界、中断後の再開条件を artifact として固定する必要がある。

この appendix では、CH09 から CH12 で繰り返し使った harness artifact を再利用しやすい形でまとめる。対象は single-agent と long-running task の両方だが、どちらも基本は同じである。どこまで自律で進めてよいか、どこで止まるか、再開時に何を読むかを先に書く。

## 1. Verify Checklist Template

`templates/verify-checklist.md` は、verification harness を review-ready な形に揃えるための checklist である。test を回す前後の確認事項を 1 つの list にまとめる。

推奨の使い方は三段階である。

- `Before Edit`: 守るべき behavior、failing test の必要性、local verify command、approval boundary を先に確定する
- `During Change`: `Scope and Non-goals` の逸脱、docs / task artifact の更新漏れ、verify failure の分類を確認する
- `Before Review`: `Goal`、`Changed Files`、`Verification`、`Evidence / Approval`、`Remaining Gaps` が current-run の内容と一致しているか確認する

`checklists/verification.md` は、この template を book repo 用に具体化した実例である。checklist は長くするより、merge 前に本当に見返す項目だけに絞る方が運用しやすい。

## 2. Restart Protocol Template

`templates/restart-protocol.md` は、long-running task を session 間で安全に再開する手順である。CH11 で扱ったとおり、restart は「前回の続きらしいこと」を始める作業ではない。最新の verify と open question を前提に、次の 1 手を選び直す作業である。

template の中核は 3 つある。

- `Restart Packet (Canonical Inputs)`: 再開前に揃える最小入力
- `Restart Steps`: 読み順と次の 1 手の決め方
- `Stop Conditions`: 情報不足や衝突の疑いがあるときに止まる条件

`sample-repo/docs/harness/restart-protocol.md` では、plan、feature list、最新 `Progress Note`、verify evidence、open questions から成る `restart packet` を定義している。restart protocol がないまま multi-agent を始めると、役割分担より先に state が壊れる。

## 3. Permission Policy Template

`templates/permission-policy.md` は、coding agent が自律で進めてよい変更と human approval が必要な変更を分けるための template である。Harness Engineering では、権限境界を prompt の中に埋め込むのではなく、独立 artifact として持つ方が保守しやすい。

最低限、次の section を持つとよい。

- `Purpose`: どの harness で使う policy かを書く
- `Agent May Proceed`: 自律実行してよい変更を列挙する
- `Require Human Approval`: approval boundary に触れる変更、interface 変更、外部依存、verify 基盤変更などを止める
- `Stop And Report`: source of truth の衝突や無関係 failure など、作業継続より報告を優先すべき条件を書く
- `Escalation Format`: `Evidence / Approval` に残すべき判断材料と、何を人間へ報告すべきかを固定する

`sample-repo/docs/harness/permission-policy.md` は、single-agent harness 向けの具体例である。policy が曖昧な repo では、agent が不用意に public interface や CI を変更しやすい。逆に policy が明確なら、止まるべきときに止まれる。

## 4. 運用上の注意

Harness artifact では、次の 3 点を混同しない。

- verify が通ったこと
- done criteria を満たしたこと
- approval boundary に触れていない、または必要な承認が `Evidence / Approval` に残っていること

test pass は必要条件だが十分条件ではない。evidence が足りない、approval boundary に触れているのに承認が整理されていない、task artifact が stale という状態では、まだ review-ready ではない。Harness Engineering は、この差分を言語化して artifact に残すための工程である。

## 参照する artifact

- `templates/verify-checklist.md`
- `templates/restart-protocol.md`
- `templates/permission-policy.md`
- `checklists/verification.md`
- `sample-repo/docs/harness/restart-protocol.md`
- `sample-repo/docs/harness/permission-policy.md`
