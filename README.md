# Academic Research Automation System (ARAS)

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Updated](https://img.shields.io/badge/last%20updated-June%202024-orange.svg)

> A comprehensive multi-agent system for automating academic research workflows, citation management, and reference extraction.

## Overview

The Academic Research Automation System (ARAS) is an open-source, multi-agent framework designed to transform manual academic research workflows into efficient, automated processes. It combines two powerful subsystems:

1. **Academic Research Agent System (ARAS)**: Discovers, verifies, and manages academic publications and citations
2. **PDF Reference Extraction Agent (PREA)**: Extracts and processes references from PDF documents

Together, these systems provide a complete solution for academic researchers, librarians, publishers, and institutions to automate citation management, reference extraction, and research validation.

## 🔍 What Problems Does It Solve?

Academic research involves numerous manual, time-consuming tasks that are prone to errors:

- **Citation Verification**: Manually checking hundreds of citations for accuracy
- **Reference Extraction**: Tediously copying references from PDFs into structured formats
- **Publication Discovery**: Searching multiple databases for a researcher's complete works
- **Citation Formatting**: Converting between different citation styles (APA, MLA, Chicago)
- **Quality Assessment**: Evaluating the credibility and impact of cited sources

ARAS automates these processes with high accuracy, reducing hours of manual work to seconds while maintaining academic integrity.

## Agent Architecture

### Academic Research Agent System (ARAS)

ARAS employs a multi-agent architecture with specialized components:

#### 1. **Research Discovery Agent**
- **Primary Role**: Publication discovery and data collection
- **Capabilities**: 
  - Multi-database academic search (Google Scholar, Semantic Scholar, Crossref, DBLP, arXiv)
  - Intelligent deduplication of results
  - Comprehensive metadata extraction
  - Rate-limited processing to respect API terms

#### 2. **Source Verification Agent**
- **Primary Role**: Citation verification and quality assurance
- **Capabilities**:
  - URL accessibility checking
  - DOI validation
  - Metadata verification
  - Publisher validation
  - Quality scoring with confidence metrics

#### 3. **Citation Formatting Agent**
- **Primary Role**: Citation formatting and style standardization
- **Capabilities**:
  - Multi-style formatting (APA, MLA, Chicago, IEEE, Harvard)
  - Intelligent style detection
  - Consistency checking
  - Custom template creation

#### 4. **Orchestration Agent**
- **Primary Role**: System coordination and workflow management
- **Capabilities**:
  - Multi-agent workflow coordination
  - Resource allocation
  - Error handling
  - Progress monitoring

### PDF Reference Extraction Agent (PREA)

PREA employs specialized components for PDF processing:

#### 1. **PDF Text Extractor**
- **Primary Role**: PDF text extraction and content processing
- **Capabilities**:
  - Multi-method extraction (PDFPlumber, PyPDF2, OCR)
  - Automatic quality assessment
  - Large file handling
  - Error handling with graceful degradation

#### 2. **Reference Parser**
- **Primary Role**: Reference identification and metadata extraction
- **Capabilities**:
  - Multi-format citation recognition
  - Advanced pattern matching
  - Metadata standardization
  - Reference type classification
  - Confidence scoring

#### 3. **Reference Storage Manager**
- **Primary Role**: Data organization and multi-format output generation
- **Capabilities**:
  - Professional output generation (JSON, CSV, Excel, Text, Markdown)
  - Statistical analysis
  - Quality assessment reporting

#### 4. **PDF Reference Extraction Orchestrator**
- **Primary Role**: Workflow orchestration and system integration
- **Capabilities**:
  - End-to-end coordination
  - Component integration
  - Quality assurance
  - Batch processing
  - ARAS integration

## Sample Use Case: Research Paper Citation Analysis

A common workflow demonstrates the system's capabilities:

1. **Input**: A research paper PDF with 40+ citations
2. **Process**:
   - PREA extracts all references from the PDF
   - References are parsed and structured
   - ARAS verifies each citation for accuracy
   - System generates quality metrics and identifies potential errors
3. **Output**:
   - Structured reference data (JSON, CSV)
   - Professional Excel spreadsheet with analysis
   - Quality assessment report
   - Corrected citations in multiple formats

This process transforms hours of manual work into a 30-second automated workflow with higher accuracy.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Required libraries (see `requirements.txt`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/academic-research-automation-system.git
cd academic-research-automation-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Optional: Install PDF processing libraries if needed:
```bash
pip install PyPDF2 pdfplumber pdf2image pytesseract
```

4. Optional: Install spreadsheet libraries if needed:
```bash
pip install openpyxl pandas
```

## Usage

### Command Line Interface

The system provides a simple CLI for common operations:

```bash
# Process a single PDF and extract references
python main.py extract --pdf path/to/paper.pdf --output references_output

# Verify citations in a document
python main.py verify --references references.json --output verification_report

# Research a specific academic author
python main.py research --author "Jane Smith" --affiliation "Stanford University" --output smith_research

# Full workflow: Extract, verify, and analyze
python main.py workflow --pdf path/to/paper.pdf --output full_analysis
```

### Python API

For more advanced usage, import the modules directly:

```python
from academic_research_agent_system import AcademicResearchAgentSystem
from pdf_reference_extraction_agent import PDFReferenceExtractionAgent

# Initialize agents
aras = AcademicResearchAgentSystem()
prea = PDFReferenceExtractionAgent()

# Extract references from PDF
references = prea.extract_references_from_pdf("paper.pdf", "output_dir")

# Verify extracted references
verification = aras.validate_citations(references)

# Research an author
publications = aras.research_publications("Jane Smith", "Stanford University")
```

## Expected Results

The system generates multiple output files:

- **JSON files**: Structured data with complete metadata
- **CSV files**: Spreadsheet-compatible format for analysis
- **Excel workbooks**: Professional spreadsheets with formatting and summary sheets
- **Text reports**: Human-readable reports with detailed information
- **Markdown files**: Documentation-friendly format with tables

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Keywords

academic research, citation automation, reference extraction, PDF processing, multi-agent system, research tooling, workflow orchestration, academic integrity, data analysis, report generation
