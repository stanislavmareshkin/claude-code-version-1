---
name: coding-standards
description: Universal coding standards — naming, structure, documentation, code quality
origin: ECC
---

# Coding Standards

## When to Activate

- Writing any new code
- Reviewing code changes
- Setting up new projects

## Naming

- **Files**: lowercase with hyphens (`user-service.py`)
- **Classes**: PascalCase (`UserService`)
- **Functions**: snake_case (Python) / camelCase (JS/TS)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Booleans**: is/has/should prefix (`is_active`, `has_permission`)

## Function Guidelines

- Max 50 lines per function
- Max 800 lines per file
- Max 4 levels of nesting
- Single responsibility
- Use early returns to reduce nesting

## Code Organization

1. Imports (stdlib → third-party → local)
2. Constants
3. Types/Interfaces
4. Main logic
5. Helpers (private)

## Comments

- Code should be self-documenting
- Comment "why", not "what"
- Docstrings for public APIs only
- No commented-out code

## Error Handling

- Fail fast — validate inputs early
- Use typed exceptions
- Handle errors at the appropriate level
- Never swallow errors silently
- Log with context
