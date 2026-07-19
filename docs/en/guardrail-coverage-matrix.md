# Guardrail Surface Coverage Matrix

Confirmed: 2026-07-19 UTC

## Purpose

Inspect controls and blind spots per data and side-effect surface instead of treating a guardrail as an automatic safety layer over the whole agent. This artifact makes the tool-independent minimum contract authoritative. Product and protocol features are profiles that implement parts of the contract, not the contract itself.

## Tool-independent contract

Decide the following before execution for every surface.

1. Assign an owner and trust level, then classify data independently as `public`, `internal`, `restricted`, or `prohibited`.
2. Minimize the data before the next surface and redact secrets, credentials, personal data, customer data, and unreleased information.
3. Restrict the actor, tool, resource, and destination with allowlists and least privilege.
4. Obtain approval immediately before irreversible side effects, external submission of restricted data, or use of an unknown tool or provider.
5. Define the storage location, readers, retention, deletion conditions, and provider logging or training use.
6. Verify schemas, provenance, postconditions, leakage, and current-run evidence.
7. Return `allow`, `deny`, or `escalate`; never guess `allow` when a required control or evidence item is missing.

Classify inputs and outputs separately. Treat tool definitions, tool results, resources, and old traces or sessions as external input unless their trust is demonstrated. Guardrails do not replace review, verification, sandboxing, authorization, or human approval.

## Surface coverage matrix

| Surface | Classification / redaction | Permission / approval | Storage / retention | Verification | Guardrail coverage and blind spot |
|---|---|---|---|---|---|
| external input (user, issue, PR, upload) | Record sender, trust level, and data class at ingress; remove secrets, PII, and unreleased data before prompting | Allowlist sources and task scope; `escalate` restricted data or unknown instructions | Separate raw and sanitized input; define raw-data readers and deletion deadline | Check provenance, prompt injection, and missing redaction | An input guardrail inspects only configured ingress. It may not carry automatically to mid-chain retrieval or tool results |
| model output | Reclassify for the destination; remove secrets, PII, hidden internal material, and unverified claims | Treat publication, merge, and reuse as tool arguments as separate permissions; require approval for irreversible decisions | Store only required final output and shorten retention for intermediate output | Check schema, citations, facts, prohibited data, and task acceptance | A final-agent output guardrail does not protect intermediate-agent output or tool arguments |
| tool definition / discovery metadata | Classify and sanitize tool names, descriptions, schemas, annotations, and discovery results as untrusted input | Allowlist trusted registry, server, and version; approve new or changed tools | Cache source, version, confirmation date, and TTL | Check schema, capability, destination, side effect, and signature or trusted source | A tool guardrail does not establish the trust of tool metadata; a hostile description can inject instructions |
| tool call arguments | Classify and redact arguments, queries, paths, and outbound payload independently of the target data | Apply actor- and tool-specific allowlists plus path, host, and operation restrictions; approve high-risk arguments | Never log raw secrets; store only the decision and a sanitized summary | Check schema, bounds, path traversal, destination, and minimization | Some runtimes cover only attached function tools; hosted and MCP tools can have different attachment paths |
| tool execution / side effect | Assign a risk class such as read, write, delete, deploy, or purchase | Use least privilege and sandboxing; show target and diff for approval immediately before the side effect | Keep immutable evidence of approval, actor, target, time, and result | Check preconditions, target, postconditions, and rollback readiness | Pre/post guardrails do not replace OS permissions, transactions, sandboxes, or authorization |
| tool result / output | Reclassify and redact stdout, API responses, database results, and web results as untrusted input | Re-authorize before forwarding to another tool or service; approve restricted results | Do not retain full results by default; define required evidence and retention | Check provenance, instruction injection, secrets, schema, and staleness | Results are exposed when output guardrails are unattached or cover only selected tool types |
| resource / file / web content | Classify and redact repository files, MCP resources, web pages, and attachments by trust level | Allowlist paths, domains, resource URIs, and reader roles; `deny` or `escalate` out-of-scope resources | Record source, hash, retrieval date, TTL, and deletion conditions | Check provenance, content type, integrity, prompt injection, and freshness | Resource retrieval can bypass a tool-call guardrail path; never treat resource content as system instruction |
| trace / evidence / log | Classify before storage and sharing; redact prompts, arguments, results, and stack traces | Restrict trace viewers, export targets, and telemetry providers; approve external export | Define minimum events, access, retention, deletion, and training or analytics terms | Scan leakage and link run id, task, and current-run verification | Agent and tool guardrails may not inspect tracing SDKs, CI logs, artifact uploads, or provider telemetry automatically |
| session / memory / resume | Classify on write and restore, remove secrets and irrelevant dialogue, and separate facts from hypotheses | Prohibit or approve reuse across task, repository, or tenant boundaries | Define owner, TTL, refresh and invalidation conditions, and deletion method | Check source of truth, freshness, scope, contamination, and revoked credentials | An ingress guardrail does not delete persisted memory and must not make stale context authoritative |
| external service / provider submission | Record payload, destination, jurisdiction, and data class before sending; minimize and redact | Allowlist provider, model, region, and purpose; `escalate` restricted data or unknown terms | Confirm retention, logging, training use, subprocessors, deletion, and evidence location | Verify terms confirmation date, payload summary, response provenance, and egress log | A local guardrail cannot enforce provider storage, training use, operator access, or downstream subprocessors |
| protocol prompts / roots | Classify and redact server prompts, prompt arguments, and root URIs as untrusted protocol input | Allowlist trusted servers, prompts, and roots; approve unknown prompts or root expansion, and enforce the actual boundary with host ACLs or sandboxes | Record prompt source and version, root scope, confirmation date, and TTL | Check prompt provenance and injection and keep root URIs inside the host-authorized boundary | Prompt discovery does not establish instruction trust, and root notification is not a filesystem sandbox or authorization control |
| protocol sampling / elicitation | Classify and redact model requests, requests for human input, and form fields independently | Display the request and destination, then approve sampling or elicitation explicitly | Separate retention decisions for prompts, responses, and approval records | Check requested data, model parameters, approval, and returned content | A protocol can define surfaces without guaranteeing the host consent UI or policy enforcement |

