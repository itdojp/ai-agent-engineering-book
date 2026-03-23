# Verification Checklist

## Before Edit

- Have you confirmed which behavior must be preserved in the spec, acceptance criteria, or task brief?
- Have you decided whether a failing test should be added or updated first?
- Have you identified the local verify command before starting the change?

## During Change

- Have you kept the diff inside the smallest practical work package?
- Have you updated docs, brief, and Progress Note where needed?
- Have you classified verify failures by failure mode?

## Before Review

- Have you run local verify?
- Can the same quality bar be enforced in CI?
- If the change is UI-facing or user-visible, have you preserved an evidence bundle?
- If evidence is not required, can you explain why?
- Have you called out the points that still require human approval?
