"""
Configuration utilities for the Academic Research Automation System.

This module provides functions for loading and accessing configuration settings.
"""

import os
import yaml
from typing import Dict, Any, Optional

# Default configuration file path
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file. If None, uses default path.
        
    Returns:
        Dictionary containing configuration settings.
        
    Raises:
        FileNotFoundError: If configuration file does not exist.
        yaml.YAMLError: If configuration file is not valid YAML.
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
        
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing configuration file: {e}")

def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a configuration value using a dot-separated path.
    
    Args:
        config: Configuration dictionary.
        key_path: Dot-separated path to configuration value (e.g., 'logging.level').
        default: Default value to return if key is not found.
        
    Returns:
        Configuration value or default if not found.
    """
    keys = key_path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure and required values.
    
    Args:
        config: Configuration dictionary to validate.
        
    Returns:
        True if configuration is valid, False otherwise.
    """
    # Check for required top-level sections
    required_sections = ['paths', 'logging', 'agents', 'output']
    for section in required_sections:
        if section not in config:
            print(f"Missing required configuration section: {section}")
            return False
    
    # Check for required logging settings
    if 'level' not in config.get('logging', {}):
        print("Missing required configuration: logging.level")
        return False
    
    # Check for valid logging level
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if config.get('logging', {}).get('level') not in valid_levels:
        print(f"Invalid logging level. Must be one of: {', '.join(valid_levels)}")
        return False
    
    return True

def create_directories(config: Dict[str, Any]) -> None:
    """
    Create directories specified in configuration if they don't exist.
    
    Args:
        config: Configuration dictionary.
    """
    paths = config.get('paths', {})
    for path_name, path_value in paths.items():
        if path_value and not os.path.isabs(path_value):
            # Make relative paths absolute from project root
            path_value = os.path.join(os.path.dirname(os.path.dirname(__file__)), path_value)
            
        if path_value and not os.path.exists(path_value):
            try:
                os.makedirs(path_value, exist_ok=True)
                print(f"Created directory: {path_value}")
            except OSError as e:
                print(f"Error creating directory {path_value}: {e}")
