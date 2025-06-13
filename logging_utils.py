"""
Enhanced logging utilities for the Academic Research Automation System.

This module provides functions for setting up and using structured logging
across all agent modules, with additional support for real-time logging
to the Streamlit UI and comprehensive error tracking.
"""

import os
import sys
import time
import logging
import traceback
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

# Global callback for real-time logging to Streamlit
_log_callbacks = []

def register_log_callback(callback: Callable[[str, str, str], None]) -> None:
    """
    Register a callback function to receive log messages in real-time.
    
    Args:
        callback: Function that takes (message, level, timestamp) as arguments
    """
    global _log_callbacks
    if callback not in _log_callbacks:
        _log_callbacks.append(callback)

def unregister_log_callback(callback: Callable[[str, str, str], None]) -> None:
    """
    Unregister a previously registered callback function.
    
    Args:
        callback: Function to unregister
    """
    global _log_callbacks
    if callback in _log_callbacks:
        _log_callbacks.remove(callback)

class StreamlitLogHandler(logging.Handler):
    """Custom log handler that forwards logs to registered callbacks."""
    
    def emit(self, record):
        """
        Emit a log record to all registered callbacks.
        
        Args:
            record: Log record to emit
        """
        try:
            msg = self.format(record)
            timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            
            # Forward to all registered callbacks
            for callback in _log_callbacks:
                try:
                    callback(msg, record.levelname, timestamp)
                except Exception:
                    # Don't let callback errors affect logging
                    pass
        except Exception:
            self.handleError(record)

