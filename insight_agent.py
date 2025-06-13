"""
Insight Agent implementation with structured logging integration.

This module provides functionality for analyzing references and generating insights.
"""

import os
import sys
import time
import json
import logging
import pandas as pd
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

class InsightAgent:
    """
    Insight Agent for analyzing references and generating insights.
    
    This agent analyzes reference data to extract insights, generate
    recommendations, and create visualizations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, verbose: bool = False):
        """
        Initialize the Insight Agent.
        
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
        self.logger = setup_logger("ARAS", self.config, verbose, "InsightAgent")
        self.logger.info("Insight Agent initialized")
        
        # Initialize quality thresholds from config
        self.quality_thresholds = get_config_value(
            self.config, 
            'reference_analysis.quality_thresholds', 
            {'high': 0.8, 'medium': 0.6, 'low': 0.4}
        )
        
        self.logger.debug(f"Quality thresholds: {self.quality_thresholds}")
    
    def analyze_references(self, references_file: str) -> Dict[str, Any]:
        """
        Analyze references to extract insights.
        
        Args:
            references_file: Path to the references file (JSON).
            
        Returns:
            Dictionary containing analysis results.
        """
        log_method_call(self.logger, "analyze_references", references_file=references_file)
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
            
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            self.logger.info(f"Analyzing {len(references)} references")
            
            # Analyze reference types
            reference_types = self._analyze_reference_types(references)
            self.logger.info(f"Reference types: {reference_types}")
            
            # Analyze year distribution
            year_distribution = self._analyze_year_distribution(references)
            self.logger.info(f"Year distribution: {year_distribution}")
            
            # Analyze quality metrics
            quality_metrics = self._analyze_quality_metrics(references)
            self.logger.info(f"Quality metrics: {quality_metrics}")
            
            # Generate insights
            insights = self._generate_insights(references, reference_types, year_distribution, quality_metrics)
            self.logger.info(f"Generated {len(insights)} insights")
            
            result = {
                "status": "success",
                "total_references": len(references),
                "reference_types": reference_types,
                "year_distribution": year_distribution,
                "quality_metrics": quality_metrics,
                "insights": insights
            }
            
            log_execution_time(self.logger, start_time, "Reference analysis")
            log_result(self.logger, "analyze_references", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "analyze_references", e)
            return {"status": "error", "message": str(e)}
    
    def generate_recommendations(self, references_file: str, research_brief_file: str) -> Dict[str, Any]:
        """
        Generate recommendations based on references and research brief.
        
        Args:
            references_file: Path to the references file (JSON).
            research_brief_file: Path to the research brief file.
            
        Returns:
            Dictionary containing recommendations.
        """
        log_method_call(self.logger, "generate_recommendations", 
                      references_file=references_file, 
                      research_brief_file=research_brief_file)
        start_time = time.time()
        
        try:
            # Check if files exist
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
                
            if not os.path.exists(research_brief_file):
                self.logger.error(f"Research brief file not found: {research_brief_file}")
                return {"status": "error", "message": f"Research brief file not found: {research_brief_file}"}
            
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            # Load research brief
            self.logger.info(f"Loading research brief from {research_brief_file}")
            with open(research_brief_file, 'r') as f:
                research_brief = f.read()
            
            # Analyze references
            self.logger.info("Analyzing references")
            analysis_result = self.analyze_references(references_file)
            
            if analysis_result["status"] != "success":
                return analysis_result
            
            # Compare with research brief
            self.logger.info("Comparing references with research brief")
            comparison_result = self.compare_with_research_brief(
                references_file=references_file,
                research_brief_file=research_brief_file
            )
            
            if comparison_result["status"] != "success":
                return comparison_result
            
            # Generate recommendations based on analysis and comparison
            self.logger.info("Generating recommendations")
            recommendations = []
            
            # Check for recency
            recent_count = analysis_result["year_distribution"].get("2020-2024", 0)
            total_count = analysis_result["total_references"]
            if recent_count / total_count < 0.4:
                recommendations.append("Consider adding more recent references (last 5 years)")
            
            # Check for diversity of source types
            if len(analysis_result["reference_types"]) < 3:
                recommendations.append("Include more diverse source types")
            
            # Check for quality
            low_quality_count = analysis_result["quality_metrics"].get("low", 0)
            if low_quality_count > 0:
                recommendations.append("Replace low-quality references with higher-quality alternatives")
            
            # Check for coverage gaps
            for gap in comparison_result.get("gaps", []):
                recommendations.append(f"Address gap in coverage: {gap}")
            
            result = {
                "status": "success",
                "recommendations": recommendations,
                "analysis_result": analysis_result,
                "comparison_result": comparison_result
            }
            
            log_execution_time(self.logger, start_time, "Recommendation generation")
            log_result(self.logger, "generate_recommendations", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "generate_recommendations", e)
            return {"status": "error", "message": str(e)}
    
    def generate_visualizations(self, references_file: str, output_dir: str) -> Dict[str, Any]:
        """
        Generate visualizations based on reference analysis.
        
        Args:
            references_file: Path to the references file (JSON).
            output_dir: Directory to store visualization files.
            
        Returns:
            Dictionary containing visualization results.
        """
        log_method_call(self.logger, "generate_visualizations", 
                      references_file=references_file, 
                      output_dir=output_dir)
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Analyze references
            self.logger.info("Analyzing references")
            analysis_result = self.analyze_references(references_file)
            
            if analysis_result["status"] != "success":
                return analysis_result
            
            # Get visualization settings from config
            viz_format = get_config_value(self.config, 'visualizations.format', 'png')
            dpi = get_config_value(self.config, 'visualizations.dpi', 300)
            figure_size = get_config_value(self.config, 'visualizations.figure_size', [10, 6])
            color_scheme = get_config_value(self.config, 'visualizations.color_scheme', 'viridis')
            include_titles = get_config_value(self.config, 'visualizations.include_titles', True)
            
            self.logger.debug(f"Visualization settings: format={viz_format}, dpi={dpi}, figure_size={figure_size}")
            
            # Generate visualizations
            self.logger.info("Generating visualizations")
            visualizations = []
            
            try:
                import matplotlib.pyplot as plt
                import matplotlib as mpl
                
                # Set style
                plt.style.use('seaborn-v0_8-whitegrid')
                mpl.rcParams['figure.figsize'] = figure_size
                
                # 1. Reference Types Chart
                self.logger.info("Generating reference types chart")
                ref_types_file = os.path.join(output_dir, f"reference_types_chart.{viz_format}")
                
                fig, ax = plt.subplots()
                types_data = analysis_result["reference_types"]
                ax.bar(types_data.keys(), types_data.values(), color=plt.cm.get_cmap(color_scheme)(0.6))
                if include_titles:
                    ax.set_title("Distribution of Reference Types")
                ax.set_xlabel("Reference Type")
                ax.set_ylabel("Count")
                plt.tight_layout()
                plt.savefig(ref_types_file, dpi=dpi)
                plt.close()
                
                visualizations.append({
                    "name": "reference_types_chart",
                    "path": ref_types_file
                })
                
                # 2. Year Distribution Chart
                self.logger.info("Generating year distribution chart")
                year_dist_file = os.path.join(output_dir, f"year_distribution_chart.{viz_format}")
                
                fig, ax = plt.subplots()
                year_data = analysis_result["year_distribution"]
                ax.bar(year_data.keys(), year_data.values(), color=plt.cm.get_cmap(color_scheme)(0.4))
                if include_titles:
                    ax.set_title("Distribution of References by Year Range")
                ax.set_xlabel("Year Range")
                ax.set_ylabel("Count")
                plt.tight_layout()
                plt.savefig(year_dist_file, dpi=dpi)
                plt.close()
                
                visualizations.append({
                    "name": "year_distribution_chart",
                    "path": year_dist_file
                })
                
                # 3. Quality Metrics Chart
                self.logger.info("Generating quality metrics chart")
                quality_file = os.path.join(output_dir, f"quality_metrics_chart.{viz_format}")
                
                fig, ax = plt.subplots()
                quality_data = analysis_result["quality_metrics"]
                colors = {'high': 'green', 'medium': 'orange', 'low': 'red'}
                ax.bar(quality_data.keys(), quality_data.values(), color=[colors[k] for k in quality_data.keys()])
                if include_titles:
                    ax.set_title("Reference Quality Distribution")
                ax.set_xlabel("Quality Level")
                ax.set_ylabel("Count")
                plt.tight_layout()
                plt.savefig(quality_file, dpi=dpi)
                plt.close()
                
                visualizations.append({
                    "name": "quality_metrics_chart",
                    "path": quality_file
                })
                
            except ImportError as e:
                self.logger.warning(f"Could not generate visualizations: {str(e)}")
                self.logger.warning("Install matplotlib for visualization support")
            
            result = {
                "status": "success",
                "visualizations": visualizations,
                "analysis_result": analysis_result
            }
            
            log_execution_time(self.logger, start_time, "Visualization generation")
            log_result(self.logger, "generate_visualizations", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "generate_visualizations", e)
            return {"status": "error", "message": str(e)}
    
    def analyze_reference_quality(self, reference: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the quality of a reference.
        
        Args:
            reference: Reference text.
            metadata: Reference metadata.
            
        Returns:
            Dictionary containing quality analysis results.
        """
        log_method_call(self.logger, "analyze_reference_quality", reference_length=len(reference))
        
        try:
            # Calculate quality factors
            factors = {}
            
            # Source reliability factor
            venue = metadata.get('venue', '').lower()
            publisher = metadata.get('publisher', '').lower()
            
            reliable_sources = [
                'nature', 'science', 'cell', 'nejm', 'lancet', 'jama',
                'ieee', 'acm', 'springer', 'elsevier', 'wiley', 'oxford',
                'cambridge', 'harvard', 'mit', 'stanford'
            ]
            
            source_reliability = 0.5  # Default
            for source in reliable_sources:
                if source in venue or source in publisher:
                    source_reliability = 0.9
                    break
            
            factors['source_reliability'] = source_reliability
            
            # Citation count factor
            citation_count = metadata.get('citation_count', 0)
            if citation_count > 100:
                factors['citation_count'] = 0.9
            elif citation_count > 50:
                factors['citation_count'] = 0.8
            elif citation_count > 10:
                factors['citation_count'] = 0.7
            else:
                factors['citation_count'] = 0.5
            
            # Recency factor
            year = metadata.get('year', 0)
            current_year = 2024  # Hardcoded for example
            
            if year >= current_year - 2:
                factors['recency'] = 0.9
            elif year >= current_year - 5:
                factors['recency'] = 0.8
            elif year >= current_year - 10:
                factors['recency'] = 0.7
            elif year >= current_year - 20:
                factors['recency'] = 0.5
            else:
                factors['recency'] = 0.3
            
            # Completeness factor
            completeness = 0.5
            required_fields = ['authors', 'title', 'year']
            optional_fields = ['venue', 'volume', 'issue', 'pages', 'doi', 'url']
            
            required_count = sum(1 for field in required_fields if field in metadata and metadata[field])
            optional_count = sum(1 for field in optional_fields if field in metadata and metadata[field])
            
            if required_count == len(required_fields):
                completeness = 0.7 + (0.2 * optional_count / len(optional_fields))
            else:
                completeness = 0.5 * required_count / len(required_fields)
            
            factors['completeness'] = completeness
            
            # Calculate overall quality score
            weights = {
                'source_reliability': 0.3,
                'citation_count': 0.2,
                'recency': 0.2,
                'completeness': 0.3
            }
            
            quality_score = sum(factors[k] * weights[k] for k in factors)
            
            # Determine classification
            if quality_score >= self.quality_thresholds['high']:
                classification = 'high'
            elif quality_score >= self.quality_thresholds['medium']:
                classification = 'medium'
            else:
                classification = 'low'
            
            result = {
                "status": "success",
                "reference": reference[:50] + "..." if len(reference) > 50 else reference,
                "quality_score": quality_score,
                "factors": factors,
                "classification": classification
            }
            
            log_result(self.logger, "analyze_reference_quality", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "analyze_reference_quality", e)
            return {"status": "error", "message": str(e)}
    
    def compare_with_research_brief(self, references_file: str, research_brief_file: str) -> Dict[str, Any]:
        """
        Compare references with research brief to identify coverage and gaps.
        
        Args:
            references_file: Path to the references file (JSON).
            research_brief_file: Path to the research brief file.
            
        Returns:
            Dictionary containing comparison results.
        """
        log_method_call(self.logger, "compare_with_research_brief", 
                      references_file=references_file, 
                      research_brief_file=research_brief_file)
        start_time = time.time()
        
        try:
            # Check if files exist
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
                
            if not os.path.exists(research_brief_file):
                self.logger.error(f"Research brief file not found: {research_brief_file}")
                return {"status": "error", "message": f"Research brief file not found: {research_brief_file}"}
            
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            # Load research brief
            self.logger.info(f"Loading research brief from {research_brief_file}")
            with open(research_brief_file, 'r') as f:
                research_brief = f.read()
            
            # Extract topics from research brief
            self.logger.info("Extracting topics from research brief")
            topics = self._extract_topics_from_brief(research_brief)
            self.logger.info(f"Extracted topics: {topics}")
            
            # Calculate coverage for each topic
            self.logger.info("Calculating topic coverage")
            coverage = {}
            for topic in topics:
                coverage[topic] = self._calculate_topic_coverage(topic, references)
            
            # Identify gaps
            self.logger.info("Identifying coverage gaps")
            gaps = []
            for topic, score in coverage.items():
                if score < 0.7:  # Threshold for adequate coverage
                    gaps.append(topic)
            
            # Generate recommendations
            self.logger.info("Generating recommendations")
            recommendations = []
            for gap in gaps:
                recommendations.append(f"Consider adding references for {gap}")
            
            # Calculate overall alignment score
            alignment_score = sum(coverage.values()) / len(coverage) if coverage else 0
            
            result = {
                "status": "success",
                "alignment_score": alignment_score,
                "coverage": coverage,
                "gaps": gaps,
                "recommendations": recommendations
            }
            
            log_execution_time(self.logger, start_time, "Research brief comparison")
            log_result(self.logger, "compare_with_research_brief", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "compare_with_research_brief", e)
            return {"status": "error", "message": str(e)}
    
    def export_analysis_to_excel(self, references_file: str, output_file: str) -> Dict[str, Any]:
        """
        Export reference analysis to Excel format.
        
        Args:
            references_file: Path to the references file (JSON).
            output_file: Path to the output Excel file.
            
        Returns:
            Dictionary containing export results.
        """
        log_method_call(self.logger, "export_analysis_to_excel", 
                      references_file=references_file, 
                      output_file=output_file)
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            # Analyze references
            self.logger.info("Analyzing references")
            analysis_result = self.analyze_references(references_file)
            
            if analysis_result["status"] != "success":
                return analysis_result
            
            # Create Excel workbook
            self.logger.info("Creating Excel workbook")
            try:
                import pandas as pd
                
                # Create a writer for Excel
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    # Sheet 1: References
                    self.logger.info("Creating References sheet")
                    refs_df = pd.DataFrame(references)
                    refs_df.to_excel(writer, sheet_name='References', index=False)
                    
                    # Sheet 2: Analysis Summary
                    self.logger.info("Creating Analysis Summary sheet")
                    summary_data = {
                        'Metric': [
                            'Total References',
                            'Reference Types',
                            'Year Distribution',
                            'Quality Metrics'
                        ],
                        'Value': [
                            analysis_result['total_references'],
                            str(analysis_result['reference_types']),
                            str(analysis_result['year_distribution']),
                            str(analysis_result['quality_metrics'])
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Analysis Summary', index=False)
                    
                    # Sheet 3: Insights
                    self.logger.info("Creating Insights sheet")
                    insights_data = {
                        'Insight': analysis_result['insights']
                    }
                    insights_df = pd.DataFrame(insights_data)
                    insights_df.to_excel(writer, sheet_name='Insights', index=False)
                    
                    # Sheet 4: Reference Types
                    self.logger.info("Creating Reference Types sheet")
                    types_data = {
                        'Type': list(analysis_result['reference_types'].keys()),
                        'Count': list(analysis_result['reference_types'].values())
                    }
                    types_df = pd.DataFrame(types_data)
                    types_df.to_excel(writer, sheet_name='Reference Types', index=False)
                    
                    # Sheet 5: Year Distribution
                    self.logger.info("Creating Year Distribution sheet")
                    years_data = {
                        'Year Range': list(analysis_result['year_distribution'].keys()),
                        'Count': list(analysis_result['year_distribution'].values())
                    }
                    years_df = pd.DataFrame(years_data)
                    years_df.to_excel(writer, sheet_name='Year Distribution', index=False)
                    
                    # Sheet 6: Quality Metrics
                    self.logger.info("Creating Quality Metrics sheet")
                    quality_data = {
                        'Quality Level': list(analysis_result['quality_metrics'].keys()),
                        'Count': list(analysis_result['quality_metrics'].values())
                    }
                    quality_df = pd.DataFrame(quality_data)
                    quality_df.to_excel(writer, sheet_name='Quality Metrics', index=False)
                
            except ImportError as e:
                self.logger.error(f"Could not create Excel file: {str(e)}")
                self.logger.error("Install pandas and openpyxl for Excel support")
                return {"status": "error", "message": f"Could not create Excel file: {str(e)}"}
            
            result = {
                "status": "success",
                "file_path": output_file,
                "sheets": ['References', 'Analysis Summary', 'Insights', 
                          'Reference Types', 'Year Distribution', 'Quality Metrics']
            }
            
            log_execution_time(self.logger, start_time, "Excel export")
            log_result(self.logger, "export_analysis_to_excel", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "export_analysis_to_excel", e)
            return {"status": "error", "message": str(e)}
    
    # Private helper methods
    
    def _load_references(self, references_file: str) -> List[Dict[str, Any]]:
        """Load references from a file."""
        ext = os.path.splitext(references_file)[1].lower()
        
        if ext == '.json':
            with open(references_file, 'r') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                return data
            elif 'references' in data:
                return data['references']
            else:
                return list(data.values())
        elif ext == '.csv':
            try:
                df = pd.read_csv(references_file)
                return df.to_dict('records')
            except Exception as e:
                self.logger.error(f"Error loading CSV: {str(e)}")
                return []
        else:
            self.logger.error(f"Unsupported file format: {ext}")
            return []
    
    def _analyze_reference_types(self, references: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze reference types."""
        types = {}
        
        for ref in references:
            ref_type = ref.get('reference_type', 'unknown').lower()
            types[ref_type] = types.get(ref_type, 0) + 1
        
        return types
    
    def _analyze_year_distribution(self, references: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze year distribution."""
        years = {}
        
        # Define year ranges
        ranges = {
            '2020-2024': (2020, 2024),
            '2015-2019': (2015, 2019),
            '2010-2014': (2010, 2014),
            '2000-2009': (2000, 2009),
            'Pre-2000': (0, 1999)
        }
        
        # Initialize counts
        for range_name in ranges:
            years[range_name] = 0
        
        # Count references by year range
        for ref in references:
            year = ref.get('year', 0)
            if not year:
                continue
                
            for range_name, (start, end) in ranges.items():
                if start <= year <= end:
                    years[range_name] += 1
                    break
        
        return years
    
    def _analyze_quality_metrics(self, references: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze quality metrics."""
        quality = {'high': 0, 'medium': 0, 'low': 0}
        
        for ref in references:
            # Extract metadata
            metadata = {
                'year': ref.get('year', 0),
                'venue': ref.get('venue', ''),
                'publisher': ref.get('publisher', ''),
                'citation_count': ref.get('citation_count', 0),
                'authors': ref.get('authors', []),
                'title': ref.get('title', ''),
                'volume': ref.get('volume', ''),
                'issue': ref.get('issue', ''),
                'pages': ref.get('pages', ''),
                'doi': ref.get('doi', ''),
                'url': ref.get('url', '')
            }
            
            # Analyze quality
            result = self.analyze_reference_quality(ref.get('full_text', ''), metadata)
            
            if result['status'] == 'success':
                classification = result['classification']
                quality[classification] = quality.get(classification, 0) + 1
        
        return quality
    
    def _generate_insights(self, references: List[Dict[str, Any]], 
                         reference_types: Dict[str, int],
                         year_distribution: Dict[str, int],
                         quality_metrics: Dict[str, int]) -> List[str]:
        """Generate insights from analysis results."""
        insights = []
        
        # Insight on reference types
        total_refs = len(references)
        academic_types = ['journal', 'conference', 'book', 'thesis']
        academic_count = sum(reference_types.get(t, 0) for t in academic_types)
        academic_percentage = academic_count / total_refs * 100 if total_refs > 0 else 0
        
        insights.append(f"{academic_percentage:.0f}% of references are from academic sources")
        
        # Insight on recency
        recent_count = year_distribution.get('2020-2024', 0)
        recent_percentage = recent_count / total_refs * 100 if total_refs > 0 else 0
        
        insights.append(f"{recent_percentage:.0f}% of references are from the last 5 years")
        
        # Insight on quality
        high_quality_count = quality_metrics.get('high', 0)
        high_quality_percentage = high_quality_count / total_refs * 100 if total_refs > 0 else 0
        
        insights.append(f"{high_quality_percentage:.0f}% of references have high quality scores")
        
        # Additional insights
        if 'journal' in reference_types and reference_types['journal'] > 0:
            journal_percentage = reference_types['journal'] / total_refs * 100
            insights.append(f"Journal articles make up {journal_percentage:.0f}% of all references")
        
        if 'website' in reference_types and reference_types['website'] > 0:
            website_percentage = reference_types['website'] / total_refs * 100
            insights.append(f"Web sources make up {website_percentage:.0f}% of all references")
        
        return insights
    
    def _extract_topics_from_brief(self, research_brief: str) -> List[str]:
        """Extract research topics from brief."""
        # Simple extraction based on headings and keywords
        topics = []
        
        # Look for section titles
        lines = research_brief.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('##') and 'question' in line.lower():
                # This might be a research question section
                # Check the next few lines for questions
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip() and lines[j].strip()[0].isdigit():
                        # This looks like a numbered question
                        question = lines[j].strip()
                        # Extract the main topic
                        words = question.split()
                        if len(words) > 5:
                            # Take a few key words as the topic
                            topic = ' '.join(words[3:6])
                            topics.append(topic)
        
        # If no topics found from questions, try to extract from the text
        if not topics:
            # Look for keywords like "focus on", "analyze", "examine"
            keywords = ['focus on', 'analyze', 'examine', 'study', 'investigate', 'research']
            for keyword in keywords:
                if keyword in research_brief.lower():
                    # Find the sentence containing this keyword
                    start = research_brief.lower().find(keyword)
                    # Find the end of the sentence
                    end = research_brief.find('.', start)
                    if end > start:
                        sentence = research_brief[start:end]
                        # Extract a few words after the keyword as the topic
                        words = sentence.split()
                        keyword_index = -1
                        for i, word in enumerate(words):
                            if keyword in word.lower():
                                keyword_index = i
                                break
                        
                        if keyword_index >= 0 and keyword_index + 3 < len(words):
                            topic = ' '.join(words[keyword_index+1:keyword_index+4])
                            topics.append(topic)
        
        # If still no topics, use generic topics
        if not topics:
            topics = ['topic_1', 'topic_2', 'topic_3', 'topic_4']
        
        return topics
    
    def _calculate_topic_coverage(self, topic: str, references: List[Dict[str, Any]]) -> float:
        """Calculate coverage score for a topic."""
        # Simple keyword matching for demonstration
        topic_words = set(topic.lower().split())
        
        covered_refs = 0
        for ref in references:
            # Check title
            title = ref.get('title', '').lower()
            title_words = set(title.split())
            
            # Check if any topic word is in the title
            if any(word in title_words for word in topic_words):
                covered_refs += 1
                continue
            
            # Check full text if available
            full_text = ref.get('full_text', '').lower()
            if any(word in full_text for word in topic_words):
                covered_refs += 0.5  # Partial match
        
        # Calculate coverage score (0 to 1)
        coverage = min(1.0, covered_refs / (len(references) * 0.3)) if references else 0
        
        return coverage


# Example usage when run directly
if __name__ == "__main__":
    # Create agent
    agent = InsightAgent(verbose=True)
    
    # Process a file if provided
    if len(sys.argv) > 1:
        references_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
        
        print(f"Analyzing references: {references_file}")
        result = agent.analyze_references(references_file)
        
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Generate visualizations if output directory provided
        if len(sys.argv) > 2:
            print(f"Generating visualizations in: {output_dir}")
            viz_result = agent.generate_visualizations(references_file, output_dir)
            
            if viz_result["status"] == "success":
                print(f"Generated {len(viz_result['visualizations'])} visualizations")
                for viz in viz_result['visualizations']:
                    print(f"- {viz['name']}: {viz['path']}")
    else:
        print("Usage: python insight_agent.py <references_file> [output_dir]")
