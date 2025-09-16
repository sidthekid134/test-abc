# FastAPI Project

This is a FastAPI project using SQLModel for database models.

## Project Structure

- `src/app/`: Main application code
  - `main.py`: API endpoints
  - `models.py`: Database models
- `tests/`: Test files
- `docs/`: Documentation files

## Running the Application

To run the application, use:

```
uvicorn src.app.main:app --reload
```

## Running Tests

To run tests, use:

```
pytest
```