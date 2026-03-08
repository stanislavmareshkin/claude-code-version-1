---
name: security-review
description: Security review skill — OWASP checklist, secrets, input validation, auth
origin: ECC
---

# Security Review

Comprehensive security review checklist for code changes.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Checklist

### 1. Secrets Management
- **Never** hardcode API keys, tokens, or passwords
- Store secrets in environment variables
- Add `.env` to `.gitignore`
- No secrets in git history
- Production secrets in hosting platform's secret manager

### 2. Input Validation
- Validate all user inputs before processing
- Use validation schemas (Pydantic, Zod)
- File upload restrictions: size limits, MIME type checks, extension allowlists
- Error messages don't leak internal information

### 3. SQL/Command Injection Prevention
- Use parameterized queries — never concatenate user input into queries
- Use ORMs correctly
- Use `subprocess` with lists, not shell strings

### 4. Authentication & Authorization
- Store tokens in httpOnly cookies (not localStorage)
- Verify user permissions before sensitive operations
- Implement role-based access control
- Enable Row Level Security (RLS) in databases

### 5. XSS Prevention
- Sanitize user-provided HTML (DOMPurify)
- Configure Content-Security-Policy headers
- Leverage framework protections (React auto-escaping)

### 6. Rate Limiting
- Rate limit API endpoints
- Throttle expensive operations

### 7. Data Exposure
- Never log passwords, tokens, or PII
- Return generic error messages
- Never expose internal details in responses

### 8. Dependency Security
- Regularly update dependencies
- Commit lock files
- Run `npm audit` / `pip audit` regularly