## Minimum adversarial walkthrough

The machine-readable source of truth is `evals/guardrail-surface-cases.json`. `scripts/check-guardrail-coverage.py` verifies required surfaces, controls, cases, and evidence.

| Case | Expected decision | Walkthrough check |
|---|---|---|
| `hostile-input` | `deny` or `escalate` | Do not make an external instruction authoritative; stop after classification, redaction, and provenance checks |
| `hostile-tool-output` | `deny` or `escalate` | Do not execute a result as an instruction; reclassify before passing it to another tool |
| `tainted-tool-metadata` | `deny` or `escalate` | Distrust descriptions and annotations; check registry, version, and capability |
| `unsafe-side-effect` | `deny` or `escalate` | Require immediate approval, least privilege, postcondition, and rollback evidence |
| `trace-leakage` | `deny` or `escalate` | Check prompt, argument, result, and secret redaction plus retention |
| `stale-sensitive-session` | `deny` or `escalate` | Check task boundary, freshness, source of truth, and deletion conditions |
| `external-provider-boundary` | `deny` or `escalate` | Do not send while provider, purpose, region, retention, or training use is unknown |

## Vendor / protocol profiles

### OpenAI Agents / Tools profile

The OpenAI official documentation was checked on 2026-07-19 UTC. An agent-level input guardrail covers the first agent in a chain, an agent-level output guardrail covers the agent that returns the final output, and a tool guardrail covers function tools to which it is attached. Do not assume blanket coverage for custom managers or other tool surfaces. Treat human-in-the-loop approval as a separate gate before a side-effecting tool runs. Because built-in tools, function calling, tool search, and remote MCP have different surfaces and execution owners, this book makes a design inference: verify their permission and storage contracts instead of assuming automatic inheritance.

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Tools](https://developers.openai.com/api/docs/guides/tools)

### MCP 2025-11-25 profile

The MCP specification was checked on 2026-07-19 UTC. Server features—prompts, resources, and tools—and client features—sampling, roots, and elicitation—are distinct surfaces. Do not trust prompts, tool descriptions or annotations, or resource content until the server and provenance are trusted. Implement consent or approval for tool invocation, sampling, and other protected operations in host policy, and do not treat root notification as a substitute for host ACLs or sandboxing. Defining a surface in the protocol does not let the protocol enforce every security principle by itself.

- [Model Context Protocol specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)

## Update rule

- Recheck the applicable profile and minimum case after changing a runtime, provider, tool type, trace backend, or session store.
- Record an unclear surface as `uncovered`, then make the permission policy return `deny` or `escalate`.
- Keep the official specification version, confirmation date, differences, and adopted controls in Source Notes.
