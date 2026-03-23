# GitHub Pages 公開

## 目的

この repo の `manuscript/` と `manuscript-en/` から reader-facing な static site を生成し、GitHub Pages で公開するための運用手順を定義する。

## 構成

- `scripts/build-pages.py`
  - 日本語版と英語版の原稿から static HTML を生成する
- `scripts/verify-pages.sh`
  - local で Pages build が成立するか検証する
- `.github/workflows/verify.yml`
  - PR / push 時に Pages build も検証する
- `.github/workflows/pages.yml`
  - `main` への push または `workflow_dispatch` で GitHub Pages に deploy する
- `site-assets/book.css`
  - Pages 用の最小スタイル

## Local Verify

```bash
./scripts/verify-pages.sh
```

この script は一時 virtualenv を作り、`requirements-pages.txt` を install したうえで site を build する。verify では次を確認する。

- root index が生成される
- `ja/` と `en/` の language home が生成される
- CH01 の日本語版 / 英語版 page が生成される
- CSS asset が配置される

## GitHub Actions

### PR / push verify

通常の `verify` workflow に `verify-pages` job を追加している。これにより、chapter や front matter を編集した PR でも Pages build failure を merge 前に検出できる。

### Pages deploy

`pages.yml` は `main` への push と `workflow_dispatch` で動く。build job が `_site/` を生成し、GitHub Pages artifact として upload し、deploy job が `github-pages` environment へ反映する。

2026-03-24 時点で利用している GitHub 公式 action version は次の通り。

- `actions/configure-pages@v5.0.0`
- `actions/upload-pages-artifact@v4.0.0`
- `actions/deploy-pages@v4.0.5`

## 最初に必要な repository 設定

GitHub Pages を初回有効化するには、repository の Settings > Pages で publish source を GitHub Actions に設定する。

この repository では branch publish ではなく custom workflow deploy を前提にする。理由は 2 つある。

- manuscript source から HTML build を挟む必要がある
- PR 時点で build-only verify と main deploy を分けたい

## 公開 URL

標準の repository site であれば、公開 URL は通常次の形になる。

```text
https://<owner>.github.io/ai-agent-engineering-book/
```

実際の URL は Pages deploy job の output でも確認できる。
