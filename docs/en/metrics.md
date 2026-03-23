# Metrics

## Throughput

- `closed issues / week`
  - shows whether work packages are closing at the intended size
- `PR cycle time`
  - shows whether the review budget is backing up
- `draft-to-merge time`
  - measures how long verify and review are delaying closure

## Quality

- `verify failure rate`
  - shows the quality of briefing, prompting, and task decomposition
- `post-merge regression count`
  - shows how well review and the verification harness are working
- `artifact drift incidents`
  - shows missed synchronization among docs, tests, and task artifacts

## Hygiene

- `stale docs count`
  - shows whether entropy cleanup is keeping up
- `orphaned task brief count`
  - shows whether non-canonical task artifacts are piling up
- `missing verification evidence count`
  - detects weak review evidence for user-visible changes

## Review Questions

- Is throughput increasing without exceeding the review budget?
- Is the main cause of verify failure prompt, context, or harness design?
- Is worsening repo hygiene slowing the next round of work?
