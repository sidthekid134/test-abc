# Task Management API

A RESTful API for task management built with FastAPI and SQLModel.

## Features

- Create, read, update, and delete tasks
- Filter tasks by completion status
- Pagination support
- Input validation with Pydantic
- SQLModel for database operations
- Comprehensive error handling and logging

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check endpoint |
| POST | /tasks/ | Create a new task |
| GET | /tasks/ | Get all tasks (with optional filtering) |
| GET | /tasks/{task_id} | Get a specific task by ID |
| PUT | /tasks/{task_id} | Update an existing task |
| DELETE | /tasks/{task_id} | Delete a task |

## Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)

## Development

The application will run in development mode with auto-reload enabled.
Access the Swagger UI documentation at http://localhost:8000/docs