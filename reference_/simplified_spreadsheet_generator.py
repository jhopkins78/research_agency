"""
Simplified Enhanced Reference Processing and Spreadsheet Generation
Creating comprehensive Excel spreadsheets from the extracted references
"""

import json
import pandas as pd
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

def create_enhanced_spreadsheets():
    """Create comprehensive Excel spreadsheets from the extracted references"""
    
    print("=" * 70)
    print("ENHANCED REFERENCE PROCESSING AND SPREADSHEET GENERATION")
    print("=" * 70)
    
    # Load the extracted references
    print("\\n1. Loading extracted reference data...")
    
    try:
        with open('/home/ubuntu/research_report_reference_analysis.json', 'r') as f:
            analysis_data = json.load(f)
        
        references = analysis_data['references']
        statistics = analysis_data['statistics']
        
        print(f"✓ Loaded {len(references)} references from analysis file")
        
    except Exception as e:
        print(f"✗ Error loading reference data: {e}")
        return None
    
    # Create comprehensive DataFrame
    print("\\n2. Creating comprehensive reference DataFrame...")
    
    df = create_reference_dataframe(references)
    print(f"✓ Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
    
    # Generate enhanced Excel workbook
    print("\\n3. Generating enhanced Excel workbook...")
    
    excel_file = create_simple_excel_workbook(df, statistics, analysis_data)
    print(f"✓ Created enhanced Excel workbook: {os.path.basename(excel_file)}")
    
    # Generate summary CSV
    print("\\n4. Generating summary CSV files...")
    
    csv_files = create_summary_csv_files(df, statistics)
    print(f"✓ Created {len(csv_files)} summary CSV files")
    
    # Generate analysis report
    print("\\n5. Generating detailed analysis report...")
    
    report_file = create_analysis_report(df, statistics, analysis_data)
    print(f"✓ Created analysis report: {os.path.basename(report_file)}")
    
    return {
        "excel_file": excel_file,
        "csv_files": csv_files,
        "report_file": report_file,
        "dataframe": df,
        "statistics": statistics
    }

def create_reference_dataframe(references):
    """Create a comprehensive pandas DataFrame from the references"""
    
    data = []
    
    for ref in references:
        # Handle authors list
        authors_str = ", ".join(ref.get('authors', [])) if ref.get('authors') else ""
        first_author = ref.get('authors', [''])[0] if ref.get('authors') else ""
        author_count = len(ref.get('authors', []))
        
        # Extract domain from URL if available
        url = ref.get('url', '')
        domain = ""
        if url:
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
            except:
                domain = ""
        
        # Determine citation style
        full_text = ref.get('full_text', '')
        citation_style = determine_citation_style(full_text)
        
        row = {
            'Reference_Number': ref.get('reference_number', ''),
            'Title': ref.get('title', ''),
            'Authors': authors_str,
            'First_Author': first_author,
            'Author_Count': author_count,
            'Year': ref.get('year', ''),
            'Venue': ref.get('venue', ''),
            'Volume': ref.get('volume', ''),
            'Issue': ref.get('issue', ''),
            'Pages': ref.get('pages', ''),
            'DOI': ref.get('doi', ''),
            'URL': url,
            'Domain': domain,
            'ISBN': ref.get('isbn', ''),
            'Reference_Type': ref.get('reference_type', ''),
            'Citation_Style': citation_style,
            'Confidence_Score': ref.get('confidence_score', 0),
            'Full_Text': full_text,
            'Text_Length': len(full_text),
            'Has_DOI': bool(ref.get('doi')),
            'Has_URL': bool(url),
            'Has_ISBN': bool(ref.get('isbn')),
            'Decade': (ref.get('year') // 10 * 10) if ref.get('year') else None
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

def determine_citation_style(full_text):
    """Determine the likely citation style based on the text format"""
    
    if not full_text:
        return "Unknown"
    
    # Simple heuristics for citation style detection
    if "doi:" in full_text.lower() or "DOI:" in full_text:
        return "APA"
    elif full_text.count("(") > 1 and full_text.count(")") > 1:
        return "APA"
    elif '"' in full_text and full_text.count('"') >= 2:
        return "MLA"
    elif "vol." in full_text.lower() or "no." in full_text.lower():
        return "Chicago"
    elif "pp." in full_text:
        return "MLA"
    else:
        return "Mixed"

def create_simple_excel_workbook(df, statistics, analysis_data):
    """Create a simple Excel workbook with multiple sheets"""
    
    filename = "/home/ubuntu/research_report_references_enhanced.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        
        # 1. Summary statistics
        summary_data = {
            'Metric': [
                'Total References',
                'Average Confidence Score',
                'Year Range',
                'Unique Authors',
                'Unique Venues',
                'High Confidence (>0.8)',
                'Medium Confidence (0.5-0.8)',
                'Low Confidence (<0.5)',
                'References with DOI',
                'References with URL',
                'References with ISBN'
            ],
            'Value': [
                statistics['total_references'],
                f"{statistics['average_confidence']:.2f}",
                statistics['year_range'],
                statistics['unique_authors'],
                statistics['unique_venues'],
                len(df[df['Confidence_Score'] > 0.8]),
                len(df[(df['Confidence_Score'] >= 0.5) & (df['Confidence_Score'] <= 0.8)]),
                len(df[df['Confidence_Score'] < 0.5]),
                df['Has_DOI'].sum(),
                df['Has_URL'].sum(),
                df['Has_ISBN'].sum()
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # 2. All references (key columns)
        display_columns = [
            'Reference_Number', 'Title', 'Authors', 'Year', 'Venue', 
            'Reference_Type', 'Confidence_Score', 'Has_DOI', 'Has_URL'
        ]
        
        display_df = df[display_columns].copy()
        display_df.to_excel(writer, sheet_name='All References', index=False)
        
        # 3. By type analysis
        type_summary = df.groupby('Reference_Type').agg({
            'Reference_Number': 'count',
            'Confidence_Score': 'mean',
            'Year': ['min', 'max'],
            'Has_DOI': 'sum',
            'Has_URL': 'sum'
        }).round(2)
        
        # Flatten column names
        type_summary.columns = ['Count', 'Avg_Confidence', 'Min_Year', 'Max_Year', 'DOI_Count', 'URL_Count']
        type_summary = type_summary.reset_index()
        type_summary.to_excel(writer, sheet_name='By Type', index=False)
        
        # 4. By year analysis
        year_summary = df[df['Year'].notna()].groupby('Year').agg({
            'Reference_Number': 'count',
            'Confidence_Score': 'mean',
            'Reference_Type': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
        }).round(2)
        
        year_summary.columns = ['Count', 'Avg_Confidence', 'Most_Common_Type']
        year_summary = year_summary.reset_index()
        year_summary = year_summary.sort_values('Year')
        year_summary.to_excel(writer, sheet_name='By Year', index=False)
        
        # 5. Quality analysis
        quality_data = {
            'Quality_Metric': [
                'High Confidence (>0.8)',
                'Medium Confidence (0.5-0.8)',
                'Low Confidence (<0.5)',
                'References with DOI',
                'References with URL',
                'References with ISBN',
                'Complete Author Info',
                'Complete Year Info',
                'Complete Venue Info'
            ],
            'Count': [
                len(df[df['Confidence_Score'] > 0.8]),
                len(df[(df['Confidence_Score'] >= 0.5) & (df['Confidence_Score'] <= 0.8)]),
                len(df[df['Confidence_Score'] < 0.5]),
                df['Has_DOI'].sum(),
                df['Has_URL'].sum(),
                df['Has_ISBN'].sum(),
                (df['Author_Count'] > 0).sum(),
                df['Year'].notna().sum(),
                (df['Venue'].notna() & (df['Venue'] != '')).sum()
            ]
        }
        
        quality_df = pd.DataFrame(quality_data)
        quality_df['Percentage'] = (quality_df['Count'] / len(df) * 100).round(1)
        quality_df.to_excel(writer, sheet_name='Quality Analysis', index=False)
        
        # 6. Full data
        df.to_excel(writer, sheet_name='Full Data', index=False)
    
    return filename

def create_summary_csv_files(df, statistics):
    """Create summary CSV files for different analyses"""
    
    csv_files = {}
    
    # 1. Basic reference summary
    summary_df = df[['Reference_Number', 'Title', 'Authors', 'Year', 'Venue', 'Reference_Type', 'Confidence_Score']].copy()
    summary_file = "/home/ubuntu/research_report_references_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    csv_files['summary'] = summary_file
    
    # 2. Type analysis
    type_analysis = df.groupby('Reference_Type').agg({
        'Reference_Number': 'count',
        'Confidence_Score': 'mean',
        'Year': ['min', 'max']
    }).round(2)
    type_file = "/home/ubuntu/research_report_references_by_type.csv"
    type_analysis.to_csv(type_file)
    csv_files['by_type'] = type_file
    
    # 3. Year analysis
    year_analysis = df[df['Year'].notna()].groupby('Year').size().reset_index(name='Count')
    year_file = "/home/ubuntu/research_report_references_by_year.csv"
    year_analysis.to_csv(year_file, index=False)
    csv_files['by_year'] = year_file
    
    # 4. Quality metrics
    quality_df = df[['Reference_Number', 'Title', 'Confidence_Score', 'Has_DOI', 'Has_URL', 'Has_ISBN', 'Author_Count']].copy()
    quality_file = "/home/ubuntu/research_report_references_quality.csv"
    quality_df.to_csv(quality_file, index=False)
    csv_files['quality'] = quality_file
    
    return csv_files

def create_analysis_report(df, statistics, analysis_data):
    """Create a detailed text analysis report"""
    
    report_file = "/home/ubuntu/research_report_reference_analysis_report.txt"
    
    with open(report_file, 'w') as f:
        f.write("RESEARCH REPORT REFERENCE ANALYSIS\\n")
        f.write("=" * 50 + "\\n\\n")
        
        # Basic statistics
        f.write("EXTRACTION SUMMARY\\n")
        f.write("-" * 20 + "\\n")
        f.write(f"Total References Extracted: {statistics['total_references']}\\n")
        f.write(f"Average Confidence Score: {statistics['average_confidence']:.2f}\\n")
        f.write(f"Year Range: {statistics['year_range']}\\n")
        f.write(f"Unique Authors: {statistics['unique_authors']}\\n")
        f.write(f"Unique Venues: {statistics['unique_venues']}\\n\\n")
        
        # Reference types
        f.write("REFERENCE TYPES\\n")
        f.write("-" * 15 + "\\n")
        for ref_type, count in statistics['reference_types'].items():
            percentage = count / statistics['total_references'] * 100
            f.write(f"{ref_type.title()}: {count} ({percentage:.1f}%)\\n")
        f.write("\\n")
        
        # Quality analysis
        f.write("QUALITY ANALYSIS\\n")
        f.write("-" * 15 + "\\n")
        high_conf = len(df[df['Confidence_Score'] > 0.8])
        med_conf = len(df[(df['Confidence_Score'] >= 0.5) & (df['Confidence_Score'] <= 0.8)])
        low_conf = len(df[df['Confidence_Score'] < 0.5])
        
        f.write(f"High Confidence (>0.8): {high_conf} ({high_conf/len(df)*100:.1f}%)\\n")
        f.write(f"Medium Confidence (0.5-0.8): {med_conf} ({med_conf/len(df)*100:.1f}%)\\n")
        f.write(f"Low Confidence (<0.5): {low_conf} ({low_conf/len(df)*100:.1f}%)\\n\\n")
        
        # Metadata completeness
        f.write("METADATA COMPLETENESS\\n")
        f.write("-" * 20 + "\\n")
        f.write(f"References with DOI: {df['Has_DOI'].sum()} ({df['Has_DOI'].sum()/len(df)*100:.1f}%)\\n")
        f.write(f"References with URL: {df['Has_URL'].sum()} ({df['Has_URL'].sum()/len(df)*100:.1f}%)\\n")
        f.write(f"References with ISBN: {df['Has_ISBN'].sum()} ({df['Has_ISBN'].sum()/len(df)*100:.1f}%)\\n")
        f.write(f"References with Authors: {(df['Author_Count'] > 0).sum()} ({(df['Author_Count'] > 0).sum()/len(df)*100:.1f}%)\\n")
        f.write(f"References with Year: {df['Year'].notna().sum()} ({df['Year'].notna().sum()/len(df)*100:.1f}%)\\n\\n")
        
        # Top venues
        f.write("TOP VENUES\\n")
        f.write("-" * 10 + "\\n")
        venue_counts = df[df['Venue'].notna() & (df['Venue'] != '')]['Venue'].value_counts().head(10)
        for venue, count in venue_counts.items():
            f.write(f"{venue}: {count}\\n")
        f.write("\\n")
        
        # Year distribution
        f.write("YEAR DISTRIBUTION\\n")
        f.write("-" * 15 + "\\n")
        year_counts = df[df['Year'].notna()]['Year'].value_counts().sort_index()
        for year, count in year_counts.items():
            f.write(f"{int(year)}: {count}\\n")
    
    return report_file

if __name__ == "__main__":
    result = create_enhanced_spreadsheets()
    
    if result:
        print("\\n" + "=" * 70)
        print("ENHANCED SPREADSHEET GENERATION COMPLETED")
        print("=" * 70)
        
        print(f"\\n Excel Workbook: {os.path.basename(result['excel_file'])}")
        print(f" Analysis Report: {os.path.basename(result['report_file'])}")
        
        print("\\n CSV Files Generated:")
        for csv_type, csv_file in result['csv_files'].items():
            print(f"  - {csv_type.title()}: {os.path.basename(csv_file)}")
        
        print("\\n Key Statistics:")
        stats = result['statistics']
        print(f"  - Total References: {stats['total_references']}")
        print(f"  - Average Confidence: {stats['average_confidence']:.2f}")
        print(f"  - Reference Types: {len(stats['reference_types'])}")
        print(f"  - Year Range: {stats['year_range']}")
        
        print("\\n🎉 All files generated successfully!")
        
    else:
        print("\\n Spreadsheet generation failed.")

