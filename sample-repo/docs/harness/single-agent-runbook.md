# Single-agent Runbook

## Purpose
support-hub で coding agent を single-agent harness として動かすときの標準起動手順、作業境界、retry rule、exit rule を定義する。コマンドは repo root で実行する前提とする。

## Required Inputs
- `AGENTS.md`
- `sample-repo/AGENTS.md`
- 対象 task brief
- `sample-repo/docs/repo-map.md`
- `sample-repo/docs/architecture.md`
- task 固有の docs / tests

## Startup Sequence
1. `./scripts/init.sh <task-brief>` を実行し、読込順と verify コマンドを確定する。
2. `sample-repo/docs/harness/permission-policy.md` を開き、approval が必要な変更を先に確認する。
3. `sample-repo/docs/harness/done-criteria.md` を開き、終了条件と report format を確認する。
4. task brief から scope、non-goals、verify 条件を抜き出す。
5. owned files、想定 verify command、approval 境界、stop condition を自分の作業メモに固定する。
6. repo に unexpected dirty diff がある場合は作業を進めず `blocked` として返す。

## Workflow
1. 変更対象を task brief で明示された work package に限定する。
2. 次の 1 手を、verify 可能な最小差分として選ぶ。
3. code、docs、tests、task artifact に drift が出ないよう同時に更新する。
4. `./scripts/verify-sample.sh` を実行し、実行コマンドと pass/fail を記録する。
5. exit state を `done` / `blocked` / `needs-human-approval` のいずれかで判定する。
6. `Changed Files`、`Verification`、`Remaining Gaps` を短く報告する。

## Retry Rules
- retry の前に failure mode を分類する。
  - missing-context: 参照 artifact が不足している
  - verify-failure: 変更仮説が外れている
  - permission-boundary: human approval が必要
  - environment-failure: command / tool / path の問題
- 新しい仮説や入力なしに同じ操作を繰り返さない。
- 同じ verify failure が続き、追加 evidence がない場合は retry ではなく `blocked` として止まる。
- tentative diff が誤っていた場合は、現在の work package 内で自分の差分だけを戻してやり直す。
- destructive な git command で repo 全体を巻き戻さない。

## Exit Rule
- `done` と言ってよいのは、`sample-repo/docs/harness/done-criteria.md` の必須条件を満たし、`./scripts/verify-sample.sh` が通ったときだけである。
- approval が必要な場合は `needs-human-approval`、入力不足や未解決の verify failure が残る場合は `blocked` として返す。

## Report Contract
- canonical な報告項目は `Changed Files`、`Verification`、`Remaining Gaps` とする。
- `blocked` または `needs-human-approval` の場合は、先頭で exit state を明示する。
- approval が必要な場合は、`Requested Change`、`Reason Approval Is Needed`、`Affected Files`、`Smallest Safe Proposal` を併記する。
