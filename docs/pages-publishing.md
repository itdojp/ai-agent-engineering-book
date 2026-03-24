# GitHub Pages 公開

## 目的

この repo の `manuscript/` と `manuscript-en/` から、`itdojp/book-formatter` の shared layout に揃えた reader-facing な book site を生成し、GitHub Pages で公開するための運用手順を定義する。

## 構成

- `scripts/build-pages.py`
  - 日本語版と英語版の原稿から book-formatter 互換の static HTML を生成する
- `scripts/verify-pages.sh`
  - local で Pages build が成立するか検証する
- `.github/workflows/verify.yml`
  - PR / push 時に Pages build も検証する
- `.github/workflows/pages.yml`
  - `main` への push または `workflow_dispatch` で GitHub Pages に deploy する
- `site-assets/formatter/`
  - `book-formatter` から vendor した shared CSS / JS
- `site-assets/book-custom.css`
  - formatter shared asset の上に載せる、この repo 固有の追加 CSS

## Local Verify

```bash
./scripts/verify-pages.sh
```

この script は一時 virtualenv を作り、`requirements-pages.txt` を install したうえで site を build する。verify では次を確認する。

- root が日本語版の書籍トップとして生成される
- `/en/` が英語版トップとして生成される
- CH01 の日本語版 / 英語版 page が生成される
- formatter shared asset と custom CSS / JS が配置される
- 公開トップに operator wording (`Publishing Guide` / `canonical source`) が残っていない

## GitHub Actions

### PR / push verify

通常の `verify` workflow に `verify-pages` job を追加している。これにより、chapter や front matter を編集した PR でも Pages build failure と public-site drift を merge 前に検出できる。

### Pages deploy

`pages.yml` は `main` への push と `workflow_dispatch` で動く。build job が `_site/` を生成し、GitHub Pages artifact として upload し、deploy job が `github-pages` environment へ反映する。

公開 URL の構成は次の通りである。

- `/`
  - 日本語版の導入ページ
- `/en/`
  - 英語版の導入ページ
- `/chapters/ch01/` 以降
  - 日本語版 chapter / appendix / backmatter
- `/en/chapters/ch01/` 以降
  - 英語版 chapter / appendix / backmatter

2026-03-24 時点で利用している GitHub 公式 action version は次の通り。

- `actions/configure-pages@v5.0.0`
- `actions/upload-pages-artifact@v4.0.0`
- `actions/deploy-pages@v4.0.5`

2026-03-24 時点の formatter asset vendor source は次の通り。

- `https://github.com/itdojp/book-formatter`
- commit `2170e0589d1d323649f3602db688d7d12cd7b21d`

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
