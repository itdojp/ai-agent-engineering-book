# Part I Prompt Engineering

Prompt Engineering is not the work of persuading an AI agent to sound helpful. It is the work of fixing the boundary of one task as a contract and reducing wrong answers. This part turns an ambiguous request into a Prompt Contract, a spec, acceptance criteria, and prompt evaluation artifacts.

## Role of This Part

This part deals with failures that happen at the entrance to the work. Its main target is the wrong answer. If the request is still ambiguous, if objective and constraints are blended together, or if completion criteria are missing, the AI agent can still sound coherent while missing the task.

Prompt Engineering proceeds in three steps.

1. Fix the input/output contract of one task with a Prompt Contract
2. Use ChatGPT to turn an ambiguous request into a spec and design decisions
3. Evaluate the prompt with reusable cases and a rubric so success does not depend on luck

## Artifacts Added in This Part

By the end of this part, the reader will have at least the following artifacts.

- Prompt Contract
- product spec
- acceptance criteria
- ADR
- prompt eval case
- prompt rubric

This part does not yet cover long-running task memory or verification operations. The first goal is to make a single task hard to misread.

## Chapter Map

- CH02: design prompts as contracts
- CH03: use ChatGPT to shape requirements and design
- CH04: evaluate prompts and detect regressions

The three chapters have distinct roles. CH02 fixes the contract. CH03 stabilizes the request itself. CH04 makes prompt quality comparable across revisions. Any one of the three is too weak on its own.

## What You Should Be Able to Do by the End of This Part

By the end of this part, the reader should be able to move beyond “a prompt that seems good enough” and turn a single task into implementation-ready artifacts. The next part keeps those artifacts stable across repo work and multiple sessions by moving into Context Engineering.
