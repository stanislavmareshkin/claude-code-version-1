---
name: python-testing
description: Python testing strategies using pytest, TDD, fixtures, mocking, parametrization
origin: ECC
---

# Python Testing Patterns

## When to Activate

- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites
- Reviewing test coverage
- Setting up testing infrastructure

## TDD Cycle

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve while green

## Coverage

- Target: 80%+ overall
- Critical paths: 100%

```bash
pytest --cov=mypackage --cov-report=term-missing --cov-report=html
```

## Fixtures

```python
import pytest

@pytest.fixture
def sample_user():
    return User(name="Test", email="test@example.com")

@pytest.fixture
def mock_api(mocker):
    return mocker.patch("myapp.client.api_call")
```

## Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (0, 0),
])
def test_double(input, expected):
    assert double(input) == expected
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("https://api.example.com")
    assert result["status"] == "ok"
```

## Mocking Best Practices

- Mock at boundaries (HTTP calls, database, filesystem)
- Use `pytest-mock` (mocker fixture)
- Prefer dependency injection over monkey-patching
- Verify mock interactions when behavior matters
