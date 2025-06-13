import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arrow, ConnectionPatch
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create Samaritan AI Architecture Diagram
fig, ax = plt.subplots(figsize=(16, 12))

# Define architecture layers
layers = [
    {'name': 'User Interface Layer', 'y': 10, 'color': '#3498DB', 'components': [
        'Agentic Dashboards', 'Natural Language Interface', 'Mobile Apps', 'API Gateway'
    ]},
    {'name': 'Harmony Engine™ (Multi-Agent Orchestration)', 'y': 8, 'color': '#E74C3C', 'components': [
        'Insight Agent', 'Data Agent', 'Analytics Agent', 'Report Agent'
    ]},
    {'name': 'Intelligence Layer', 'y': 6, 'color': '#F39C12', 'components': [
        'Business Intelligence Model (BIM)', 'Predictive Models', 'Prescriptive Analytics', 'NLP Engine'
    ]},
    {'name': 'Data Processing Layer', 'y': 4, 'color': '#27AE60', 'components': [
        'ETL/ELT Engine', 'Entity Interlinking Layer (EIL)', 'Data Quality Engine', 'Real-time Processor'
    ]},
    {'name': 'Data Sources', 'y': 2, 'color': '#9B59B6', 'components': [
        'CRM Systems', 'POS/ERP', 'Marketing Tools', 'External APIs'
    ]}
]

# Draw layers
for layer in layers:
    # Draw layer background
    rect = FancyBboxPatch((1, layer['y']-0.8), 14, 1.6, boxstyle="round,pad=0.1", 
                         facecolor=layer['color'], alpha=0.3, edgecolor=layer['color'], linewidth=2)
    ax.add_patch(rect)
    
    # Add layer title
    ax.text(0.5, layer['y'], layer['name'], fontsize=12, fontweight='bold', 
            rotation=90, va='center', ha='center', color=layer['color'])
    
    # Add components
    component_width = 14 / len(layer['components'])
    for i, component in enumerate(layer['components']):
        x_pos = 1.5 + i * component_width + component_width/2
        comp_rect = FancyBboxPatch((1.5 + i * component_width, layer['y']-0.6), 
                                  component_width-0.2, 1.2, boxstyle="round,pad=0.05",
                                  facecolor=layer['color'], alpha=0.8, edgecolor='white', linewidth=1)
        ax.add_patch(comp_rect)
        ax.text(x_pos, layer['y'], component, ha='center', va='center', 
                fontsize=9, fontweight='bold', color='white', wrap=True)

# Draw data flow arrows
arrow_props = dict(arrowstyle='->', lw=3, color='#2C3E50', alpha=0.7)
for i in range(len(layers)-1):
    ax.annotate('', xy=(8, layers[i+1]['y'] + 0.8), xytext=(8, layers[i]['y'] - 0.8),
                arrowprops=arrow_props)

# Add side annotations
annotations = [
    {'pos': (16.5, 10), 'text': 'User\nExperience', 'color': '#3498DB'},
    {'pos': (16.5, 8), 'text': 'AI\nOrchestration', 'color': '#E74C3C'},
    {'pos': (16.5, 6), 'text': 'Machine\nLearning', 'color': '#F39C12'},
    {'pos': (16.5, 4), 'text': 'Data\nIntegration', 'color': '#27AE60'},
    {'pos': (16.5, 2), 'text': 'Source\nSystems', 'color': '#9B59B6'}
]

for ann in annotations:
    ax.text(ann['pos'][0], ann['pos'][1], ann['text'], ha='center', va='center',
            fontsize=10, fontweight='bold', color=ann['color'],
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=ann['color']))

# Set title and formatting
ax.set_title('Samaritan AI Architecture Diagram\nMulti-Layer Agentic Intelligence Platform', 
             fontsize=16, fontweight='bold', pad=20)

# Remove axes
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz10_samaritan_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Multi-Agent Orchestration Workflow
fig, ax = plt.subplots(figsize=(16, 10))

