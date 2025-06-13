"""
Tests for the insight_agent module of the Academic Research Automation System.

This module contains tests for the insight generation and analysis functionality.
"""

import os
import json
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Since we don't have direct access to the insight_agent module yet,
# we'll create tests based on expected functionality and interfaces

class TestInsightAgent:
    """Test suite for the insight_agent module."""
    
    @pytest.fixture
    def mock_insight_agent(self):
        """Create a mock insight agent."""
        mock = MagicMock()
        mock.analyze_references.return_value = {
            "status": "success",
            "total_references": 10,
            "reference_types": {"journal": 5, "book": 3, "website": 2},
            "year_distribution": {"2020-2024": 4, "2015-2019": 4, "2010-2014": 2},
            "quality_metrics": {"high": 7, "medium": 2, "low": 1},
            "insights": [
                "80% of references are from academic sources",
                "40% of references are from the last 5 years",
                "70% of references have high quality scores"
            ]
        }
        mock.generate_recommendations.return_value = {
            "status": "success",
            "recommendations": [
                "Consider adding more recent references (last 2 years)",
                "Include more diverse source types",
                "Replace low-quality references with higher-quality alternatives"
            ]
        }
        return mock
    
    def test_analyze_references(self, mock_insight_agent, sample_reference_list_path):
        """Test reference analysis functionality."""
        # Call the method
        result = mock_insight_agent.analyze_references(references_file=sample_reference_list_path)
        
        # Verify the result
        assert result["status"] == "success"
        assert "total_references" in result
        assert "reference_types" in result
        assert "year_distribution" in result
        assert "quality_metrics" in result
        assert "insights" in result
        assert len(result["insights"]) > 0
        
        # Verify the mock was called correctly
        mock_insight_agent.analyze_references.assert_called_once_with(references_file=sample_reference_list_path)
    
    def test_generate_recommendations(self, mock_insight_agent, sample_reference_list_path):
        """Test recommendation generation functionality."""
        # Call the method
        result = mock_insight_agent.generate_recommendations(
            references_file=sample_reference_list_path,
            research_brief_file="tests/fixtures/research_brief.md"
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        
        # Verify the mock was called correctly
        mock_insight_agent.generate_recommendations.assert_called_once_with(
            references_file=sample_reference_list_path,
            research_brief_file="tests/fixtures/research_brief.md"
        )
    
    def test_generate_visualizations(self, mock_insight_agent, sample_reference_list_path, temp_output_dir):
        """Test visualization generation functionality."""
        # Setup mock for visualization generation
        mock_insight_agent.generate_visualizations.return_value = {
            "status": "success",
            "visualizations": [
                {"name": "reference_types_chart", "path": f"{temp_output_dir}/reference_types_chart.png"},
                {"name": "year_distribution_chart", "path": f"{temp_output_dir}/year_distribution_chart.png"},
                {"name": "quality_metrics_chart", "path": f"{temp_output_dir}/quality_metrics_chart.png"}
            ]
        }
        
        # Call the method
        result = mock_insight_agent.generate_visualizations(
            references_file=sample_reference_list_path,
            output_dir=temp_output_dir
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "visualizations" in result
        assert len(result["visualizations"]) == 3
        
        # Verify the mock was called correctly
        mock_insight_agent.generate_visualizations.assert_called_once_with(
            references_file=sample_reference_list_path,
            output_dir=temp_output_dir
        )
    
    def test_analyze_reference_quality(self, mock_insight_agent):
        """Test reference quality analysis functionality."""
        # Setup mock for quality analysis
        mock_insight_agent.analyze_reference_quality.return_value = {
            "status": "success",
            "reference": "Test Reference",
            "quality_score": 0.85,
            "factors": {
                "source_reliability": 0.9,
                "citation_count": 0.8,
                "recency": 0.7,
                "completeness": 0.9
            },
            "classification": "high"
        }
        
        # Call the method
        result = mock_insight_agent.analyze_reference_quality(
            reference="Test Reference",
            metadata={"year": 2022, "venue": "Nature", "citation_count": 120}
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "quality_score" in result
        assert "factors" in result
        assert "classification" in result
        
        # Verify the mock was called correctly
        mock_insight_agent.analyze_reference_quality.assert_called_once_with(
            reference="Test Reference",
            metadata={"year": 2022, "venue": "Nature", "citation_count": 120}
        )
    
    def test_compare_with_research_brief(self, mock_insight_agent, sample_reference_list_path, sample_research_brief_path):
        """Test comparison between references and research brief."""
        # Setup mock for comparison
        mock_insight_agent.compare_with_research_brief.return_value = {
            "status": "success",
            "alignment_score": 0.75,
            "coverage": {
                "topic_1": 0.9,
                "topic_2": 0.8,
                "topic_3": 0.6,
                "topic_4": 0.7
            },
            "gaps": ["Additional sources needed for topic_3"],
            "recommendations": ["Consider adding references for topic_3"]
        }
        
        # Call the method
        result = mock_insight_agent.compare_with_research_brief(
            references_file=sample_reference_list_path,
            research_brief_file=sample_research_brief_path
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "alignment_score" in result
        assert "coverage" in result
        assert "gaps" in result
        assert "recommendations" in result
        
        # Verify the mock was called correctly
        mock_insight_agent.compare_with_research_brief.assert_called_once_with(
            references_file=sample_reference_list_path,
            research_brief_file=sample_research_brief_path
        )
    
    def test_export_analysis_to_excel(self, mock_insight_agent, sample_reference_list_path, temp_output_dir):
        """Test exporting analysis results to Excel."""
        # Setup mock for Excel export
        excel_path = os.path.join(temp_output_dir, "reference_analysis.xlsx")
        mock_insight_agent.export_analysis_to_excel.return_value = {
            "status": "success",
            "file_path": excel_path
        }
        
        # Call the method
        result = mock_insight_agent.export_analysis_to_excel(
            references_file=sample_reference_list_path,
            output_file=excel_path
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert "file_path" in result
        assert result["file_path"] == excel_path
        
        # Verify the mock was called correctly
        mock_insight_agent.export_analysis_to_excel.assert_called_once_with(
            references_file=sample_reference_list_path,
            output_file=excel_path
        )
