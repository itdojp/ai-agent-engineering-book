# Permission Policy

## Purpose

single-agent harness で、coding agent が自律で進めてよい変更と human approval が必要な変更を分ける。

## Chosen Policy Direction

Issue #227 の方針として、permission policy は **strict-by-default** を維持する。
Runtime が foreground command、hosted tool、または自動実行を提供していても、承認境界はこの artifact を source of truth とする。

- current session で完結する foreground command は、task brief の範囲内で、短時間に終了し、repo 内の検証・調査・生成に閉じる場合だけ自律実行してよい。
- destructive な git command、永続的な background process、repo 外への書き込み、secret / credential を使う操作、追加 agent の spawn、parallel writer の起動は human approval のまま維持する。
- `done` 判定では、approval boundary を越えていないことを明示的に確認する。
- required artifact が欠けている場合は、推測で補完せず `Stop And Report` として扱う。

## Agent May Proceed

- task brief に含まれる範囲での code / docs / tests 更新
- failing test の追加または更新
- 変更した挙動に追随する docs / task artifact の同期
- read-only の調査コマンド、`./scripts/verify-sample.sh` の実行
- scope 内の `Progress Note` 更新
- current session で完結する foreground command の実行
  - 例: repo 内の test、lint、format、build、grep、生成スクリプト
  - 条件: command が foreground で終了し、永続 process を残さず、repo 外へ書き込まず、secret / credential を要求しない

## Require Human Approval

- public interface、CLI、出力契約の変更
- `docs/domain-overview.md`、`docs/architecture.md` にあるドメイン前提の変更
- verify script、CI、permission policy 自体の変更
  - ただし current issue がそれらの更新を deliverable に含む場合は、その issue scope 内で進めてよい
- dependency 追加、外部 service 利用、secret / credential が必要な操作
- destructive な git command、永続的な background process、repo 外への書き込み
- 追加 agent の spawn や parallel writer の起動
- stated work package の外側へ広がる変更

## Stop And Report

- task brief、spec、tests の間で矛盾があり source of truth が決められない
- 現在の diff と無関係な verify failure が出ている
- 他者の未理解な差分や unexpected dirty file があり、上書きの危険がある
- required artifact が欠けていて init 契約を満たせない
- approval が必要な操作をしないと acceptance criteria を満たせない

## Escalation Format

- Requested Change
- Reason Approval Is Needed
- Affected Files
- Smallest Safe Proposal
