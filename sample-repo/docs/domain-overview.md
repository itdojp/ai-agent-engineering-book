# Domain Overview

support-hub は、社内サポートチームが問い合わせチケットを扱うための最小ドメインモデルです。題材は小さいですが、日々の triage、担当アサイン、再発問い合わせの検索、運用変更の追跡という、実務で頻出する判断を載せています。本書では、この小ささを「単純だから安全」とは扱いません。小さな repo でも、要件の曖昧さ、context の欠落、verify 不足で仕事は簡単に壊れるからです。

## 利用者と役割
- 一次受け担当
  新規 ticket を確認し、重複や緊急度を見ながら status を更新する
- 当番リード
  assignee の偏りや放置 ticket を監視し、ownership を調整する
- 実装担当 / 運用担当
  繰り返し起きる問い合わせを検索し、根本原因や運用ルール変更を検討する

## 業務フロー
1. 問い合わせを ticket として起票する
2. 一次受け担当が status と assignee を更新して triage する
3. 既存の類似 ticket を検索し、再発か新規かを判断する
4. 対応結果を残し、必要なら assignment change や履歴を追えるようにする

この流れがあるため、support-hub では status、search、assignee、history が互いに独立していません。どれか 1 つの仕様が曖昧だと、現場の判断全体がぶれます。

## 失敗コスト
- status が古いままだと、未対応に見える ticket へ別担当が重複着手する
- 検索が弱いと、既知事象を見つけられず調査をやり直す
- assignee の意味が曖昧だと、誰が次に動くか分からなくなる
- verify と証跡が弱いと、直した変更を安心して review や merge に回せない

## Core Objects
- `Ticket`
  問い合わせ 1 件の状態を表す。status、assignee、history を持つ
- `TicketStore`
  ticket を保持し、読み書きの起点になる
- `SupportHubService`
  一覧取得、status 更新、検索、filter をまとめる service layer である

## Current Capabilities
- 一覧取得
- ステータス更新
- キーワード検索
- assignee での絞り込み

## 本書でこの題材を使う理由
- 1 回で読み切れるサイズなので、artifact と code の対応を追いやすい
- bugfix、feature spec、context pack、verification harness を同じ現場文脈で積み上げられる
- `docs/seed-issues.md` の 4 件を通して、Prompt Engineering から Harness Engineering までの成熟を追跡できる
