---
name: python-patterns
description: Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.
origin: ECC
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

## Core Principles

### 1. Readability Counts

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]

# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. Explicit is Better Than Implicit

### 3. EAFP - Easier to Ask Forgiveness Than Permission

```python
# Good: EAFP style
try:
    return dictionary[key]
except KeyError:
    return default_value
```

## Type Hints

### Modern Type Hints (Python 3.10+)

```python
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Union types
JSON = dict[str, Any] | list[Any] | str | int | float | bool | None
```

### Protocol-Based Duck Typing

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: list[Renderable]) -> str:
    return "\n".join(item.render() for item in items)
```

## Error Handling Patterns

### Specific Exception Handling

```python
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e
```

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for all application errors."""

class ValidationError(AppError):
    """Raised when input validation fails."""

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
```

## Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name} took {elapsed:.4f} seconds")

with timer("data processing"):
    process_large_dataset()
```

## Data Classes

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
```

## Decorators

```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

## Concurrency Patterns

### Async/Await for Concurrent I/O

```python
import asyncio
import httpx

async def fetch_all(urls: list[str]) -> dict[str, str]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(zip(urls, responses))
```

### Threading for I/O-Bound Tasks

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_all_urls(urls: list[str]) -> dict[str, str]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        results = {}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            results[url] = future.result()
    return results
```

## Package Organization

```
myproject/
├── src/mypackage/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── models/
│   └── utils/
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── pyproject.toml
└── .gitignore
```

## Memory and Performance

```python
# Use __slots__ for memory efficiency
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Use generators for lazy evaluation
total = sum(x * x for x in range(1_000_000))

# Use join for string concatenation
result = "".join(str(item) for item in items)
```

## Python Tooling

```bash
black .                                    # Formatting
isort .                                    # Import sorting
ruff check .                               # Linting
mypy .                                     # Type checking
pytest --cov=mypackage --cov-report=html   # Testing
bandit -r .                                # Security scanning
pip-audit                                  # Dependency audit
```

## Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):    # WRONG
def append_to(item, items=None):  # CORRECT
    if items is None:
        items = []

# Bad: Bare except
try: risky()
except: pass                      # WRONG

# Good: Specific exception
try: risky()
except SpecificError as e:        # CORRECT
    logger.error(f"Failed: {e}")

# Bad: type() for type checking
if type(obj) == list:             # WRONG
if isinstance(obj, list):         # CORRECT

# Bad: == None
if value == None:                 # WRONG
if value is None:                 # CORRECT
```
