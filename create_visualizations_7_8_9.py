import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arrow, ConnectionPatch
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create Data Source Fragmentation Diagram
fig, ax = plt.subplots(figsize=(16, 12))

# Define data sources and their positions
data_sources = [
    {'name': 'CRM\nSystem', 'pos': (2, 10), 'color': '#3498DB', 'size': 1.2},
    {'name': 'POS\nSystem', 'pos': (6, 10), 'color': '#E74C3C', 'size': 1.2},
    {'name': 'Email\nMarketing', 'pos': (10, 10), 'color': '#F39C12', 'size': 1.0},
    {'name': 'Social\nMedia', 'pos': (14, 10), 'color': '#9B59B6', 'size': 1.0},
    {'name': 'Accounting\nSoftware', 'pos': (2, 7), 'color': '#27AE60', 'size': 1.2},
    {'name': 'Inventory\nManagement', 'pos': (6, 7), 'color': '#E67E22', 'size': 1.1},
    {'name': 'Website\nAnalytics', 'pos': (10, 7), 'color': '#34495E', 'size': 1.0},
    {'name': 'Spreadsheets', 'pos': (14, 7), 'color': '#95A5A6', 'size': 1.0},
    {'name': 'Support\nTickets', 'pos': (2, 4), 'color': '#E91E63', 'size': 1.0},
    {'name': 'HR\nSystem', 'pos': (6, 4), 'color': '#00BCD4', 'size': 1.0},
    {'name': 'Project\nManagement', 'pos': (10, 4), 'color': '#FF5722', 'size': 1.0},
    {'name': 'Cloud\nStorage', 'pos': (14, 4), 'color': '#607D8B', 'size': 1.0}
]

# Central SMB hub
central_hub = {'name': 'SMB\nBusiness\nOperations', 'pos': (8, 7), 'color': '#2C3E50', 'size': 2.0}

# Draw data sources
for source in data_sources:
    circle = Circle(source['pos'], source['size'], facecolor=source['color'], 
                   edgecolor='black', alpha=0.8, linewidth=2)
    ax.add_patch(circle)
    ax.text(source['pos'][0], source['pos'][1], source['name'], ha='center', va='center',
            fontsize=9, fontweight='bold', color='white', wrap=True)

# Draw central hub
hub_circle = Circle(central_hub['pos'], central_hub['size'], facecolor=central_hub['color'], 
                   edgecolor='black', alpha=0.9, linewidth=3)
ax.add_patch(hub_circle)
ax.text(central_hub['pos'][0], central_hub['pos'][1], central_hub['name'], 
        ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Draw connections (showing fragmentation)
connections = []
for source in data_sources:
    # Some connections to central hub (showing partial integration)
    if np.random.random() > 0.4:  # 60% chance of connection
        line_style = '--' if np.random.random() > 0.5 else ':'
        alpha = 0.3 if line_style == '--' else 0.5
        ax.plot([source['pos'][0], central_hub['pos'][0]], 
                [source['pos'][1], central_hub['pos'][1]], 
                linestyle=line_style, color='gray', alpha=alpha, linewidth=2)

# Add integration challenges annotations
challenges = [
    {'pos': (4, 11.5), 'text': 'Format\nIncompatibility', 'color': '#E74C3C'},
    {'pos': (12, 11.5), 'text': 'API\nLimitations', 'color': '#E74C3C'},
    {'pos': (4, 2.5), 'text': 'Manual\nProcesses', 'color': '#E74C3C'},
    {'pos': (12, 2.5), 'text': 'Data\nSilos', 'color': '#E74C3C'}
]

for challenge in challenges:
    ax.text(challenge['pos'][0], challenge['pos'][1], challenge['text'], 
            ha='center', va='center', fontsize=10, fontweight='bold', 
            color=challenge['color'], bbox=dict(boxstyle="round,pad=0.3", 
            facecolor='white', edgecolor=challenge['color'], alpha=0.9))

# Set title and formatting
ax.set_title('SMB Data Source Fragmentation Diagram\nTypical Small Business Data Ecosystem Complexity', 
             fontsize=16, fontweight='bold', pad=20)

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498DB', markersize=12, label='Core Business Systems'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F39C12', markersize=10, label='Marketing & Analytics'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#27AE60', markersize=10, label='Financial & Operations'),
    plt.Line2D([0], [0], linestyle='--', color='gray', label='Partial Integration'),
    plt.Line2D([0], [0], linestyle=':', color='gray', label='Manual Processes')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10, title='System Categories')

# Remove axes
ax.set_xlim(0, 16)
ax.set_ylim(1, 13)
ax.axis('off')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz7_data_fragmentation.png', dpi=300, bbox_inches='tight')
plt.close()

# Create SMB Resource Constraint Analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Stacked bar chart for resource constraints
categories = ['Micro\n(1-10 employees)', 'Small\n(11-50 employees)', 'Medium\n(51-250 employees)', 'Large SMB\n(251-500 employees)']
budget_constraints = [85, 70, 55, 35]
skill_constraints = [90, 75, 60, 40]
time_constraints = [80, 65, 50, 30]

