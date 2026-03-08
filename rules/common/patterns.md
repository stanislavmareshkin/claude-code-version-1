# Design Patterns

## Preferred Patterns

- **Early returns** — Reduce nesting, handle edge cases first
- **Composition over inheritance** — Prefer composing behaviors
- **Dependency injection** — Pass dependencies, don't hardcode them
- **Single responsibility** — Each module/class/function does one thing
- **Fail fast** — Validate inputs early, throw errors immediately

## Error Handling

- Use typed/custom errors for different failure modes
- Handle errors at the appropriate level
- Don't swallow errors silently
- Log errors with context (what was being done, what failed)
- Provide actionable error messages

## API Design

- Use consistent naming conventions
- Return appropriate HTTP status codes
- Validate inputs at system boundaries
- Version APIs when breaking changes are needed
- Document public APIs

## Anti-patterns to Avoid

- God objects / God functions
- Premature optimization
- Premature abstraction
- Magic numbers / magic strings
- Deep inheritance hierarchies
- Circular dependencies
