# Common Patterns

## Skeleton Projects

When implementing new functionality:
1. Search for battle-tested skeleton projects
2. Evaluate options for security, extensibility, relevance
3. Clone best match as foundation
4. Iterate within proven structure

## Design Patterns

### Repository Pattern

Encapsulate data access behind a consistent interface:
- Define standard operations: findAll, findById, create, update, delete
- Concrete implementations handle storage details
- Business logic depends on abstract interface, not storage mechanism
- Enables easy swapping of data sources and simplifies testing

### API Response Format

Use a consistent envelope for all API responses:
- Include a success/status indicator
- Include the data payload (nullable on error)
- Include an error message field (nullable on success)
- Include metadata for paginated responses (total, page, limit)

### Early Returns

Reduce nesting by handling edge cases first:

```python
# BAD: Deep nesting
def process(data):
    if data:
        if data.valid:
            if data.ready:
                return do_work(data)
    return None

# GOOD: Early returns
def process(data):
    if not data:
        return None
    if not data.valid:
        return None
    if not data.ready:
        return None
    return do_work(data)
```

### Dependency Injection

Pass dependencies, don't hardcode them:

```python
# BAD
class UserService:
    def __init__(self):
        self.db = Database()  # hardcoded

# GOOD
class UserService:
    def __init__(self, db: Database):
        self.db = db  # injected
```
