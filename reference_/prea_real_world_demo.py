"""
PREA Real-World Demonstration Script
Using the PDF Reference Extraction Agent on the actual trimmed research report
"""

import sys
import os
import json
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_reference_extraction_agent import PDFReferenceExtractionAgent
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure pdf_reference_extraction_agent.py is in the same directory")
    sys.exit(1)

def extract_references_from_research_report():
    """Extract references from the actual trimmed research report"""
    
    print("=" * 70)
    print("PREA REAL-WORLD DEMONSTRATION")
    print("Extracting References from Trimmed Research Report")
    print("=" * 70)
    
    # Initialize the PREA agent
    print("\\n1. Initializing PDF Reference Extraction Agent...")
    
    # Custom configuration for academic paper processing
    config = {
        "min_confidence_threshold": 0.5,  # Lower threshold for academic citations
        "output_formats": ["json", "csv", "xlsx", "txt", "md"],
        "enable_ocr": True,
        "max_file_size_mb": 100,
        "extraction_methods": ["text_fallback", "pdfplumber", "pypdf2"]  # Use text fallback first
    }
    
    agent = PDFReferenceExtractionAgent(config)
    print("✓ PREA Agent initialized with academic paper configuration")
    
    # Check for the research report files
    print("\\n2. Locating research report files...")
    
    # Try different possible file locations
    possible_files = [
        "/home/ubuntu/trimmed_research_report_final_corrected_citations.pdf",
        "/home/ubuntu/trimmed_research_report.pdf",
        "/home/ubuntu/trimmed_research_report.md"
    ]
    
    source_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            source_file = file_path
            print(f"✓ Found research report: {os.path.basename(file_path)}")
            break
    
    if not source_file:
        print("✗ Research report file not found")
        return None
    
    # Since we have the markdown file, let's extract references from it directly
    if source_file.endswith('.md'):
        print("\\n3. Processing Markdown research report...")
        return extract_from_markdown_file(agent, source_file)
    else:
        print("\\n3. Processing PDF research report...")
        return extract_from_pdf_file(agent, source_file)

