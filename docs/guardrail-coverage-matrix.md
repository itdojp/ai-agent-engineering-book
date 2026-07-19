# Guardrail Surface Coverage Matrix

確認日: 2026-07-19 UTC

## 目的

guardrail を「agent 全体へ自動的に効く安全装置」とみなさず、データと副作用が通過する surface ごとに control と blind spot を確認する。この artifact は tool-independent な最低契約を正本とする。製品や protocol の機能は、その契約を実装する profile であり、契約そのものではない。

## Tool-independent contract

すべての surface について、実行前に次を決める。

1. owner と trust level を決め、データを独立に `public` / `internal` / `restricted` / `prohibited` へ分類する。
2. 次の surface へ渡す前に最小化し、secret、credential、個人情報、顧客情報、未公開情報を redact する。
3. actor、tool、resource、destination を allowlist と least privilege で制限する。
4. 不可逆な副作用、restricted data の外部送信、未知の tool / provider は実行直前に approval を得る。
5. 保存先、閲覧者、retention、削除条件、provider の logging / training use を明示する。
6. schema、provenance、postcondition、漏えい、current-run evidence を検証する。
7. 判定は `allow` / `deny` / `escalate` のいずれかにし、必要な control や証拠が欠ける場合は推測で `allow` にしない。

入力と出力は別々に分類する。tool definition、tool result、resource、過去の trace / session は、信頼済みであることを証明できない限り外部入力として扱う。guardrail は review、verification、sandbox、authorization、human approval の代替ではない。

## Surface coverage matrix

| Surface | Classification / redaction | Permission / approval | Storage / retention | Verification | Guardrail coverage と blind spot |
|---|---|---|---|---|---|
| external input（user、Issue、PR、upload） | ingress で送信者、trust level、データクラスを記録し、prompt に入れる前に secret / PII / 未公開情報を除く | source と task scope をallowlist化し、restricted data や不明な instruction は `escalate` | raw input と sanitized input を分離し、raw data の閲覧者と削除期限を固定 | provenance、prompt injection、欠落した redaction を確認 | input guardrail は設定された入口だけを検査する。chain途中のretrievalやtool resultへ自動継承されない場合がある |
| model output | 公開先と用途に合わせて再分類し、secret、PII、内部推論、未確認主張を除く | publish、merge、tool引数への転用は別permissionとし、不可逆判断はapproval対象 | 必要な最終出力だけ保存し、中間出力はretentionを短くする | schema、引用、事実、禁止情報、task acceptanceを確認 | output guardrail が最終agentだけを対象とする構成では、中間agent出力やtool引数を保護しない |
| tool definition / discovery metadata | tool名、description、schema、annotation、discovery結果をuntrusted inputとして分類・sanitize | trusted registry、server、versionをallowlist化し、新規または変更されたtoolはapproval対象 | definition cacheにsource、version、確認日、TTLを持たせる | schema、capability、destination、side effect、署名またはtrusted sourceを確認 | tool guardrailはtool metadata自体の信頼性を保証しない。悪意あるdescriptionがinstructionとして混入しうる |
| tool call arguments | 引数、query、file path、送信payloadを対象データと独立に分類・redact | actorとtoolごとのallowlist、path / host / operation制限を適用し、高リスク引数はapproval対象 | raw secretをlogへ残さず、decisionとsanitized summaryだけ保存 | schema、境界値、path traversal、destination、data minimizationを検査 | attachされたfunction toolだけに効くguardrailや、hosted / MCP toolで適用方式が異なるruntimeがある |
| tool execution / side effect | read / write / delete / deploy / purchase等のrisk classを付ける | least privilegeとsandboxを使い、副作用の直前に対象と差分を示してapprovalを得る | approval、実行者、対象、時刻、結果をimmutable evidenceとして保持 | precondition、実行対象、postcondition、rollback readinessを確認 | pre/post guardrailはOS権限、transaction、sandbox、authorizationを置き換えない |
| tool result / output | stdout、API response、DB結果、web結果をuntrusted inputとして再分類・redact | 次のtoolや外部serviceへ転送する前に再permission判定し、restricted resultはapproval対象 | full resultを既定保存せず、必要なevidenceとretentionを定義 | provenance、instruction injection、secret、schema、stalenessを検査 | tool output guardrailが未接続、または特定tool typeだけを対象にする場合、結果は無防備になる |
| resource / file / web content | repository file、MCP resource、web page、attachmentをtrust level別に分類・redact | path、domain、resource URI、reader roleをallowlist化し、scope外resourceは `deny` / `escalate` | snapshotのsource、hash、取得日、TTL、削除条件を記録 | provenance、content-type、integrity、prompt injection、freshnessを確認 | resource取得はtool call guardrailと別経路になりうる。内容をsystem instructionとして扱わない |
| trace / evidence / log | 保存前と共有前にデータクラスを付け、prompt、arguments、results、stack traceをredact | trace viewer、export先、telemetry providerを制限し、外部exportはapproval対象 | 最小event、access control、retention、deletion、training / analytics条件を固定 | leakage scan、run id、task linkage、current-run verifyとの対応を確認 | agent / tool guardrailがtracing SDK、CI log、artifact upload、provider telemetryを自動検査するとは限らない |
| session / memory / resume | 保存時と復元時に分類し、secretや不要な会話を除き、事実と仮説を区別 | task / repo / tenant境界を越える再利用は禁止またはapproval対象 | owner、TTL、refresh / invalidate条件、削除方法を持たせる | source-of-truth、freshness、scope、contamination、revoked credentialを確認 | prompt入口のguardrailだけでは既に保存されたmemoryを削除せず、stale contextを正本にしない |
| external service / provider submission | payload、destination、jurisdiction、data classを送信前に記録し、最小化・redact | approved provider / model / region / purposeをallowlist化し、restricted dataや条件不明は `escalate` | retention、logging、training use、subprocessor、deletion、evidence locationを確認 | provider termsの確認日、送信payload summary、response provenance、egress logを検証 | local guardrailはprovider側の保存、学習利用、operator access、downstream subprocessorを強制できない |
| protocol prompts / roots | server prompt、prompt argument、root URIをuntrusted protocol inputとして分類・redact | trusted server / prompt / rootをallowlist化し、未知promptの利用やroot拡張はapproval対象。実際の境界はhost ACL / sandboxでenforceする | prompt source / version、root scope、確認日、TTLを記録 | prompt provenance / injectionとroot URIがhost側の許可範囲内か確認 | protocolのprompt discoveryはinstructionの信頼性を保証せず、rootsの通知だけではfilesystem sandboxやauthorizationにならない |
| protocol sampling / elicitation | model request、human入力要求、form fieldを独立surfaceとして分類・redact | request内容と送信先を表示し、sampling / elicitationを明示承認する | prompt、response、approval recordの保存要否とretentionを分ける | requested data、model parameters、approval、returned contentを確認 | protocolがsurfaceを定義してもhost/runtimeのconsent UIやpolicy enforcementを自動保証しない |

