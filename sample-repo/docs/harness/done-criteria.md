# Done Criteria

## Core

- task brief の Goal と Acceptance Criteria を満たす
- 変更ファイルが current issue / work package の範囲に収まっている
- code、docs、tests、task artifact の間に drift がない
- required artifact が存在し、init 契約を満たしている
- `./scripts/verify-sample.sh` が `current session` で通っている
- `Changed Files`、`Verification`、`Remaining Gaps` を報告できる

## Chosen Policy Direction

Issue #227 の方針として、`done` は **approval boundary check + current-run evidence** を必須条件にする。
簡単な docs 変更であっても、古い verify 結果や推測だけでは `done` にしない。

- `current session` の foreground command 実行は許可されるが、実行した command と結果を `Verification` に残す。
- destructive git command、永続的な background process、repo 外への書き込み、追加 agent の spawn、parallel writer の起動、secret / credential 操作を実行していないことを確認する。
- missing required artifact、approval pending、または未解決の verify failure がある場合は `done` ではなく `blocked` または `needs-human-approval` にする。
- Evidence Minimum は緩和せず、少なくとも verify command、実行結果、未実行 check の理由を報告できる状態にする。

## Approval Boundary Check

- approval が必要な変更を、承認なしで実行していない
- approval 待ちの項目がある場合、exit state を `done` にしない
- `permission-policy.md` の `Agent May Proceed` と `Require Human Approval` のどちらに該当したかを説明できる

## Evidence Minimum

- 実行した verify command をそのまま言える
- pass / fail と、未実行の check があればその理由を言える
- verify が古い実行結果ではなく `current run` に紐づいている
- required artifact の有無を current tree で確認している

## Bugfix Addendum

- failing behavior を test で再現した、または既存 test で回帰 guard を確認した
- Root Cause を 1 段落で説明できる
- 不要な public interface 変更を入れていない

## Feature Or Docs Addendum

- spec、acceptance criteria、design doc の差分が現行挙動と一致している
- non-goals を scope に混ぜていない

## Exit States

- `done`: Core、Approval Boundary Check、Evidence Minimum と task 種別の追加条件を満たす
- `blocked`: 入力不足、矛盾する artifact、missing required artifact、未解決の verify failure がある
- `needs-human-approval`: permission policy の approval 条件に入った
