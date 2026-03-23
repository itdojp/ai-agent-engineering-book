---
id: ch06
title: Repo Context を設計する
status: draft
artifacts:
  - AGENTS.md
  - manuscript/AGENTS.md
  - sample-repo/AGENTS.md
  - sample-repo/docs/repo-map.md
  - sample-repo/docs/architecture.md
  - sample-repo/docs/coding-standards.md
dependencies:
  - ch05

---

# Repo Context を設計する

## この章の位置づけ
repo に入った直後の AI agent が `AGENTS.md` と `README.md` と `sample-repo/tests/` を行き来し始めたら、入口設計は弱い。CH05 で Context Engineering の分類を導入した。次に必要なのは、AI agent が repo に入った瞬間に迷わないための永続コンテキストを設計することである。

この章では、`AGENTS.md`、`repo-map`、`architecture`、`coding-standards` をどう分担させるかを扱う。対象は `Codex CLI` のような coding agent だが、人間のレビューにも同じ構造が効く。

## 学習目標
- 巨大 AGENTS.md を避ける理由を説明できる
- root / manuscript / sample-repo の instruction layering を設計できる
- repo-map と architecture doc の責務を分けられる


## 小見出し
### 1. AGENTS.md は百科事典ではなく地図
`AGENTS.md` は、repo の全文説明を書く場所ではない。AI agent が「まず何を読み、何を守り、どの artifact を確認すべきか」を知るための地図である。root の `AGENTS.md` は repo 全体の不変条件だけを定義し、詳細は `manuscript/AGENTS.md` と `sample-repo/AGENTS.md` に委譲している。この分割が重要なのは、すべてを root に詰めると、対象ディレクトリに無関係な detail が常に混ざるからである。

たとえば原稿だけを触る作業では、`sample-repo` の domain constraint まで毎回読む必要はない。逆に `sample-repo` のコードを直すなら、原稿向けの文体ルールよりも verify と domain constraint の方が重要になる。layering があると、AI agent は「今いるディレクトリに必要な detail」だけを追加で読める。

良い `AGENTS.md` は、完結した百科事典ではなく、次に開くべき artifact への起点である。詳細な設計理由や repo 構造の説明は、別 doc に逃がすべきである。

### 2. repo-map と architecture の役割分担
`sample-repo/docs/repo-map.md` と `sample-repo/docs/architecture.md` は似て見えるが、役割は異なる。repo-map は「どこに何があるか」を示す索引であり、architecture は「なぜその構成なのか」を示す設計説明である。この 2 つを混ぜると、参照起点も設計理由も読みにくくなる。

`repo-map.md` は `docs/domain-overview.md`、`docs/architecture.md`、`docs/coding-standards.md`、`tasks/`、`context-packs/`、コード、tests への read order を示している。これは AI agent が最初に repo を舐めるための文書である。一方 `architecture.md` は、`models.py`、`store.py`、`service.py`、`tests/` の責務と change rule を説明している。`FEATURE-001` の検索改善で `service.py` を触るべき理由は、repo-map ではなく architecture に書くべき情報である。

要するに、repo-map は「探すための文書」、architecture は「判断するための文書」である。片方で両方を済ませようとすると、map は長文化し、architecture は索引だらけになる。

### 3. coding standards と docs の更新境界
`sample-repo/docs/coding-standards.md` の役割は、コードの書き方を抽象的に語ることではない。どの種類の変更で、どの artifact を同時更新すべきかを明示することにある。実務で docs drift が起きるのは、「コードを直す」「仕様を直す」「task artifact を直す」の境界が暗黙だからである。

この repo では、public behavior を変えるなら test を必須とし、仕様変更時は product spec、acceptance criteria、ADR を同時更新し、中断や handoff があるなら progress note も更新すると決めている。これにより、AI agent は code 変更だけで done にしにくくなる。CH01 の failure mode でいう breaking things と stopping early を、repo context 側から防いでいるわけである。

coding standard に「何を同時更新するか」がないと、AI agent はコードだけ green にして docs を置き去りにしやすい。書籍プロジェクトと sample-repo のように artifact が多い repo では、実装規約より更新境界の方が重要になる。

### 4. ownership と変更影響範囲
Repo Context は ownership と影響範囲の見積もりにも使う。たとえば `sample-repo/src/support_hub/service.py` を変更するなら、少なくとも `sample-repo/tests/test_service.py` または `sample-repo/tests/test_ticket_search.py`、関連する spec / acceptance criteria / progress note を確認すべきである。`repo-map.md` の hot path と update guide は、この最小影響範囲を見積もるためにある。

大事なのは、ownership を人名で持たなくても、artifact 単位で責務を分けられることだ。`architecture.md` は設計の source of truth、`coding-standards.md` は変更規律、`tasks/` は今回の scope、`context-packs/` は再利用用の最小読み込みセットである。どの artifact が何の責務を持つかが曖昧だと、同じ説明が複数箇所に重複し、drift が起きやすい。

影響範囲の見積もりは、Context Engineering の中心的な作業である。AI agent にファイル一覧を渡すだけでなく、「変更したらどこまで再確認するか」を repo context に埋め込む必要がある。

### 5. instruction layering をどう作るか
この repo の instruction layering は 4 層で考えると整理しやすい。