## Minimum adversarial walkthrough

機械可読な正本は `evals/guardrail-surface-cases.json` であり、`scripts/check-guardrail-coverage.py` が必須surface、control、case、evidenceを検査する。

| Case | 期待判定 | Walkthroughで確認すること |
|---|---|---|
| `hostile-input` | `deny` または `escalate` | 外部instructionを正本にせず、分類・redaction・provenance確認後に停止できる |
| `hostile-tool-output` | `deny` または `escalate` | tool resultを命令として実行せず、次のtoolへ渡す前に再分類できる |
| `tainted-tool-metadata` | `deny` または `escalate` | description / annotationを信頼せず、registry、version、capabilityを確認できる |
| `unsafe-side-effect` | `deny` または `escalate` | 実行直前approval、least privilege、postcondition、rollback evidenceを要求できる |
| `trace-leakage` | `deny` または `escalate` | prompt / argument / result / secretのredactionとretentionを確認できる |
| `stale-sensitive-session` | `deny` または `escalate` | task境界、freshness、source-of-truth、削除条件を確認できる |
| `external-provider-boundary` | `deny` または `escalate` | provider、purpose、region、retention、training useが未確認なら送信しない |

## Vendor / protocol profiles

### OpenAI Agents / Tools profile

OpenAI公式文書を2026-07-19 UTCに確認した。agent-level input guardrailはchainの最初のagent、agent-level output guardrailは最終出力を返すagent、tool guardrailはattachされたfunction toolを対象にする。custom managerや異なるtool surfaceへblanket coverageがあると仮定しない。human-in-the-loop approvalは副作用を伴うtoolを実行する前の独立gateとして扱う。built-in tool、function calling、tool search、remote MCP等のsurfaceと実行主体が異なるため、本書では設計上の推論として、同一のpermission / storage契約を自動継承しないものとして確認する。

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Tools](https://developers.openai.com/api/docs/guides/tools)

### MCP 2025-11-25 profile

MCP仕様を2026-07-19 UTCに確認した。server featureのprompts / resources / toolsと、client featureのsampling / roots / elicitationは別surfaceである。prompt、tool description / annotation、resource contentはtrusted serverとprovenanceを確認できるまで信頼済みとみなさず、tool invocationやsampling等のconsent / approvalをhost側のpolicyへ実装する。rootsの通知はhost ACL / sandboxの代替にしない。protocolがsurfaceを定義しても、すべてのsecurity principleをprotocol単体でenforceできるわけではない。

- [Model Context Protocol specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)

## 更新ルール

- runtime、provider、tool type、trace backend、session storeを変更したら、該当profileとminimum caseを再確認する。
- coverageが不明なsurfaceは `uncovered` と記録し、permission policyで `deny` または `escalate` にする。
- 公式仕様の版、確認日、差分、採用したcontrolをSource Notesへ残す。
