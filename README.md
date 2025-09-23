# TODO Application

A full-featured TODO list application built with FastAPI and SQLModel that allows users to manage their tasks.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Complete CRUD operations for tasks
- **User-Based Access Control**: Users can only manage their own tasks
- **API Documentation**: Auto-generated with Swagger UI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database for data storage
- **JWT Authentication**: Secure token-based authentication
- **Alembic**: Database migration tool

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your database:
   - Create a PostgreSQL database named `todo_app`
   - Update the database connection string in `app/database.py` if needed

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the application:
   ```bash
   python main.py
   ```

6. Access the API documentation:
   - Open your browser and navigate to `http://localhost:8000/docs`

## API Endpoints

### Authentication

- **POST /token** - Get access token (login)
- **POST /users/** - Register a new user

### Users

- **GET /users/me** - Get current user information
- **PUT /users/me** - Update current user
- **DELETE /users/me** - Delete current user

### Tasks

- **GET /tasks** - List all tasks for the current user
  - Query parameters:
    - `skip`: Number of items to skip (pagination)
    - `limit`: Maximum number of items to return
    - `is_completed`: Filter by completion status (true/false)
- **POST /tasks** - Create a new task
- **GET /tasks/{task_id}** - Get a specific task
- **PUT /tasks/{task_id}** - Update a task
- **DELETE /tasks/{task_id}** - Delete a task

## Data Models

### User

```python
{
  "id": int,
  "email": string,
  "is_active": boolean,
  "created_at": datetime
}
```

### Task

```python
{
  "id": int,
  "title": string,
  "description": string (optional),
  "is_completed": boolean,
  "owner_id": int,
  "created_at": datetime,
  "updated_at": datetime
}
```

## Authentication Flow

1. Register a user: `POST /users/`
2. Obtain access token: `POST /token`
3. Include token in requests using the `Authorization: Bearer {token}` header

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Authentication required or invalid credentials
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.