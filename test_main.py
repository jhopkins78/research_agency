"""
Tests for the main.py module of the Academic Research Automation System.

This module contains tests for the CLI interface and main workflow functions.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

# Import the main module
import main
from main import AcademicResearchAutomationSystem

class TestMainModule:
    """Test suite for the main.py module."""
    
    def test_initialization(self):
        """Test that the system initializes correctly."""
        system = AcademicResearchAutomationSystem(verbose=True)
        # Since we can't guarantee the actual components are available in test,
        # we're just checking that the object was created
        assert isinstance(system, AcademicResearchAutomationSystem)
    
    @patch('main.AcademicResearchAutomationSystem')
    def test_extract_references_command(self, mock_system):
        """Test the extract command in the CLI."""
        # Setup mock
        mock_instance = mock_system.return_value
        mock_instance.extract_references.return_value = {
            "status": "success",
            "references": [{"reference_number": 1, "full_text": "Test reference"}]
        }
        
        # Run the command with test arguments
        with patch('sys.argv', ['main.py', 'extract', 
                               '--pdf', 'tests/fixtures/sample_document.md',
                               '--output', 'test_output']):
            with patch('builtins.print') as mock_print:
                main.main()
                
        # Verify the correct method was called with expected arguments
        mock_instance.extract_references.assert_called_once()
        args, kwargs = mock_instance.extract_references.call_args
        assert kwargs['pdf_path'] == 'tests/fixtures/sample_document.md'
        assert kwargs['output_path'] == 'test_output'
        
        # Verify success message was printed
        mock_print.assert_called_with(pytest.approx("Successfully extracted 1 references", rel=1e-3))
    
    @patch('main.AcademicResearchAutomationSystem')
    def test_verify_citations_command(self, mock_system):
        """Test the verify command in the CLI."""
        # Setup mock
        mock_instance = mock_system.return_value
        mock_instance.verify_citations.return_value = {
            "status": "success",
            "valid_count": 8,
            "issues_count": 2,
            "invalid_count": 0
        }
        
        # Run the command with test arguments
        with patch('sys.argv', ['main.py', 'verify', 
                               '--references', 'tests/fixtures/reference_list.json',
                               '--output', 'test_output']):
            with patch('builtins.print') as mock_print:
                main.main()
                
        # Verify the correct method was called with expected arguments
        mock_instance.verify_citations.assert_called_once()
        args, kwargs = mock_instance.verify_citations.call_args
        assert kwargs['citations_source'] == 'tests/fixtures/reference_list.json'
        assert kwargs['output_path'] == 'test_output'
        
        # Verify success message was printed
        mock_print.assert_any_call("Citation verification complete")
    
    @patch('main.AcademicResearchAutomationSystem')
    def test_research_author_command(self, mock_system):
        """Test the research command in the CLI."""
        # Setup mock
        mock_instance = mock_system.return_value
        mock_instance.research_author.return_value = {
            "status": "success",
            "publications": [{"title": "Test Publication"}]
        }
        
        # Run the command with test arguments
        with patch('sys.argv', ['main.py', 'research', 
                               '--author', 'Test Author',
                               '--affiliation', 'Test University',
                               '--output', 'test_output']):
            with patch('builtins.print') as mock_print:
                main.main()
                
        # Verify the correct method was called with expected arguments
        mock_instance.research_author.assert_called_once()
        args, kwargs = mock_instance.research_author.call_args
        assert kwargs['author_name'] == 'Test Author'
        assert kwargs['affiliation'] == 'Test University'
        assert kwargs['output_path'] == 'test_output'
        
        # Verify success message was printed
        mock_print.assert_any_call(pytest.approx("Research complete: found 1 publications", rel=1e-3))
    
    @patch('main.AcademicResearchAutomationSystem')
    def test_workflow_command(self, mock_system):
        """Test the workflow command in the CLI."""
        # Setup mock
        mock_instance = mock_system.return_value
        mock_instance.execute_full_workflow.return_value = {
            "status": "success",
            "extraction_result": {"references": [{"reference_number": 1}]},
            "processing_time": 5.23,
            "report_path": "test_output/reference_analysis_report.md"
        }
        
        # Run the command with test arguments
        with patch('sys.argv', ['main.py', 'workflow', 
                               '--pdf', 'tests/fixtures/sample_document.md',
                               '--output', 'test_output']):
            with patch('builtins.print') as mock_print:
                main.main()
                
        # Verify the correct method was called with expected arguments
        mock_instance.execute_full_workflow.assert_called_once()
        args, kwargs = mock_instance.execute_full_workflow.call_args
        assert kwargs['pdf_path'] == 'tests/fixtures/sample_document.md'
        assert kwargs['output_path'] == 'test_output'
        
        # Verify success message was printed
        mock_print.assert_any_call(pytest.approx("Full workflow completed successfully", rel=1e-3))

class TestExtractReferences:
    """Test suite for the extract_references functionality."""
    
    @patch('main.PDFReferenceExtractionAgent')
    def test_extract_references_success(self, mock_prea):
        """Test successful reference extraction."""
        # Setup mock
        mock_prea_instance = MagicMock()
        mock_prea_instance.extract_references_from_pdf.return_value = {
            "status": "success",
            "references": [
                {"reference_number": 1, "full_text": "Test Reference 1"},
                {"reference_number": 2, "full_text": "Test Reference 2"}
            ]
        }
        mock_prea.return_value = mock_prea_instance
        
        # Create system with mocked component
        system = AcademicResearchAutomationSystem()
        system.prea = mock_prea_instance
        
        # Call the method
        result = system.extract_references(
            pdf_path="test.pdf",
            output_path="test_output",
            formats=["json", "csv"]
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert len(result["references"]) == 2
        
        # Verify the mock was called correctly
        mock_prea_instance.extract_references_from_pdf.assert_called_once_with(
            pdf_path="test.pdf",
            output_path="test_output",
            output_formats=["json", "csv"],
            use_ocr_if_needed=False
        )
    
    def test_extract_references_file_not_found(self):
        """Test reference extraction with non-existent file."""
        system = AcademicResearchAutomationSystem()
        result = system.extract_references(
            pdf_path="non_existent_file.pdf",
            output_path="test_output"
        )
        
        assert result["status"] == "error"
        assert "not found" in result["message"]

class TestVerifyCitations:
    """Test suite for the verify_citations functionality."""
    
    @patch('main.AcademicResearchAgentSystem')
    def test_verify_citations_with_json_input(self, mock_aras):
        """Test citation verification with JSON input."""
        # Setup mock
        mock_aras_instance = MagicMock()
        mock_aras_instance.validate_citations.return_value = [
            {"citation": "Citation 1", "status": "valid", "issues": []},
            {"citation": "Citation 2", "status": "issues_found", "issues": ["year_mismatch"]}
        ]
        mock_aras.return_value = mock_aras_instance
        
        # Create a temporary JSON file
        temp_json = "temp_citations.json"
        with open(temp_json, 'w') as f:
            json.dump(["Citation 1", "Citation 2"], f)
        
        try:
            # Create system with mocked component
            system = AcademicResearchAutomationSystem()
            system.aras = mock_aras_instance
            
            # Call the method
            with patch('os.makedirs'):
                with patch('builtins.open', create=True):
                    result = system.verify_citations(
                        citations_source=temp_json,
                        output_path="test_output"
                    )
            
            # Verify the result
            assert result["status"] == "success"
            assert result["valid_count"] == 1
            assert result["issues_count"] == 1
            
            # Verify the mock was called correctly
            mock_aras_instance.validate_citations.assert_called_once()
        
        finally:
            # Clean up
            if os.path.exists(temp_json):
                os.remove(temp_json)
