
# Contributing to DBase

Thank you for considering contributing to DBase! This document provides guidelines and instructions for contributors.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How Can I Contribute?

### Reporting Bugs
1. Check if the bug hasn't already been reported in the Issues section
2. Use the bug report template when creating a new issue
3. Include detailed steps to reproduce the issue
4. Provide your Python version and operating system information

### Suggesting Features
1. Check if the feature hasn't already been suggested
2. Use the feature request template
3. Explain why this feature would be useful
4. Provide examples of how it would work

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature/fix
3. Write clear, concise commit messages
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Steps

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/dbase.git
cd dbase
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Coding Standards

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 88)
- Use isort for import sorting
- Use type hints for all function parameters and return values

### Documentation
- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Update README.md and CHANGELOG.md when needed
- Add examples for new features

### Testing
- Write tests for all new functionality
- Maintain 100% test coverage for new code
- Use pytest for testing
- Include both unit tests and integration tests

### Commit Messages
Follow the Conventional Commits specification:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test changes
- `chore:` for maintenance tasks

Example:
```
feat: add temporary database support

- Add is_temp parameter to DataBase constructor
- Implement in-memory storage for temporary databases
- Add tests for temporary database functionality
```

## Project Structure

```
dbase/
├── dbase/           # Main package
│   ├── __init__.py  # Main module
│   ├── logger.py    # Logging system
│   ├── messages.py  # Localization
│   ├── errors.py    # Error classes
│   └── security.py  # Security utilities
├── tests/           # Test suite
├── docs/            # Documentation
└── examples/        # Example code
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_database.py

# Run with coverage
pytest --cov=dbase

# Run with verbose output
pytest -v
```

## Code Quality Tools

```bash
# Format code
black dbase/ tests/

# Sort imports
isort dbase/ tests/

# Check code style
flake8 dbase/ tests/

# Type checking
mypy dbase/
```

## Building Documentation

```bash
# Build and view documentation
python setup.py build_sphinx
```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run all tests
4. Build and test package
5. Create a release tag
6. Push to PyPI

## Questions?

If you have questions about contributing, please:
1. Check the existing documentation
2. Search existing issues
3. Create a new issue for discussion

Thank you for helping improve DBase!
