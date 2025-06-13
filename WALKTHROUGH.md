# Walkthrough: Academic Research Automation System

This walkthrough demonstrates how to use the Academic Research Automation System (ARAS) to automate common academic research tasks, including reference extraction, citation verification, and research analysis.

## Prerequisites

Before starting, ensure you have:

1. Installed all dependencies: `pip install -r requirements.txt`
2. Downloaded or prepared your research documents (PDFs, reference lists, etc.)

## Example Workflow

This walkthrough demonstrates a complete workflow using the sample files provided in the `examples/input` directory:

- `research_brief.md`: A research project brief outlining requirements
- `reference_list.json`: A list of academic references in JSON format
- `sample_document.md`: A sample document containing references for extraction

## Step 1: Extract References from a Document

The first step is to extract references from a document. In a real-world scenario, this would typically be a PDF file, but for demonstration purposes, we'll use the Markdown file.

### Command:

```bash
python main.py extract --pdf examples/input/sample_document.md --output examples/output/extracted_references
```

### Expected Output:

```
Successfully extracted 10 references
Output files saved to: examples/output/extracted_references
```

### Generated Files:

- `examples/output/extracted_references/references.json`: Structured reference data
- `examples/output/extracted_references/references.csv`: CSV format for spreadsheet analysis
- `examples/output/extracted_references/references.xlsx`: Excel workbook with formatting
- `examples/output/extracted_references/references.txt`: Human-readable text format

### Sample JSON Output:

```json
[
  {
    "reference_number": 1,
    "full_text": "Leonardi, P. M., & Neeley, T. (2022). The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI. Harvard Business Review Press.",
    "authors": ["Leonardi, P. M.", "Neeley, T."],
    "title": "The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI",
    "year": 2022,
    "publisher": "Harvard Business Review Press",
    "reference_type": "book",
    "confidence_score": 0.95
  },
  ...
]
```

## Step 2: Verify Citations for Accuracy

Next, we'll verify the extracted references for accuracy, checking for issues like incorrect years, publisher information, or DOIs.

### Command:

```bash
python main.py verify --references examples/output/extracted_references/references.json --output examples/output/verification_results
```

### Expected Output:

```
Citation verification complete
Valid citations: 8
Citations with issues: 2
Invalid citations: 0
Output files saved to: examples/output/verification_results
```

### Generated Files:

- `examples/output/verification_results/verification_results.json`: Detailed verification data
- `examples/output/verification_results/verification_summary.txt`: Human-readable summary

### Sample Verification Summary:

```
Citation Verification Summary
===========================

Total citations: 10
Valid citations: 8 (80.0%)
Citations with issues: 2 (20.0%)
Invalid citations: 0 (0.0%)

Citations with issues:

1. Beane, M. (2024). The skill code: Why some people are better at learning than others—and how to join them...
   Status: issues_found
   Issues: future_publication_year, url_missing

2. Samaritan AI. (2023). Harmony Engine: Technical architecture and implementation guide. Internal Technical Documentation...
   Status: issues_found
   Issues: unverifiable_source, limited_metadata
```

## Step 3: Research an Academic Author

Now, let's research publications by one of the authors mentioned in our research brief.

### Command:

```bash
python main.py research --author "Paul Leonardi" --affiliation "UC Santa Barbara" --output examples/output/author_research
```

### Expected Output:

```
Research complete: found 15 publications
Output files saved to: examples/output/author_research
```

### Generated Files:

- `examples/output/author_research/Paul_Leonardi_publications.json`: Publication data
- `examples/output/author_research/Paul_Leonardi_citations.txt`: Formatted citation list

### Sample Citations Output:

```
Publications by Paul Leonardi (UC Santa Barbara)
==================================================

1. Leonardi, P. M., & Neeley, T. (2022). The digital mindset: What it really takes to thrive in the age of data, algorithms, and AI. Harvard Business Review Press.

2. Leonardi, P. M. (2021). COVID-19 and the New Technologies of Organizing: Digital Exhaust, Digital Footprints, and Artificial Intelligence in the Wake of Remote Work. Journal of Management Studies, 58(1), 249-253.

3. Leonardi, P. M., & Treem, J. W. (2020). Behavioral visibility: A new paradigm for organization studies in the age of digitization, digitalization, and datafication. Organization Studies, 41(12), 1601-1625.

...
```

## Step 4: Execute a Complete Workflow

Finally, let's run a complete workflow that combines extraction, verification, and analysis.

### Command:

```bash
python main.py workflow --pdf examples/input/sample_document.md --output examples/output/full_analysis
```

### Expected Output:

```
Full workflow completed successfully in 5.23 seconds
References extracted: 10
Analysis report: examples/output/full_analysis/reference_analysis_report.md
All output files saved to: examples/output/full_analysis
```

### Generated Files:

- `examples/output/full_analysis/1_extracted_references/`: Extraction results
- `examples/output/full_analysis/2_verification_results/`: Verification results
- `examples/output/full_analysis/workflow_results.json`: Combined workflow data
- `examples/output/full_analysis/reference_analysis_report.md`: Comprehensive analysis report

### Sample Analysis Report:

The analysis report provides a comprehensive overview of the references, including:

- Summary statistics (total references, valid/invalid counts)
- Reference quality analysis table
- Specific recommendations for problematic references

## Advanced Usage

### Batch Processing

For processing multiple documents:

```bash
# Create a batch processing script
for file in documents/*.pdf; do
  python main.py workflow --pdf "$file" --output "results/$(basename "$file" .pdf)"
done
```

### Custom Configuration

For advanced users, you can modify the behavior of the system by editing the configuration settings in the Python API:

```python
from academic_research_agent_system import AcademicResearchAgentSystem
from pdf_reference_extraction_agent import PDFReferenceExtractionAgent

# Custom configuration
aras = AcademicResearchAgentSystem(
    verification_settings={
        "min_confidence_threshold": 0.7,
        "verification_timeout": 30
    }
)

prea = PDFReferenceExtractionAgent(
    extraction_settings={
        "preferred_method": "pdfplumber",
        "use_ocr_if_needed": True
    }
)

# Continue with custom-configured agents
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Error: `ModuleNotFoundError: No module named 'pdfplumber'`
   - Solution: Install PDF processing libraries: `pip install PyPDF2 pdfplumber pdf2image pytesseract`

2. **OCR Not Working**
   - Error: `pytesseract.pytesseract.TesseractNotFound`
   - Solution: Install Tesseract OCR on your system and ensure it's in your PATH

3. **Rate Limiting on Academic APIs**
   - Error: `APIRateLimitExceeded: Too many requests`
   - Solution: Add delays between requests or use the `--rate-limit` option

### Getting Help

If you encounter issues not covered here, please:

1. Check the logs in `aras_runner.log`
2. Consult the detailed documentation in the `docs/` directory
3. Open an issue on the GitHub repository

## Next Steps

Now that you've completed this walkthrough, you can:

1. Process your own research documents
2. Integrate the system into your academic workflow
3. Extend the system with custom components
4. Contribute to the open-source project

For more information, see the [README.md](../README.md) and the detailed agent guides in the `docs/` directory.
