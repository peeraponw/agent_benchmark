# RESTful API Design Best Practices

## Introduction
REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs are widely used for web services due to their simplicity and scalability.

## Core Principles

### 1. Stateless
Each request must contain all information needed to process it. The server should not store client context between requests.

### 2. Client-Server Architecture
Clear separation between client and server responsibilities.

### 3. Cacheable
Responses should be cacheable when appropriate to improve performance.

### 4. Uniform Interface
Consistent interface design across the API.

## HTTP Methods

- **GET**: Retrieve data (idempotent, safe)
- **POST**: Create new resources
- **PUT**: Update/replace entire resource (idempotent)
- **PATCH**: Partial update of resource
- **DELETE**: Remove resource (idempotent)

## URL Design

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural nouns: `/users` not `/user`
- Hierarchical structure: `/users/123/orders`

### Examples
```
GET /api/v1/users          # Get all users
GET /api/v1/users/123      # Get specific user
POST /api/v1/users         # Create new user
PUT /api/v1/users/123      # Update user
DELETE /api/v1/users/123   # Delete user
```

## Status Codes

### Success (2xx)
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE

### Client Error (4xx)
- 400 Bad Request: Invalid request
- 401 Unauthorized: Authentication required
- 403 Forbidden: Access denied
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation errors

### Server Error (5xx)
- 500 Internal Server Error: Generic server error
- 503 Service Unavailable: Server overloaded

## Response Format

### JSON Structure
```json
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

## Pagination

### Offset-based
```
GET /api/v1/users?offset=20&limit=10
```

### Cursor-based
```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=10
```

## Filtering and Sorting

```
GET /api/v1/users?status=active&sort=created_at&order=desc
```

## Versioning

### URL Versioning
```
GET /api/v1/users
GET /api/v2/users
```

### Header Versioning
```
GET /api/users
Accept: application/vnd.api+json;version=1
```

## Security

### Authentication
- API Keys
- JWT Tokens
- OAuth 2.0

### Authorization
- Role-based access control
- Resource-level permissions

### HTTPS
Always use HTTPS in production.

## Documentation

### OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Successful response
```

## Rate Limiting

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Best Practices

1. Use consistent naming conventions
2. Implement proper error handling
3. Provide comprehensive documentation
4. Use appropriate HTTP status codes
5. Implement caching strategies
6. Monitor API performance
7. Version your APIs
8. Validate input data
9. Use HTTPS
10. Implement rate limiting
