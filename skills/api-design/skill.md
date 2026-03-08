---
name: api-design
description: REST API design patterns — endpoints, error handling, pagination, versioning
origin: ECC
---

# API Design

## When to Activate

- Designing new API endpoints
- Reviewing API contracts
- Implementing error handling for APIs
- Adding pagination or filtering

## RESTful Conventions

- `GET /resources` — List resources
- `GET /resources/:id` — Get single resource
- `POST /resources` — Create resource
- `PUT /resources/:id` — Full update
- `PATCH /resources/:id` — Partial update
- `DELETE /resources/:id` — Delete resource

## Status Codes

- `200` OK — Successful GET/PUT/PATCH
- `201` Created — Successful POST
- `204` No Content — Successful DELETE
- `400` Bad Request — Invalid input
- `401` Unauthorized — Missing/invalid auth
- `403` Forbidden — Insufficient permissions
- `404` Not Found — Resource doesn't exist
- `422` Unprocessable — Validation errors
- `429` Too Many Requests — Rate limited
- `500` Internal Server Error — Unexpected failure

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```

## Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

## Best Practices

- Validate inputs at boundaries
- Use consistent naming (snake_case or camelCase)
- Version APIs (`/api/v1/`, `/api/v2/`)
- Rate limit all endpoints
- Log requests with correlation IDs
