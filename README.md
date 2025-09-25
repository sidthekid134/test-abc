# Task Management API

A simple task management API built with FastAPI and SQLModel.

## Features

- Create, read, update, and delete tasks
- Advanced filtering and sorting
- Data validation and error handling
- Comprehensive unit tests

## Technology Stack

- FastAPI: Modern API framework with automatic OpenAPI documentation
- SQLModel: SQL database interaction with type annotations
- Pydantic: Data validation and settings management
- SQLite: Lightweight database (configurable to use other databases)

## Project Structure

- `app/`: Main application directory
  - `models.py`: SQLModel database models
  - `database.py`: Database configuration
  - `main.py`: FastAPI application setup
  - `routers/`: API endpoint routes
- `tests/`: Unit tests

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd task-management-api
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000. 

API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
pytest
```

## API Endpoints

### Tasks

- `GET /tasks`: List all tasks (with filtering and sorting)
- `GET /tasks/{task_id}`: Get a specific task
- `POST /tasks/`: Create a new task
- `PATCH /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task

### Users

- `GET /users`: List all users
- `GET /users/{user_id}`: Get a specific user
- `POST /users/`: Create a new user
- `DELETE /users/{user_id}`: Delete a user