---
name: code-review
description: Comprehensive code review for uncommitted changes
allowed_tools: ["Bash", "Read", "Grep", "Glob"]
---

# Code Review

Review uncommitted code changes with three severity categories.

## Severity Levels

### Security (CRITICAL)
- Hardcoded credentials, API keys, tokens
- Injection vulnerabilities (SQL, command, XSS)
- Path traversal vulnerabilities
- Insecure deserialization

### Code Quality (HIGH)
- Functions exceeding 50 lines
- Files over 800 lines
- Deep nesting beyond 4 levels
- Duplicated logic

### Best Practices (MEDIUM)
- Unnecessary mutations
- Test coverage gaps
- Missing error handling at boundaries
- Accessibility issues

## Output

Generate report with:
- Severity level
- File location (path:line)
- Description of issue
- Remediation suggestion

## Enforcement

**Block commit if CRITICAL or HIGH issues found.**
