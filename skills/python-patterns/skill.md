---
name: python-patterns
description: Python development patterns — project structure, async, error handling, config
origin: ECC
---

# Python Patterns

Best practices and patterns for Python development.

## When to Activate

- Starting a new Python project
- Structuring Python code
- Implementing async operations
- Setting up configuration management

## Project Structure

```
project/
├── src/package/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── config.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   └── test_services.py
├── pyproject.toml
├── requirements.txt
└── .env.example
```

## Configuration with Pydantic

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Async Patterns

```python
import asyncio
import httpx

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Domain Exceptions

```python
class AppError(Exception):
    """Base application error."""

class NotFoundError(AppError):
    pass

class ValidationError(AppError):
    pass
```

## Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Processing order", extra={"order_id": order.id})
```
