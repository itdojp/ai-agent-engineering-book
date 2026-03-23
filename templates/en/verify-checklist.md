# Verify Checklist Template

## Before Edit
- Confirm the behavior and source of truth that must be preserved.
- Decide whether a failing test should be added or updated first.
- Fix the local verify command before starting the change.

## During Change
- Keep the diff inside one work package.
- Check for missing updates in docs, task artifacts, or the Progress Note.
- Classify verify failures instead of treating every red result the same way.

## Before Review
- Run local verify.
- Confirm that the same bar is reflected in CI.
- Decide whether an evidence bundle is required.
- Make any required human approval explicit.
