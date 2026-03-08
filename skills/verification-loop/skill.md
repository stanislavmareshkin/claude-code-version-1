---
name: verification-loop
description: Verification loop — systematic checking of changes before committing
origin: ECC
---

# Verification Loop

## When to Activate

- After completing a feature or fix
- Before committing changes
- Before creating a PR
- After refactoring

## Loop Steps

1. **Build** — Ensure the project builds without errors
2. **Type Check** — Run type checker (mypy, tsc)
3. **Lint** — Run linter (ruff, eslint)
4. **Test** — Run full test suite
5. **Coverage** — Check coverage meets threshold (80%+)
6. **Review** — Scan diff for debug statements, secrets, issues
7. **Clean** — Remove temporary files, console.logs, print statements

## Pass Criteria

- All steps must pass
- No regressions in existing tests
- No new linting errors
- No debug statements in production code
- No secrets in committed code

## On Failure

- Fix the issue
- Re-run the entire loop
- Do NOT commit with known failures
