README.txt
==========

MY RESEARCH AGENCY SYSTEM
-------------------------
Dissertation: Joshua Hopkins 
Description: Multi-agent research automation framework for citation validation, literature analysis, and academic publishing support.

This repository hosts a complete research automation ecosystem comprised of agents, data tools, citation validators, visualizations, and orchestrated agent workflows. It was built to increase research velocity, improve citation accuracy, and extract deeper insights from multi-source academic documents.

-------------------------
📁 DIRECTORY STRUCTURE
-------------------------
my_research_agency/
│
├── agents/                        # Core research agents and scripts
│   ├── academic_research_agent_system.py
│   ├── aras_demonstration.py
│   ├── prea_quick_start.py
│   └── test_prea.py
│
├── agent_documentation/          # JSON definitions for agent roles and metadata
│   ├── master_agent_registry.json
│   ├── aras_agent_documentation.json
│   ├── prea_agent_documentation.json
│   └── Agent Documentation Summary.md
│
├── reference/                    # Citation quality analysis, reference exports, and validation tools
│   ├── research_report_references.txt
│   ├── research_report_references_quality.csv
│   ├── research_report_reference_analysis.json
│   └── prea_real_world_demo.py
│
├── visualizations/               # Visual outputs and chart generation scripts
│   ├── png_output/               # Final rendered visualizations
│   └── png_python/               # Python scripts to generate visualizations
│
├── SamaritanAI.pdf               # Background context on platform vision
├── In-Text Citation Corrections Summary.md
├── Data Challenges Report.zip    # Compressed report with SMB insights and data issues
└── .DS_Store (macOS system file)

-------------------------
GETTING STARTED
-------------------------
1. Clone this repository:
   git clone https://github.com/your-username/my_research_agency.git

2. Navigate to the agent scripts:
   cd my_research_agency/agents

3. Run a quick demo (e.g., for ARAS):
   python aras_demonstration.py

4. To test PDF citation extraction:
   python pdf_reference_extraction_agent.py path_to_pdf

-------------------------
KEY AGENTS
-------------------------
- **ARAS** (Academic Research Agent System): Automates multi-source discovery, verification, and citation formatting.
- **PREA** (PDF Reference Extraction Agent): Parses academic papers to extract, validate, and structure reference data.
- **Documentation Registry**: Tracks agent behaviors, expected inputs/outputs, and configuration.

-------------------------
ISUALIZATIONS
-------------------------
Visuals in `visualizations/png_output/` illustrate:
- SMB data challenges
- Agent orchestration architecture
- ROI projections
- Competitive landscapes

You can regenerate them using the Python scripts in `visualizations/png_python/`.

-------------------------
📄 LICENSE
-------------------------
This project is licensed under the AGPL-3.0 License – see the LICENSE file for details.

-------------------------
VISION
-------------------------
This system was developed to explore the boundaries of what agentic AI can do for academic research. It is meant to enable researchers, developers, and institutions to publish with speed and precision—by reducing manual tasks, preventing citation errors, and enhancing insight generation at scale.The system was developed for my Master's field project at UC Santa Barbara's College of Engineering, Technology Management Program.

Built by an AI Architect who believes intelligence should be orchestrated—not outsourced.