def setup_logger(
    name: str,
    config: Dict[str, Any],
    verbose: bool = False,
    module_name: Optional[str] = None,
    log_to_streamlit: bool = False
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.
    
    Args:
        name: Name of the logger
        config: Configuration dictionary
        verbose: Whether to enable verbose logging
        module_name: Optional module name for more specific logging
        log_to_streamlit: Whether to enable logging to Streamlit UI
        
    Returns:
        Configured logger instance
    """
    # Get logging configuration
    log_level_name = config.get('logging', {}).get('level', 'INFO')
    log_level = getattr(logging, log_level_name)
    
    if verbose:
        log_level = logging.DEBUG
        
    log_format = config.get('logging', {}).get(
        'format', 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create logger
    if module_name:
        logger_name = f"{name}.{module_name}"
    else:
        logger_name = name
        
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add console handler if enabled
    if config.get('logging', {}).get('console', True):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)
    
    # Add file handler if enabled
    if config.get('logging', {}).get('file', True):
        logs_dir = config.get('paths', {}).get('logs_dir', 'logs')
        if not os.path.isabs(logs_dir):
            logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), logs_dir)
            
        os.makedirs(logs_dir, exist_ok=True)
        
        log_filename = config.get('logging', {}).get('filename', 'research_agent.log')
        log_path = os.path.join(logs_dir, log_filename)
        
        max_size = config.get('logging', {}).get('max_size', 5 * 1024 * 1024)  # 5MB default
        backup_count = config.get('logging', {}).get('backup_count', 3)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_size,
            backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    
    # Add Streamlit handler if enabled
    if log_to_streamlit:
        streamlit_handler = StreamlitLogHandler()
        streamlit_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        streamlit_handler.setLevel(log_level)
        logger.addHandler(streamlit_handler)
    
    return logger

def log_execution_time(logger: logging.Logger, start_time: float, operation: str) -> float:
    """
    Log the execution time of an operation.
    
    Args:
        logger: Logger instance
        start_time: Start time from time.time()
        operation: Description of the operation
        
    Returns:
        Elapsed time in seconds
    """
    elapsed_time = time.time() - start_time
    logger.info(f"{operation} completed in {elapsed_time:.2f} seconds")
    return elapsed_time

def log_method_call(logger: logging.Logger, method_name: str, **kwargs) -> None:
    """
    Log a method call with its arguments.
    
    Args:
        logger: Logger instance
        method_name: Name of the method being called
        **kwargs: Method arguments
    """
    # Filter out sensitive or large arguments
    filtered_kwargs = {}
    for key, value in kwargs.items():
        if key.lower() in ('password', 'token', 'secret', 'key'):
            filtered_kwargs[key] = '******'
        elif isinstance(value, (str, int, float, bool, type(None))):
            filtered_kwargs[key] = value
        else:
            filtered_kwargs[key] = f"{type(value).__name__}"
            
    logger.debug(f"Calling {method_name} with args: {filtered_kwargs}")

def log_result(logger: logging.Logger, method_name: str, result: Dict[str, Any]) -> None:
    """
    Log the result of a method call.
    
    Args:
        logger: Logger instance
        method_name: Name of the method that was called
        result: Result dictionary
    """
    status = result.get('status', 'unknown')
    if status == 'success':
        logger.info(f"{method_name} completed successfully")
    else:
        logger.error(f"{method_name} failed: {result.get('message', 'Unknown error')}")
        
    # Log additional result details at debug level
    filtered_result = {}
    for key, value in result.items():
        if key not in ('status', 'message'):
            if isinstance(value, (str, int, float, bool, type(None))):
                filtered_result[key] = value
            elif isinstance(value, list):
                filtered_result[key] = f"List with {len(value)} items"
            else:
                filtered_result[key] = f"{type(value).__name__}"
                
    logger.debug(f"{method_name} result details: {filtered_result}")

def log_exception(logger: logging.Logger, method_name: str, exception: Exception) -> Dict[str, Any]:
    """
    Log an exception that occurred during method execution.
    
    Args:
        logger: Logger instance
        method_name: Name of the method where the exception occurred
        exception: The exception that was raised
        
    Returns:
        Dictionary with exception details
    """
    # Get full traceback
    tb_str = traceback.format_exc()
    
    # Log the exception
    logger.error(f"Exception in {method_name}: {str(exception)}")
    logger.debug(f"Exception traceback: {tb_str}")
    
    # Return structured exception info
    return {
        "timestamp": datetime.now().isoformat(),
        "method": method_name,
        "exception_type": type(exception).__name__,
        "message": str(exception),
        "traceback": tb_str
    }

def setup_test_run_logger(log_file: str = "full_test_run.log") -> logging.Logger:
    """
    Set up a dedicated logger for end-to-end test runs.
    
    Args:
        log_file: Name of the log file
        
    Returns:
        Configured logger instance
    """
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Full path to log file
    log_path = os.path.join(logs_dir, log_file)
    
    # Create logger
    logger = logging.getLogger("test_run")
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add file handler
    file_handler = logging.FileHandler(log_path, mode="w")
    file_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_format)
    logger.addHandler(console_handler)
    
    return logger

def log_test_step(logger: logging.Logger, step_name: str, status: str, details: Optional[Dict[str, Any]] = None) -> None:
    """
    Log a test step with structured information.
    
    Args:
        logger: Logger instance
        step_name: Name of the test step
        status: Status of the step (e.g., "PASS", "FAIL", "SKIP")
        details: Optional details about the step
    """
    if status == "PASS":
        logger.info(f"TEST STEP [{step_name}] - {status}")
    elif status == "FAIL":
        logger.error(f"TEST STEP [{step_name}] - {status}")
        if details:
            logger.error(f"Details: {details}")
    else:
        logger.warning(f"TEST STEP [{step_name}] - {status}")
        if details:
            logger.warning(f"Details: {details}")

def log_system_info(logger: logging.Logger) -> None:
    """
    Log system information for debugging purposes.
    
    Args:
        logger: Logger instance
    """
    import platform
    
    logger.info("=== System Information ===")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"System: {platform.system()} {platform.release()}")
    
    # Log installed packages
    try:
        import pkg_resources
        installed_packages = sorted([f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set])
        logger.debug("Installed packages:")
        for pkg in installed_packages:
            logger.debug(f"  {pkg}")
    except ImportError:
        logger.debug("Could not log installed packages (pkg_resources not available)")
    
    logger.info("===========================")
