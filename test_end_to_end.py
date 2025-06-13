#!/usr/bin/env python3
"""
End-to-end system test for Academic Research Automation System.

This script performs a comprehensive test of the entire system,
logging any errors or issues encountered during execution.
"""

import os
import sys
import time
import json
import yaml
import shutil
import logging
import argparse
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARAS modules
try:
    from aras.config_utils import load_config, get_config_value
    from aras.logging_utils import setup_test_run_logger, log_test_step, log_system_info
except ImportError:
    print("Failed to import ARAS modules. Make sure you're running from the project root directory.")
    sys.exit(1)

# Define paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"
EXAMPLES_DIR = BASE_DIR / "examples"
TEST_OUTPUT_DIR = BASE_DIR / "test_output"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

# Set up logger
logger = setup_test_run_logger("full_test_run.log")

def run_test(test_name: str, test_func, *args, **kwargs) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Run a test function and log the result.
    
    Args:
        test_name: Name of the test
        test_func: Test function to run
        *args: Arguments to pass to the test function
        **kwargs: Keyword arguments to pass to the test function
        
    Returns:
        Tuple of (success, details)
    """
    logger.info(f"Starting test: {test_name}")
    start_time = time.time()
    
    try:
        result = test_func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"Test {test_name} completed in {elapsed_time:.2f} seconds")
        log_test_step(logger, test_name, "PASS", {"elapsed_time": elapsed_time})
        return True, result
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "elapsed_time": elapsed_time
        }
        logger.error(f"Test {test_name} failed: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        log_test_step(logger, test_name, "FAIL", error_details)
        return False, error_details

def test_config_loading() -> Dict[str, Any]:
    """
    Test loading configuration from file.
    
    Returns:
        Loaded configuration
    """
    logger.info("Testing configuration loading")
    
    # Check if config file exists
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")
    
    # Load configuration
    config = load_config(str(CONFIG_FILE))
    
    # Validate essential configuration sections
    required_sections = ["paths", "logging", "agents", "output"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required configuration section: {section}")
    
    logger.info(f"Configuration loaded successfully with {len(config)} sections")
    return config

def test_file_router_agent(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test the file router agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Test results
    """
    logger.info("Testing file router agent")
    
    # Import file router agent
    from aras.file_router_agent import FileRouterAgent
    
    # Create agent
    agent = FileRouterAgent(config, verbose=True)
    
    # Test file detection with example files
    results = {}
    
    # Find example files
    example_files = list((EXAMPLES_DIR / "input").glob("*.*"))
    if not example_files:
        raise FileNotFoundError(f"No example files found in {EXAMPLES_DIR / 'input'}")
    
    # Test each file
    for file_path in example_files:
        logger.info(f"Testing file detection for {file_path.name}")
        result = agent.route_file(str(file_path))
        
        if result["status"] != "success":
            logger.warning(f"File routing failed for {file_path.name}: {result.get('message', 'Unknown error')}")
        
        results[file_path.name] = result
    
    logger.info(f"File router agent tested with {len(results)} files")
    return {"files_tested": len(results), "results": results}

