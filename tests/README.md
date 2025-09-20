# Tests Directory

This directory contains tests for the FastAPI application.

## Structure

- `conftest.py`: Pytest fixtures and configurations
- `test_*.py`: Test files corresponding to application components

## Running Tests

To run the tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/
```

Tests are organized to match the application structure for easier maintenance.