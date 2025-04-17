"""Test fixtures for the {{project_name}} project."""

import pytest


@pytest.fixture
def sample_data():
    """Return sample data for testing.
    
    This fixture provides a standard set of test data that can be used
    across multiple tests.
    
    Returns:
        dict: A dictionary containing sample test data
    """
    return {
        "id": 1,
        "name": "Test Item",
        "value": 100,
        "active": True,
    }


@pytest.fixture
def mock_config():
    """Return a mock configuration for testing.
    
    This fixture provides a standard configuration that can be used
    for testing without accessing real configuration files.
    
    Returns:
        dict: A dictionary containing configuration values
    """
    return {
        "api_url": "https://api.example.com",
        "timeout": 30,
        "retry_attempts": 3,
        "log_level": "INFO",
    }


# Add more fixtures as needed for your project
