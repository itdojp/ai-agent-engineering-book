# How to Read This Book

The book has three parts, and the order is intentional. Prompts alone cannot preserve assumptions. Context alone cannot close execution and verification. Harnesses alone can still make the wrong assumptions fail more efficiently. The three layers need to stack in order.

## Three-Part Structure

### Part I Prompt Engineering

The first goal is to fix the contract for one task. This part covers Prompt Contracts, requirements shaping, and prompt evaluation. The point is to keep the AI agent from misreading what it is supposed to do.

### Part II Context Engineering

The second goal is to fix the decision inputs. This part covers repo context, task briefs, session memory, skills, and context packs. The point is to keep the AI agent from dropping assumptions or losing the path to the right artifacts.

### Part III Harness Engineering

The final goal is to fix execution boundaries and operating rules. This part covers the single-agent harness, verification harness, restart protocol, and operating model. The point is to keep the AI agent from stopping before verification or drifting into unsafe autonomy.

## Three Ways to Read This Book

### Read Straight Through

This is the recommended path. Read CH01 through CH12 in order and watch the same recurring cases accumulate Prompt, Context, and Harness layers. This path is the best fit for readers who want to introduce AI agents into team development work.

### Read Backward from the Failure Mode

If the main failure mode is already clear, you can start from that part of the book.

- Too many wrong answers: CH02-CH04
- The agent forgets assumptions or loses track of artifacts: CH05-CH08
- The agent stops early or breaks working behavior: CH09-CH12

Later parts depend on earlier ones, so this path still assumes you will move backward when needed.

### Read Alongside the Repo

This method opens `sample-repo` while you read. Use the `Referenced Artifacts` section at the end of each chapter to inspect the actual files after you understand their role from the prose. It is usually easier to read the explanation first and then open the artifact than to browse the repo from the start.

## How to Use the Repo

The repo is not the main character. It is the supporting evidence, the storage for reusable artifacts, and the basis for verification. The most effective order is:

1. Read the problem statement in the chapter
2. Understand the role of the artifact introduced in that chapter
3. Open the repo artifact only when you need the concrete example

If you browse the repo first, the artifacts can look like an unstructured list. If you read the prose first, the reason each artifact exists is easier to see.

## How to Track the Recurring Cases

The recurring cases change meaning as the book moves through Prompt, Context, and Harness.

- `BUG-001`: Prompt Contracts for bugfix work, the single-agent harness, and done criteria
- `FEATURE-001`: product specs, acceptance criteria, ADRs, context packs, and the verification harness
- `FEATURE-002`: feature lists, restart protocols, and multi-agent planning
- `HARNESS-001`: verification, evidence, and review-ready operations

The repetition is intentional. Each chapter looks at the same work through a different layer rather than introducing disconnected examples.

## Chapter Map

CH01 defines the failure model. CH02 through CH04 establish Prompt Engineering. CH05 through CH08 add Context Engineering. CH09 through CH12 close the loop with Harness Engineering. The appendices collect reusable templates and glossary support. The backmatter collects source notes, reading guidance, index seeds, and figure/table navigation for later reference.

The same questions stay useful across the whole manuscript.

- Which failure mode does this chapter primarily reduce?
- Which artifacts are added here?
- How will those artifacts be used in the next chapter?

## What You Should Be Able to Do by the End

The goal is not to finish the book thinking that AI agents seem useful. The goal is to reach a concrete operational state.

- Turn ambiguous requests into implementation-ready artifacts
- Decompose and maintain the context an AI agent needs to work safely
- Design the harness that closes work through verification, handoff, and review

From here, the book moves into CH01 and defines where capable-looking AI agents actually fail in engineering work.
