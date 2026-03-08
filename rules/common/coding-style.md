# Coding Style

## General Principles

- Write clear, readable code — prefer clarity over cleverness
- Use descriptive variable and function names
- Keep functions focused — one function, one responsibility
- Functions should be under 50 lines; files under 800 lines
- Maximum nesting depth: 4 levels
- DRY — Don't Repeat Yourself, but don't over-abstract prematurely

## Naming Conventions

- **Files**: lowercase with hyphens (`my-component.ts`, `user-service.py`)
- **Classes**: PascalCase (`UserService`, `PaymentProcessor`)
- **Functions/Methods**: camelCase (JS/TS) or snake_case (Python)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `API_BASE_URL`)
- **Booleans**: prefix with is/has/should (`isActive`, `hasPermission`)

## Code Organization

- Group imports: stdlib, third-party, local
- Place constants at the top of the file
- Export public API explicitly
- Keep related code close together

## Comments

- Write self-documenting code — minimize comments
- Comment the "why", not the "what"
- Use JSDoc/docstrings for public APIs only
- Remove commented-out code — use version control
