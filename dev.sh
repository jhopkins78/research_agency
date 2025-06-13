#!/bin/bash
# Academic Research Automation System (ARAS) Developer Utilities
# This script provides common development and testing operations

# Set the base directory to the script's location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$BASE_DIR/config"
EXAMPLES_DIR="$BASE_DIR/examples"
LOGS_DIR="$BASE_DIR/logs"
TESTS_DIR="$BASE_DIR/tests"

# Create required directories if they don't exist
mkdir -p "$LOGS_DIR"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
print_header() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}  Academic Research Automation System  ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo ""
}

# Print usage information
print_usage() {
    echo -e "Usage: ${YELLOW}./dev.sh${NC} ${GREEN}<command>${NC}"
    echo ""
    echo -e "Available commands:"
    echo -e "  ${GREEN}test${NC}              Run all tests"
    echo -e "  ${GREEN}test-unit${NC}         Run unit tests only"
    echo -e "  ${GREEN}test-integration${NC}  Run integration tests only"
    echo -e "  ${GREEN}run-example${NC}       Run the system with example inputs"
    echo -e "  ${GREEN}clean${NC}             Clean output directories"
    echo -e "  ${GREEN}lint${NC}              Run code linting"
    echo -e "  ${GREEN}install${NC}           Install dependencies"
    echo -e "  ${GREEN}help${NC}              Show this help message"
    echo ""
}

# Run all tests
run_tests() {
    echo -e "${BLUE}Running all tests...${NC}"
    python -m pytest "$TESTS_DIR" -v
}

# Run unit tests only
run_unit_tests() {
    echo -e "${BLUE}Running unit tests...${NC}"
    python -m pytest "$TESTS_DIR" -v -k "not integration"
}

# Run integration tests only
run_integration_tests() {
    echo -e "${BLUE}Running integration tests...${NC}"
    python -m pytest "$TESTS_DIR" -v -k "integration"
}

# Run the system with example inputs
run_example() {
    echo -e "${BLUE}Running example workflow...${NC}"
    
    # Ensure output directory exists
    mkdir -p "$EXAMPLES_DIR/output"
    
    # Run the workflow
    python main.py workflow \
        --pdf "$EXAMPLES_DIR/input/sample_document.md" \
        --output "$EXAMPLES_DIR/output/full_analysis" \
        --verbose
        
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Example workflow completed successfully!${NC}"
        echo -e "Output files are available in: ${YELLOW}$EXAMPLES_DIR/output/full_analysis${NC}"
    else
        echo -e "${RED}Example workflow failed!${NC}"
        echo -e "Check the logs in: ${YELLOW}$LOGS_DIR/research_agent.log${NC}"
    fi
}

# Clean output directories
clean() {
    echo -e "${BLUE}Cleaning output directories...${NC}"
    
    # Clean example outputs
    rm -rf "$EXAMPLES_DIR/output"/*
    mkdir -p "$EXAMPLES_DIR/output"
    
    # Clean logs
    rm -f "$LOGS_DIR"/*.log
    
    # Clean pytest cache
    rm -rf .pytest_cache
    rm -rf "$TESTS_DIR"/__pycache__
    rm -rf "$TESTS_DIR"/.pytest_cache
    
    # Clean Python cache files
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    
    echo -e "${GREEN}Cleaned output directories and cache files.${NC}"
}

# Run code linting
lint() {
    echo -e "${BLUE}Running code linting...${NC}"
    
    # Check if flake8 is installed
    if ! command -v flake8 &> /dev/null; then
        echo -e "${YELLOW}flake8 not found. Installing...${NC}"
        pip install flake8
    fi
    
    # Run flake8
    flake8 "$BASE_DIR" --exclude=venv,__pycache__,.pytest_cache
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Linting passed!${NC}"
    else
        echo -e "${RED}Linting failed!${NC}"
    fi
}

# Install dependencies
install_deps() {
    echo -e "${BLUE}Installing dependencies...${NC}"
    pip install -r requirements.txt
    
    # Install development dependencies
    pip install pytest flake8 black
    
    echo -e "${GREEN}Dependencies installed successfully!${NC}"
}

# Main function
main() {
    print_header
    
    # Check if a command was provided
    if [ $# -eq 0 ]; then
        print_usage
        exit 1
    fi
    
    # Process command
    case "$1" in
        test)
            run_tests
            ;;
        test-unit)
            run_unit_tests
            ;;
        test-integration)
            run_integration_tests
            ;;
        run-example)
            run_example
            ;;
        clean)
            clean
            ;;
        lint)
            lint
            ;;
        install)
            install_deps
            ;;
        help)
            print_usage
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
