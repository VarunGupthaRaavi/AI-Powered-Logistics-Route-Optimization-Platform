# 🔌 RESTful API Guidelines & Standards

## Base URL
All API endpoints are versioned under `/api/v1`.

## Standard Response Format
Successful responses return standard JSON payloads.

Error responses adhere to the following schema:
```json
{
  "detail": "Detailed human-readable error description",
  "status_code": 404
}
```

## Standard Status Codes
- `200 OK`: Request succeeded.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Validation failure or invalid parameters.
- `401 Unauthorized`: Missing or invalid Bearer token.
- `403 Forbidden`: Insufficient user permissions.
- `404 Not Found`: Target entity does not exist.
- `500 Internal Error`: Unexpected server failure.
