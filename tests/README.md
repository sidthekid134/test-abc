# Tests

This directory contains the test suite for the FastAPI application.

## Structure

- `test_main.py`: Tests for the main API endpoints
- `test_models.py`: Tests for the database models
- `conftest.py`: Pytest fixtures and configuration

## Running Tests

To run the tests, use the following command from the project root:

```bash
pytest tests/
```

## Test Coverage

To generate a test coverage report, run:

```bash
pytest --cov=app tests/
```