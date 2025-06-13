"""
Test configuration for pytest.
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define fixtures that can be reused across tests
@pytest.fixture
def sample_document_path():
    """Return path to sample document for testing."""
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_document.md')

@pytest.fixture
def sample_reference_list_path():
    """Return path to sample reference list for testing."""
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'reference_list.json')

@pytest.fixture
def sample_research_brief_path():
    """Return path to sample research brief for testing."""
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'research_brief.md')

@pytest.fixture
def temp_output_dir(tmpdir):
    """Create a temporary directory for test outputs."""
    output_dir = tmpdir.mkdir("test_output")
    return str(output_dir)
