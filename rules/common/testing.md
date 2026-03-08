# Testing Rules

## Philosophy

- Tests are first-class code — maintain them with the same rigor
- Follow TDD when possible: RED → GREEN → REFACTOR
- Test behavior, not implementation details
- Each test should test exactly one thing

## Coverage

- **80% minimum** overall coverage
- **100%** for security-critical, financial, and auth logic
- Measure with coverage tools (`pytest --cov`, `jest --coverage`)

## Test Structure (AAA Pattern)

1. **Arrange** — Set up test data and preconditions
2. **Act** — Execute the code under test
3. **Assert** — Verify the expected outcome

## Naming

- Test names should describe the behavior: `test_user_can_login_with_valid_credentials`
- Group related tests in describe/class blocks

## Types of Tests

- **Unit tests** — Fast, isolated, no external dependencies
- **Integration tests** — Test component interactions
- **E2E tests** — Full user workflows (use sparingly)

## Anti-patterns to Avoid

- Tests that depend on execution order
- Tests that depend on external services without mocking
- Flaky tests — fix or quarantine immediately
- Testing private/internal methods directly
- Asserting on implementation details
