---
name: verification-loop
description: A comprehensive verification system for Claude Code sessions.
origin: ECC
---

# Verification Loop Skill

A comprehensive verification system for Claude Code sessions.

## When to Use

- After completing a feature or significant code change
- Before creating a PR
- When you want to ensure quality gates pass
- After refactoring

## Verification Phases

### Phase 1: Build Verification
```bash
npm run build 2>&1 | tail -20
# OR for Python:
python -m py_compile main.py
```
If build fails, STOP and fix before continuing.

### Phase 2: Type Check
```bash
# TypeScript
npx tsc --noEmit 2>&1 | head -30

# Python
mypy . 2>&1 | head -30
```

### Phase 3: Lint Check
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### Phase 4: Test Suite
```bash
# Run tests with coverage
pytest --cov=mypackage --cov-report=term-missing

# Target: 80% minimum coverage
```

### Phase 5: Security Scan
```bash
# Check for secrets
grep -rn "sk-\|api_key\|password" --include="*.py" . 2>/dev/null | head -10

# Check for debug statements
grep -rn "print(\|console.log" --include="*.py" --include="*.ts" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review
```bash
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for unintended changes, missing error handling, edge cases.

## Output Format

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

Run verification every 15 minutes or after major changes:
- After completing each function
- After finishing a component
- Before moving to next task
