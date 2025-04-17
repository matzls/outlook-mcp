# Testing and Linting Standards Guide

This document provides comprehensive guidelines for testing and linting standards across all projects. It serves as a reference for developers and AI agents to ensure consistent code quality and testing practices.

## Table of Contents

1. [Linting Standards](#linting-standards)
   - [Tools](#linting-tools)
   - [Configuration](#linting-configuration)
   - [Code Style](#code-style)
   - [Documentation Standards](#documentation-standards)
   - [Type Annotations](#type-annotations)
   - [Security Standards](#security-standards)
   - [Implementation Process](#linting-implementation-process)

2. [Testing Standards](#testing-standards)
   - [Tools](#testing-tools)
   - [Test Organization](#test-organization)
   - [Test Types](#test-types)
   - [Test Coverage](#test-coverage)
   - [Test Fixtures](#test-fixtures)
   - [Mocking](#mocking)
   - [Assertions](#assertions)
   - [Implementation Process](#testing-implementation-process)

3. [CI/CD Integration](#cicd-integration)
   - [GitHub Actions](#github-actions)
   - [Quality Gates](#quality-gates)

4. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Linting Standards

### Linting Tools

We use the following tools for code quality:

1. **Ruff**: Primary linter for Python code
   - Comprehensive linting with 100+ rules
   - Fast execution (written in Rust)
   - Replaces multiple tools (flake8, pylint, etc.)

2. **Black**: Code formatter
   - Consistent code formatting
   - No debates about style
   - Default line length of 88 characters

3. **isort**: Import sorter
   - Consistent import organization
   - Compatible with Black
   - Grouped imports by type

4. **mypy**: Static type checker
   - Enforces type annotations
   - Catches type-related errors
   - Improves code readability and maintainability

5. **Bandit**: Security linter
   - Identifies security vulnerabilities
   - Focuses on common security issues
   - Configurable severity levels

6. **pre-commit**: Git hooks for automated checks
   - Runs linters before commits
   - Prevents committing non-compliant code
   - Consistent enforcement across team

### Linting Configuration

#### pyproject.toml

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
# Enable comprehensive set of rules
select = [
    "E", "F", "B", "I", "N", "D", "UP", "ANN", "S", "BLE", "A", "C4",
    "T10", "EM", "EXE", "ISC", "ICN", "G", "INP", "PIE", "T20", "PT",
    "Q", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "ARG", "ERA", "PD",
    "PGH", "PL", "TRY", "NPY", "RUF"
]
# Exclude some docstring violations (Google style allows these)
ignore = ["D203", "D212", "D107"]

# Docstring style enforcement
[tool.ruff.lint.pydocstyle]
convention = "google"  # Enforce Google-style docstrings

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "D104"]  # Allow unused imports in __init__.py files
"tests/*" = ["ANN", "S101", "D100", "D101", "D102", "D103"]  # Relax rules for tests

[tool.black]
line-length = 88
target-version = ["py312"]
include = '\.pyi?$'

[tool.isort]
profile = "black"  # Compatible with Black
line_length = 88
known_first_party = ["project_name"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
plugins = ["pydantic.mypy"]  # If using pydantic

# For existing projects, consider a more gradual approach
[[tool.mypy.overrides]]
module = "src.legacy.*"
disallow_untyped_defs = false
check_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
disallow_incomplete_defs = false

[tool.bandit]
exclude_dirs = ["tests", "venv"]
skips = ["B101"]  # Skip assert warnings in tests
```

#### .pre-commit-config.yaml

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: check-ast  # Verify Python syntax
    -   id: check-json
    -   id: check-toml
    -   id: debug-statements  # Check for debugger imports

-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.3.0
    hooks:
    -   id: ruff
        args: [--fix, --exit-non-zero-on-fix]

-   repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
    -   id: black
        language_version: python3.12

-   repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
    -   id: isort

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
    -   id: mypy
        additional_dependencies: [
            types-requests,
            types-PyYAML,
            pydantic,
        ]

-   repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
    -   id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

### Code Style

#### Naming Conventions

- **Classes**: `CamelCase`
- **Functions/Methods**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private attributes/methods**: Prefix with underscore (`_private_method`)
- **Module names**: Short, lowercase, no underscores

#### Function and Method Structure

- Keep functions focused on a single responsibility
- Limit function length to 50 lines
- Limit function complexity (max 12 branches)
- Limit function parameters (max 5 parameters)
- Use keyword arguments for clarity
- Return early to avoid deep nesting

#### File Organization

- Keep files under 500 lines
- Group related functionality in modules
- Use clear module boundaries
- Organize imports in standard order (stdlib, third-party, local)
- One class per file for large classes

### Documentation Standards

#### Google-style Docstrings

```python
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from the specified URL.

    This function makes an HTTP request to the given URL and returns
    the parsed JSON response.

    Args:
        url: The URL to fetch data from
        timeout: Request timeout in seconds

    Returns:
        Dictionary containing the fetched data

    Raises:
        ValueError: If the URL is invalid
        RequestError: If the request fails
    """
    # Implementation
```

#### Module Docstrings

```python
"""
User authentication module.

This module handles user authentication, including login, logout,
password reset, and session management.
"""
```

#### Class Docstrings

```python
class User:
    """User model for authentication and profile management.

    This class represents a user in the system and provides methods
    for authentication, profile updates, and permission checks.

    Attributes:
        id: Unique identifier for the user
        username: User's login name
        email: User's email address
        is_active: Whether the user account is active
    """
```

### Type Annotations

#### Basic Types

```python
def process_data(data: list[str], limit: int = 10) -> list[str]:
    """Process a list of strings."""
    return data[:limit]
```

#### Complex Types

```python
from typing import Dict, List, Optional, TypeVar, Union, Callable, Any

T = TypeVar('T')

def transform_data(
    data: Dict[str, List[T]],
    transformer: Callable[[T], Union[str, int]],
    filter_func: Optional[Callable[[T], bool]] = None
) -> Dict[str, List[Union[str, int]]]:
    """Transform data using the provided transformer function."""
```

#### Type Aliases

```python
from typing import Dict, List, TypedDict, Union

# Type aliases
UserId = int
UserData = Dict[str, Union[str, int, bool]]

# TypedDict for structured dictionaries
class UserDict(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool
```

### Security Standards

#### Input Validation

- Validate all user inputs
- Use Pydantic models for structured data validation
- Sanitize inputs before processing
- Use parameterized queries for database operations

#### Exception Handling

```python
# Bad - Catching all exceptions without specific handling
try:
    result = process_data(user_input)
except Exception as e:
    logger.error(f"Error: {e}")
    return None

# Good - Specific exception handling
try:
    result = process_data(user_input)
    return result
except ValueError as e:
    logger.exception("Invalid data format")
    return None
except IOError as e:
    logger.exception("I/O error during processing")
    return None
except Exception:
    logger.exception("Unexpected error during processing")
    return None
```

#### Secure Coding Practices

- No hardcoded secrets
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization
- Follow the principle of least privilege
- Use HTTPS/TLS for all external communications
- Validate file paths to prevent path traversal

### Linting Implementation Process

1. **Setup Configuration Files**
   - Create pyproject.toml with linting configurations
   - Set up pre-commit hooks
   - Configure CI/CD integration

2. **Apply to New Code**
   - All new code must comply with full set of linting rules
   - New files should have complete type annotations
   - New functions should have Google-style docstrings

3. **Gradually Improve Existing Code**
   - Address security issues first
   - Add type annotations to public APIs
   - Improve docstrings for public functions
   - Fix code style issues

4. **Enforce Standards**
   - Run pre-commit hooks before each commit
   - Use CI/CD to enforce standards
   - Conduct code reviews with linting standards in mind

---

## Testing Standards

### Testing Tools

1. **pytest**: Primary testing framework
   - Powerful fixture system
   - Parameterized tests
   - Comprehensive plugin ecosystem

2. **pytest-asyncio**: For testing async code
   - Supports async fixtures
   - Handles async test functions
   - Manages event loop properly

3. **pytest-cov**: For test coverage
   - Measures code coverage
   - Generates coverage reports
   - Identifies untested code

4. **pytest-mock**: For mocking
   - Simplifies mocking
   - Integrates with pytest fixtures
   - Tracks mock usage

### Test Organization

#### Directory Structure

```
project/
├── src/
│   └── project_name/
│       ├── module1.py
│       └── module2.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── test_module1.py
    │   └── test_module2.py
    ├── integration/
    │   └── test_integration.py
    └── e2e/
        └── test_e2e.py
```

#### Test File Naming

- Test files should be named `test_*.py`
- Test functions should be named `test_*`
- Test classes should be named `Test*`

#### Test Class Structure

```python
import pytest

@pytest.mark.unit()
class TestModule:
    """Tests for the module functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_data = {"key": "value"}

    def teardown_method(self):
        """Clean up after each test method."""
        self.test_data = None

    def test_function_success(self):
        """Test successful function execution."""
        # Test implementation

    def test_function_failure(self):
        """Test function failure handling."""
        # Test implementation
```

### Test Types

#### Unit Tests

- Test individual functions and classes in isolation
- Mock external dependencies
- Focus on specific functionality
- Fast execution

```python
@pytest.mark.unit()
def test_calculate_total():
    """Test the calculate_total function."""
    # Arrange
    items = [{"price": 10}, {"price": 20}]

    # Act
    result = calculate_total(items)

    # Assert
    assert result == 30
```

#### Integration Tests

- Test interactions between components
- Minimal mocking
- Focus on component integration
- May use external resources (database, API)

```python
@pytest.mark.integration()
async def test_user_repository_with_db(db_connection):
    """Test UserRepository with a real database."""
    # Arrange
    repo = UserRepository(db_connection)
    user_data = {"username": "test_user", "email": "test@example.com"}

    # Act
    user_id = await repo.create_user(user_data)
    user = await repo.get_user(user_id)

    # Assert
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]
```

#### End-to-End Tests

- Test complete user flows
- Minimal or no mocking
- Focus on system behavior
- May be slower to execute

```python
@pytest.mark.e2e()
async def test_user_registration_flow(client, db_connection):
    """Test the complete user registration flow."""
    # Arrange
    user_data = {"username": "new_user", "email": "new@example.com", "password": "secure_password"}

    # Act
    response = await client.post("/api/users/register", json=user_data)

    # Assert
    assert response.status_code == 201

    # Verify user was created in the database
    user_repo = UserRepository(db_connection)
    user = await user_repo.get_user_by_username("new_user")
    assert user is not None
    assert user["email"] == user_data["email"]
```

### Test Coverage

- Aim for at least 80% code coverage
- Cover all code paths (success, failure, edge cases)
- Focus on critical functionality
- Use coverage reports to identify gaps

```bash
# Run tests with coverage
pytest --cov=src.project_name tests/

# Generate HTML coverage report
pytest --cov=src.project_name --cov-report=html tests/
```

### Test Fixtures

#### Basic Fixtures

```python
@pytest.fixture
def sample_data():
    """Return sample data for testing."""
    return {"id": 1, "name": "Test", "value": 100}

def test_process_data(sample_data):
    """Test processing data using the fixture."""
    result = process_data(sample_data)
    assert result["processed_value"] == 200
```

#### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: recreated for each test
def function_fixture():
    """Fixture with function scope."""
    return {"value": 1}

@pytest.fixture(scope="class")  # Created once per test class
def class_fixture():
    """Fixture with class scope."""
    return {"value": 2}

@pytest.fixture(scope="module")  # Created once per test module
def module_fixture():
    """Fixture with module scope."""
    return {"value": 3}

@pytest.fixture(scope="session")  # Created once per test session
def session_fixture():
    """Fixture with session scope."""
    return {"value": 4}
```

#### Async Fixtures

```python
@pytest_asyncio.fixture
async def db_connection():
    """Create a database connection for testing."""
    conn = await asyncpg.connect(DATABASE_URL)
    yield conn
    await conn.close()

@pytest.mark.asyncio
async def test_async_function(db_connection):
    """Test an async function with an async fixture."""
    result = await async_function(db_connection)
    assert result is not None
```

#### Fixture Factories

```python
@pytest.fixture
def create_user():
    """Factory fixture to create users with different attributes."""
    def _create_user(username, email=None, is_active=True):
        return {
            "username": username,
            "email": email or f"{username}@example.com",
            "is_active": is_active
        }
    return _create_user

def test_user_activation(create_user):
    """Test user activation using the factory fixture."""
    user = create_user("testuser", is_active=False)
    activated_user = activate_user(user)
    assert activated_user["is_active"] is True
```

### Mocking

#### Basic Mocking

```python
def test_send_email(mocker):
    """Test the send_email function with mocked dependencies."""
    # Arrange
    mock_smtp = mocker.patch("smtplib.SMTP")
    mock_smtp_instance = mock_smtp.return_value

    # Act
    result = send_email("recipient@example.com", "Subject", "Body")

    # Assert
    assert result is True
    mock_smtp.assert_called_once_with("smtp.example.com", 587)
    mock_smtp_instance.send_message.assert_called_once()
```

#### Mocking Async Functions

```python
async def test_fetch_user_data(mocker):
    """Test fetching user data with mocked API client."""
    # Arrange
    mock_client = mocker.AsyncMock()
    mock_client.get.return_value = {"id": 1, "name": "Test User"}

    # Act
    result = await fetch_user_data(1, client=mock_client)

    # Assert
    assert result["name"] == "Test User"
    mock_client.get.assert_called_once_with("/users/1")
```

#### Mocking Classes

```python
def test_user_service(mocker):
    """Test UserService with mocked repository."""
    # Arrange
    mock_repo = mocker.Mock()
    mock_repo.get_user.return_value = {"id": 1, "name": "Test User"}
    service = UserService(repository=mock_repo)

    # Act
    user = service.get_user_by_id(1)

    # Assert
    assert user["name"] == "Test User"
    mock_repo.get_user.assert_called_once_with(1)
```

### Assertions

#### Basic Assertions

```python
def test_basic_assertions():
    """Demonstrate basic assertions."""
    # Equality
    assert 1 + 1 == 2

    # Identity
    assert [] is not []

    # Membership
    assert "a" in "abc"

    # Boolean
    assert True
    assert not False

    # Comparison
    assert 5 > 3
    assert 10 >= 10
```

#### Exception Assertions

```python
def test_exception_handling():
    """Test that exceptions are raised correctly."""
    # Test that an exception is raised
    with pytest.raises(ValueError):
        int("not a number")

    # Test exception message
    with pytest.raises(ValueError) as excinfo:
        raise ValueError("Invalid value")
    assert "Invalid value" in str(excinfo.value)
```

#### Approximate Assertions

```python
def test_approximate_values():
    """Test approximate equality for floating-point values."""
    # Test approximate equality
    assert 0.1 + 0.2 == pytest.approx(0.3)

    # Test with relative tolerance
    assert 100 == pytest.approx(101, rel=0.02)  # 2% tolerance

    # Test with absolute tolerance
    assert 100 == pytest.approx(101, abs=2)  # ±2 tolerance
```

#### Collection Assertions

```python
def test_collection_assertions():
    """Test assertions for collections."""
    # List equality (order matters)
    assert [1, 2, 3] == [1, 2, 3]

    # Set equality (order doesn't matter)
    assert {1, 2, 3} == {3, 1, 2}

    # Dictionary equality
    assert {"a": 1, "b": 2} == {"b": 2, "a": 1}

    # Subset assertion
    assert {1, 2}.issubset({1, 2, 3})
```

### Testing Implementation Process

1. **Setup Test Environment**
   - Configure pytest
   - Set up test directories
   - Create common fixtures

2. **Write Tests First (TDD)**
   - Write tests before implementation
   - Define expected behavior
   - Run tests to verify they fail

3. **Implement Functionality**
   - Write code to make tests pass
   - Focus on simplicity and correctness
   - Refactor as needed

4. **Run Tests Continuously**
   - Run tests after each change
   - Ensure all tests pass
   - Check test coverage

5. **Refine and Expand**
   - Add edge case tests
   - Improve test coverage
   - Refactor tests for clarity

---

## CI/CD Integration

### GitHub Actions

#### Linting Workflow

```yaml
name: Lint

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install ruff black isort mypy bandit
        pip install -e .
    - name: Lint with ruff
      run: ruff check .
    - name: Check formatting with black
      run: black --check .
    - name: Check import sorting with isort
      run: isort --check-only .
    - name: Type check with mypy
      run: mypy src/
    - name: Security check with bandit
      run: bandit -c pyproject.toml -r src/
```

#### Testing Workflow

```yaml
name: Tests

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-asyncio pytest-cov
        pip install -e .
    - name: Run tests
      run: |
        pytest --cov=src.project_name tests/
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

### Quality Gates

- Require all linting checks to pass
- Require tests to pass
- Set minimum code coverage threshold (e.g., 80%)
- Require code review approval
- Enforce branch protection rules

---

## Common Issues and Solutions

### Type Annotation Issues

#### Problem: Missing Return Type

```python
# Bad
def get_user(user_id):
    return {"id": user_id, "name": "User"}

# Good
def get_user(user_id: int) -> dict[str, Any]:
    return {"id": user_id, "name": "User"}

# Better
class User(TypedDict):
    id: int
    name: str

def get_user(user_id: int) -> User:
    return {"id": user_id, "name": "User"}
```

#### Problem: Any Type

```python
# Bad
def process_data(data: Any) -> Any:
    return data["value"] * 2

# Good
def process_data(data: dict[str, int]) -> int:
    return data["value"] * 2
```

### Exception Handling Issues

#### Problem: Broad Exception Catching

```python
# Bad
try:
    result = process_data(data)
except Exception as e:
    logger.error(f"Error: {e}")

# Good
try:
    result = process_data(data)
except ValueError as e:
    logger.exception("Invalid data format")
except KeyError as e:
    logger.exception("Missing required key")
except Exception:
    logger.exception("Unexpected error during processing")
```

#### Problem: Swallowing Exceptions

```python
# Bad
try:
    result = process_data(data)
except Exception:
    pass  # Silently ignore errors

# Good
try:
    result = process_data(data)
except Exception:
    logger.exception("Error processing data")
    raise  # Re-raise or handle appropriately
```

### Testing Issues

#### Problem: Incomplete Test Coverage

```python
# Function with multiple paths
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Incomplete test (only tests happy path)
def test_divide():
    assert divide(10, 2) == 5

# Complete tests
def test_divide_success():
    assert divide(10, 2) == 5
    assert divide(0, 5) == 0
    assert divide(-10, 2) == -5

def test_divide_by_zero():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "Cannot divide by zero" in str(excinfo.value)
```

#### Problem: Brittle Tests

```python
# Brittle test (depends on exact implementation details)
def test_get_users_brittle(mocker):
    mock_db = mocker.Mock()
    service = UserService(mock_db)
    users = service.get_users()
    assert mock_db.execute.call_args[0][0] == "SELECT * FROM users"

# Robust test (focuses on behavior, not implementation)
def test_get_users_robust(mocker):
    # Arrange
    mock_db = mocker.Mock()
    mock_db.execute.return_value = [{"id": 1, "name": "User 1"}]
    service = UserService(mock_db)

    # Act
    users = service.get_users()

    # Assert
    assert len(users) == 1
    assert users[0]["name"] == "User 1"
    assert mock_db.execute.called  # Just verify it was called
```

---

By following these standards, we ensure consistent code quality and testing practices across all projects. This guide should be referenced when setting up new projects or contributing to existing ones.
