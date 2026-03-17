# support-hub (sample-repo)

本ディレクトリは書籍全体で使うサンプル実装です。サポートチケット管理の小さな Python ドメインモデルを題材に、Prompt Engineering / Context Engineering / Harness Engineering の各章で artifact とコード変更を積み上げます。
本書では `docs/seed-issues.md` にある 4 件を貫通ケースとして繰り返し扱い、Prompt Engineering から Context Engineering、Harness Engineering へと artifact を増やしていきます。

## ドメイン
- チケットの一覧
- ステータス更新
- キーワード検索
- assignee フィルタ
- 監査ログ（後続 issue で追加）

## 実行
```bash
python -m unittest discover -s tests -v
```

## 重要な docs
- `docs/domain-overview.md`
- `docs/repo-map.md`
- `docs/architecture.md`
- `docs/seed-issues.md`

## タスク資料
- `tasks/`
- `context-packs/`
- `.agents/skills/`
