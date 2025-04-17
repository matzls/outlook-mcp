"""Main module for the {{project_name}} project.

This module contains the main functionality of the project.
"""

import logging
from typing import Any, Dict, List, Optional

import logfire

# Configure logging
logfire.configure()
logger = logfire.getLogger(__name__)


def process_data(data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Process the input data according to the specified options.
    
    Args:
        data: The input data to process
        options: Optional processing options
        
    Returns:
        The processed data
        
    Raises:
        ValueError: If the input data is invalid
        KeyError: If a required key is missing from the data
    """
    if not data:
        raise ValueError("Input data cannot be empty")
    
    options = options or {}
    logger.info("Processing data", data_size=len(data), options=options)
    
    # Process the data (replace with actual implementation)
    result = {
        "processed": True,
        "original": data,
        "options_used": options,
    }
    
    logger.info("Data processing complete", result_size=len(result))
    return result


def run(input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run the main functionality of the project.
    
    This is the main entry point for the project.
    
    Args:
        input_data: Optional input data to process
        
    Returns:
        The result of the processing
    """
    logger.info("Starting {{project_name}}")
    
    # Use default data if none provided
    if input_data is None:
        input_data = {"default": True, "value": 42}
    
    # Process the data
    result = process_data(input_data)
    
    logger.info("{{project_name}} completed successfully")
    return result


if __name__ == "__main__":
    # Example usage when run as a script
    sample_data = {
        "name": "Sample",
        "values": [1, 2, 3],
    }
    
    result = run(sample_data)
    print(f"Result: {result}")
