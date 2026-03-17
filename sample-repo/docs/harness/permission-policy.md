# Permission Policy

## Purpose
single-agent harness で、coding agent が自律で進めてよい変更と human approval が必要な変更を分ける。

## Agent May Proceed
- task brief に含まれる範囲での code / docs / tests 更新
- failing test の追加または更新
- 変更した挙動に追随する docs / task artifact の同期
- read-only の調査コマンド、`./scripts/verify-sample.sh` の実行
- scope 内の progress note 更新

## Require Human Approval
- public interface、CLI、出力契約の変更
- `docs/domain-overview.md`、`docs/architecture.md` にあるドメイン前提の変更
- verify script、CI、permission policy 自体の変更
  - ただし current issue がそれらの更新を deliverable に含む場合は、その issue scope 内で進めてよい
- dependency 追加、外部 service 利用、secret / credential が必要な操作
- stated work package の外側へ広がる変更

## Stop And Report
- task brief、spec、tests の間で矛盾があり source of truth が決められない
- 現在の diff と無関係な verify failure が出ている
- 他者の未理解な差分にぶつかり、上書きの危険がある

## Escalation Format
- Requested Change
- Reason Approval Is Needed
- Affected Files
- Smallest Safe Proposal