def test_insight_agent(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test the insight agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Test results
    """
    logger.info("Testing insight agent")
    
    # Import insight agent
    from aras.insight_agent import InsightAgent
    
    # Create agent
    agent = InsightAgent(config, verbose=True)
    
    # Find reference file
    reference_files = list((EXAMPLES_DIR / "input").glob("*reference*.json"))
    if not reference_files:
        raise FileNotFoundError(f"No reference files found in {EXAMPLES_DIR / 'input'}")
    
    reference_file = reference_files[0]
    logger.info(f"Using reference file: {reference_file.name}")
    
    # Test reference analysis
    analysis_result = agent.analyze_references(str(reference_file))
    
    if analysis_result["status"] != "success":
        logger.warning(f"Reference analysis failed: {analysis_result.get('message', 'Unknown error')}")
    
    # Test visualization generation
    viz_output_dir = TEST_OUTPUT_DIR / "visualizations"
    viz_output_dir.mkdir(exist_ok=True)
    
    viz_result = agent.generate_visualizations(str(reference_file), str(viz_output_dir))
    
    if viz_result["status"] != "success":
        logger.warning(f"Visualization generation failed: {viz_result.get('message', 'Unknown error')}")
    
    # Test Excel export
    excel_output_file = TEST_OUTPUT_DIR / "reference_analysis.xlsx"
    
    try:
        excel_result = agent.export_analysis_to_excel(str(reference_file), str(excel_output_file))
        
        if excel_result["status"] != "success":
            logger.warning(f"Excel export failed: {excel_result.get('message', 'Unknown error')}")
    except Exception as e:
        logger.warning(f"Excel export failed: {str(e)}")
        excel_result = {"status": "error", "message": str(e)}
    
    logger.info("Insight agent testing completed")
    return {
        "analysis_result": analysis_result,
        "visualization_result": viz_result,
        "excel_result": excel_result
    }

def test_report_agent(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test the report agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Test results
    """
    logger.info("Testing report agent")
    
    # Import report agent
    from aras.report_agent import ReportAgent
    
    # Create agent
    agent = ReportAgent(config, verbose=True)
    
    # Find reference and brief files
    reference_files = list((EXAMPLES_DIR / "input").glob("*reference*.json"))
    brief_files = list((EXAMPLES_DIR / "input").glob("*brief*.md"))
    
    if not reference_files:
        raise FileNotFoundError(f"No reference files found in {EXAMPLES_DIR / 'input'}")
    
    if not brief_files:
        # Create a simple brief file
        brief_file = EXAMPLES_DIR / "input" / "test_brief.md"
        with open(brief_file, "w") as f:
            f.write("# Test Research Brief\n\nThis is a test research brief for the report agent.")
    else:
        brief_file = brief_files[0]
    
    reference_file = reference_files[0]
    logger.info(f"Using reference file: {reference_file.name}")
    logger.info(f"Using brief file: {brief_file.name}")
    
    # Test report generation
    report_output_dir = TEST_OUTPUT_DIR / "reports"
    report_output_dir.mkdir(exist_ok=True)
    
    report_result = agent.generate_report(
        str(reference_file),
        str(brief_file),
        str(report_output_dir),
        template="academic"
    )
    
    if report_result["status"] != "success":
        logger.warning(f"Report generation failed: {report_result.get('message', 'Unknown error')}")
        return {"report_result": report_result}
    
    # Test report formatting
    if report_result["status"] == "success" and "report_file" in report_result:
        format_result = agent.format_report(
            report_result["report_file"],
            output_formats=["md", "pdf", "docx"],
            output_dir=str(report_output_dir)
        )
        
        if format_result["status"] != "success":
            logger.warning(f"Report formatting failed: {format_result.get('message', 'Unknown error')}")
    else:
        format_result = {"status": "skipped", "message": "Report generation failed"}
    
    logger.info("Report agent testing completed")
    return {
        "report_result": report_result,
        "format_result": format_result
    }

def test_main_workflow(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test the main workflow.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Test results
    """
    logger.info("Testing main workflow")
    
    # Import main module
    sys.path.insert(0, str(BASE_DIR))
    from main import run_workflow
    
    # Find example files
    pdf_files = list((EXAMPLES_DIR / "input").glob("*.md"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF/MD files found in {EXAMPLES_DIR / 'input'}")
    
    pdf_file = pdf_files[0]
    logger.info(f"Using document file: {pdf_file.name}")
    
    # Test extraction workflow
    extract_output_dir = TEST_OUTPUT_DIR / "extract_workflow"
    extract_output_dir.mkdir(exist_ok=True)
    
    extract_result = run_workflow(
        workflow_type="extract",
        pdf_path=str(pdf_file),
        output_dir=str(extract_output_dir),
        config=config,
        verbose=True
    )
    
    if not extract_result or "status" not in extract_result or extract_result["status"] != "success":
        logger.warning(f"Extraction workflow failed: {extract_result.get('message', 'Unknown error')}")
    
    # Test full workflow if brief file exists
    brief_files = list((EXAMPLES_DIR / "input").glob("*brief*.md"))
    
    if brief_files:
        brief_file = brief_files[0]
        logger.info(f"Using brief file: {brief_file.name}")
        
        workflow_output_dir = TEST_OUTPUT_DIR / "full_workflow"
        workflow_output_dir.mkdir(exist_ok=True)
        
        workflow_result = run_workflow(
            workflow_type="workflow",
            pdf_path=str(pdf_file),
            brief_path=str(brief_file),
            output_dir=str(workflow_output_dir),
            config=config,
            verbose=True
        )
        
        if not workflow_result or "status" not in workflow_result or workflow_result["status"] != "success":
            logger.warning(f"Full workflow failed: {workflow_result.get('message', 'Unknown error')}")
    else:
        logger.warning("No brief file found, skipping full workflow test")
        workflow_result = {"status": "skipped", "message": "No brief file found"}
    
    logger.info("Main workflow testing completed")
    return {
        "extract_result": extract_result,
        "workflow_result": workflow_result
    }

def test_streamlit_app() -> Dict[str, Any]:
    """
    Test the Streamlit app.
    
    Returns:
        Test results
    """
    logger.info("Testing Streamlit app")
    
    # Check if Streamlit app exists
    streamlit_app = BASE_DIR / "streamlit_app.py"
    if not streamlit_app.exists():
        raise FileNotFoundError(f"Streamlit app not found: {streamlit_app}")
    
    # Check if Streamlit is installed
    try:
        import streamlit
        logger.info(f"Streamlit version: {streamlit.__version__}")
    except ImportError:
        logger.warning("Streamlit not installed, skipping app test")
        return {"status": "skipped", "message": "Streamlit not installed"}
    
    # Check app syntax
    try:
        with open(streamlit_app, "r") as f:
            app_code = f.read()
        
        compile(app_code, streamlit_app, "exec")
        logger.info("Streamlit app syntax check passed")
    except Exception as e:
        logger.error(f"Streamlit app syntax check failed: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    # We can't actually run the Streamlit app in a test environment,
    # but we can check for key components
    required_components = [
        "st.file_uploader",
        "st.sidebar",
        "st.tabs",
        "st.json",
        "st.markdown",
        "st.download_button"
    ]
    
    missing_components = []
    for component in required_components:
        if component not in app_code:
            missing_components.append(component)
    
    if missing_components:
        logger.warning(f"Streamlit app missing components: {missing_components}")
    else:
        logger.info("Streamlit app contains all required components")
    
    logger.info("Streamlit app testing completed")
    return {
        "status": "success" if not missing_components else "warning",
        "missing_components": missing_components
    }

def apply_fixes(test_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply fixes to issues found during testing.
    
    Args:
        test_results: Dictionary of test results
        
    Returns:
        Dictionary of applied fixes
    """
    logger.info("Analyzing test results for potential fixes")
    
    fixes_applied = {}
    
    # Check for missing directories
    required_dirs = ["logs", "temp", "examples/input", "examples/output"]
    for dir_path in required_dirs:
        full_path = BASE_DIR / dir_path
        if not full_path.exists():
            logger.info(f"Creating missing directory: {dir_path}")
            full_path.mkdir(parents=True, exist_ok=True)
            fixes_applied[f"create_dir_{dir_path}"] = True
    
    # Check for configuration issues
    if "config_test" in test_results and not test_results["config_test"][0]:
        logger.info("Attempting to fix configuration issues")
        
        # Create default config if missing
        if not CONFIG_FILE.exists():
            logger.info(f"Creating default configuration file: {CONFIG_FILE}")
            
            default_config = {
                "paths": {
                    "input_dir": "input",
                    "output_dir": "output",
                    "logs_dir": "logs",
                    "temp_dir": "temp",
                    "templates_dir": "templates"
                },
                "logging": {
                    "level": "INFO",
                    "console": True,
                    "file": True,
                    "filename": "research_agent.log",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "max_size": 5242880,
                    "backup_count": 3
                },
                "agents": {
                    "file_router_agent": True,
                    "insight_agent": True,
                    "report_agent": True,
                    "aras_integration": True,
                    "prea_integration": True
                },
                "output": {
                    "report_format": "md",
                    "generate_pdf": True,
                    "generate_docx": True,
                    "generate_excel": True,
                    "generate_visualizations": True,
                    "citation_style": "APA"
                }
            }
            
            CONFIG_DIR.mkdir(exist_ok=True)
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            fixes_applied["create_default_config"] = True
    
    # Check for example file issues
    example_input_dir = EXAMPLES_DIR / "input"
    if not example_input_dir.exists() or not list(example_input_dir.glob("*.*")):
        logger.info("Creating example input files")
        
        example_input_dir.mkdir(parents=True, exist_ok=True)
        
        # Create example research brief
        brief_file = example_input_dir / "research_brief.md"
        with open(brief_file, "w") as f:
            f.write("""# Research Analysis Brief

## Project Overview
This research project aims to analyze the impact of artificial intelligence on academic research methodologies.

## Research Questions
1. How has AI changed the way researchers conduct literature reviews?
2. What are the ethical considerations of using AI in academic research?
3. How can AI tools improve citation accuracy and reference management?

## Methodology
The research will involve a comprehensive analysis of recent publications, focusing on:
- AI applications in research
- Citation analysis
- Reference extraction techniques
- Ethical considerations

## Expected Outcomes
- Identification of key trends in AI-assisted research
- Recommendations for best practices in reference management
- Framework for ethical use of AI in academic contexts
""")
        
        # Create example reference list
        reference_file = example_input_dir / "reference_list.json"
        with open(reference_file, "w") as f:
            f.write("""[
  {
    "reference_number": 1,
    "full_text": "Leonardi, P. M., & Neeley, T. (2022). The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI. Harvard Business Review Press.",
    "authors": ["Leonardi, P. M.", "Neeley, T."],
    "title": "The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI",
    "year": 2022,
    "publisher": "Harvard Business Review Press",
    "reference_type": "book",
    "confidence_score": 0.95,
    "url": "https://www.harvard.com/book/9781647820107"
  },
  {
    "reference_number": 2,
    "full_text": "Beane, M. (2024). The skill code: Why some people are better at learning than others—and how to join them. HarperBusiness.",
    "authors": ["Beane, M."],
    "title": "The skill code: Why some people are better at learning than others—and how to join them",
    "year": 2024,
    "publisher": "HarperBusiness",
    "reference_type": "book",
    "confidence_score": 0.95
  },
  {
    "reference_number": 3,
    "full_text": "Phillips, N., & Lawrence, T. B. (2012). The turn to work in organization and management theory: Some implications for strategic organization. Strategic Organization, 10(3), 223-230.",
    "authors": ["Phillips, N.", "Lawrence, T. B."],
    "title": "The turn to work in organization and management theory: Some implications for strategic organization",
    "year": 2012,
    "venue": "Strategic Organization",
    "volume": "10",
    "issue": "3",
    "pages": "223-230",
    "reference_type": "journal",
    "confidence_score": 0.92,
    "doi": "10.1177/1476127012453109"
  }
]""")
        
        # Create example document
        document_file = example_input_dir / "sample_document.md"
        with open(document_file, "w") as f:
            f.write("""# Sample Document for Reference Extraction

## Introduction
This document contains several references that can be used to test the reference extraction capabilities of the Academic Research Automation System.

## Literature Review
According to Leonardi and Neeley (2022), developing a digital mindset is crucial for success in the modern workplace. This perspective is further supported by Beane (2024), who argues that learning ability is a key differentiator in technology-driven environments.

Phillips and Lawrence (2012) provide an organizational theory perspective that complements these views, particularly in how work practices evolve in response to technological change.

## Methodology
Our approach builds on established methodologies in the field (Santana & Parigi, 2021; Russell & Norvig, 2020).

## Results
The findings align with previous research on artificial intelligence applications (Brynjolfsson & McAfee, 2014) and business intelligence (Chen et al., 2012).

## Discussion
These results have significant implications for both theory and practice, as noted by Davenport and Ronanki (2018) in their analysis of real-world AI applications.

## Conclusion
In conclusion, the integration of AI technologies in research processes represents both an opportunity and a challenge (Provost & Fawcett, 2013).

## References
Beane, M. (2024). The skill code: Why some people are better at learning than others—and how to join them. HarperBusiness.

Brynjolfsson, E., & McAfee, A. (2014). The second machine age: Work, progress, and prosperity in a time of brilliant technologies. W. W. Norton & Company.

Chen, H., Chiang, R. H., & Storey, V. C. (2012). Business intelligence and analytics: From big data to big impact. MIS Quarterly, 36(4), 1165-1188.

Davenport, T. H., & Ronanki, R. (2018). Artificial intelligence for the real world. Harvard Business Review, 96(1), 108-116.

Leonardi, P. M., & Neeley, T. (2022). The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI. Harvard Business Review Press.

Phillips, N., & Lawrence, T. B. (2012). The turn to work in organization and management theory: Some implications for strategic organization. Strategic Organization, 10(3), 223-230.

Provost, F., & Fawcett, T. (2013). Data science for business: What you need to know about data mining and data-analytic thinking. O'Reilly Media.

Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.

Santana, J., & Parigi, P. (2021). Tuning in or turning off: The influence of visual cues in computer-mediated interactions. Social Science Computer Review, 39(5), 879-892.

Samaritan AI. (2023). Harmony Engine: Technical architecture and implementation guide. Internal Technical Documentation.
""")
        
        fixes_applied["create_example_files"] = True
    
    # Check for missing output examples
    example_output_dir = EXAMPLES_DIR / "output"
    if not example_output_dir.exists() or not list(example_output_dir.glob("*.*")):
        logger.info("Creating example output files")
        
        example_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy any test outputs as examples
        if TEST_OUTPUT_DIR.exists():
            for item in TEST_OUTPUT_DIR.glob("**/*"):
                if item.is_file():
                    rel_path = item.relative_to(TEST_OUTPUT_DIR)
                    target_path = example_output_dir / rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_path)
        
        fixes_applied["create_example_outputs"] = True
    
    logger.info(f"Applied {len(fixes_applied)} fixes")
    return fixes_applied

def main():
    """Main function for end-to-end system test."""
    parser = argparse.ArgumentParser(description="Run end-to-end system test")
    parser.add_argument("--fix", action="store_true", help="Automatically fix issues")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    logger.info("=== Academic Research Automation System: End-to-End Test ===")
    logger.info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Log system information
    log_system_info(logger)
    
    # Run tests
    test_results = {}
    
    # Test configuration loading
    test_results["config_test"] = run_test("Configuration Loading", test_config_loading)
    
    if test_results["config_test"][0]:
        config = test_results["config_test"][1]
        
        # Test file router agent
        test_results["file_router_test"] = run_test("File Router Agent", test_file_router_agent, config)
        
        # Test insight agent
        test_results["insight_agent_test"] = run_test("Insight Agent", test_insight_agent, config)
        
        # Test report agent
        test_results["report_agent_test"] = run_test("Report Agent", test_report_agent, config)
        
        # Test main workflow
        test_results["main_workflow_test"] = run_test("Main Workflow", test_main_workflow, config)
    else:
        logger.error("Configuration test failed, skipping agent tests")
    
    # Test Streamlit app
    test_results["streamlit_app_test"] = run_test("Streamlit App", test_streamlit_app)
    
    # Apply fixes if requested
    if args.fix:
        fixes = apply_fixes(test_results)
        test_results["fixes_applied"] = fixes
    
    # Summarize results
    logger.info("=== Test Summary ===")
    
    passed = sum(1 for result in test_results.values() if result[0])
    failed = len(test_results) - passed
    
    logger.info(f"Tests passed: {passed}")
    logger.info(f"Tests failed: {failed}")
    
    for test_name, (success, _) in test_results.items():
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name}: {status}")
    
    # Save test results
    results_file = LOGS_DIR / "test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "passed": passed,
            "failed": failed,
            "results": {k: {"success": v[0], "details": v[1]} for k, v in test_results.items()}
        }, f, indent=2, default=str)
    
    logger.info(f"Test results saved to {results_file}")
    logger.info(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return exit code
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
