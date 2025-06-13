"""
PREA Quick Start Script
Quick testing and validation for the PDF Reference Extraction Agent
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_reference_extraction_agent import PDFReferenceExtractionAgent, demonstrate_pdf_extraction
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure pdf_reference_extraction_agent.py is in the same directory")
    sys.exit(1)

def quick_test():
    """Quick test of the PREA system"""
    print("PREA Quick Start Test")
    print("=" * 30)
    
    try:
        # Initialize agent
        agent = PDFReferenceExtractionAgent()
        print("✓ PDF Reference Extraction Agent initialized successfully")
        
        # Test configuration
        config = agent.config
        print(f"✓ Configuration loaded: {len(config)} settings")
        print(f"  - Min confidence threshold: {config['min_confidence_threshold']}")
        print(f"  - Output formats: {config['output_formats']}")
        print(f"  - Max file size: {config['max_file_size_mb']}MB")
        
        # Test statistics
        stats = agent.get_processing_statistics()
        print("✓ Statistics system working")
        
        # Test demonstration
        print("\\nRunning demonstration...")
        demo_result = demonstrate_pdf_extraction()
        
        if demo_result:
            print("✓ Demonstration completed successfully")
            print(f"✓ Generated {len(demo_result['sample_references'])} sample references")
            print(f"✓ Created {len(demo_result['output_files'])} output files")
        
        print("\\n✓ PREA system is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def show_capabilities():
    """Show system capabilities"""
    print("\\n" + "=" * 50)
    print("PDF REFERENCE EXTRACTION AGENT CAPABILITIES")
    print("=" * 50)
    
    capabilities = [
        "📄 Multi-method PDF text extraction (PDFPlumber, PyPDF2, OCR)",
        "🔍 Advanced reference parsing with pattern recognition",
        "📊 Multiple output formats (JSON, CSV, Excel, Text, Markdown)",
        "🎯 Confidence scoring and quality assessment",
        "📚 Citation style recognition (APA, MLA, Chicago, IEEE)",
        "🔗 Integration with Academic Research Agent System (ARAS)",
        "⚡ Batch processing for multiple PDF files",
        "📈 Processing statistics and error tracking",
        "🛠️ Configurable extraction parameters",
        "✅ Comprehensive testing and validation"
    ]
    
    for capability in capabilities:
        print(f"  {capability}")

def show_usage_examples():
    """Show basic usage examples"""
    print("\\n" + "=" * 50)
    print("BASIC USAGE EXAMPLES")
    print("=" * 50)
    
    examples = [
        {
            "title": "Single PDF Extraction",
            "code": '''from pdf_reference_extraction_agent import PDFReferenceExtractionAgent

agent = PDFReferenceExtractionAgent()
result = agent.extract_references_from_pdf("paper.pdf")
print(f"Extracted {len(result['references'])} references")'''
        },
        {
            "title": "Batch Processing",
            "code": '''pdf_files = ["paper1.pdf", "paper2.pdf", "paper3.pdf"]
batch_result = agent.batch_extract_references(pdf_files, "output_dir")
print(f"Processed {batch_result['batch_summary']['total_files']} files")'''
        },
        {
            "title": "Custom Configuration",
            "code": '''config = {
    "min_confidence_threshold": 0.7,
    "output_formats": ["json", "xlsx"],
    "max_file_size_mb": 100
}
agent = PDFReferenceExtractionAgent(config)'''
        }
    ]
    
    for example in examples:
        print(f"\\n{example['title']}:")
        print("-" * len(example['title']))
        print(example['code'])

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        show_capabilities()
        show_usage_examples()
        
        print("\\n" + "=" * 50)
        print("PDF REFERENCE EXTRACTION AGENT READY")
        print("=" * 50)
        print("\\nNext steps:")
        print("1. Run 'python test_prea.py' for comprehensive testing")
        print("2. See PREA_Documentation.md for detailed usage")
        print("3. Check the examples/ directory for implementation samples")
        print("4. Import the agent in your own scripts:")
        print("   from pdf_reference_extraction_agent import PDFReferenceExtractionAgent")
    else:
        print("\\nPlease check the error messages above and try again.")
        sys.exit(1)