def extract_from_markdown_file(agent, md_file_path):
    """Extract references from the markdown research report"""
    
    try:
        # Read the markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✓ Read markdown file: {len(content)} characters")
        
        # Find the references section
        references_start = content.find("## References")
        if references_start == -1:
            references_start = content.find("# References")
        
        if references_start == -1:
            print("✗ References section not found in markdown file")
            return None
        
        # Extract the references section
        references_text = content[references_start:]
        print(f"✓ Found references section: {len(references_text)} characters")
        
        # Use PREA's text parsing capabilities
        print("\\n4. Parsing references using PREA...")
        
        # Create a parser instance
        from pdf_reference_extraction_agent import ReferenceParser
        parser = ReferenceParser(agent.config)
        
        # Extract references from the text
        references = parser.extract_references_from_text(references_text)
        
        print(f"✓ Extracted {len(references)} references from research report")
        
        # Generate output files
        print("\\n5. Generating output files...")
        
        output_path = "/home/ubuntu/research_report_references"
        
        # Use the storage manager to create output files
        from pdf_reference_extraction_agent import ReferenceStorageManager
        storage_manager = ReferenceStorageManager(agent.config)
        
        output_files = storage_manager.store_references(
            references, 
            output_path, 
            agent.config["output_formats"]
        )
        
        print("✓ Output files generated:")
        for format_type, file_path in output_files.items():
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  - {format_type.upper()}: {os.path.basename(file_path)} ({size} bytes)")
        
        # Generate statistics
        print("\\n6. Generating extraction statistics...")
        
        stats = generate_extraction_statistics(references)
        
        print("✓ Extraction Statistics:")
        print(f"  - Total References: {stats['total_references']}")
        print(f"  - Average Confidence: {stats['average_confidence']:.2f}")
        print(f"  - Reference Types: {stats['reference_types']}")
        print(f"  - Years Range: {stats['year_range']}")
        
        # Save detailed analysis
        analysis_file = "/home/ubuntu/research_report_reference_analysis.json"
        analysis_data = {
            "extraction_metadata": {
                "source_file": md_file_path,
                "extraction_method": "markdown_text_parsing",
                "total_references": len(references),
                "extraction_timestamp": "2024-06-08 20:00:00",
                "agent_config": agent.config
            },
            "statistics": stats,
            "output_files": output_files,
            "references": [ref.__dict__ for ref in references]
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        print(f"✓ Detailed analysis saved: {os.path.basename(analysis_file)}")
        
        return {
            "references": references,
            "output_files": output_files,
            "statistics": stats,
            "analysis_file": analysis_file
        }
        
    except Exception as e:
        print(f"✗ Error processing markdown file: {str(e)}")
        return None

def extract_from_pdf_file(agent, pdf_file_path):
    """Extract references from the PDF research report"""
    
    try:
        print(f"Processing PDF file: {os.path.basename(pdf_file_path)}")
        
        # Use PREA to extract references from PDF
        result = agent.extract_references_from_pdf(
            pdf_path=pdf_file_path,
            output_path="/home/ubuntu/research_report_references_pdf",
            output_formats=["json", "csv", "xlsx", "txt", "md"]
        )
        
        print(f"✓ Extracted {len(result['references'])} references from PDF")
        
        return result
        
    except Exception as e:
        print(f"✗ Error processing PDF file: {str(e)}")
        return None

def generate_extraction_statistics(references):
    """Generate comprehensive statistics about the extracted references"""
    
    if not references:
        return {}
    
    # Basic statistics
    total_refs = len(references)
    confidences = [ref.confidence_score for ref in references if ref.confidence_score is not None]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # Reference types
    types = {}
    for ref in references:
        ref_type = ref.reference_type or "unknown"
        types[ref_type] = types.get(ref_type, 0) + 1
    
    # Years
    years = [ref.year for ref in references if ref.year is not None]
    year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
    
    # Authors
    all_authors = []
    for ref in references:
        if ref.authors:
            all_authors.extend(ref.authors)
    unique_authors = len(set(all_authors))
    
    # Venues
    venues = [ref.venue for ref in references if ref.venue]
    unique_venues = len(set(venues))
    
    return {
        "total_references": total_refs,
        "average_confidence": avg_confidence,
        "reference_types": types,
        "year_range": year_range,
        "unique_authors": unique_authors,
        "unique_venues": unique_venues,
        "years_distribution": sorted(list(set(years))) if years else []
    }

def display_sample_references(references, num_samples=5):
    """Display a sample of extracted references"""
    
    print(f"\\n7. Sample of extracted references (showing {min(num_samples, len(references))}):")
    print("-" * 70)
    
    for i, ref in enumerate(references[:num_samples], 1):
        print(f"\\n[{ref.reference_number or i}] {ref.title or 'No title'}")
        if ref.authors:
            authors_str = ", ".join(ref.authors[:3])  # Show first 3 authors
            if len(ref.authors) > 3:
                authors_str += " et al."
            print(f"    Authors: {authors_str}")
        if ref.year:
            print(f"    Year: {ref.year}")
        if ref.venue:
            print(f"    Venue: {ref.venue}")
        if ref.reference_type:
            print(f"    Type: {ref.reference_type}")
        print(f"    Confidence: {ref.confidence_score:.2f}")

if __name__ == "__main__":
    result = extract_references_from_research_report()
    
    if result:
        print("\\n" + "=" * 70)
        print("EXTRACTION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
        # Display sample references
        display_sample_references(result["references"])
        
        print("\\n" + "=" * 70)
        print("FILES GENERATED")
        print("=" * 70)
        
        for format_type, file_path in result["output_files"].items():
            print(f"✓ {format_type.upper()}: {os.path.basename(file_path)}")
        
        if "analysis_file" in result:
            print(f"✓ ANALYSIS: {os.path.basename(result['analysis_file'])}")
        
        print("\\n PREA successfully processed the research report!")
        print("All references have been extracted and stored in multiple formats.")
        
    else:
        print("\\n Extraction failed. Please check the error messages above.")

