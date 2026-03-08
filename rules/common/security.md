# Security Rules

## Secrets Management

- NEVER hardcode secrets, API keys, tokens, or passwords
- Use environment variables or secret managers
- Add `.env` files to `.gitignore`
- Rotate compromised credentials immediately

## Input Validation

- Validate ALL external input (user input, API responses, file contents)
- Use allowlists over denylists
- Sanitize data before rendering (prevent XSS)
- Parameterize database queries (prevent SQL injection)
- Validate file paths (prevent path traversal)

## Authentication & Authorization

- Use established libraries (don't roll your own crypto)
- Implement proper session management
- Apply principle of least privilege
- Validate permissions on every request

## Dependencies

- Keep dependencies updated
- Audit for known vulnerabilities (`npm audit`, `pip audit`)
- Pin dependency versions in production
- Review new dependencies before adding

## OWASP Top 10 Awareness

- Injection (SQL, command, XSS)
- Broken authentication
- Sensitive data exposure
- XML external entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-site scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging and monitoring
