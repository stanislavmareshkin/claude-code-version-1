# Python Coding Style

## Formatting

- Follow PEP 8
- Use `black` for auto-formatting (line length: 88)
- Use `isort` for import sorting
- Use `ruff` or `flake8` for linting

## Type Hints

- Use type hints for all function signatures
- Use `from __future__ import annotations` for forward references
- Prefer `str | None` over `Optional[str]` (Python 3.10+)

## Imports

```python
# 1. Standard library
import os
from pathlib import Path

# 2. Third-party
import requests
from pydantic import BaseModel

# 3. Local
from .models import User
from .utils import validate
```

## Functions

- Use snake_case for functions and variables
- Use PascalCase for classes
- Use UPPER_SNAKE_CASE for constants
- Default to immutable data structures
- Use dataclasses or Pydantic models for structured data

## Docstrings

- Use Google-style docstrings for public APIs
- Include Args, Returns, Raises sections
- Skip docstrings for obvious/private methods

## Error Handling

```python
# Good — specific exceptions
try:
    result = api_call()
except requests.Timeout:
    logger.warning("API timeout")
    return fallback_value
except requests.HTTPError as e:
    logger.error(f"API error: {e.response.status_code}")
    raise

# Bad — bare except
try:
    result = api_call()
except:
    pass
```
