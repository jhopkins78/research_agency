#!/usr/bin/env python3
"""
Academic Research Automation System (ARAS) - Main Runner Script

This script provides a command-line interface for the Academic Research Automation System,
integrating both the Academic Research Agent System (ARAS) and PDF Reference Extraction
Agent (PREA) components into unified workflows.

Usage:
    python main.py extract --pdf path/to/paper.pdf --output references_output
    python main.py verify --references references.json --output verification_report
    python main.py research --author "Jane Smith" --affiliation "Stanford" --output smith_research
    python main.py workflow --pdf path/to/paper.pdf --output full_analysis

Author: Manus AI
Created: 2024
"""

import argparse
import json
import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union, Any

# Import core system components
try:
    from academic_research_agent_system import AcademicResearchAgentSystem
    from pdf_reference_extraction_agent import PDFReferenceExtractionAgent
except ImportError:
    print("Error: Required modules not found. Please ensure you've installed all dependencies.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("aras_runner.log")
    ]
)
logger = logging.getLogger("ARAS-Runner")

class AcademicResearchAutomationSystem:
    """Main orchestration class for the Academic Research Automation System"""
    
    def __init__(self, verbose: bool = False):
        """Initialize the automation system with both ARAS and PREA components
        
        Args:
            verbose: Whether to enable verbose logging
        """
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            
        logger.info("Initializing Academic Research Automation System")
        
        # Initialize component systems
        try:
            self.aras = AcademicResearchAgentSystem()
            logger.info("Academic Research Agent System (ARAS) initialized")
        except Exception as e:
            logger.error(f"Failed to initialize ARAS: {str(e)}")
            self.aras = None
            
        try:
            self.prea = PDFReferenceExtractionAgent()
            logger.info("PDF Reference Extraction Agent (PREA) initialized")
        except Exception as e:
            logger.error(f"Failed to initialize PREA: {str(e)}")
            self.prea = None
    
    def extract_references(self, pdf_path: str, output_path: str, 
                          formats: List[str] = None, use_ocr: bool = False) -> Dict[str, Any]:
        """Extract references from a PDF document
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Directory to store output files
            formats: List of output formats (default: ["json", "csv", "xlsx"])
            use_ocr: Whether to use OCR for text extraction if needed
            
        Returns:
            Dictionary containing extraction results
        """
        if self.prea is None:
            logger.error("PREA component not available")
            return {"status": "error", "message": "PREA component not available"}
            
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return {"status": "error", "message": f"PDF file not found: {pdf_path}"}
            
        if formats is None:
            formats = ["json", "csv", "xlsx"]
            
        logger.info(f"Extracting references from {pdf_path}")
        start_time = time.time()
        
        try:
            result = self.prea.extract_references_from_pdf(
                pdf_path=pdf_path,
                output_path=output_path,
                output_formats=formats,
                use_ocr_if_needed=use_ocr
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Extraction completed in {elapsed_time:.2f} seconds")
            logger.info(f"Found {len(result['references'])} references")
            
            return result
        except Exception as e:
            logger.error(f"Reference extraction failed: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def verify_citations(self, citations_source: Union[str, List[str]], 
                        output_path: str) -> Dict[str, Any]:
        """Verify citations for accuracy and completeness
        
        Args:
            citations_source: Either a file path (JSON, CSV, TXT) or a list of citation strings
            output_path: Directory to store verification results
            
        Returns:
            Dictionary containing verification results
        """
        if self.aras is None:
            logger.error("ARAS component not available")
            return {"status": "error", "message": "ARAS component not available"}
            
        logger.info("Starting citation verification")
        start_time = time.time()
        
        # Load citations if a file path is provided
        citations = citations_source
        if isinstance(citations_source, str):
            if not os.path.exists(citations_source):
                logger.error(f"Citations file not found: {citations_source}")
                return {"status": "error", "message": f"Citations file not found: {citations_source}"}
                
            try:
                ext = os.path.splitext(citations_source)[1].lower()
                if ext == '.json':
                    with open(citations_source, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            citations = data
                        elif 'references' in data:
                            citations = data['references']
                        else:
                            citations = [item['full_text'] for item in data.values() 
                                        if 'full_text' in item]
                elif ext == '.csv':
                    import csv
                    with open(citations_source, 'r') as f:
                        reader = csv.reader(f)
                        # Skip header
                        next(reader, None)
                        citations = [row[0] for row in reader if row]
                else:  # Assume text file with one citation per line
                    with open(citations_source, 'r') as f:
                        citations = [line.strip() for line in f if line.strip()]
            except Exception as e:
                logger.error(f"Failed to load citations: {str(e)}")
                return {"status": "error", "message": f"Failed to load citations: {str(e)}"}
        
        try:
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Verify citations
            verification_results = self.aras.validate_citations(citations)
            
            # Save results
            output_file = os.path.join(output_path, "verification_results.json")
            with open(output_file, 'w') as f:
                json.dump(verification_results, f, indent=2)
                
            # Generate summary report
            summary_file = os.path.join(output_path, "verification_summary.txt")
            with open(summary_file, 'w') as f:
                f.write("Citation Verification Summary\n")
                f.write("===========================\n\n")
                f.write(f"Total citations: {len(verification_results)}\n")
                
                valid_count = sum(1 for r in verification_results if r['status'] == 'valid')
                issues_count = sum(1 for r in verification_results if r['status'] == 'issues_found')
                invalid_count = sum(1 for r in verification_results if r['status'] == 'invalid')
                
                f.write(f"Valid citations: {valid_count} ({valid_count/len(verification_results)*100:.1f}%)\n")
                f.write(f"Citations with issues: {issues_count} ({issues_count/len(verification_results)*100:.1f}%)\n")
                f.write(f"Invalid citations: {invalid_count} ({invalid_count/len(verification_results)*100:.1f}%)\n\n")
                
                if issues_count + invalid_count > 0:
                    f.write("Citations with issues:\n")
                    for i, result in enumerate(verification_results):
                        if result['status'] != 'valid':
                            f.write(f"\n{i+1}. {result['citation'][:80]}...\n")
                            f.write(f"   Status: {result['status']}\n")
                            f.write(f"   Issues: {', '.join(result['issues'])}\n")
            
            elapsed_time = time.time() - start_time
            logger.info(f"Verification completed in {elapsed_time:.2f} seconds")
            
            return {
                "status": "success",
                "output_files": [output_file, summary_file],
                "valid_count": valid_count,
                "issues_count": issues_count,
                "invalid_count": invalid_count
            }
        except Exception as e:
            logger.error(f"Citation verification failed: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def research_author(self, author_name: str, affiliation: Optional[str] = None,
                      start_year: Optional[int] = None, end_year: Optional[int] = None,
                      output_path: str = None) -> Dict[str, Any]:
        """Research publications by an academic author
        
        Args:
            author_name: Name of the author to research
            affiliation: Optional affiliation to narrow results
            start_year: Optional start year for publication range
            end_year: Optional end year for publication range
            output_path: Directory to store research results
            
        Returns:
            Dictionary containing research results
        """
        if self.aras is None:
            logger.error("ARAS component not available")
            return {"status": "error", "message": "ARAS component not available"}
            
        logger.info(f"Researching publications for author: {author_name}")
        start_time = time.time()
        
        try:
            # Research publications
            publications = self.aras.research_publications(
                researcher_name=author_name,
                affiliation=affiliation,
                start_year=start_year,
                end_year=end_year
            )
            
            if output_path:
                # Ensure output directory exists
                os.makedirs(output_path, exist_ok=True)
                
                # Save results as JSON
                output_file = os.path.join(output_path, f"{author_name.replace(' ', '_')}_publications.json")
                with open(output_file, 'w') as f:
                    json.dump(publications, f, indent=2)
                    
                # Generate formatted citation list
                citations_file = os.path.join(output_path, f"{author_name.replace(' ', '_')}_citations.txt")
                with open(citations_file, 'w') as f:
                    f.write(f"Publications by {author_name}")
                    if affiliation:
                        f.write(f" ({affiliation})")
                    f.write("\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, pub in enumerate(publications):
                        f.write(f"{i+1}. {pub['formatted_citation']}\n\n")
            
            elapsed_time = time.time() - start_time
            logger.info(f"Research completed in {elapsed_time:.2f} seconds")
            logger.info(f"Found {len(publications)} publications")
            
            return {
                "status": "success",
                "publications": publications,
                "output_files": [output_file, citations_file] if output_path else None
            }
        except Exception as e:
            logger.error(f"Author research failed: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def execute_full_workflow(self, pdf_path: str, output_path: str) -> Dict[str, Any]:
        """Execute a complete workflow: extract references, verify them, and generate analysis
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Directory to store all output files
            
        Returns:
            Dictionary containing workflow results
        """
        if self.prea is None or self.aras is None:
            logger.error("Both PREA and ARAS components are required for full workflow")
            return {"status": "error", "message": "Required components not available"}
            
        logger.info(f"Starting full workflow for {pdf_path}")
        start_time = time.time()
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Step 1: Extract references
        logger.info("Step 1: Extracting references")
        extract_dir = os.path.join(output_path, "1_extracted_references")
        os.makedirs(extract_dir, exist_ok=True)
        
        extraction_result = self.extract_references(
            pdf_path=pdf_path,
            output_path=extract_dir,
            formats=["json", "csv", "xlsx", "txt"]
        )
        
        if extraction_result["status"] != "success":
            logger.error(f"Workflow failed at extraction step: {extraction_result.get('message', 'Unknown error')}")
            return {"status": "error", "step": "extraction", "message": extraction_result.get('message')}
            
        # Step 2: Verify citations
        logger.info("Step 2: Verifying citations")
        verify_dir = os.path.join(output_path, "2_verification_results")
        os.makedirs(verify_dir, exist_ok=True)
        
        # Get references from extraction result
        references = [ref.get('full_text', '') for ref in extraction_result.get('references', [])]
        
        verification_result = self.verify_citations(
            citations_source=references,
            output_path=verify_dir
        )
        
        if verification_result["status"] != "success":
            logger.error(f"Workflow failed at verification step: {verification_result.get('message', 'Unknown error')}")
            return {"status": "error", "step": "verification", "message": verification_result.get('message')}
            
        # Step 3: Generate comprehensive analysis report
        logger.info("Step 3: Generating analysis report")
        report_path = os.path.join(output_path, "reference_analysis_report.md")
        
        try:
            # Combine extraction and verification data
            combined_data = {
                "document": os.path.basename(pdf_path),
                "extraction": extraction_result,
                "verification": verification_result
            }
            
            # Save combined data
            with open(os.path.join(output_path, "workflow_results.json"), 'w') as f:
                json.dump(combined_data, f, indent=2)
                
            # Generate markdown report
            with open(report_path, 'w') as f:
                f.write(f"# Reference Analysis Report\n\n")
                f.write(f"## Document: {os.path.basename(pdf_path)}\n\n")
                f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("## Summary\n\n")
                f.write(f"- **Total References**: {len(extraction_result.get('references', []))}\n")
                f.write(f"- **Valid References**: {verification_result.get('valid_count', 0)}\n")
                f.write(f"- **References with Issues**: {verification_result.get('issues_count', 0)}\n")
                f.write(f"- **Invalid References**: {verification_result.get('invalid_count', 0)}\n\n")
                
                f.write("## Reference Quality Analysis\n\n")
                f.write("| # | Reference | Type | Year | Confidence | Status |\n")
                f.write("|---|----------|------|------|------------|--------|\n")
                
                for i, ref in enumerate(extraction_result.get('references', [])):
                    # Find corresponding verification result
                    ver_result = verification_result.get('verification_results', [])[i] if i < len(verification_result.get('verification_results', [])) else {"status": "unknown"}
                    
                    ref_text = ref.get('full_text', '')[:80] + "..." if len(ref.get('full_text', '')) > 80 else ref.get('full_text', '')
                    ref_type = ref.get('reference_type', 'unknown')
                    ref_year = ref.get('year', 'N/A')
                    ref_confidence = f"{ref.get('confidence_score', 0):.2f}"
                    ref_status = ver_result.get('status', 'unknown')
                    
                    f.write(f"| {i+1} | {ref_text} | {ref_type} | {ref_year} | {ref_confidence} | {ref_status} |\n")
                
                f.write("\n\n## Recommendations\n\n")
                
                if verification_result.get('issues_count', 0) + verification_result.get('invalid_count', 0) > 0:
                    f.write("The following references require attention:\n\n")
                    for i, ver_result in enumerate(verification_result.get('verification_results', [])):
                        if ver_result.get('status', '') != 'valid':
                            f.write(f"1. **Reference {i+1}**: {ver_result.get('citation', '')[:80]}...\n")
                            f.write(f"   - **Issues**: {', '.join(ver_result.get('issues', ['Unknown issue']))}\n")
                            f.write(f"   - **Recommendation**: {ver_result.get('recommendation', 'Verify and correct the reference')}\n\n")
                else:
                    f.write("All references appear to be valid and properly formatted. No corrections needed.\n")
        except Exception as e:
            logger.error(f"Failed to generate analysis report: {str(e)}")
            return {"status": "error", "step": "analysis", "message": str(e)}
            
        elapsed_time = time.time() - start_time
        logger.info(f"Full workflow completed in {elapsed_time:.2f} seconds")
        
        return {
            "status": "success",
            "extraction_result": extraction_result,
            "verification_result": verification_result,
            "output_directory": output_path,
            "report_path": report_path,
            "processing_time": elapsed_time
        }

def main():
    """Main entry point for the command-line interface"""
    parser = argparse.ArgumentParser(
        description="Academic Research Automation System - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py extract --pdf paper.pdf --output refs_output
  python main.py verify --references refs.json --output verification
  python main.py research --author "Jane Smith" --output smith_research
  python main.py workflow --pdf paper.pdf --output full_analysis
        """
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract references from a PDF")
    extract_parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    extract_parser.add_argument("--output", required=True, help="Output directory")
    extract_parser.add_argument("--formats", nargs="+", default=["json", "csv", "xlsx"], 
                              help="Output formats (default: json csv xlsx)")
    extract_parser.add_argument("--ocr", action="store_true", help="Use OCR if needed")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify citations")
    verify_parser.add_argument("--references", required=True, 
                             help="Path to references file (JSON, CSV, or TXT)")
    verify_parser.add_argument("--output", required=True, help="Output directory")
    
    # Research command
    research_parser = subparsers.add_parser("research", help="Research academic author")
    research_parser.add_argument("--author", required=True, help="Author name")
    research_parser.add_argument("--affiliation", help="Author affiliation")
    research_parser.add_argument("--start-year", type=int, help="Start year for publications")
    research_parser.add_argument("--end-year", type=int, help="End year for publications")
    research_parser.add_argument("--output", required=True, help="Output directory")
    
    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Execute full workflow")
    workflow_parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    workflow_parser.add_argument("--output", required=True, help="Output directory")
    
    # Global options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the system
    system = AcademicResearchAutomationSystem(verbose=args.verbose)
    
    # Execute the requested command
    if args.command == "extract":
        result = system.extract_references(
            pdf_path=args.pdf,
            output_path=args.output,
            formats=args.formats,
            use_ocr=args.ocr
        )
        
        if result["status"] == "success":
            print(f"Successfully extracted {len(result['references'])} references")
            print(f"Output files saved to: {args.output}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    elif args.command == "verify":
        result = system.verify_citations(
            citations_source=args.references,
            output_path=args.output
        )
        
        if result["status"] == "success":
            print(f"Citation verification complete")
            print(f"Valid citations: {result['valid_count']}")
            print(f"Citations with issues: {result['issues_count']}")
            print(f"Invalid citations: {result['invalid_count']}")
            print(f"Output files saved to: {args.output}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    elif args.command == "research":
        result = system.research_author(
            author_name=args.author,
            affiliation=args.affiliation,
            start_year=args.start_year,
            end_year=args.end_year,
            output_path=args.output
        )
        
        if result["status"] == "success":
            print(f"Research complete: found {len(result['publications'])} publications")
            print(f"Output files saved to: {args.output}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    elif args.command == "workflow":
        result = system.execute_full_workflow(
            pdf_path=args.pdf,
            output_path=args.output
        )
        
        if result["status"] == "success":
            print(f"Full workflow completed successfully in {result['processing_time']:.2f} seconds")
            print(f"References extracted: {len(result['extraction_result']['references'])}")
            print(f"Analysis report: {result['report_path']}")
            print(f"All output files saved to: {args.output}")
        else:
            print(f"Workflow failed at {result.get('step', 'unknown')} step")
            print(f"Error: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
