import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create SMB Data Challenge Severity Matrix
fig, ax = plt.subplots(figsize=(12, 8))

# Define challenge types and business impact categories
challenges = [
    'Data Source\nFragmentation',
    'Integration\nComplexity', 
    'Quality &\nReliability',
    'Schema\nEvolution',
    'Real-time\nProcessing',
    'Governance &\nLineage',
    'Resource\nConstraints',
    'Technical\nExpertise Gap'
]

impact_categories = [
    'Revenue\nImpact',
    'Operational\nEfficiency', 
    'Decision\nLatency',
    'Competitive\nDisadvantage',
    'Compliance\nRisk'
]

# Severity matrix (1-5 scale, 5 being highest severity)
severity_data = np.array([
    [4, 5, 4, 4, 3],  # Data Source Fragmentation
    [3, 4, 5, 3, 2],  # Integration Complexity
    [5, 4, 5, 4, 4],  # Quality & Reliability
    [3, 3, 4, 2, 3],  # Schema Evolution
    [4, 5, 5, 4, 2],  # Real-time Processing
    [2, 3, 3, 2, 5],  # Governance & Lineage
    [5, 5, 4, 5, 3],  # Resource Constraints
    [4, 4, 4, 5, 2]   # Technical Expertise Gap
])

# Create heatmap
im = ax.imshow(severity_data, cmap='RdYlBu_r', aspect='auto', vmin=1, vmax=5)

# Set ticks and labels
ax.set_xticks(np.arange(len(impact_categories)))
ax.set_yticks(np.arange(len(challenges)))
ax.set_xticklabels(impact_categories, fontsize=10, fontweight='bold')
ax.set_yticklabels(challenges, fontsize=10, fontweight='bold')

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# Add text annotations
for i in range(len(challenges)):
    for j in range(len(impact_categories)):
        text = ax.text(j, i, severity_data[i, j],
                      ha="center", va="center", color="white", fontweight='bold', fontsize=12)

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
cbar.ax.set_ylabel('Severity Level', rotation=-90, va="bottom", fontweight='bold', fontsize=12)
cbar.set_ticks([1, 2, 3, 4, 5])
cbar.set_ticklabels(['Low', 'Moderate', 'High', 'Severe', 'Critical'])

# Set title and labels
ax.set_title('SMB Data Challenge Severity Matrix\nImpact Assessment Across Business Dimensions', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Business Impact Categories', fontsize=12, fontweight='bold')
ax.set_ylabel('Data Challenge Types', fontsize=12, fontweight='bold')

# Add grid
ax.set_xticks(np.arange(len(impact_categories)+1)-.5, minor=True)
ax.set_yticks(np.arange(len(challenges)+1)-.5, minor=True)
ax.grid(which="minor", color="white", linestyle='-', linewidth=2)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz1_smb_challenge_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Samaritan AI ROI Projection Chart
fig, ax = plt.subplots(figsize=(12, 8))

# Time periods (months)
months = np.arange(0, 37, 3)  # 3 years, quarterly data points
month_labels = ['Baseline', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1 Y2', 'Q2 Y2', 'Q3 Y2', 'Q4 Y2', 'Q1 Y3', 'Q2 Y3', 'Q3 Y3', 'Q4 Y3']

# ROI projections (percentage)
traditional_bi_roi = [0, -5, -3, 2, 8, 15, 22, 28, 35, 40, 45, 48, 50]
samaritan_ai_roi = [0, -10, 5, 25, 45, 75, 110, 150, 195, 245, 300, 360, 425]

# Investment costs (negative ROI initially)
investment_cost = [0, -15, -20, -18, -15, -10, -5, 0, 5, 10, 15, 20, 25]

# Create the plot
ax.plot(months, traditional_bi_roi, 'o-', linewidth=3, markersize=8, 
        color='#FF6B6B', label='Traditional BI Solutions', alpha=0.8)
ax.plot(months, samaritan_ai_roi, 's-', linewidth=3, markersize=8, 
        color='#4ECDC4', label='Samaritan AI Platform', alpha=0.8)
ax.plot(months, investment_cost, '^-', linewidth=2, markersize=6, 
        color='#95A5A6', label='Initial Investment Cost', alpha=0.7, linestyle='--')

# Fill areas under curves
ax.fill_between(months, traditional_bi_roi, alpha=0.2, color='#FF6B6B')
ax.fill_between(months, samaritan_ai_roi, alpha=0.2, color='#4ECDC4')

# Add break-even line
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
ax.text(18, 5, 'Break-even Line', fontsize=10, ha='center', alpha=0.7)

# Customize the plot
ax.set_xlabel('Implementation Timeline', fontsize=12, fontweight='bold')
ax.set_ylabel('Return on Investment (%)', fontsize=12, fontweight='bold')
ax.set_title('Samaritan AI ROI Projection vs Traditional BI Solutions\nThree-Year Performance Comparison', 
             fontsize=16, fontweight='bold', pad=20)

# Set x-axis labels
ax.set_xticks(months)
ax.set_xticklabels(month_labels, rotation=45, ha='right')

# Add grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

# Add legend
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

# Add annotations for key milestones
ax.annotate('Samaritan AI\nBreak-even', xy=(6, 25), xytext=(8, 80),
            arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=2),
            fontsize=10, ha='center', fontweight='bold', color='#4ECDC4')

ax.annotate('425% ROI\nat 3 Years', xy=(36, 425), xytext=(30, 350),
            arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=2),
            fontsize=10, ha='center', fontweight='bold', color='#4ECDC4')

# Set y-axis limits
ax.set_ylim(-30, 450)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz2_samaritan_roi_projection.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 1 and 2 created successfully!")
print("- viz1_smb_challenge_matrix.png: SMB Data Challenge Severity Matrix")
print("- viz2_samaritan_roi_projection.png: Samaritan AI ROI Projection Chart")

