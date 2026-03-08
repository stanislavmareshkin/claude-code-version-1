# Python Testing

## Framework

- Use `pytest` as the primary testing framework
- Use `pytest-cov` for coverage reporting
- Use `pytest-asyncio` for async tests

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=mypackage --cov-report=term-missing

# Specific file
pytest tests/test_user.py

# Specific test
pytest tests/test_user.py::test_create_user

# Verbose
pytest -v
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
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

## Mocking

- Use `pytest-mock` (mocker fixture)
- Mock at the boundary, not internal details
- Prefer dependency injection over patching

## Coverage

- Target: 80%+ overall
- 100% for critical paths (auth, payments, security)
