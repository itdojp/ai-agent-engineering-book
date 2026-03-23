# manuscript-en/AGENTS.md

## Purpose
英語版原稿の構成、文体、そして日本語版との parity ルールを定義する。

## Style
- 本文は英語で書く
- technical book tone を保ち、冗長な会話調にしない
- 日本語版の chapter contract、artifact 参照、演習数を維持する
- 日本語版にある具体例、bad / good example、artifact 参照を落とさない
- 意訳で構成を崩さず、chapter / appendix / front matter / backmatter / figures の対応関係を守る

## Chapter Contract
英語版 chapter には次を含める。
- `## Role in This Book`
- `## Learning Objectives`
- `## Outline`
- `## Exercises`
- `## Referenced Artifacts`
- `## Parity Notes`

## Appendix Contract
英語版 appendix には次を含める。
- `## Purpose`
- `## Included Artifacts`
- `## Parity Notes`
- `## Referenced Artifacts`

## Parity Rules
- `manuscript/` の対応 chapter / appendix / `manuscript/front-matter/` / `manuscript/backmatter/` / `manuscript/figures/` を source とする
- chapter / appendix は日本語版 brief と対応させる
- front matter / backmatter は対応する directory / file 構成と対応させる
- figures は `manuscript/figures/figure-plan.md` と figure source 群と対応させる
- 英語版の progress は `manuscript-en/STATUS.md` に反映する
- 日本語版で artifact が増減したら、英語版 brief と status も追従させる
