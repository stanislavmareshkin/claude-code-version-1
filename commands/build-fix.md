---
name: build-fix
description: Incrementally fix build and type errors with minimal, safe changes
allowed_tools: ["Bash", "Read", "Edit", "Grep", "Glob"]
---

# Build Fix

Fix build errors one at a time with minimal changes.

## Process

1. **Detect Build System** — Identify tool (npm, tsc, cargo, mvn, gradle, go, python)
2. **Parse and Group Errors** — Run build, capture stderr, group by file, sort by dependency order
3. **Fix Loop (One Error at a Time)**:
   - Read file (10 lines around error)
   - Diagnose root cause
   - Fix minimally with Edit tool
   - Re-run build to verify
   - Move to next error
4. **Guardrails** — Stop and ask user if:
   - Fix introduces more errors than it resolves
   - Same error persists after 3 attempts
   - Fix requires architectural changes
   - Errors stem from missing dependencies
5. **Summary** — Show errors fixed, remaining, new errors (should be zero)

## Recovery Strategies

- **Missing module/import**: Check if package installed
- **Type mismatch**: Read both type definitions, fix narrower type
- **Circular dependency**: Identify cycle, suggest extraction
- **Version conflict**: Check version constraints
- **Build tool misconfiguration**: Read config, compare with defaults
