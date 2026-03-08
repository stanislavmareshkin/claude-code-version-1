---
name: tdd-workflow
description: Test-driven development workflow — RED, GREEN, REFACTOR cycle with pytest
origin: ECC
---

# TDD Workflow

Comprehensive TDD workflow for building reliable software.

## When to Activate

- Starting any new feature or module
- Fixing bugs (write failing test first, then fix)
- Refactoring existing code (ensure tests exist first)
- Code review reveals missing test coverage

## The Cycle

### 1. RED — Write a Failing Test

```python
def test_calculate_total_with_discount():
    order = Order(items=[Item(price=100), Item(price=50)])
    total = order.calculate_total(discount_percent=10)
    assert total == 135.0  # (100 + 50) * 0.9
```

Run the test — it should FAIL because `calculate_total` doesn't exist yet.

### 2. GREEN — Minimal Implementation

```python
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self, discount_percent=0):
        subtotal = sum(item.price for item in self.items)
        return subtotal * (1 - discount_percent / 100)
```

Run the test — it should PASS.

### 3. REFACTOR — Improve While Green

- Extract methods if needed
- Improve naming
- Remove duplication
- Run ALL tests after each change

## Coverage Requirements

- **80%** minimum overall
- **100%** for critical paths (auth, payments, security)

## Best Practices

- One assertion per test (when possible)
- Test behavior, not implementation
- Use descriptive test names
- Keep tests fast and independent
- Mock external dependencies at boundaries
