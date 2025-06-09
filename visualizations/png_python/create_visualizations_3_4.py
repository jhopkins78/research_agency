import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create Research Methodology Flowchart
fig, ax = plt.subplots(figsize=(14, 10))

# Define flowchart elements
boxes = [
    {'name': 'Literature Review\n& Market Analysis', 'pos': (2, 8), 'color': '#3498DB'},
    {'name': 'UCSB Academic\nResearch Integration', 'pos': (6, 8), 'color': '#3498DB'},
    {'name': 'Industry Data\nCollection', 'pos': (10, 8), 'color': '#3498DB'},
    {'name': 'Technical Documentation\nAnalysis', 'pos': (2, 6), 'color': '#E74C3C'},
    {'name': 'Samaritan AI\nArchitecture Review', 'pos': (6, 6), 'color': '#E74C3C'},
    {'name': 'Competitive\nLandscape Analysis', 'pos': (10, 6), 'color': '#E74C3C'},
    {'name': 'SMB Challenge\nIdentification', 'pos': (2, 4), 'color': '#F39C12'},
    {'name': 'Solution Capability\nMapping', 'pos': (6, 4), 'color': '#F39C12'},
    {'name': 'ROI & Performance\nModeling', 'pos': (10, 4), 'color': '#F39C12'},
    {'name': 'Synthesis &\nRecommendations', 'pos': (4, 2), 'color': '#27AE60'},
    {'name': 'Report Generation\n& Validation', 'pos': (8, 2), 'color': '#27AE60'}
]

# Draw boxes
for box in boxes:
    rect = FancyBboxPatch((box['pos'][0]-0.8, box['pos'][1]-0.4), 1.6, 0.8,
                         boxstyle="round,pad=0.1", facecolor=box['color'], 
                         edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    ax.text(box['pos'][0], box['pos'][1], box['name'], ha='center', va='center',
            fontsize=9, fontweight='bold', color='white', wrap=True)

# Draw arrows
arrows = [
    # Phase 1 to Phase 2
    ((2, 7.6), (2, 6.4)),
    ((6, 7.6), (6, 6.4)),
    ((10, 7.6), (10, 6.4)),
    # Phase 2 to Phase 3
    ((2, 5.6), (2, 4.4)),
    ((6, 5.6), (6, 4.4)),
    ((10, 5.6), (10, 4.4)),
    # Phase 3 to Phase 4
    ((2.8, 3.6), (3.2, 2.4)),
    ((6, 3.6), (6, 2.4)),
    ((9.2, 3.6), (8.8, 2.4)),
    # Final connection
    ((4.8, 2), (7.2, 2))
]

for start, end in arrows:
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', lw=2, color='#2C3E50'))

# Add phase labels
phase_labels = [
    {'text': 'Phase 1: Data Collection', 'pos': (6, 9), 'color': '#3498DB'},
    {'text': 'Phase 2: Technical Analysis', 'pos': (6, 7), 'color': '#E74C3C'},
    {'text': 'Phase 3: Challenge-Solution Mapping', 'pos': (6, 5), 'color': '#F39C12'},
    {'text': 'Phase 4: Synthesis & Reporting', 'pos': (6, 3), 'color': '#27AE60'}
]

for label in phase_labels:
    ax.text(label['pos'][0], label['pos'][1], label['text'], ha='center', va='center',
            fontsize=12, fontweight='bold', color=label['color'],
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=label['color'], alpha=0.9))

# Set title and formatting
ax.set_title('Research Methodology Flowchart\nSystematic Approach to SMB Data Intelligence Analysis', 
             fontsize=16, fontweight='bold', pad=20)

# Remove axes
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz3_research_methodology.png', dpi=300, bbox_inches='tight')
plt.close()

# Create SMB Market Segmentation Analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Pie chart for market segments
segments = ['Service-Based\nBusinesses', 'Retail &\nE-commerce', 'Manufacturing\n& Production', 
           'Professional\nServices', 'Healthcare\n& Medical', 'Technology\n& Software', 'Other']
sizes = [32, 24, 18, 12, 8, 4, 2]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=segments, colors=colors,
                                  autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})

# Enhance the pie chart
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax1.set_title('SMB Market Segmentation by Industry\n(% of Total SMB Market)', 
              fontsize=14, fontweight='bold', pad=20)

# Bar chart for data complexity by segment
segments_short = ['Service', 'Retail', 'Manufacturing', 'Professional', 'Healthcare', 'Technology', 'Other']
data_complexity = [3.2, 4.1, 4.8, 3.8, 4.5, 4.9, 3.0]
integration_difficulty = [2.8, 4.3, 4.6, 3.5, 4.2, 4.7, 2.9]
resource_constraints = [4.2, 3.8, 3.5, 3.9, 4.0, 3.2, 4.1]

x = np.arange(len(segments_short))
width = 0.25

bars1 = ax2.bar(x - width, data_complexity, width, label='Data Complexity', color='#FF6B6B', alpha=0.8)
bars2 = ax2.bar(x, integration_difficulty, width, label='Integration Difficulty', color='#4ECDC4', alpha=0.8)
bars3 = ax2.bar(x + width, resource_constraints, width, label='Resource Constraints', color='#45B7D1', alpha=0.8)

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Industry Segments', fontweight='bold')
ax2.set_ylabel('Challenge Severity (1-5 Scale)', fontweight='bold')
ax2.set_title('Data Challenge Severity by Industry Segment\nComparative Analysis of Key Constraints', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(segments_short, rotation=45, ha='right')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 5.5)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz4_smb_market_segmentation.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 3 and 4 created successfully!")
print("- viz3_research_methodology.png: Research Methodology Flowchart")
print("- viz4_smb_market_segmentation.png: SMB Market Segmentation Analysis")

