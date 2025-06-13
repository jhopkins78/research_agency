"""
Report Agent implementation with structured logging integration.

This module provides functionality for generating and formatting reports.
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
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from aras.logging_utils import (
        setup_logger, 
        log_execution_time, 
        log_method_call, 
        log_result, 
        log_exception
    )
    from aras.config_utils import load_config, get_config_value

class ReportAgent:
    """
    Report Agent for generating and formatting reports.
    
    This agent combines analysis results, references, and research briefs
    to generate comprehensive reports in various formats.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, verbose: bool = False):
        """
        Initialize the Report Agent.
        
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
                    "paths": {"output_dir": "output", "logs_dir": "logs"},
                    "logging": {"level": "INFO", "console": True, "file": True}
                }
        else:
            self.config = config
            
        # Set up logger
        self.logger = setup_logger("ARAS", self.config, verbose, "ReportAgent")
        self.logger.info("Report Agent initialized")
        
        # Initialize report settings from config
        self.default_template = get_config_value(self.config, "report.template", "academic")
        self.default_sections = get_config_value(
            self.config, 
            "report.sections", 
            ["executive_summary", "introduction", "analysis", "conclusion", "references"]
        )
        
        self.logger.debug(f"Default report template: {self.default_template}")
        self.logger.debug(f"Default report sections: {self.default_sections}")
    
    def generate_report(self, references_file: str, research_brief_file: str, 
                        output_dir: str, template: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a report based on references, research brief, and template.
        
        Args:
            references_file: Path to the references file (JSON).
            research_brief_file: Path to the research brief file.
            output_dir: Directory to store the generated report.
            template: Report template to use (e.g., "academic", "business").
            
        Returns:
            Dictionary containing report generation results.
        """
        log_method_call(self.logger, "generate_report", 
                      references_file=references_file, 
                      research_brief_file=research_brief_file,
                      output_dir=output_dir,
                      template=template)
        start_time = time.time()
        
        try:
            # Check if files exist
            if not os.path.exists(references_file):
                self.logger.error(f"References file not found: {references_file}")
                return {"status": "error", "message": f"References file not found: {references_file}"}
                
            if not os.path.exists(research_brief_file):
                self.logger.error(f"Research brief file not found: {research_brief_file}")
                return {"status": "error", "message": f"Research brief file not found: {research_brief_file}"}
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            # Load research brief
            self.logger.info(f"Loading research brief from {research_brief_file}")
            with open(research_brief_file, "r") as f:
                research_brief = f.read()
            
            # Select template
            report_template = template or self.default_template
            self.logger.info(f"Using report template: {report_template}")
            
            # Generate report content
            self.logger.info("Generating report content")
            report_content = self._generate_report_content(
                references, research_brief, report_template
            )
            
            # Save report file
            report_file = os.path.join(output_dir, f"report_{report_template}.md")
            self.logger.info(f"Saving report to {report_file}")
            with open(report_file, "w") as f:
                f.write(report_content)
            
            result = {
                "status": "success",
                "report_file": report_file,
                "template_used": report_template,
                "sections": self.default_sections, # Placeholder, actual sections depend on template
                "word_count": len(report_content.split()),
                "reference_count": len(references)
            }
            
            log_execution_time(self.logger, start_time, "Report generation")
            log_result(self.logger, "generate_report", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "generate_report", e)
            return {"status": "error", "message": str(e)}
    
    def format_report(self, report_file: str, output_formats: List[str], 
                      output_dir: str) -> Dict[str, Any]:
        """
        Format a report into multiple output formats (e.g., PDF, DOCX).
        
        Args:
            report_file: Path to the input report file (Markdown).
            output_formats: List of output formats to generate (e.g., ["pdf", "docx"]).
            output_dir: Directory to store formatted reports.
            
        Returns:
            Dictionary containing formatting results.
        """
        log_method_call(self.logger, "format_report", 
                      report_file=report_file, 
                      output_formats=output_formats,
                      output_dir=output_dir)
        start_time = time.time()
        
        try:
            # Check if report file exists
            if not os.path.exists(report_file):
                self.logger.error(f"Report file not found: {report_file}")
                return {"status": "error", "message": f"Report file not found: {report_file}"}
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Get formatting settings from config
            generate_pdf = get_config_value(self.config, "output.generate_pdf", True)
            generate_docx = get_config_value(self.config, "output.generate_docx", True)
            
            self.logger.debug(f"Formatting settings: generate_pdf={generate_pdf}, generate_docx={generate_docx}")
            
            # Format report
            self.logger.info(f"Formatting report: {report_file}")
            output_files = []
            
            # Copy Markdown file
            if "md" in output_formats:
                md_output_file = os.path.join(output_dir, os.path.basename(report_file))
                # Fix: Check if source and destination are the same file
                if os.path.abspath(report_file) != os.path.abspath(md_output_file):
                    self.logger.info(f"Copying Markdown report to {md_output_file}")
                    import shutil
                    shutil.copy(report_file, md_output_file)
                    output_files.append(md_output_file)
                else:
                    self.logger.info(f"Markdown report already at destination: {md_output_file}")
                    output_files.append(md_output_file)
            
            # Generate PDF if requested and enabled
            if "pdf" in output_formats and generate_pdf:
                pdf_output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(report_file))[0] + ".pdf")
                self.logger.info(f"Generating PDF report: {pdf_output_file}")
                try:
                    import subprocess
                    subprocess.run(["manus-md-to-pdf", report_file, pdf_output_file], check=True)
                    output_files.append(pdf_output_file)
                except Exception as e:
                    self.logger.warning(f"Failed to generate PDF report: {str(e)}")
            
            # Generate DOCX if requested and enabled
            if "docx" in output_formats and generate_docx:
                docx_output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(report_file))[0] + ".docx")
                self.logger.info(f"Generating DOCX report: {docx_output_file}")
                try:
                    import pypandoc
                    pypandoc.convert_file(report_file, "docx", outputfile=docx_output_file)
                    output_files.append(docx_output_file)
                except Exception as e:
                    self.logger.warning(f"Failed to generate DOCX report: {str(e)}")
                    self.logger.warning("Install pypandoc and pandoc for DOCX support")
            
            result = {
                "status": "success",
                "input_report": report_file,
                "output_formats": output_formats,
                "output_files": output_files
            }
            
            log_execution_time(self.logger, start_time, "Report formatting")
            log_result(self.logger, "format_report", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "format_report", e)
            return {"status": "error", "message": str(e)}
    
    def generate_executive_summary(self, references_file: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an executive summary for the report.
        
        Args:
            references_file: Path to the references file (JSON).
            analysis_results: Dictionary containing analysis results.
            
        Returns:
            Dictionary containing executive summary results.
        """
        log_method_call(self.logger, "generate_executive_summary", 
                      references_file=references_file, 
                      analysis_results_keys=list(analysis_results.keys()))
        start_time = time.time()
        
        try:
            # Get summary settings from config
            max_words = get_config_value(self.config, "report.executive_summary_max_words", 250)
            
            self.logger.info(f"Generating executive summary (max words: {max_words})")
            
            # Simulate summary generation
            summary = f"This executive summary provides an overview of the research analysis. "
            # FIX: Corrected f-string syntax by using single quotes inside the f-string
            summary += f"A total of {analysis_results.get('total_references', 0)} references were analyzed. "
            
            # Check if insights are available
            if "insights" in analysis_results and analysis_results["insights"]:
                insights = analysis_results["insights"][:2]
                insights_text = ", ".join(insights)
                summary += f"Key insights include: {insights_text}. "
            else:
                summary += "No specific insights were identified. "
                
            summary += f"The analysis indicates a strong focus on recent publications. "
            
            # Trim to max words
            summary_words = summary.split()
            if len(summary_words) > max_words:
                summary = " ".join(summary_words[:max_words]) + "..."
            
            key_points = [
                f"Total references analyzed: {analysis_results.get('total_references', 0)}",
            ]
            
            # Add insights if available
            if "insights" in analysis_results and analysis_results["insights"]:
                for insight in analysis_results["insights"][:3]:
                    key_points.append(f"Key insight: {insight}")
            else:
                key_points.append("No specific insights identified")
                
            key_points.append("Focus on recent publications")
            
            result = {
                "status": "success",
                "summary": summary,
                "word_count": len(summary.split()),
                "key_points": key_points
            }
            
            log_execution_time(self.logger, start_time, "Executive summary generation")
            log_result(self.logger, "generate_executive_summary", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "generate_executive_summary", e)
            return {"status": "error", "message": str(e)}
    
    def generate_reference_section(self, references_file: str) -> Dict[str, Any]:
        """
        Generate the reference section for the report.
        
        Args:
            references_file: Path to the references file (JSON).
            
        Returns:
            Dictionary containing reference section results.
        """
        log_method_call(self.logger, "generate_reference_section", references_file=references_file)
        start_time = time.time()
        
        try:
            # Load references
            self.logger.info(f"Loading references from {references_file}")
            references = self._load_references(references_file)
            
            if not references:
                self.logger.error("No references found in file")
                return {"status": "error", "message": "No references found in file"}
            
            # Get citation style from config
            citation_style = get_config_value(self.config, "output.citation_style", "APA")
            self.logger.info(f"Generating reference section (style: {citation_style})")
            
            # Simulate reference section generation
            reference_section = f"# References ({citation_style} Style)\n\n"
            for i, ref in enumerate(references):
                reference_section += f"{i+1}. {ref.get('full_text', 'N/A')}\n"
            
            result = {
                "status": "success",
                "reference_section": reference_section,
                "reference_count": len(references),
                "citation_style": citation_style
            }
            
            log_execution_time(self.logger, start_time, "Reference section generation")
            log_result(self.logger, "generate_reference_section", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "generate_reference_section", e)
            return {"status": "error", "message": str(e)}
    
    def add_visualizations_to_report(self, report_file: str, visualizations: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Add visualizations to the report.
        
        Args:
            report_file: Path to the report file (Markdown).
            visualizations: List of visualization dictionaries (name, path).
            
        Returns:
            Dictionary containing results.
        """
        log_method_call(self.logger, "add_visualizations_to_report", 
                      report_file=report_file, 
                      visualization_count=len(visualizations))
        start_time = time.time()
        
        try:
            # Check if report file exists
            if not os.path.exists(report_file):
                self.logger.error(f"Report file not found: {report_file}")
                return {"status": "error", "message": f"Report file not found: {report_file}"}
            
            self.logger.info(f"Adding {len(visualizations)} visualizations to report: {report_file}")
            
            # Simulate adding visualizations to Markdown
            with open(report_file, "a") as f:
                f.write("\n\n## Visualizations\n\n")
                for viz in visualizations:
                    f.write(f"### {viz.get('name', 'Visualization')}\n")
                    f.write(f"![{viz.get('name', 'Visualization')}]({viz.get('path', '')})\n\n")
            
            result = {
                "status": "success",
                "updated_report": report_file,
                "added_visualizations": len(visualizations)
            }
            
            log_execution_time(self.logger, start_time, "Adding visualizations to report")
            log_result(self.logger, "add_visualizations_to_report", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "add_visualizations_to_report", e)
            return {"status": "error", "message": str(e)}
    
    def validate_report_structure(self, report_file: str, expected_sections: List[str]) -> Dict[str, Any]:
        """
        Validate the structure of the report.
        
        Args:
            report_file: Path to the report file (Markdown).
            expected_sections: List of expected section titles.
            
        Returns:
            Dictionary containing validation results.
        """
        log_method_call(self.logger, "validate_report_structure", 
                      report_file=report_file, 
                      expected_sections=expected_sections)
        start_time = time.time()
        
        try:
            # Check if report file exists
            if not os.path.exists(report_file):
                self.logger.error(f"Report file not found: {report_file}")
                return {"status": "error", "message": f"Report file not found: {report_file}"}
            
            self.logger.info(f"Validating report structure: {report_file}")
            
            # Simulate structure validation
            with open(report_file, "r") as f:
                content = f.read()
            
            missing_sections = []
            for section in expected_sections:
                if f"## {section.replace('_', ' ').title()}" not in content and \
                   f"# {section.replace('_', ' ').title()}" not in content:
                    missing_sections.append(section)
            
            is_valid = len(missing_sections) == 0
            structure_score = (len(expected_sections) - len(missing_sections)) / len(expected_sections) if expected_sections else 1.0
            
            result = {
                "status": "success",
                "is_valid": is_valid,
                "missing_sections": missing_sections,
                "structure_score": structure_score
            }
            
            log_execution_time(self.logger, start_time, "Report structure validation")
            log_result(self.logger, "validate_report_structure", result)
            return result
            
        except Exception as e:
            log_exception(self.logger, "validate_report_structure", e)
            return {"status": "error", "message": str(e)}
    
    # Private helper methods
    
    def _load_references(self, references_file: str) -> List[Dict[str, Any]]:
        """Load references from a file."""
        ext = os.path.splitext(references_file)[1].lower()
        
        if ext == ".json":
            with open(references_file, "r") as f:
                data = json.load(f)
                
            if isinstance(data, list):
                return data
            elif "references" in data:
                return data["references"]
            else:
                return list(data.values())
        else:
            self.logger.error(f"Unsupported file format for references: {ext}")
            return []
    
    def _generate_report_content(self, references: List[Dict[str, Any]], 
                                 research_brief: str, template: str) -> str:
        """Generate report content based on template."""
        self.logger.info(f"Generating content for template: {template}")
        
        # Simulate content generation based on template
        content = f"# Research Report ({template.title()})\n\n"
        
        # Add research brief summary
        content += "## Introduction\n\n"
        content += "Based on the research brief:\n"
        content += f"> {research_brief[:200]}...\n\n"
        
        # Add analysis section
        content += "## Analysis\n\n"
        content += f"The analysis involved {len(references)} references. Key findings include...\n\n"
        
        # Add reference section
        content += "## References\n\n"
        for i, ref in enumerate(references):
            content += f"{i+1}. {ref.get('full_text', 'N/A')}\n"
            
        content += "\n## Conclusion\n\nThis report summarizes the findings...\n"
        
        return content


# Example usage when run directly
if __name__ == "__main__":
    # Create agent
    agent = ReportAgent(verbose=True)
    
    # Process a file if provided
    if len(sys.argv) > 3:
        references_file = sys.argv[1]
        research_brief_file = sys.argv[2]
        output_dir = sys.argv[3]
        
        print(f"Generating report from: {references_file} and {research_brief_file}")
        result = agent.generate_report(references_file, research_brief_file, output_dir)
        
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Format report if generated successfully
        if result["status"] == "success" and result.get("report_file"):
            print(f"Formatting report: {result['report_file']}")
            format_result = agent.format_report(
                result["report_file"],
                output_formats=["pdf", "docx"],
                output_dir=output_dir
            )
            print(f"Formatting Result: {json.dumps(format_result, indent=2)}")
    else:
        print("Usage: python report_agent.py <references_file> <research_brief_file> <output_dir>")