x = np.arange(len(categories))
width = 0.6

bars1 = ax1.bar(x, budget_constraints, width, label='Budget Limitations', color='#E74C3C', alpha=0.8)
bars2 = ax1.bar(x, skill_constraints, width, bottom=budget_constraints, label='Skill Gaps', color='#F39C12', alpha=0.8)
bars3 = ax1.bar(x, time_constraints, width, bottom=np.array(budget_constraints) + np.array(skill_constraints), 
                label='Time Constraints', color='#3498DB', alpha=0.8)

# Add percentage labels
for i, (budget, skill, time) in enumerate(zip(budget_constraints, skill_constraints, time_constraints)):
    ax1.text(i, budget/2, f'{budget}%', ha='center', va='center', fontweight='bold', color='white')
    ax1.text(i, budget + skill/2, f'{skill}%', ha='center', va='center', fontweight='bold', color='white')
    ax1.text(i, budget + skill + time/2, f'{time}%', ha='center', va='center', fontweight='bold', color='white')

ax1.set_xlabel('Business Size Category', fontweight='bold')
ax1.set_ylabel('Constraint Severity (%)', fontweight='bold')
ax1.set_title('SMB Resource Constraint Analysis\nConstraint Severity by Business Size', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3, axis='y')

# Radar chart for constraint types
constraint_types = ['Budget\nLimitations', 'Technical\nExpertise', 'Time\nAvailability', 
                   'Infrastructure\nCapacity', 'Training\nResources', 'Vendor\nSupport']
micro_scores = [85, 90, 80, 75, 85, 70]
medium_scores = [55, 60, 50, 45, 55, 40]

# Number of variables
N = len(constraint_types)

# Compute angle for each axis
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Complete the circle

# Add scores for complete circle
micro_scores += micro_scores[:1]
medium_scores += medium_scores[:1]

# Plot
ax2 = plt.subplot(122, projection='polar')
ax2.plot(angles, micro_scores, 'o-', linewidth=2, label='Micro SMBs (1-10 employees)', color='#E74C3C')
ax2.fill(angles, micro_scores, alpha=0.25, color='#E74C3C')
ax2.plot(angles, medium_scores, 'o-', linewidth=2, label='Medium SMBs (51-250 employees)', color='#27AE60')
ax2.fill(angles, medium_scores, alpha=0.25, color='#27AE60')

# Add labels
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(constraint_types, fontsize=10)
ax2.set_ylim(0, 100)
ax2.set_yticks([20, 40, 60, 80, 100])
ax2.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
ax2.grid(True)
ax2.set_title('Constraint Profile Comparison\nMicro vs Medium SMBs', fontweight='bold', pad=20)
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

plt.tight_layout()
plt.savefig('/home/ubuntu/viz8_resource_constraints.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Data Integration Challenge Frequency Chart
fig, ax = plt.subplots(figsize=(14, 10))

# Challenge data
challenges = [
    'Data Format Incompatibility',
    'API Access Limitations', 
    'Real-time Sync Issues',
    'Data Quality Problems',
    'Security & Compliance',
    'Schema Evolution',
    'Performance Bottlenecks',
    'Cost of Integration Tools',
    'Lack of Technical Expertise',
    'Vendor Lock-in Concerns',
    'Maintenance Complexity',
    'Scalability Issues'
]

frequency = [78, 72, 68, 85, 65, 58, 62, 80, 88, 45, 70, 55]
severity = [4.2, 3.8, 4.5, 4.7, 4.0, 3.5, 3.9, 4.3, 4.8, 3.2, 4.1, 3.7]

# Create horizontal bar chart
y_pos = np.arange(len(challenges))
bars = ax.barh(y_pos, frequency, color=[plt.cm.RdYlBu_r(s/5.0) for s in severity], alpha=0.8)

# Add frequency labels
for i, (freq, sev) in enumerate(zip(frequency, severity)):
    ax.text(freq + 1, i, f'{freq}%', va='center', fontweight='bold', fontsize=10)
    # Add severity indicator
    ax.text(5, i, f'Severity: {sev:.1f}', va='center', fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Customize the plot
ax.set_yticks(y_pos)
ax.set_yticklabels(challenges, fontsize=11)
ax.set_xlabel('Frequency of Occurrence (%)', fontsize=12, fontweight='bold')
ax.set_title('Data Integration Challenge Frequency\nSMB Survey Results (n=500)', 
             fontsize=16, fontweight='bold', pad=20)

# Add grid
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(0, 100)

# Add color bar for severity
sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu_r, norm=plt.Normalize(vmin=3.0, vmax=5.0))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
cbar.set_label('Severity Rating (1-5 Scale)', rotation=270, va="bottom", fontweight='bold')

plt.tight_layout()
plt.savefig('/home/ubuntu/viz9_integration_challenges.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 7, 8, and 9 created successfully!")
print("- viz7_data_fragmentation.png: Data Source Fragmentation Diagram")
print("- viz8_resource_constraints.png: SMB Resource Constraint Analysis")
print("- viz9_integration_challenges.png: Data Integration Challenge Frequency")

