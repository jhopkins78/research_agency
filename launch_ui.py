#!/usr/bin/env python3
"""
Streamlit app launcher with dependency check.

This script checks for required dependencies before launching the Streamlit app,
ensuring a smooth user experience.
"""

import os
import sys
import subprocess
import importlib.util
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("launcher")

# Required packages for the Streamlit app
REQUIRED_PACKAGES = [
    "streamlit",
    "pandas",
    "numpy",
    "matplotlib",
    "pyyaml",
    "plotly",
    "openpyxl"
]

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            logger.info("All dependencies installed successfully!")
        except subprocess.CalledProcessError:
            logger.error("Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    return True

def launch_streamlit():
    """Launch the Streamlit app."""
    # Get the directory of this script
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    streamlit_app = script_dir / "streamlit_app.py"
    
    if not streamlit_app.exists():
        logger.error(f"Streamlit app not found: {streamlit_app}")
        return False
    
    logger.info(f"Launching Streamlit app: {streamlit_app}")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(streamlit_app)], check=True)
        return True
    except subprocess.CalledProcessError:
        logger.error("Failed to launch Streamlit app")
        return False

if __name__ == "__main__":
    logger.info("Starting Academic Research Automation System UI")
    
    if check_dependencies():
        launch_streamlit()
    else:
        logger.error("Dependency check failed. Please install required packages and try again.")
        sys.exit(1)
