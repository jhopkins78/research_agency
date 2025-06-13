"""
Example agent implementation with structured logging integration.

This module demonstrates how to integrate structured logging into an agent module.
"""

import os
import sys
import time
import json
import logging
from typing import Dict, Any, List, Optional, Union

# Import logging utilities
try:
    from aras.logging_utils import (
        setup_logger, 
        log_execution_time, 
        log_method_call, 
        log_result, 
        log_exception
    )
    from aras.config_utils import load_config, get_config_value
except ImportError:
    # Fallback for direct module execution
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from aras.logging_utils import (
        setup_logger, 
        log_execution_time, 
        log_method_call, 
        log_result, 
        log_exception
    )
    from aras.config_utils import load_config, get_config_value

class FileRouterAgent:
    """
    Example implementation of a File Router Agent with structured logging.
    
    This agent is responsible for routing files to appropriate processors
    based on file type and content.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, verbose: bool = False):
        """
        Initialize the File Router Agent.
        
        Args:
            config: Configuration dictionary. If None, loads from default path.
            verbose: Whether to enable verbose logging.
        """
        # Load configuration if not provided
        if config is None:
            try:
                self.config = load_config()
            except Exception as e:
                print(f"Error loading configuration: {str(e)}")
                self.config = {
                    'paths': {'output_dir': 'output', 'logs_dir': 'logs'},
                    'logging': {'level': 'INFO', 'console': True, 'file': True}
                }
        else:
            self.config = config
            
        # Set up logger
        self.logger = setup_logger("ARAS", self.config, verbose, "FileRouterAgent")
        self.logger.info("File Router Agent initialized")
        
        # Initialize supported file types
        self.supported_file_types = {
            '.pdf': 'pdf_processor',
            '.json': 'json_processor',
            '.csv': 'csv_processor',
            '.md': 'markdown_processor',
            '.txt': 'text_processor',
            '.docx': 'docx_processor',
            '.xlsx': 'excel_processor'
        }
        
        self.logger.debug(f"Supported file types: {list(self.supported_file_types.keys())}")
    
    def route_file(self, file_path: str) -> Dict[str, Any]:
        """
        Route a file to the appropriate processor based on file type.
        
        Args:
            file_path: Path to the file to route.
            
        Returns:
            Dictionary containing routing results.
        """
        log_method_call(self.logger, "route_file", file_path=file_path)
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return {"status": "error", "message": f"File not found: {file_path}"}
            
            # Detect file type
            file_type = self.detect_file_type(file_path)
            self.logger.info(f"Detected file type: {file_type}")
            
            # Determine destination processor
            if file_type in self.supported_file_types:
                destination = self.supported_file_types[file_type]
                self.logger.info(f"Routing file to {destination}")
                
                result = {
                    "status": "success",
                    "file_type": file_type.lstrip('.'),
                    "destination": destination,
                    "file_path": file_path
                }
            else:
                self.logger.warning(f"Unsupported file type: {file_type}")
                result = {
                    "status": "error",
                    "message": "Unsupported file type",
                    "file_type": "unknown",
                    "file_path": file_path
                }
            
            log_execution_time(self.logger, start_time, "File routing")
            log_result(self.logger, "route_file", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "route_file", e)
            return {"status": "error", "message": str(e)}
    
    def detect_file_type(self, file_path: str) -> str:
        """
        Detect the type of a file based on extension and content.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            File type extension (e.g., '.pdf', '.json').
        """
        log_method_call(self.logger, "detect_file_type", file_path=file_path)
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # If no extension or unknown, try to detect from content
        if not ext or ext not in self.supported_file_types:
            self.logger.debug(f"No extension or unknown extension: {ext}")
            self.logger.debug("Attempting to detect file type from content")
            
            # Read first few bytes to detect file type
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(8)
                    
                # Check for PDF signature
                if header.startswith(b'%PDF'):
                    self.logger.debug("Detected PDF signature")
                    return '.pdf'
                    
                # Check for JSON content
                try:
                    with open(file_path, 'r') as f:
                        json.load(f)
                    self.logger.debug("Detected JSON content")
                    return '.json'
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
                    
                # Default to text
                try:
                    with open(file_path, 'r') as f:
                        f.read(100)
                    self.logger.debug("Detected text content")
                    return '.txt'
                except UnicodeDecodeError:
                    # Binary file
                    self.logger.debug("Detected binary content")
                    return '.bin'
                    
            except Exception as e:
                self.logger.warning(f"Error detecting file type: {str(e)}")
                return ext or '.unknown'
        
        return ext
    
    def process_file(self, file_path: str, output_path: str) -> Dict[str, Any]:
        """
        Process a file based on its type.
        
        Args:
            file_path: Path to the file to process.
            output_path: Directory to store processing results.
            
        Returns:
            Dictionary containing processing results.
        """
        log_method_call(self.logger, "process_file", file_path=file_path, output_path=output_path)
        start_time = time.time()
        
        try:
            # Route file to determine processor
            routing_result = self.route_file(file_path)
            
            if routing_result["status"] != "success":
                return routing_result
            
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Process based on file type
            file_type = routing_result["file_type"]
            self.logger.info(f"Processing {file_type} file: {file_path}")
            
            # Simulate processing based on file type
            if file_type == "pdf":
                result = self._process_pdf(file_path, output_path)
            elif file_type == "json":
                result = self._process_json(file_path, output_path)
            elif file_type in ["markdown", "md"]:
                result = self._process_markdown(file_path, output_path)
            else:
                result = self._process_generic(file_path, output_path)
            
            log_execution_time(self.logger, start_time, f"File processing ({file_type})")
            log_result(self.logger, "process_file", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "process_file", e)
            return {"status": "error", "message": str(e)}
    
    def batch_process(self, file_paths: List[str], output_path: str) -> Dict[str, Any]:
        """
        Process multiple files in batch.
        
        Args:
            file_paths: List of file paths to process.
            output_path: Directory to store processing results.
            
        Returns:
            Dictionary containing batch processing results.
        """
        log_method_call(self.logger, "batch_process", file_count=len(file_paths), output_path=output_path)
        start_time = time.time()
        
        try:
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            results = []
            processed_count = 0
            failed_count = 0
            
            # Get parallel processing setting from config
            parallel_processes = get_config_value(self.config, 'performance.parallel_processes', 1)
            
            if parallel_processes > 1:
                self.logger.info(f"Using parallel processing with {parallel_processes} processes")
                # Implement parallel processing here if needed
                # For simplicity, we'll use sequential processing in this example
            
            # Process each file
            for file_path in file_paths:
                self.logger.info(f"Processing file {processed_count + failed_count + 1}/{len(file_paths)}: {file_path}")
                
                # Create file-specific output directory
                file_name = os.path.basename(file_path)
                file_output_path = os.path.join(output_path, os.path.splitext(file_name)[0])
                os.makedirs(file_output_path, exist_ok=True)
                
                # Process the file
                result = self.process_file(file_path, file_output_path)
                
                # Track results
                if result["status"] == "success":
                    processed_count += 1
                else:
                    failed_count += 1
                    
                results.append({
                    "file": file_path,
                    "status": result["status"],
                    "output_path": file_output_path if result["status"] == "success" else None,
                    "message": result.get("message")
                })
            
            batch_result = {
                "status": "success" if failed_count == 0 else "partial_success",
                "processed_files": processed_count,
                "failed_files": failed_count,
                "results": results
            }
            
            log_execution_time(self.logger, start_time, f"Batch processing ({len(file_paths)} files)")
            log_result(self.logger, "batch_process", batch_result)
            return batch_result
            
        except Exception as e:
            log_exception(self.logger, "batch_process", e)
            return {"status": "error", "message": str(e)}
    
    # Private processing methods
    
    def _process_pdf(self, file_path: str, output_path: str) -> Dict[str, Any]:
        """Process a PDF file."""
        self.logger.debug(f"Processing PDF file: {file_path}")
        # Simulate PDF processing
        return {
            "status": "success",
            "processed_content": "Sample processed PDF content",
            "metadata": {"pages": 10, "references": 5}
        }
    
    def _process_json(self, file_path: str, output_path: str) -> Dict[str, Any]:
        """Process a JSON file."""
        self.logger.debug(f"Processing JSON file: {file_path}")
        # Simulate JSON processing
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return {
                "status": "success",
                "processed_content": "JSON data processed",
                "metadata": {"entries": len(data) if isinstance(data, list) else 1}
            }
        except Exception as e:
            self.logger.error(f"Error processing JSON file: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _process_markdown(self, file_path: str, output_path: str) -> Dict[str, Any]:
        """Process a Markdown file."""
        self.logger.debug(f"Processing Markdown file: {file_path}")
        # Simulate Markdown processing
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Count sections (headers)
            section_count = 0
            for line in content.split('\n'):
                if line.startswith('#'):
                    section_count += 1
            
            return {
                "status": "success",
                "processed_content": "Markdown content processed",
                "metadata": {"sections": section_count, "word_count": len(content.split())}
            }
        except Exception as e:
            self.logger.error(f"Error processing Markdown file: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _process_generic(self, file_path: str, output_path: str) -> Dict[str, Any]:
        """Process a generic file."""
        self.logger.debug(f"Processing generic file: {file_path}")
        # Simulate generic processing
        return {
            "status": "success",
            "processed_content": "Generic file processed",
            "metadata": {"size_bytes": os.path.getsize(file_path)}
        }


# Example usage when run directly
if __name__ == "__main__":
    # Create agent
    agent = FileRouterAgent(verbose=True)
    
    # Process a file if provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "output"
        
        print(f"Processing file: {file_path}")
        result = agent.process_file(file_path, output_path)
        
        print(f"Result: {json.dumps(result, indent=2)}")
    else:
        print("Usage: python file_router_agent.py <file_path> [output_path]")
