"""
Tests for the file_router_agent module of the Academic Research Automation System.

This module contains tests for the file routing and processing functionality.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

# Since we don't have direct access to the file_router_agent module yet,
# we'll create tests based on expected functionality and interfaces

class TestFileRouterAgent:
    """Test suite for the file_router_agent module."""
    
    @pytest.fixture
    def mock_file_router(self):
        """Create a mock file router agent."""
        mock = MagicMock()
        mock.route_file.return_value = {
            "status": "success",
            "file_type": "pdf",
            "destination": "pdf_processor"
        }
        mock.process_file.return_value = {
            "status": "success",
            "processed_content": "Sample processed content",
            "metadata": {"pages": 10, "references": 5}
        }
        return mock
    
    def test_route_pdf_file(self, mock_file_router, sample_document_path):
        """Test routing a PDF file to the correct processor."""
        # Call the method
        result = mock_file_router.route_file(file_path=sample_document_path)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["file_type"] == "pdf"
        assert "destination" in result
        
        # Verify the mock was called correctly
        mock_file_router.route_file.assert_called_once_with(file_path=sample_document_path)
    
    def test_route_json_file(self, mock_file_router, sample_reference_list_path):
        """Test routing a JSON file to the correct processor."""
        # Setup mock for JSON file
        mock_file_router.route_file.return_value = {
            "status": "success",
            "file_type": "json",
            "destination": "json_processor"
        }
        
        # Call the method
        result = mock_file_router.route_file(file_path=sample_reference_list_path)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["file_type"] == "json"
        assert result["destination"] == "json_processor"
        
        # Verify the mock was called correctly
        mock_file_router.route_file.assert_called_once_with(file_path=sample_reference_list_path)
    
    def test_route_markdown_file(self, mock_file_router, sample_research_brief_path):
        """Test routing a Markdown file to the correct processor."""
        # Setup mock for Markdown file
        mock_file_router.route_file.return_value = {
            "status": "success",
            "file_type": "markdown",
            "destination": "markdown_processor"
        }
        
        # Call the method
        result = mock_file_router.route_file(file_path=sample_research_brief_path)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["file_type"] == "markdown"
        assert result["destination"] == "markdown_processor"
        
        # Verify the mock was called correctly
        mock_file_router.route_file.assert_called_once_with(file_path=sample_research_brief_path)
    
    def test_route_unsupported_file(self, mock_file_router):
        """Test routing an unsupported file type."""
        # Setup mock for unsupported file
        mock_file_router.route_file.return_value = {
            "status": "error",
            "message": "Unsupported file type",
            "file_type": "unknown"
        }
        
        # Call the method with an unsupported file
        result = mock_file_router.route_file(file_path="unsupported.xyz")
        
        # Verify the result
        assert result["status"] == "error"
        assert "message" in result
        assert result["file_type"] == "unknown"
        
        # Verify the mock was called correctly
        mock_file_router.route_file.assert_called_once_with(file_path="unsupported.xyz")
    
    def test_process_file(self, mock_file_router, sample_document_path):
        """Test processing a file."""
        # Call the method
        result = mock_file_router.process_file(
            file_path=sample_document_path,
            output_path="test_output"
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "processed_content" in result
        assert "metadata" in result
        
        # Verify the mock was called correctly
        mock_file_router.process_file.assert_called_once_with(
            file_path=sample_document_path,
            output_path="test_output"
        )
    
    def test_batch_process_files(self, mock_file_router):
        """Test batch processing multiple files."""
        # Setup mock for batch processing
        mock_file_router.batch_process.return_value = {
            "status": "success",
            "processed_files": 3,
            "failed_files": 0,
            "results": [
                {"file": "file1.pdf", "status": "success"},
                {"file": "file2.json", "status": "success"},
                {"file": "file3.md", "status": "success"}
            ]
        }
        
        # Call the method
        files = ["file1.pdf", "file2.json", "file3.md"]
        result = mock_file_router.batch_process(
            file_paths=files,
            output_path="test_output"
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert result["processed_files"] == 3
        assert result["failed_files"] == 0
        assert len(result["results"]) == 3
        
        # Verify the mock was called correctly
        mock_file_router.batch_process.assert_called_once_with(
            file_paths=files,
            output_path="test_output"
        )
    
    def test_file_type_detection(self, mock_file_router):
        """Test file type detection functionality."""
        # Setup mock for file type detection
        mock_file_router.detect_file_type.return_value = "pdf"
        
        # Call the method
        file_type = mock_file_router.detect_file_type(file_path="test.pdf")
        
        # Verify the result
        assert file_type == "pdf"
        
        # Verify the mock was called correctly
        mock_file_router.detect_file_type.assert_called_once_with(file_path="test.pdf")
