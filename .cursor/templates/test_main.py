"""Tests for the main module."""

import pytest

from {{project_name}}.main import process_data, run


class TestProcessData:
    """Tests for the process_data function."""

    def test_process_data_with_valid_input(self):
        """Test process_data with valid input data."""
        # Arrange
        data = {"name": "Test", "value": 42}
        options = {"option1": True}
        
        # Act
        result = process_data(data, options)
        
        # Assert
        assert result["processed"] is True
        assert result["original"] == data
        assert result["options_used"] == options

    def test_process_data_with_empty_input(self):
        """Test process_data with empty input data raises ValueError."""
        # Arrange
        data = {}
        
        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            process_data(data)
        
        assert "Input data cannot be empty" in str(excinfo.value)

    def test_process_data_with_default_options(self):
        """Test process_data with default options."""
        # Arrange
        data = {"name": "Test", "value": 42}
        
        # Act
        result = process_data(data)
        
        # Assert
        assert result["processed"] is True
        assert result["original"] == data
        assert result["options_used"] == {}


class TestRun:
    """Tests for the run function."""

    def test_run_with_custom_input(self):
        """Test run with custom input data."""
        # Arrange
        input_data = {"name": "Custom", "value": 100}
        
        # Act
        result = run(input_data)
        
        # Assert
        assert result["processed"] is True
        assert result["original"] == input_data

    def test_run_with_default_input(self):
        """Test run with default input (None)."""
        # Act
        result = run()
        
        # Assert
        assert result["processed"] is True
        assert result["original"]["default"] is True
        assert result["original"]["value"] == 42