# Define agents and their positions
agents = [
    {'name': 'Data\nIngestion\nAgent', 'pos': (3, 8), 'color': '#3498DB', 'size': 1.2},
    {'name': 'Quality\nAssurance\nAgent', 'pos': (7, 8), 'color': '#E74C3C', 'size': 1.2},
    {'name': 'Analytics\nAgent', 'pos': (11, 8), 'color': '#F39C12', 'size': 1.2},
    {'name': 'Insight\nGeneration\nAgent', 'pos': (15, 8), 'color': '#27AE60', 'size': 1.2},
    {'name': 'Semantic\nMapping\nAgent', 'pos': (3, 5), 'color': '#9B59B6', 'size': 1.0},
    {'name': 'Model\nTraining\nAgent', 'pos': (7, 5), 'color': '#E67E22', 'size': 1.0},
    {'name': 'Report\nGeneration\nAgent', 'pos': (11, 5), 'color': '#34495E', 'size': 1.0},
    {'name': 'Action\nRecommendation\nAgent', 'pos': (15, 5), 'color': '#E91E63', 'size': 1.0},
    {'name': 'Harmony Engine\n(Orchestrator)', 'pos': (9, 2), 'color': '#2C3E50', 'size': 2.0}
]

# Draw agents
for agent in agents:
    circle = Circle(agent['pos'], agent['size'], facecolor=agent['color'], 
                   edgecolor='black', alpha=0.8, linewidth=2)
    ax.add_patch(circle)
    ax.text(agent['pos'][0], agent['pos'][1], agent['name'], ha='center', va='center',
            fontsize=9, fontweight='bold', color='white', wrap=True)

# Define workflow connections
workflows = [
    # Primary workflow
    ((3, 8), (7, 8), 'Data Flow'),
    ((7, 8), (11, 8), 'Clean Data'),
    ((11, 8), (15, 8), 'Analysis Results'),
    # Secondary workflows
    ((3, 8), (3, 5), 'Schema Mapping'),
    ((7, 8), (7, 5), 'Model Updates'),
    ((11, 8), (11, 5), 'Report Data'),
    ((15, 8), (15, 5), 'Recommendations'),
    # Orchestration connections
    ((9, 3.5), (3, 6.5), ''),
    ((9, 3.5), (7, 6.5), ''),
    ((9, 3.5), (11, 6.5), ''),
    ((9, 3.5), (15, 6.5), ''),
    ((9, 3.5), (3, 6.8), ''),
    ((9, 3.5), (7, 6.8), ''),
    ((9, 3.5), (11, 6.8), ''),
    ((9, 3.5), (15, 6.8), '')
]

# Draw workflow arrows
for i, (start, end, label) in enumerate(workflows[:7]):  # Only labeled arrows
    if i < 4:  # Primary workflow
        arrow_color = '#2C3E50'
        arrow_width = 3
    else:  # Secondary workflow
        arrow_color = '#7F8C8D'
        arrow_width = 2
    
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', lw=arrow_width, color=arrow_color, alpha=0.8))
    
    if label:  # Add label
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + 0.3
        ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=8, 
                fontweight='bold', bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Draw orchestration connections (dashed lines)
for start, end, _ in workflows[7:]:
    ax.plot([start[0], end[0]], [start[1], end[1]], 
            linestyle='--', color='#95A5A6', alpha=0.6, linewidth=1.5)

# Add process stages
stages = [
    {'pos': (5, 9.5), 'text': 'Stage 1: Data Acquisition & Quality', 'color': '#3498DB'},
    {'pos': (13, 9.5), 'text': 'Stage 2: Analysis & Insight Generation', 'color': '#27AE60'},
    {'pos': (9, 6.5), 'text': 'Stage 3: Semantic Processing & Reporting', 'color': '#9B59B6'},
    {'pos': (9, 0.5), 'text': 'Harmony Engine: Continuous Orchestration & Optimization', 'color': '#2C3E50'}
]

