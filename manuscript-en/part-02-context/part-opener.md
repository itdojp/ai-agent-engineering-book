# Part II Context Engineering

Even a strong Prompt Contract will fail if the information shown to the AI agent is stale, incomplete, overloaded, or mixed together. Context Engineering is the work of separating the decision inputs for the agent and designing their freshness, priority, and ownership.

## Role of This Part

This part mainly targets forgetting. If repo-wide assumptions, task-specific requirements, session-local progress, and reusable workflows are not separated, the AI agent drops premises, creates summary drift, and duplicates explanations across competing artifacts.

Context Engineering builds in this order.

1. Separate context types and context budget
2. Build a stable entry point for persistent repo context
3. Fix the current task and session position with a task brief and session memory
4. Turn repeatable work into skills and context packs

## Artifacts Added in This Part

By the end of this part, the reader will have at least the following artifacts.

- context model
- repo map
- architecture / coding standards
- task brief
- Progress Note
- context pack
- SKILL.md

The point is not to add more information. The point is to keep the source of truth stable and prevent broken context from lingering.

## Chapter Map

- CH05: define the boundary between Prompt and Context
- CH06: design persistent repo context
- CH07: turn an issue into a task brief and session memory
- CH08: reuse skills and context packs

This part does not exist to accumulate docs. It exists to carry the Prompt Engineering contract through real work without letting it collapse.

## What You Should Be Able to Do by the End of This Part

By the end of this part, the reader should be able to design what an AI agent must see in repo, task, and session terms so the work does not lose its assumptions in the middle. The next part uses those inputs to close execution, verification, retry, and handoff through Harness Engineering.
