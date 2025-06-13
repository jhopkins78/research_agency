#!/usr/bin/env python3
"""
Makefile alternative for Academic Research Automation System.

This script provides common development and testing operations
in a platform-independent way.
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

# Set base directories
BASE_DIR = Path(__file__).parent.absolute()
CONFIG_DIR = BASE_DIR / "config"
EXAMPLES_DIR = BASE_DIR / "examples"
LOGS_DIR = BASE_DIR / "logs"
TESTS_DIR = BASE_DIR / "tests"

# Create required directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)

# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def print_header():
    """Print header with project name."""
    print(f"{BLUE}======================================={NC}")
    print(f"{BLUE}  Academic Research Automation System  {NC}")
    print(f"{BLUE}======================================={NC}")
    print("")


def run_tests(args):
    """Run all tests."""
    print(f"{BLUE}Running all tests...{NC}")
    result = subprocess.run([sys.executable, "-m", "pytest", str(TESTS_DIR), "-v"])
    return result.returncode


def run_unit_tests(args):
    """Run unit tests only."""
    print(f"{BLUE}Running unit tests...{NC}")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(TESTS_DIR), "-v", "-k", "not integration"]
    )
    return result.returncode


def run_integration_tests(args):
    """Run integration tests only."""
    print(f"{BLUE}Running integration tests...{NC}")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(TESTS_DIR), "-v", "-k", "integration"]
    )
    return result.returncode


def run_example(args):
    """Run the system with example inputs."""
    print(f"{BLUE}Running example workflow...{NC}")
    
    # Ensure output directory exists
    output_dir = EXAMPLES_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Run the workflow
    cmd = [
        sys.executable, 
        "main.py", 
        "workflow",
        "--pdf", 
        str(EXAMPLES_DIR / "input" / "sample_document.md"),
        "--output", 
        str(output_dir / "full_analysis"),
        "--verbose"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"{GREEN}Example workflow completed successfully!{NC}")
        print(f"Output files are available in: {YELLOW}{output_dir / 'full_analysis'}{NC}")
    else:
        print(f"{RED}Example workflow failed!{NC}")
        print(f"Check the logs in: {YELLOW}{LOGS_DIR / 'research_agent.log'}{NC}")
    
    return result.returncode


def clean(args):
    """Clean output directories."""
    print(f"{BLUE}Cleaning output directories...{NC}")
    
    # Clean example outputs
    if (EXAMPLES_DIR / "output").exists():
        for item in (EXAMPLES_DIR / "output").iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    
    # Clean logs
    for log_file in LOGS_DIR.glob("*.log"):
        log_file.unlink()
    
    # Clean pytest cache
    if Path(".pytest_cache").exists():
        shutil.rmtree(".pytest_cache")
    if (TESTS_DIR / "__pycache__").exists():
        shutil.rmtree(TESTS_DIR / "__pycache__")
    if (TESTS_DIR / ".pytest_cache").exists():
        shutil.rmtree(TESTS_DIR / ".pytest_cache")
    
    # Clean Python cache files
    for pycache in Path(".").glob("**/__pycache__"):
        shutil.rmtree(pycache)
    for pyc in Path(".").glob("**/*.pyc"):
        pyc.unlink()
    
    print(f"{GREEN}Cleaned output directories and cache files.{NC}")
    return 0


def lint(args):
    """Run code linting."""
    print(f"{BLUE}Running code linting...{NC}")
    
    # Check if flake8 is installed
    try:
        import flake8
    except ImportError:
        print(f"{YELLOW}flake8 not found. Installing...{NC}")
        subprocess.run([sys.executable, "-m", "pip", "install", "flake8"])
    
    # Run flake8
    result = subprocess.run(
        [sys.executable, "-m", "flake8", str(BASE_DIR), "--exclude=venv,__pycache__,.pytest_cache"]
    )
    
    if result.returncode == 0:
        print(f"{GREEN}Linting passed!{NC}")
    else:
        print(f"{RED}Linting failed!{NC}")
    
    return result.returncode


def install_deps(args):
    """Install dependencies."""
    print(f"{BLUE}Installing dependencies...{NC}")
    
    # Install main dependencies
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )
    
    # Install development dependencies
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "pytest", "flake8", "black"]
    )
    
    print(f"{GREEN}Dependencies installed successfully!{NC}")
    return result.returncode


def main():
    """Main function."""
    print_header()
    
    parser = argparse.ArgumentParser(
        description="Academic Research Automation System Developer Utilities"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run all tests")
    test_parser.set_defaults(func=run_tests)
    
    # Unit test command
    unit_test_parser = subparsers.add_parser("test-unit", help="Run unit tests only")
    unit_test_parser.set_defaults(func=run_unit_tests)
    
    # Integration test command
    integration_test_parser = subparsers.add_parser("test-integration", help="Run integration tests only")
    integration_test_parser.set_defaults(func=run_integration_tests)
    
    # Run example command
    example_parser = subparsers.add_parser("run-example", help="Run the system with example inputs")
    example_parser.set_defaults(func=run_example)
    
    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean output directories")
    clean_parser.set_defaults(func=clean)
    
    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Run code linting")
    lint_parser.set_defaults(func=lint)
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install dependencies")
    install_parser.set_defaults(func=install_deps)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