for stage in stages:
    ax.text(stage['pos'][0], stage['pos'][1], stage['text'], ha='center', va='center',
            fontsize=11, fontweight='bold', color=stage['color'],
            bbox=dict(boxstyle="round,pad=0.4", facecolor='white', edgecolor=stage['color'], alpha=0.9))

# Set title and formatting
ax.set_title('Multi-Agent Orchestration Workflow\nSamaritan AI Harmony Engine Process Flow', 
             fontsize=16, fontweight='bold', pad=20)

# Remove axes
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz11_agent_orchestration.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Industry-Specific Solution Matrix
fig, ax = plt.subplots(figsize=(16, 10))

# Define industries and solutions
industries = ['Retail &\nE-commerce', 'Real Estate', 'Healthcare\n& Medical', 'Professional\nServices', 
              'Manufacturing', 'Hospitality', 'Automotive', 'Financial\nServices']

solutions = [
    'Dynamic Pricing',
    'Lead Scoring',
    'Inventory Optimization', 
    'Customer Segmentation',
    'Predictive Analytics',
    'Automated Reporting',
    'Compliance Monitoring',
    'Performance Dashboards'
]

# Solution applicability matrix (0-5 scale)
applicability_data = np.array([
    [5, 4, 5, 5, 4, 4, 3, 5],  # Dynamic Pricing
    [3, 5, 4, 5, 3, 4, 5, 4],  # Lead Scoring
    [5, 2, 4, 2, 5, 4, 4, 2],  # Inventory Optimization
    [5, 5, 5, 4, 3, 5, 4, 5],  # Customer Segmentation
    [4, 5, 5, 4, 5, 4, 4, 5],  # Predictive Analytics
    [4, 4, 5, 5, 4, 4, 4, 5],  # Automated Reporting
    [3, 3, 5, 4, 4, 3, 3, 5],  # Compliance Monitoring
    [5, 5, 4, 5, 5, 5, 5, 5]   # Performance Dashboards
])

# Create heatmap
im = ax.imshow(applicability_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=5)

# Set ticks and labels
ax.set_xticks(np.arange(len(industries)))
ax.set_yticks(np.arange(len(solutions)))
ax.set_xticklabels(industries, fontsize=11, fontweight='bold')
ax.set_yticklabels(solutions, fontsize=11, fontweight='bold')

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# Add text annotations
for i in range(len(solutions)):
    for j in range(len(industries)):
        value = applicability_data[i, j]
        text_color = 'white' if value < 2.5 else 'black'
        text = ax.text(j, i, value, ha="center", va="center", 
                      color=text_color, fontweight='bold', fontsize=12)

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
cbar.ax.set_ylabel('Solution Applicability Score', rotation=-90, va="bottom", fontweight='bold', fontsize=12)
cbar.set_ticks([0, 1, 2, 3, 4, 5])
cbar.set_ticklabels(['Not Applicable', 'Low', 'Moderate', 'High', 'Very High', 'Critical'])

# Set title and labels
ax.set_title('Industry-Specific Solution Matrix\nSamaritan AI Capability Mapping Across Verticals', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Industry Verticals', fontsize=12, fontweight='bold')
ax.set_ylabel('Solution Capabilities', fontsize=12, fontweight='bold')

# Add grid
ax.set_xticks(np.arange(len(industries)+1)-.5, minor=True)
ax.set_yticks(np.arange(len(solutions)+1)-.5, minor=True)
ax.grid(which="minor", color="white", linestyle='-', linewidth=2)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz12_industry_solutions.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 10, 11, and 12 created successfully!")
print("- viz10_samaritan_architecture.png: Samaritan AI Architecture Diagram")
print("- viz11_agent_orchestration.png: Multi-Agent Orchestration Workflow")
print("- viz12_industry_solutions.png: Industry-Specific Solution Matrix")

