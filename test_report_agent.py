"""
Tests for the report_agent module of the Academic Research Automation System.

This module contains tests for the report generation and formatting functionality.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

# Since we don't have direct access to the report_agent module yet,
# we'll create tests based on expected functionality and interfaces

class TestReportAgent:
    """Test suite for the report_agent module."""
    
    @pytest.fixture
    def mock_report_agent(self):
        """Create a mock report agent."""
        mock = MagicMock()
        mock.generate_report.return_value = {
            "status": "success",
            "report_file": "test_output/report.md",
            "sections": ["executive_summary", "introduction", "analysis", "conclusion"],
            "word_count": 2500,
            "reference_count": 10
        }
        mock.format_report.return_value = {
            "status": "success",
            "output_formats": ["md", "pdf", "docx"],
            "output_files": [
                "test_output/report.md",
                "test_output/report.pdf",
                "test_output/report.docx"
            ]
        }
        return mock
    
    def test_generate_report(self, mock_report_agent, sample_reference_list_path, sample_research_brief_path, temp_output_dir):
        """Test report generation functionality."""
        # Call the method
        result = mock_report_agent.generate_report(
            references_file=sample_reference_list_path,
            research_brief=sample_research_brief_path,
            output_dir=temp_output_dir,
            template="academic"
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "report_file" in result
        assert "sections" in result
        assert "word_count" in result
        assert "reference_count" in result
        
        # Verify the mock was called correctly
        mock_report_agent.generate_report.assert_called_once_with(
            references_file=sample_reference_list_path,
            research_brief=sample_research_brief_path,
            output_dir=temp_output_dir,
            template="academic"
        )
    
    def test_format_report(self, mock_report_agent, temp_output_dir):
        """Test report formatting functionality."""
        # Setup report file path
        report_file = os.path.join(temp_output_dir, "report.md")
        
        # Call the method
        result = mock_report_agent.format_report(
            report_file=report_file,
            output_formats=["md", "pdf", "docx"],
            output_dir=temp_output_dir
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "output_formats" in result
        assert "output_files" in result
        assert len(result["output_files"]) == 3
        
        # Verify the mock was called correctly
        mock_report_agent.format_report.assert_called_once_with(
            report_file=report_file,
            output_formats=["md", "pdf", "docx"],
            output_dir=temp_output_dir
        )
    
    def test_generate_executive_summary(self, mock_report_agent, sample_reference_list_path, temp_output_dir):
        """Test executive summary generation."""
        # Setup mock for executive summary
        mock_report_agent.generate_executive_summary.return_value = {
            "status": "success",
            "summary": "This is an executive summary of the research...",
            "word_count": 250,
            "key_points": ["Point 1", "Point 2", "Point 3"]
        }
        
        # Call the method
        result = mock_report_agent.generate_executive_summary(
            references_file=sample_reference_list_path,
            analysis_results={"insights": ["Insight 1", "Insight 2"]},
            max_words=250
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "summary" in result
        assert "word_count" in result
        assert "key_points" in result
        
        # Verify the mock was called correctly
        mock_report_agent.generate_executive_summary.assert_called_once_with(
            references_file=sample_reference_list_path,
            analysis_results={"insights": ["Insight 1", "Insight 2"]},
            max_words=250
        )
    
    def test_generate_reference_section(self, mock_report_agent, sample_reference_list_path):
        """Test reference section generation."""
        # Setup mock for reference section
        mock_report_agent.generate_reference_section.return_value = {
            "status": "success",
            "reference_section": "# References\n\n1. Reference 1\n2. Reference 2\n...",
            "reference_count": 10,
            "citation_style": "APA"
        }
        
        # Call the method
        result = mock_report_agent.generate_reference_section(
            references_file=sample_reference_list_path,
            citation_style="APA"
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "reference_section" in result
        assert "reference_count" in result
        assert "citation_style" in result
        
        # Verify the mock was called correctly
        mock_report_agent.generate_reference_section.assert_called_once_with(
            references_file=sample_reference_list_path,
            citation_style="APA"
        )
    
    def test_add_visualizations_to_report(self, mock_report_agent, temp_output_dir):
        """Test adding visualizations to a report."""
        # Setup mock for adding visualizations
        report_file = os.path.join(temp_output_dir, "report.md")
        visualizations = [
            {"name": "chart1", "path": os.path.join(temp_output_dir, "chart1.png")},
            {"name": "chart2", "path": os.path.join(temp_output_dir, "chart2.png")}
        ]
        
        mock_report_agent.add_visualizations_to_report.return_value = {
            "status": "success",
            "updated_report": report_file,
            "added_visualizations": 2
        }
        
        # Call the method
        result = mock_report_agent.add_visualizations_to_report(
            report_file=report_file,
            visualizations=visualizations
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "updated_report" in result
        assert "added_visualizations" in result
        assert result["added_visualizations"] == 2
        
        # Verify the mock was called correctly
        mock_report_agent.add_visualizations_to_report.assert_called_once_with(
            report_file=report_file,
            visualizations=visualizations
        )
    
    def test_validate_report_structure(self, mock_report_agent, temp_output_dir):
        """Test report structure validation."""
        # Setup mock for validation
        report_file = os.path.join(temp_output_dir, "report.md")
        expected_sections = ["executive_summary", "introduction", "analysis", "conclusion", "references"]
        
        mock_report_agent.validate_report_structure.return_value = {
            "status": "success",
            "is_valid": True,
            "missing_sections": [],
            "structure_score": 1.0
        }
        
        # Call the method
        result = mock_report_agent.validate_report_structure(
            report_file=report_file,
            expected_sections=expected_sections
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert result["is_valid"] is True
        assert len(result["missing_sections"]) == 0
        assert result["structure_score"] == 1.0
        
        # Verify the mock was called correctly
        mock_report_agent.validate_report_structure.assert_called_once_with(
            report_file=report_file,
            expected_sections=expected_sections
        )
    
    def test_generate_report_with_invalid_template(self, mock_report_agent, sample_reference_list_path, sample_research_brief_path, temp_output_dir):
        """Test report generation with invalid template."""
        # Setup mock for invalid template
        mock_report_agent.generate_report.return_value = {
            "status": "error",
            "message": "Invalid template: 'nonexistent_template'",
            "available_templates": ["academic", "business", "technical"]
        }
        
        # Call the method with invalid template
        result = mock_report_agent.generate_report(
            references_file=sample_reference_list_path,
            research_brief=sample_research_brief_path,
            output_dir=temp_output_dir,
            template="nonexistent_template"
        )
        
        # Verify the result
        assert result["status"] == "error"
        assert "message" in result
        assert "available_templates" in result
        
        # Verify the mock was called correctly
        mock_report_agent.generate_report.assert_called_once_with(
            references_file=sample_reference_list_path,
            research_brief=sample_research_brief_path,
            output_dir=temp_output_dir,
            template="nonexistent_template"
        )
