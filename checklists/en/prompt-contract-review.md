# Prompt Contract Review Checklist

- Is the Objective defined in one sentence?
- Do the Inputs name the artifact or source type explicitly?
- Are the Constraints written as observable conditions rather than vague guidance?
- Is there a Tool Contract that makes the allowed tools, commands, and external access explicit?
- Is there an Approval Gate that makes human-approval-required actions explicit?
- Do the Forbidden Actions prevent silent expansion or risky shortcuts?
- Are the Completion Criteria verifiable rather than subjective?
- Are there Refusal / Stop Conditions that define when the run must stop?
- Are the Output Schema and output version explicit so the reporting fields and compatibility stay fixed?
- Does the Output Format keep canonical report labels such as `Changed Files`, `Verification`, and `Remaining Gaps`, and align feature-specific sections such as `Implemented Scope` or bugfix-specific sections such as `Root Cause` with the Output Schema?
- Does the contract explain what to do when information is missing?
- Is the out-of-scope boundary visible?
- Are the required artifacts actually referenced?
