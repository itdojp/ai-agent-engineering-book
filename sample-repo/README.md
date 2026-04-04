# support-hub (sample-repo)

本ディレクトリは、本書全体で使うケーススタディです。題材は、社内サポートチームが問い合わせチケットをさばく小さな Python サービス `support-hub` です。規模は小さいですが、曖昧要求の仕様化、repo context の設計、task handoff、verification harness までを 1 つの題材で通して扱えるだけの現場感を持たせています。

本書では `docs/seed-issues.md` の 4 件を貫通ケースとして繰り返し扱います。目的は機能を増やすことではありません。AIエージェントが「答えられる」状態から「仕事を完了できる」状態へ進むとき、Prompt Contract、context pack、verification harness、approval boundary、restart packet のような artifact がどう連動するかを追うことです。

## この題材の現場
- 一次受け担当は、新規 ticket を読み、重複や緊急度を見て triage する
- 当番リードは、status と assignee を見ながら backlog の偏りを調整する
- 実装担当や運用担当は、繰り返し起きる問い合わせを検索し、根本原因や運用ルールの変更を判断する

この現場では、小さな不整合でもすぐに業務コストへつながります。status が古いまま見えると二重対応が起きます。検索が弱いと、既知事象を見つけられず同じ調査を繰り返します。assignee の意味が曖昧だと ownership が崩れます。verify と証跡が弱いと、直したつもりの変更を安心して出荷できません。

## 本書で追う貫通ケース

| ケース | 現場で困ること | 代表的な章 | 読者 payoff |
|---|---|---|---|
| `BUG-001` | ステータス更新後に旧状態が見え、二重対応が起きうる | CH01, CH02, CH09 | 範囲を閉じた bugfix を prompt と harness で完了へ持ち込む感覚をつかむ |
| `FEATURE-001` | 既存 ticket を見つけにくく、要求も曖昧 | CH01, CH03, CH04, CH05-CH08, CH10 | 曖昧要求を spec、context、verify に変える流れを理解する |
| `FEATURE-002` | assignee と監査ログの整理が長時間化しやすい | CH01, CH07, CH11, CH12 | long-running task を feature list、restart packet、owner / merge order で扱う |
| `HARNESS-001` | verify と証跡が弱く、変更を安心してレビューできない | CH01, CH09, CH10, CH12 | verification harness と evidence / approval の必要性を理解する |

各ケースの chapter guide と中心 artifact は `docs/seed-issues.md` にまとめてある。後続章で「なぜ今このケースを見るのか」を確認したくなったら、まずここへ戻る。

## まず読む docs
- `docs/domain-overview.md`
  support-hub の利用者、業務フロー、失敗コストを確認する
- `docs/seed-issues.md`
  4 件のケースがどの章と artifact に接続するかを確認する
- `docs/repo-map.md`
  実装と docs をどの順で読むかを確認する
- `docs/architecture.md`
  どの layer を触るべきか、変更判断の根拠を確認する

## 実行
```bash
python -m unittest discover -s tests -v
```

## タスク資料
- `tasks/`
- `context-packs/`
- `.agents/skills/`
