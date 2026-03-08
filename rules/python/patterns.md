# Python Patterns

## Project Structure

```
myproject/
├── src/mypackage/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── utils.py
│   └── config.py
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   └── test_services.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Configuration

- Use environment variables for secrets
- Use Pydantic Settings for config validation
- Use `.env` files for local development (never commit)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"
```

## Async Patterns

```python
import asyncio
import httpx

async def fetch_data(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Error Handling

- Create domain-specific exceptions
- Use context managers for resource management
- Log errors with structured context

```python
class AppError(Exception):
    """Base application error."""

class NotFoundError(AppError):
    """Resource not found."""

class ValidationError(AppError):
    """Input validation failed."""
```

## Logging

```python
import logging

logger = logging.getLogger(__name__)

# Structured logging
logger.info("User created", extra={"user_id": user.id, "email": user.email})
```