1. root `AGENTS.md`: repo 全体の不変条件、verify 義務、artifact 同期
2. `manuscript/AGENTS.md`: 原稿の標準構成と文体ルール
3. `sample-repo/AGENTS.md`: domain constraint、verify、docs 更新境界
4. task brief / context pack: 今回の issue の scope、inputs、done

この layering にすると、`Codex CLI` は root で全体の枠組みを読み、対象ディレクトリに入って detail を追加し、最後に task brief で今やる仕事を確定できる。すべてを 1 ファイルに押し込むより、context budget が保ちやすい。

重要なのは、layer ごとに責務を変えることである。root は短く保ち、local は対象領域に閉じた detail だけを書く。task brief は今回の issue に閉じる。これができると、repo context は長いが読まれない文書群ではなく、AI agent が逐次参照できる operational artifact になる。



## 紙面で押さえるポイント
### Repo Context 読み順マップ

| artifact | 最初に答える問い | いつ読むか | ここで固定される判断 |
|---|---|---|---|
| `AGENTS.md` | この repo 全体で外してはいけない条件は何か | 作業開始直後 | verify 義務、artifact 同期、issue 単位の作業境界 |
| `manuscript/AGENTS.md` | 原稿作業では何を満たせばよいか | manuscript を触る前 | 章構成、演習数、artifact-driven の書き方 |
| `sample-repo/AGENTS.md` | sample-repo では何が source of truth か | sample-repo を触る前 | domain constraint、docs 更新境界、sample verify |
| `sample-repo/docs/repo-map.md` | どこから読み始め、どこに何があるか | 対象領域を特定するとき | 読み順、hot path、変更時の参照起点 |
| `sample-repo/docs/architecture.md` | なぜその構成で、どこを変えるべきか | 実装方針を決める前 | layer 責務、change rule、影響範囲 |
| `sample-repo/docs/coding-standards.md` | 変更したら何を同時更新するか | 実装前と終了前 | test、spec、acceptance criteria、progress note の更新境界 |

この表の順序は、索引から設計理由へ降りる順序でもある。先に `architecture.md` を読むと、「どこに何があるか」が未確定なまま設計論だけを読んでしまう。逆に `repo-map.md` だけで止まると、「なぜそこを触るのか」が弱い。Repo Context は、この 6 artifact を 1 回で全部読むことではなく、判断の種類ごとに参照先を切り替えられる状態を作ることにある。

## 章で使う bad / good example
bad:

```text
root `AGENTS.md` に、書籍全体の運用、原稿の文体、sample-repo の domain rule、
verify 手順、task ごとの例外を全部書く。
repo-map と architecture には同じ説明を重複させる。
```

この構成では、AI agent は最初に読むべき情報を見失う。root が長文化し、しかも対象ディレクトリに無関係な detail が常に混ざる。

good:

```text
root `AGENTS.md` には全体の不変条件だけを書く。
`manuscript/AGENTS.md` には章構成と文体ルールを置く。
`sample-repo/AGENTS.md` には verify と domain constraint を置く。
`sample-repo/docs/repo-map.md` は参照起点を示し、
`sample-repo/docs/architecture.md` は service layer と change rule を説明する。
```

この修正版では、instruction と docs の責務が分かれ、AI agent が作業対象に応じて必要な文書だけを読める。

比較観点:
- bad は root instruction が肥大化して context budget を壊している
- bad は repo-map と architecture の責務が重複している
- good は root / local / task の layering を作り、更新境界も明示している

## 演習
1. root AGENTS.md と sample-repo/AGENTS.md を分離設計する。
2. repo-map を作成し、変更の多い箇所を特定する。

## 参照する artifact
- `AGENTS.md`
  repo 全体の不変条件を確認する。CH06 では root に何を残し、何を下位へ委譲するかを見る。
- `manuscript/AGENTS.md`
  原稿作業に閉じた要求を確認する。図表を章に入れる理由もここで読める。
- `sample-repo/AGENTS.md`
  sample-repo での verify と docs 同期の境界を確認する。root だけでは足りない detail を補う。
- `sample-repo/docs/repo-map.md`
  読み始める順序と hot path を確認する。どのファイルを最初に開くべきかを CH06 の本文と対応させて読む。
- `sample-repo/docs/architecture.md`
  実装責務と change rule を確認する。repo-map が索引なら、こちらは変更判断の根拠になる。
- `sample-repo/docs/coding-standards.md`
  code 変更時に同時更新すべき artifact を確認する。done 判定が code だけで閉じない理由を押さえる。


## Source Notes / Further Reading
- この章を探し直すときは、まず `AGENTS.md`、`sample-repo/docs/repo-map.md`、`sample-repo/docs/architecture.md`、`sample-repo/docs/coding-standards.md` を正本として見る。repo-map は索引、architecture は設計理由として読み分ける。
- 次の一歩は `manuscript/backmatter/00-source-notes.md` の「CH06 Repo Context を設計する」と `manuscript/backmatter/01-読書案内.md` の「Context と repo 設計」を参照する。

## 章末まとめ
- Repo Context の仕事は、repo の全文を説明することではなく、AI agent が正しい起点と更新境界を素早く掴めるようにすることにある。
- `AGENTS.md` は地図、repo-map は索引、architecture は設計理由、coding standards は変更規律として分離すると drift を防ぎやすい。
- repo の入口が整うと、次に必要なのは今回の task だけに縮めた context である。次章では issue を task brief と session memory に変換する。
