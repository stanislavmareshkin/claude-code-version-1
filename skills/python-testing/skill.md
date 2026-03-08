---
name: python-testing
description: Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements.
origin: ECC
---

# Python Testing Patterns

Comprehensive testing strategies for Python applications using pytest, TDD, and best practices.

## When to Activate

- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites for Python projects
- Reviewing Python test coverage
- Setting up testing infrastructure

## TDD Cycle

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve while green

## Coverage Requirements

- Target: 80%+ code coverage
- Critical paths: 100% coverage required

```bash
pytest --cov=mypackage --cov-report=term-missing --cov-report=html
```

## Fixtures

```python
@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

@pytest.fixture
def database():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

# Scopes: function (default), module, session
@pytest.fixture(scope="session")
def shared_resource():
    resource = ExpensiveResource()
    yield resource
    resource.cleanup()
```

### Conftest.py for Shared Fixtures

```python
# tests/conftest.py
@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client
```

## Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("valid@email.com", True),
    ("invalid", False),
    ("@no-domain.com", False),
], ids=["valid-email", "missing-at", "missing-domain"])
def test_email_validation(input, expected):
    assert is_valid_email(input) is expected
```

## Markers and Test Selection

```python
@pytest.mark.slow
def test_slow_operation():
    time.sleep(5)

@pytest.mark.integration
def test_api_integration():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200
```

```bash
pytest -m "not slow"
pytest -m integration
```

## Mocking

```python
from unittest.mock import patch

@patch("mypackage.external_api_call")
def test_with_mock(api_call_mock):
    api_call_mock.return_value = {"status": "success"}
    result = my_function()
    api_call_mock.assert_called_once()

@patch("mypackage.api_call")
def test_api_error(api_call_mock):
    api_call_mock.side_effect = ConnectionError("Network error")
    with pytest.raises(ConnectionError):
        api_call()
```

## Async Testing

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_add(2, 3)
    assert result == 5
```

## Assertions Reference

```python
assert result == expected           # Equality
assert item in collection           # Membership
assert isinstance(result, str)      # Type check
assert result is None               # Identity

with pytest.raises(ValueError, match="invalid input"):
    raise ValueError("invalid input provided")
```

## Test Organization

```
tests/
├── conftest.py
├── unit/
│   ├── test_models.py
│   └── test_utils.py
├── integration/
│   └── test_api.py
└── e2e/
    └── test_user_flow.py
```

## Running Tests

```bash
pytest                                    # All tests
pytest tests/test_utils.py               # Specific file
pytest -v                                # Verbose
pytest --cov=mypackage                   # With coverage
pytest -m "not slow"                     # Skip slow
pytest -x                               # Stop on first failure
pytest --lf                              # Run last failed
pytest -k "test_user"                    # Pattern matching
```

## Best Practices

### DO
- Follow TDD: write tests before code
- Test one thing per test
- Use descriptive names: `test_user_login_with_invalid_credentials_fails`
- Use fixtures to eliminate duplication
- Mock external dependencies
- Test edge cases: empty, None, boundary
- Aim for 80%+ coverage

### DON'T
- Test implementation details — test behavior
- Share state between tests
- Ignore test failures
- Test third-party code
- Use print statements — use assertions
- Write brittle tests with over-specific mocks
