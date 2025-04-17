# Development Guide

This document provides guidelines and instructions for developers working on the outlook-mcp project.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Development Workflow](#development-workflow)
- [Code Style and Standards](#code-style-and-standards)
- [Testing](#testing)
- [Project Quality Gates](#project-quality-gates)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Development Environment Setup

### Prerequisites

- Node.js (for main server)
- Python 3.10 or higher (for future Python modules and tooling)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/outlook-mcp.git
   cd outlook-mcp
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. (Optional) Set up Python virtual environment for Python tooling:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the code style guidelines.

3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   npm test
   # or for Python modules
   pytest
   ```

4. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

5. Push your branch and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style and Standards

- **PEP 8** for Python code style
- **Google-style docstrings** for Python documentation
- **Type hints** for all Python function signatures
- **Ruff** for Python linting and formatting
- **Black** for Python code formatting
- **isort** for Python import sorting
- **mypy** for Python static type checking
- **ESLint/Prettier** for JavaScript/Node code (add config if not present)

All code must pass the pre-commit hooks before being committed.

## Testing

- Write unit tests for all new functionality
- Maintain test coverage above 85%
- Run tests with `npm test` (JS) or `pytest` (Python)
- Use fixtures/mocks for test setup
- Mock external dependencies

## Project Quality Gates

The following quality gates must be passed for all code changes:

1. **Linting**: All code must pass Ruff, Black, isort, mypy (Python) and ESLint/Prettier (JS) checks
2. **Tests**: All tests must pass with no failures
3. **Coverage**: Test coverage must be maintained at 85% or higher
4. **Code Review**: All changes must be reviewed by at least one other developer
5. **CI/CD**: All GitHub Actions workflows must pass

### Advanced Testing Standards Status

Advanced testing standards (as defined in `master_cursor_rules/testing.mdc`): **Not Yet Activated**

When activated, all new code must conform to these advanced standards.

## Documentation

- Maintain up-to-date API documentation
- Update the README.md with any user-facing changes
- Document complex algorithms and design decisions
- Keep code comments current with code changes

## Release Process

1. Update the version number in package.json and/or pyproject.toml
2. Update the CHANGELOG.md file
3. Create a new release branch: `release/vX.Y.Z`
4. Create a pull request for the release
5. After approval, merge to main
6. Tag the release: `git tag vX.Y.Z`
7. Push the tag: `git push origin vX.Y.Z`
8. Create a GitHub release with release notes 