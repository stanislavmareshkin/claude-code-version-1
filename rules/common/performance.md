# Performance Guidelines

## General

- Measure before optimizing — use profilers
- Optimize hot paths, not everything
- Set performance budgets for critical operations
- Cache expensive computations

## Database

- Use indexes for frequently queried columns
- Avoid N+1 query problems
- Use connection pooling
- Paginate large result sets
- Use bulk operations for batch processing

## API

- Implement pagination for list endpoints
- Use compression (gzip/brotli)
- Cache responses where appropriate (ETags, Cache-Control)
- Set reasonable timeouts
- Use async/await for I/O-bound operations

## Memory

- Avoid memory leaks — clean up resources
- Use streaming for large data processing
- Release references when no longer needed
- Monitor memory usage in production

## Frontend

- Lazy load non-critical resources
- Minimize bundle size
- Use virtual scrolling for long lists
- Debounce/throttle expensive event handlers
