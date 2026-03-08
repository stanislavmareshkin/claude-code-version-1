---
name: verify
description: Comprehensive verification workflow — build, types, lint, tests, git status
allowed_tools: ["Bash", "Read", "Grep", "Glob"]
---

# Verify

Run comprehensive verification before PR or deployment.

## Checks (Sequential)

1. **Build validation** — stops process if it fails
2. **Type checking** — TypeScript/mypy error reporting
3. **Linter analysis** — warnings and errors
4. **Test suite** — full execution with coverage metrics
5. **Console.log audit** — identify debug statements
6. **Git status** — review uncommitted changes

## Modes

- `quick` — build + types only
- `full` — all checks (default)
- `pre-commit` — build + types + lint + console audit
- `pre-pr` — all checks + security scanning

## Output

Concise report with pass/fail status per check and a **"Ready for PR"** determination.

Early stopping on critical failures.
