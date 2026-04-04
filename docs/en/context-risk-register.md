# Context Risk Register

| Risk | Signal | Failure Mode | Mitigation |
|---|---|---|---|
| Stale docs | docs and tests disagree | implement against an old spec | run an artifact-consistency pass regularly and check docs drift during verify |
| Summary drift | the Progress Note adds interpretation instead of facts | resume from the wrong assumptions after handoff | separate `Decided`, `Open Questions`, and `Next Step`, and update only after verify |
| Instruction bloat | `AGENTS.md` becomes long and hides the entry points | important constraints are skipped and guessing increases | split instructions into root, local, and skill layers, and move detail into docs |
| Context poisoning | unverified hypotheses stay in the Progress Note or context pack | wrong answers or breakage compound across sessions | prioritize acceptance criteria and the latest verify result, and isolate guesses in `Open Questions` |
| Hidden done criteria | completion lives only in issue discussion | stopping early | write done and verification explicitly in the task brief |
| Tool spam | long logs are kept resident as context | live context washes out stable context | keep only the important points and store the full logs as evidence |
| Secret leakage | tokens, credentials, or personal data stay in the Progress Note or context pack | credential exposure, unsafe reuse, and poor auditability | keep reference names instead of values and require redaction and secret scanning |
| Resume drift | the agent resumes from the Progress Note without reacquiring live context | stale verify results or stale state drive the next run | rerun verify or status commands during resume and treat summaries only as restart aids |
