---
name: learn
description: Analyze current session and extract reusable patterns as skills
allowed_tools: ["Read", "Write", "Grep", "Glob"]
---

# Learn

Analyze the current session and extract patterns worth saving as skills.

Run `/learn` when you've solved a non-trivial problem.

## What to Extract

- **Error resolution patterns** — error, root cause, fix, reusability
- **Debugging techniques** — non-obvious steps, tool combinations
- **Workarounds** — library quirks, API limitations, version-specific fixes
- **Project-specific patterns** — codebase conventions, architecture decisions

## Process

1. Review session for extractable patterns
2. Identify most valuable/reusable insight
3. Draft skill file
4. Ask user to confirm before saving
5. Save to `~/.claude/skills/learned/`

## Notes

- Don't extract trivial fixes or one-time issues
- Focus on patterns that save time in future sessions
- One pattern per skill file
