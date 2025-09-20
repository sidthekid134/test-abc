# Tests

This directory contains test files for the application.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for testing components together
- `e2e/` - End-to-end tests for testing complete workflows

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_example.py

# Run with coverage report
pytest --cov=app
```

## Guidelines

- Write tests for all new features and bug fixes
- Aim for high code coverage
- Use fixtures to avoid duplication
- Keep tests isolated and idempotent