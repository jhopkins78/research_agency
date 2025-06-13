# Streamlit Interface Walkthrough

This guide provides a step-by-step walkthrough of using the Streamlit interface for the Academic Research Automation System.

## Getting Started

The Streamlit interface provides a user-friendly way to interact with the Academic Research Automation System, allowing you to upload research documents, run analysis workflows, and view results without writing any code.

### Running the Streamlit App

To start the Streamlit interface, run the following command from the project root directory:

```bash
streamlit run streamlit_app.py
```

This will start a local web server and automatically open the interface in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501.

## Interface Overview

The Streamlit interface is divided into two main sections:

1. **Sidebar**: Contains configuration options and controls
2. **Main Area**: Displays workflow information, results, logs, and configuration details

### Sidebar Options

The sidebar contains all the controls you need to configure and run workflows:

#### 1. Upload Files

You can upload three types of files:
- **PDF or Document**: Research papers, articles, or any document containing references
- **References (JSON)**: Pre-extracted references in JSON format
- **Research Brief**: A markdown file describing the research project

![File Upload Section](../docs/images/streamlit_file_upload.png)

#### 2. Select Agents

Choose which agents to activate for your workflow:
- **File Router Agent**: Handles file type detection and routing
- **Insight Agent**: Analyzes references and generates insights
- **Report Agent**: Creates formatted reports
- **ARAS Integration**: Enables Academic Research Agent System
- **PREA Integration**: Enables PDF Reference Extraction Agent

![Agent Selection](../docs/images/streamlit_agent_selection.png)

#### 3. Output Format

Configure the output format for generated reports:
- **Report Format**: Choose between Markdown (md), PDF, or Word (docx)
- **Logging Verbosity**: Set to Minimal, Normal, or Verbose

![Output Format](../docs/images/streamlit_output_format.png)

#### 4. Example Data Option

If you don't have your own files to upload, you can use the example data included with the system by checking the "Use Example Data" option.

![Example Data Option](../docs/images/streamlit_example_data.png)

### Main Area Tabs

The main area is organized into four tabs:

#### Workflow Tab

Displays information about the current workflow based on uploaded files:
- Workflow type (extraction, verification, or complete research workflow)
- Selected agents
- Example data information (if using example data)

![Workflow Tab](../docs/images/streamlit_workflow_tab.png)

#### Results Tab

After running a workflow, this tab displays the results:
- Success/failure status
- Execution time
- Output files organized by type
- File content previews
- Download buttons for each file

![Results Tab](../docs/images/streamlit_results_tab.png)

#### Logs Tab

Shows real-time logs from the workflow execution:
- Color-coded log messages (info, warning, error)
- Detailed error information with expandable tracebacks
- Execution progress indicators

![Logs Tab](../docs/images/streamlit_logs_tab.png)

#### Configuration Tab

Displays the current system configuration in JSON format:
- Paths
- Logging settings
- Agent activation flags
- Output format preferences
- Performance settings

![Configuration Tab](../docs/images/streamlit_config_tab.png)

## Workflow Examples

### Example 1: Extract References from a Document

1. Upload a PDF or document file
2. Ensure "File Router Agent" and "PREA Integration" are selected
3. Choose your preferred output format
4. Click "Run Workflow"
5. View the extracted references in the Results tab

### Example 2: Analyze References

1. Upload a references JSON file
2. Ensure "Insight Agent" is selected
3. Choose your preferred output format
4. Click "Run Workflow"
5. View the analysis results and visualizations in the Results tab

### Example 3: Complete Research Workflow

1. Upload both a document file and a research brief
2. Select all agents
3. Choose your preferred output format
4. Click "Run Workflow"
5. View the comprehensive report in the Results tab

### Example 4: Using Example Data

1. Check the "Use Example Data" option
2. Select the agents you want to test
3. Choose your preferred output format
4. Click "Run Workflow"
5. View the results based on the example data

## Troubleshooting

### Common Issues

1. **File Upload Errors**
   - Ensure your files are in the correct format
   - Check that file sizes are within limits (typically under 200MB)

2. **Workflow Execution Errors**
   - Check the Logs tab for detailed error information
   - Verify that all required agents are selected for your workflow

3. **Output Format Issues**
   - For PDF generation, ensure that the manus-md-to-pdf utility is installed
   - For DOCX generation, ensure that pypandoc and pandoc are installed

### Getting Help

If you encounter issues not covered in this guide, please:
1. Check the full documentation in the docs/ directory
2. Review the logs for detailed error messages
3. Submit an issue on the project's GitHub repository

## Next Steps

Now that you're familiar with the Streamlit interface, you might want to:
- Explore the API documentation to integrate the system into your own applications
- Contribute to the project by adding new features or improving existing ones
- Create custom templates for report generation

For more information, see the [README.md](../README.md) and [API documentation](../docs/API.md).
