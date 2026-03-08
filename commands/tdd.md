---
name: tdd
description: Test-driven development workflow — RED, GREEN, REFACTOR cycle
allowed_tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob"]
---

# TDD Workflow

Follow the strict TDD cycle for every change:

## Cycle

1. **RED** — Write a failing test first. The test must fail because the code doesn't exist yet.
2. **GREEN** — Write the minimal code to make the test pass. Nothing more.
3. **REFACTOR** — Improve the code while keeping all tests green.
4. **REPEAT** — Move to the next requirement.

## Steps

1. **Scaffold Interfaces** — Define types/interfaces before implementation
2. **Generate Tests First** — Write failing tests that describe desired behavior
3. **Implement Minimal Code** — Just enough to pass the tests
4. **Verify Coverage** — Ensure 80%+ test coverage

## Coverage Standards

- **80% minimum** for general code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical paths
  - Core business logic

## Rules

- Never skip the RED phase
- Never write code before tests
- One test at a time
- Each test should test one thing
- Run tests after every change
