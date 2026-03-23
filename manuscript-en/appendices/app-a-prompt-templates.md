# Prompt Templates

## Purpose

Prompt Engineering in this book is not the search for clever wording. It is the work of fixing the inputs, constraints, completion criteria, and output format that let a single task complete reliably. This appendix collects the smallest reusable templates that support that job.

Prompt templates are used to define the work boundary before implementation or review begins. The goal is not to write a long explanation. The goal is to remove ambiguity and cut the task into a unit that can be verified.

## Included Artifacts

- `templates/prompt-contract.md`
- `templates/prompt-rubric.md`
- `templates/en/prompt-contract.md`
- `templates/en/prompt-rubric.md`

## 1. Prompt Contract Template

`templates/prompt-contract.md` defines the book's canonical Prompt Contract shape, and `templates/en/prompt-contract.md` provides the English counterpart for English-manuscript use. As CH02 explains, the important thing is not only to say what the agent should do. The contract must also fix which inputs it may use, which actions it must not take, and what counts as done.

Each section has a distinct job.

- `Objective`: fix the target result in one sentence
- `Inputs`: list the issue, task brief, spec, tests, and verify commands that the worker must read
- `Constraints`: limit scope, preserve public contracts, and name artifacts that must be updated together
- `Forbidden Actions`: stop risky guesses and unrelated work before execution starts
- `Missing Information Policy`: separate the conditions that should block execution from the conditions that allow a documented assumption
- `Completion Criteria`: define done in words that can be verified
- `Output Format`: fix the final report headings so review is faster and more consistent

In practice, `prompts/en/bugfix-contract.md` and `prompts/en/feature-contract.md` are the worked examples. The `Objective` and `Completion Criteria` differ by task type, but the contract structure stays stable. First fix the structure, then fill only the task-specific differences.

A minimal fill looks like this:

```md
## Objective
Identify the root cause of the target bug and fix it with the smallest safe change.

## Inputs
- issue or task brief
- repro steps
- related tests
- verify command

## Constraints
- do not change the public interface
- add or update the failing test first

## Forbidden Actions
- do not mix unrelated refactors
- do not skip verify

## Completion Criteria
- a test fails before the fix and passes after the fix
- the required verify command passes
```

When you write a Prompt Contract, define both of these boundaries:

- what should stop the agent before execution starts
- what lets the reviewer call the work complete after execution ends

A prompt that defines only one side may still read well, but it is weak as an operational contract.

## 2. Prompt Rubric Template

`templates/prompt-rubric.md` defines the canonical rubric shape, and `templates/en/prompt-rubric.md` provides the English counterpart. The rubric exists so Prompt Engineering does not collapse into preference or folklore. As CH04 argues, prompt quality must be evaluated, not assumed.

At minimum, the rubric should cover these criteria.

- `Goal clarity`
- `Input completeness`
- `Constraint clarity`
- `Forbidden action clarity`
- `Verifiability`
- `Output format specificity`

In practical use, a three-point scale is usually enough.

- `0`: fail
- `1`: partial
- `2`: pass

The point is not fine-grained scoring. The point is to explain what improved between one prompt version and the next. Without a rubric, teams tend to preserve prompts that happened to look good once and miss the next regression.

## 3. How to Use Them in Practice

The Prompt Contract and the Prompt Rubric solve different problems.

- the Prompt Contract is the execution artifact
- the Prompt Rubric is the evaluation artifact

The recommended order is contract first, rubric second. If the rubric comes first, teams often score prompts before they have fixed which single task they are trying to stabilize.

Appendix A stays within Prompt Engineering. Repo-wide reading order, task history, and session carry-over belong to Context Engineering and later appendices. Within this appendix, focus on the prompt artifact that stabilizes one task.

## Parity Notes

- Japanese source: `manuscript/appendices/app-a-Prompt-テンプレート集.md`
- Publication target: preserve the Japanese appendix's boundary between Prompt Contract and Prompt Rubric, its practical minimal examples, and its Prompt-only scope boundary.

## Referenced Artifacts

- `templates/prompt-contract.md`
- `templates/prompt-rubric.md`
- `templates/en/prompt-contract.md`
- `templates/en/prompt-rubric.md`
- `prompts/en/bugfix-contract.md`
- `prompts/en/feature-contract.md`
