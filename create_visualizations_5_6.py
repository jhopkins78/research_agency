import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create Traditional BI vs Agentic AI Comparison Matrix
fig, ax = plt.subplots(figsize=(16, 10))

# Define comparison categories and systems
categories = [
    'Data Integration\nCapability',
    'Real-time\nProcessing',
    'Predictive\nAnalytics',
    'Automated\nInsights',
    'Natural Language\nInterface',
    'Scalability &\nFlexibility',
    'Implementation\nComplexity',
    'Cost of\nOwnership',
    'Learning\nCurve',
    'Customization\nOptions'
]

traditional_bi_scores = [3, 2, 3, 2, 1, 3, 2, 2, 3, 3]
agentic_ai_scores = [5, 5, 5, 5, 5, 5, 4, 4, 4, 5]

# Create horizontal bar chart
y_pos = np.arange(len(categories))
bar_height = 0.35

bars1 = ax.barh(y_pos - bar_height/2, traditional_bi_scores, bar_height, 
                label='Traditional BI Solutions', color='#FF6B6B', alpha=0.8)
bars2 = ax.barh(y_pos + bar_height/2, agentic_ai_scores, bar_height,
                label='Agentic AI Systems', color='#4ECDC4', alpha=0.8)

# Add value labels on bars
for i, (trad, ai) in enumerate(zip(traditional_bi_scores, agentic_ai_scores)):
    ax.text(trad + 0.1, i - bar_height/2, str(trad), va='center', fontweight='bold', fontsize=10)
    ax.text(ai + 0.1, i + bar_height/2, str(ai), va='center', fontweight='bold', fontsize=10)

# Customize the plot
ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=11, fontweight='bold')
ax.set_xlabel('Capability Score (1-5 Scale)', fontsize=12, fontweight='bold')
ax.set_title('Traditional BI vs Agentic AI Comparison Matrix\nCapability Assessment Across Key Dimensions', 
             fontsize=16, fontweight='bold', pad=20)

# Add legend
ax.legend(loc='lower right', fontsize=12, framealpha=0.9)

# Add grid
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(0, 6)

# Add performance indicators
for i, (trad, ai) in enumerate(zip(traditional_bi_scores, agentic_ai_scores)):
    improvement = ((ai - trad) / trad) * 100 if trad > 0 else 0
    if improvement > 50:
        ax.text(5.5, i, f'+{improvement:.0f}%', va='center', ha='center', 
                fontweight='bold', color='green', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('/home/ubuntu/viz5_bi_comparison_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Create AI Evolution Timeline
fig, ax = plt.subplots(figsize=(16, 8))

# Timeline data
years = [1950, 1960, 1980, 1990, 2000, 2010, 2015, 2020, 2023, 2025]
milestones = [
    'Rule-Based\nSystems',
    'Expert\nSystems',
    'Machine\nLearning',
    'Neural\nNetworks',
    'Data Mining\n& Analytics',
    'Big Data\n& Cloud',
    'Deep Learning\n& AI',
    'Large Language\nModels',
    'Agentic AI\nSystems',
    'Multi-Agent\nOrchestration'
]

# Technology categories
categories = [
    'Foundation', 'Foundation', 'Statistical', 'Statistical', 
    'Analytics', 'Infrastructure', 'AI/ML', 'AI/ML', 'Agentic', 'Agentic'
]

# Color mapping
color_map = {
    'Foundation': '#95A5A6',
    'Statistical': '#3498DB', 
    'Analytics': '#E74C3C',
    'Infrastructure': '#F39C12',
    'AI/ML': '#9B59B6',
    'Agentic': '#27AE60'
}

colors = [color_map[cat] for cat in categories]

# Create timeline
for i, (year, milestone, color) in enumerate(zip(years, milestones, colors)):
    # Draw timeline point
    ax.scatter(year, 1, s=200, c=color, alpha=0.8, edgecolors='black', linewidth=2, zorder=3)
    
    # Add milestone text
    y_offset = 1.3 if i % 2 == 0 else 0.7
    ax.text(year, y_offset, milestone, ha='center', va='center', fontsize=10, 
            fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7))
    
    # Draw connecting line
    ax.plot([year, year], [1, y_offset-0.1 if y_offset > 1 else y_offset+0.1], 
            color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Draw main timeline
ax.plot(years, [1]*len(years), color='black', linewidth=3, alpha=0.7, zorder=1)

# Add era labels
era_data = [
    {'start': 1950, 'end': 1990, 'label': 'Early AI Era', 'color': '#BDC3C7'},
    {'start': 1990, 'end': 2015, 'label': 'Data Analytics Era', 'color': '#85C1E9'},
    {'start': 2015, 'end': 2025, 'label': 'Intelligent Systems Era', 'color': '#82E0AA'}
]

for era in era_data:
    ax.axvspan(era['start'], era['end'], alpha=0.2, color=era['color'])
    ax.text((era['start'] + era['end'])/2, 0.5, era['label'], ha='center', va='center',
            fontsize=12, fontweight='bold', style='italic')

# Customize plot
ax.set_xlim(1945, 2030)
ax.set_ylim(0.3, 1.7)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_title('AI Evolution Timeline\nFrom Rule-Based Systems to Agentic AI Orchestration', 
             fontsize=16, fontweight='bold', pad=20)

# Remove y-axis
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Add legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                             markersize=10, label=cat) for cat, color in color_map.items()]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, title='Technology Categories')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz6_ai_evolution_timeline.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 5 and 6 created successfully!")
print("- viz5_bi_comparison_matrix.png: Traditional BI vs Agentic AI Comparison Matrix")
print("- viz6_ai_evolution_timeline.png: AI Evolution Timeline")

