#!/usr/bin/env python3
"""
Streamlit UI for Academic Research Automation System.

This module provides a web-based user interface for the Academic Research Automation System,
allowing users to upload files, select agents to run, configure options, and view results.
"""

import os
import sys
import json
import time
import yaml
import logging
import tempfile
import streamlit as st
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARAS modules
try:
    from aras.config_utils import load_config, get_config_value
    from aras.logging_utils import setup_logger
except ImportError:
    st.error("Failed to import ARAS modules. Make sure you're running from the project root directory.")
    st.stop()

# Set up page configuration
st.set_page_config(
    page_title="Academic Research Automation System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"
EXAMPLES_DIR = BASE_DIR / "examples"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Initialize session state
if "config" not in st.session_state:
    try:
        st.session_state.config = load_config(str(CONFIG_FILE))
    except Exception as e:
        st.error(f"Failed to load configuration: {str(e)}")
        st.session_state.config = {}

if "log_output" not in st.session_state:
    st.session_state.log_output = []

if "results" not in st.session_state:
    st.session_state.results = None

if "status" not in st.session_state:
    st.session_state.status = "idle"

if "error_log" not in st.session_state:
    st.session_state.error_log = []

# Set up logger
log_file = LOGS_DIR / "streamlit_app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("streamlit_app")

def run_workflow(uploaded_files, selected_agents, output_format, verbosity):
    """
    Run the selected workflow with the uploaded files.
    
    Args:
        uploaded_files: Dictionary of uploaded files by type
        selected_agents: List of selected agents to run
        output_format: Selected output format
        verbosity: Logging verbosity level
    
    Returns:
        Dictionary containing workflow results
    """
    st.session_state.status = "running"
    st.session_state.log_output = []
    st.session_state.error_log = []
    
    try:
        # Create temporary directory for workflow
        with tempfile.TemporaryDirectory(dir=TEMP_DIR) as temp_dir:
            temp_path = Path(temp_dir)
            input_dir = temp_path / "input"
            output_dir = temp_path / "output"
            
            input_dir.mkdir(exist_ok=True)
            output_dir.mkdir(exist_ok=True)
            
            # Save uploaded files to temporary directory
            file_paths = {}
            for file_type, file_obj in uploaded_files.items():
                if file_obj is not None:
                    file_path = input_dir / file_obj.name
                    with open(file_path, "wb") as f:
                        f.write(file_obj.getbuffer())
                    file_paths[file_type] = file_path
                    log_message(f"Saved {file_type} file: {file_path.name}")
            
            # Update configuration for this run
            run_config = st.session_state.config.copy()
            
            # Update agent activation based on selection
            for agent in ["file_router_agent", "insight_agent", "report_agent", "aras_integration", "prea_integration"]:
                run_config["agents"][agent] = agent in selected_agents
            
            # Update output format preferences
            run_config["output"]["report_format"] = output_format
            
            # Update logging level
            log_levels = {"Normal": "INFO", "Verbose": "DEBUG", "Minimal": "WARNING"}
            run_config["logging"]["level"] = log_levels.get(verbosity, "INFO")
            
            # Save temporary config
            config_path = temp_path / "config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(run_config, f)
            
            log_message(f"Configuration updated with selected options")
            
            # Import main module dynamically to avoid circular imports
            sys.path.insert(0, str(BASE_DIR))
            from main import run_workflow as main_run_workflow
            
            # Run the workflow
            log_message("Starting workflow execution")
            start_time = time.time()
            
            # Determine workflow type based on uploaded files
            if "pdf" in file_paths:
                workflow_type = "extract"
                log_message(f"Running extraction workflow on {file_paths['pdf'].name}")
                result = main_run_workflow(
                    workflow_type="extract",
                    pdf_path=str(file_paths["pdf"]),
                    output_dir=str(output_dir),
                    config=run_config,
                    verbose=(verbosity == "Verbose")
                )
            elif "references" in file_paths:
                workflow_type = "verify"
                log_message(f"Running verification workflow on {file_paths['references'].name}")
                result = main_run_workflow(
                    workflow_type="verify",
                    references_path=str(file_paths["references"]),
                    output_dir=str(output_dir),
                    config=run_config,
                    verbose=(verbosity == "Verbose")
                )
            elif "pdf" in file_paths and "brief" in file_paths:
                workflow_type = "workflow"
                log_message(f"Running full workflow with {file_paths['pdf'].name} and {file_paths['brief'].name}")
                result = main_run_workflow(
                    workflow_type="workflow",
                    pdf_path=str(file_paths["pdf"]),
                    brief_path=str(file_paths["brief"]),
                    output_dir=str(output_dir),
                    config=run_config,
                    verbose=(verbosity == "Verbose")
                )
            else:
                raise ValueError("Insufficient files uploaded for any workflow")
            
            elapsed_time = time.time() - start_time
            log_message(f"Workflow completed in {elapsed_time:.2f} seconds")
            
            # Copy results from temporary directory to a more permanent location
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = TEMP_DIR / f"results_{timestamp}"
            results_dir.mkdir(exist_ok=True)
            
            import shutil
            for item in output_dir.iterdir():
                if item.is_dir():
                    shutil.copytree(item, results_dir / item.name)
                else:
                    shutil.copy2(item, results_dir / item.name)
            
            log_message(f"Results saved to {results_dir}")
            
            # Return results
            return {
                "status": "success",
                "workflow_type": workflow_type,
                "results_dir": results_dir,
                "elapsed_time": elapsed_time,
                "output_files": list(results_dir.glob("**/*")),
                "result": result
            }
    
    except Exception as e:
        logger.exception("Error running workflow")
        log_message(f"Error: {str(e)}", level="ERROR")
        st.session_state.error_log.append({
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "traceback": sys.exc_info()
        })
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        st.session_state.status = "idle"

def log_message(message, level="INFO"):
    """
    Log a message to both the logger and the session state.
    
    Args:
        message: Message to log
        level: Log level (INFO, WARNING, ERROR, DEBUG)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{timestamp} - {level} - {message}"
    
    if level == "ERROR":
        logger.error(message)
        st.session_state.log_output.append({"level": "error", "message": log_entry})
    elif level == "WARNING":
        logger.warning(message)
        st.session_state.log_output.append({"level": "warning", "message": log_entry})
    elif level == "DEBUG":
        logger.debug(message)
        st.session_state.log_output.append({"level": "debug", "message": log_entry})
    else:
        logger.info(message)
        st.session_state.log_output.append({"level": "info", "message": log_entry})

def display_markdown_file(file_path):
    """
    Display a markdown file in the Streamlit UI.
    
    Args:
        file_path: Path to the markdown file
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
        st.markdown(content)
    except Exception as e:
        st.error(f"Error displaying markdown file: {str(e)}")

def display_json_file(file_path):
    """
    Display a JSON file in the Streamlit UI.
    
    Args:
        file_path: Path to the JSON file
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        st.json(data)
    except Exception as e:
        st.error(f"Error displaying JSON file: {str(e)}")

def display_csv_file(file_path):
    """
    Display a CSV file in the Streamlit UI.
    
    Args:
        file_path: Path to the CSV file
    """
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error displaying CSV file: {str(e)}")

def display_log_file(file_path):
    """
    Display a log file in the Streamlit UI.
    
    Args:
        file_path: Path to the log file
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
        st.text(content)
    except Exception as e:
        st.error(f"Error displaying log file: {str(e)}")

def main():
    """Main function for the Streamlit app."""
    # Display header
    st.title("📚 Academic Research Automation System")
    st.markdown("""
    This interface allows you to interact with the Academic Research Automation System,
    upload research documents, run analysis workflows, and view results.
    """)
    
    # Sidebar for configuration
    st.sidebar.title("Configuration")
    
    # File upload section
    st.sidebar.header("1. Upload Files")
    
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF or Document", type=["pdf", "md", "docx", "txt"])
    uploaded_references = st.sidebar.file_uploader("Upload References (JSON)", type=["json"])
    uploaded_brief = st.sidebar.file_uploader("Upload Research Brief", type=["md", "txt"])
    
    # Agent selection
    st.sidebar.header("2. Select Agents")
    
    file_router = st.sidebar.checkbox("File Router Agent", value=True)
    insight_agent = st.sidebar.checkbox("Insight Agent", value=True)
    report_agent = st.sidebar.checkbox("Report Agent", value=True)
    aras_integration = st.sidebar.checkbox("ARAS Integration", value=True)
    prea_integration = st.sidebar.checkbox("PREA Integration", value=True)
    
    selected_agents = []
    if file_router:
        selected_agents.append("file_router_agent")
    if insight_agent:
        selected_agents.append("insight_agent")
    if report_agent:
        selected_agents.append("report_agent")
    if aras_integration:
        selected_agents.append("aras_integration")
    if prea_integration:
        selected_agents.append("prea_integration")
    
    # Output format
    st.sidebar.header("3. Output Format")
    
    output_format = st.sidebar.selectbox(
        "Report Format",
        options=["md", "pdf", "docx"],
        index=0
    )
    
    # Verbosity
    verbosity = st.sidebar.selectbox(
        "Logging Verbosity",
        options=["Minimal", "Normal", "Verbose"],
        index=1
    )
    
    # Run button
    run_button = st.sidebar.button("Run Workflow")
    
    # Example data option
    use_example_data = st.sidebar.checkbox("Use Example Data")
    
    if use_example_data:
        st.sidebar.info("""
        Using example data from the examples directory.
        This will override any uploaded files.
        """)
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Workflow", "Results", "Logs", "Configuration"])
    
    with tab1:
        st.header("Workflow")
        
        # Display workflow status
        if st.session_state.status == "running":
            st.info("Workflow is running... Please wait.")
            progress_bar = st.progress(0)
            for i in range(100):
                # Simulating progress
                time.sleep(0.01)
                progress_bar.progress(i + 1)
        
        # Display workflow options based on uploaded files
        if uploaded_pdf and not uploaded_references and not uploaded_brief:
            st.info("Workflow: Extract references from document")
        elif uploaded_references and not uploaded_pdf:
            st.info("Workflow: Verify and analyze references")
        elif uploaded_pdf and uploaded_brief:
            st.info("Workflow: Complete research workflow")
        elif use_example_data:
            st.info("Workflow: Using example data")
        else:
            st.warning("Please upload files to determine workflow")
        
        # Display selected agents
        st.subheader("Selected Agents")
        for agent in selected_agents:
            st.write(f"- {agent.replace('_', ' ').title()}")
        
        # Display example data if selected
        if use_example_data:
            st.subheader("Example Data")
            example_files = list((EXAMPLES_DIR / "input").glob("*"))
            for file in example_files:
                st.write(f"- {file.name}")
    
    with tab2:
        st.header("Results")
        
        if st.session_state.results:
            results = st.session_state.results
            
            if results["status"] == "success":
                st.success(f"Workflow completed in {results['elapsed_time']:.2f} seconds")
                
                # Display results based on file type
                st.subheader("Output Files")
                
                # Group files by type
                output_files = {}
                for file_path in results["output_files"]:
                    file_type = file_path.suffix.lower()
                    if file_type not in output_files:
                        output_files[file_type] = []
                    output_files[file_type].append(file_path)
                
                # Create tabs for different file types
                if output_files:
                    file_tabs = st.tabs([f"{k} files ({len(v)})" for k, v in output_files.items()])
                    
                    for i, (file_type, files) in enumerate(output_files.items()):
                        with file_tabs[i]:
                            for file_path in files:
                                st.write(f"**{file_path.name}**")
                                
                                # Display file content based on type
                                if file_type == ".md":
                                    with st.expander("View Content"):
                                        display_markdown_file(file_path)
                                elif file_type == ".json":
                                    with st.expander("View Content"):
                                        display_json_file(file_path)
                                elif file_type == ".csv":
                                    with st.expander("View Content"):
                                        display_csv_file(file_path)
                                elif file_type == ".log":
                                    with st.expander("View Content"):
                                        display_log_file(file_path)
                                
                                # Download button
                                with open(file_path, "rb") as f:
                                    st.download_button(
                                        label=f"Download {file_path.name}",
                                        data=f,
                                        file_name=file_path.name,
                                        mime="application/octet-stream"
                                    )
            else:
                st.error(f"Workflow failed: {results.get('error', 'Unknown error')}")
        else:
            st.info("Run a workflow to see results here")
    
    with tab3:
        st.header("Logs")
        
        # Display real-time logs
        for log in st.session_state.log_output:
            if log["level"] == "error":
                st.error(log["message"])
            elif log["level"] == "warning":
                st.warning(log["message"])
            elif log["level"] == "debug":
                st.text(log["message"])
            else:
                st.info(log["message"])
        
        # Display error log if any
        if st.session_state.error_log:
            st.subheader("Error Details")
            for error in st.session_state.error_log:
                st.error(f"Error at {error['timestamp']}: {error['error']}")
                with st.expander("View Traceback"):
                    st.code(error["traceback"])
    
    with tab4:
        st.header("Configuration")
        
        # Display current configuration
        st.json(st.session_state.config)
    
    # Handle run button click
    if run_button:
        # Check if files are uploaded or example data is selected
        if use_example_data:
            # Use example data
            example_files = {}
            
            # Find example files
            pdf_files = list((EXAMPLES_DIR / "input").glob("*.md"))
            if pdf_files:
                with open(pdf_files[0], "rb") as f:
                    example_files["pdf"] = type('obj', (object,), {
                        'name': pdf_files[0].name,
                        'getbuffer': lambda: f.read()
                    })
            
            json_files = list((EXAMPLES_DIR / "input").glob("*.json"))
            if json_files:
                with open(json_files[0], "rb") as f:
                    example_files["references"] = type('obj', (object,), {
                        'name': json_files[0].name,
                        'getbuffer': lambda: f.read()
                    })
            
            brief_files = list((EXAMPLES_DIR / "input").glob("*brief*.md"))
            if brief_files:
                with open(brief_files[0], "rb") as f:
                    example_files["brief"] = type('obj', (object,), {
                        'name': brief_files[0].name,
                        'getbuffer': lambda: f.read()
                    })
            
            # Run workflow with example data
            st.session_state.results = run_workflow(
                example_files, selected_agents, output_format, verbosity
            )
            
        elif uploaded_pdf or uploaded_references:
            # Use uploaded files
            uploaded_files = {}
            
            if uploaded_pdf:
                uploaded_files["pdf"] = uploaded_pdf
            
            if uploaded_references:
                uploaded_files["references"] = uploaded_references
            
            if uploaded_brief:
                uploaded_files["brief"] = uploaded_brief
            
            # Run workflow with uploaded files
            st.session_state.results = run_workflow(
                uploaded_files, selected_agents, output_format, verbosity
            )
        else:
            st.error("Please upload files or select 'Use Example Data'")

if __name__ == "__main__":
    main()
