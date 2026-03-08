---
name: continuous-learning-v2
description: Continuous learning system — extract and persist patterns from coding sessions
origin: ECC
---

# Continuous Learning v2

Automatically extract and persist coding patterns from sessions.

## When to Activate

- After solving a non-trivial problem
- When discovering a useful pattern
- After debugging a complex issue
- When finding a workaround for a library/API quirk

## How It Works

1. **Observe** — Monitor tool usage and outcomes during sessions
2. **Extract** — Identify reusable patterns from successful solutions
3. **Persist** — Save patterns as skill files for future reference
4. **Apply** — Use saved patterns in similar future situations

## Pattern Categories

- **Error Resolution** — Error → Root Cause → Fix
- **Debugging Techniques** — Non-obvious diagnostic steps
- **Workarounds** — Library quirks, API limitations
- **Architecture Decisions** — Why a particular approach was chosen
- **Performance Optimizations** — Measured improvements

## Storage

Patterns are saved to `~/.claude/skills/learned/` as markdown files with:
- Pattern name
- Context (when it applies)
- Problem description
- Solution steps
- Example code
