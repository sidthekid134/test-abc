# TODO Application API Documentation

This document provides detailed information about the TODO Application API endpoints, request/response formats, and authentication requirements.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost:8000
```

## Authentication

The API uses JWT token-based authentication. To access protected endpoints, you must include an `Authorization` header with a valid token:

```
Authorization: Bearer <access_token>
```

### Get Access Token

**Endpoint**: `POST /token`

**Description**: Authenticate a user and get an access token

**Request Body**:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes**:
- `200 OK`: Authentication successful
- `401 Unauthorized`: Invalid credentials

## User Management

### Register User

**Endpoint**: `POST /users/`

**Description**: Register a new user

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2023-05-01T12:00:00"
}
```

**Status Codes**:
- `201 Created`: User created successfully
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists

### Get Current User

**Endpoint**: `GET /users/me`

**Description**: Get information about the currently authenticated user

**Authentication**: Required

**Response**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2023-05-01T12:00:00"
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Authentication required

### Update Current User

**Endpoint**: `PUT /users/me`

**Description**: Update information for the currently authenticated user

**Authentication**: Required

**Request Body**:
```json
{
  "email": "newemail@example.com",
  "password": "newpassword123",
  "is_active": true
}
```
*Note: All fields are optional. Only include fields you want to update.*

**Response**:
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "is_active": true,
  "created_at": "2023-05-01T12:00:00"
}
```

**Status Codes**:
- `200 OK`: User updated successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `409 Conflict`: New email already exists

### Delete Current User

**Endpoint**: `DELETE /users/me`

**Description**: Delete the currently authenticated user

**Authentication**: Required

**Response**: No content

**Status Codes**:
- `204 No Content`: User deleted successfully
- `401 Unauthorized`: Authentication required

## Task Management

### Create Task

**Endpoint**: `POST /tasks/`

**Description**: Create a new task for the authenticated user

**Authentication**: Required

**Request Body**:
```json
{
  "title": "Complete project",
  "description": "Finish the TODO application project",
  "is_completed": false
}
```
*Note: `description` and `is_completed` are optional. `is_completed` defaults to `false` if not provided.*

**Response**:
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the TODO application project",
  "is_completed": false,
  "owner_id": 1,
  "created_at": "2023-05-01T12:30:00",
  "updated_at": null
}
```

**Status Codes**:
- `201 Created`: Task created successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required

### Get All Tasks

**Endpoint**: `GET /tasks/`

**Description**: Get all tasks for the authenticated user

**Authentication**: Required

**Query Parameters**:
- `skip` (optional, integer): Number of items to skip (default: 0)
- `limit` (optional, integer): Maximum number of items to return (default: 100)
- `is_completed` (optional, boolean): Filter by completion status

**Response**:
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the TODO application project",
    "is_completed": false,
    "owner_id": 1,
    "created_at": "2023-05-01T12:30:00",
    "updated_at": null
  },
  {
    "id": 2,
    "title": "Write documentation",
    "description": "Create API documentation",
    "is_completed": true,
    "owner_id": 1,
    "created_at": "2023-05-01T13:00:00",
    "updated_at": "2023-05-01T14:30:00"
  }
]
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Authentication required

### Get Task by ID

**Endpoint**: `GET /tasks/{task_id}`

**Description**: Get a specific task by ID

**Authentication**: Required

**Path Parameters**:
- `task_id` (integer): The ID of the task

**Response**:
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the TODO application project",
  "is_completed": false,
  "owner_id": 1,
  "created_at": "2023-05-01T12:30:00",
  "updated_at": null
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Task not found or doesn't belong to the authenticated user

### Update Task

**Endpoint**: `PUT /tasks/{task_id}`

**Description**: Update a specific task by ID

**Authentication**: Required

**Path Parameters**:
- `task_id` (integer): The ID of the task

**Request Body**:
```json
{
  "title": "Complete project revision",
  "description": "Finish revising the TODO application project",
  "is_completed": true
}
```
*Note: All fields are optional. Only include fields you want to update.*

**Response**:
```json
{
  "id": 1,
  "title": "Complete project revision",
  "description": "Finish revising the TODO application project",
  "is_completed": true,
  "owner_id": 1,
  "created_at": "2023-05-01T12:30:00",
  "updated_at": "2023-05-01T15:00:00"
}
```

**Status Codes**:
- `200 OK`: Task updated successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Task not found or doesn't belong to the authenticated user

### Delete Task

**Endpoint**: `DELETE /tasks/{task_id}`

**Description**: Delete a specific task by ID

**Authentication**: Required

**Path Parameters**:
- `task_id` (integer): The ID of the task

**Response**: No content

**Status Codes**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Task not found or doesn't belong to the authenticated user

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

To prevent abuse, the API implements rate limiting. If you exceed the rate limits, you'll receive a `429 Too Many Requests` response.

## Security Considerations

1. Always use HTTPS in production
2. Tokens expire after 30 minutes by default
3. Passwords are securely hashed using bcrypt
4. Input validation is performed on all request data
5. SQL injection protection is provided by SQLAlchemy ORM

## Sample API Flows

### Task Management Flow

1. Login:
   ```bash
   curl -X POST "http://localhost:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@example.com&password=password123"
   ```

2. Create a task:
   ```bash
   curl -X POST "http://localhost:8000/tasks/" \
     -H "Authorization: Bearer {your_token}" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete the FastAPI tutorial"}'
   ```

3. Get all tasks:
   ```bash
   curl -X GET "http://localhost:8000/tasks/" -H "Authorization: Bearer {your_token}"
   ```

4. Update a task:
   ```bash
   curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Authorization: Bearer {your_token}" \
     -H "Content-Type: application/json" \
     -d '{"is_completed": true}'
   ```

5. Delete a task:
   ```bash
   curl -X DELETE "http://localhost:8000/tasks/1" -H "Authorization: Bearer {your_token}"
   ```