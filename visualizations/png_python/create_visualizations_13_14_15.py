import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("viridis")

# Create Competitive Landscape Positioning
fig, ax = plt.subplots(figsize=(14, 10))

# Define competitors and their positioning
competitors = [
    {'name': 'Samaritan AI', 'x': 8.5, 'y': 8.5, 'size': 200, 'color': '#E74C3C'},
    {'name': 'Tableau', 'x': 6.0, 'y': 4.0, 'size': 300, 'color': '#3498DB'},
    {'name': 'Power BI', 'x': 5.5, 'y': 5.5, 'size': 280, 'color': '#F39C12'},
    {'name': 'Looker', 'x': 7.0, 'y': 3.5, 'size': 180, 'color': '#9B59B6'},
    {'name': 'Sisense', 'x': 4.5, 'y': 6.0, 'size': 160, 'color': '#27AE60'},
    {'name': 'Qlik Sense', 'x': 5.0, 'y': 4.5, 'size': 200, 'color': '#E67E22'},
    {'name': 'Domo', 'x': 6.5, 'y': 5.0, 'size': 140, 'color': '#34495E'},
    {'name': 'ThoughtSpot', 'x': 7.5, 'y': 6.5, 'size': 120, 'color': '#E91E63'},
    {'name': 'Traditional BI', 'x': 3.0, 'y': 3.0, 'size': 250, 'color': '#95A5A6'},
    {'name': 'Custom Solutions', 'x': 2.5, 'y': 7.0, 'size': 100, 'color': '#BDC3C7'}
]

# Create scatter plot
for comp in competitors:
    if comp['name'] == 'Samaritan AI':
        # Highlight Samaritan AI with special styling
        ax.scatter(comp['x'], comp['y'], s=comp['size'], c=comp['color'], 
                  alpha=0.8, edgecolors='black', linewidth=3, marker='*', zorder=5)
        ax.annotate(comp['name'], (comp['x'], comp['y']), xytext=(10, 10), 
                   textcoords='offset points', fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=comp['color'], alpha=0.8, edgecolor='black'))
    else:
        ax.scatter(comp['x'], comp['y'], s=comp['size'], c=comp['color'], 
                  alpha=0.7, edgecolors='black', linewidth=1)
        ax.annotate(comp['name'], (comp['x'], comp['y']), xytext=(5, 5), 
                   textcoords='offset points', fontsize=10, fontweight='bold')

# Add quadrant labels
ax.text(2, 9, 'High SMB Focus\nLow AI Integration', ha='center', va='center', 
        fontsize=12, fontweight='bold', style='italic', 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))

ax.text(8, 9, 'High SMB Focus\nHigh AI Integration', ha='center', va='center', 
        fontsize=12, fontweight='bold', style='italic',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.7))

ax.text(2, 1, 'Low SMB Focus\nLow AI Integration', ha='center', va='center', 
        fontsize=12, fontweight='bold', style='italic',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightcoral', alpha=0.7))

ax.text(8, 1, 'Low SMB Focus\nHigh AI Integration', ha='center', va='center', 
        fontsize=12, fontweight='bold', style='italic',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.7))

# Add quadrant dividers
ax.axhline(y=5, color='gray', linestyle='--', alpha=0.5, linewidth=2)
ax.axvline(x=5, color='gray', linestyle='--', alpha=0.5, linewidth=2)

# Customize the plot
ax.set_xlabel('AI Integration Level', fontsize=14, fontweight='bold')
ax.set_ylabel('SMB Market Focus', fontsize=14, fontweight='bold')
ax.set_title('Competitive Landscape Positioning\nBI Solutions Market Analysis', 
             fontsize=16, fontweight='bold', pad=20)

# Set axis limits and ticks
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks(range(0, 11, 2))
ax.set_yticks(range(0, 11, 2))

# Add grid
ax.grid(True, alpha=0.3)

# Add legend for bubble sizes
size_legend = [
    {'size': 100, 'label': 'Small Market Share'},
    {'size': 200, 'label': 'Medium Market Share'},
    {'size': 300, 'label': 'Large Market Share'}
]

for i, item in enumerate(size_legend):
    ax.scatter([], [], s=item['size'], c='gray', alpha=0.7, label=item['label'])

ax.legend(loc='upper left', title='Market Share', fontsize=10)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz13_competitive_landscape.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Implementation Timeline and Milestones
fig, ax = plt.subplots(figsize=(16, 8))

# Define implementation phases
phases = [
    {'name': 'Phase 1: Assessment & Planning', 'start': 0, 'duration': 4, 'color': '#3498DB'},
    {'name': 'Phase 2: Data Integration Setup', 'start': 2, 'duration': 6, 'color': '#E74C3C'},
    {'name': 'Phase 3: Core Analytics Deployment', 'start': 6, 'duration': 8, 'color': '#F39C12'},
    {'name': 'Phase 4: Advanced Features', 'start': 12, 'duration': 6, 'color': '#27AE60'},
    {'name': 'Phase 5: Optimization & Scaling', 'start': 16, 'duration': 8, 'color': '#9B59B6'}
]

# Define milestones
milestones = [
    {'name': 'Requirements Analysis Complete', 'week': 3, 'y': 5},
    {'name': 'Data Sources Connected', 'week': 7, 'y': 4},
    {'name': 'First Reports Generated', 'week': 10, 'y': 3},
    {'name': 'Predictive Models Active', 'week': 15, 'y': 2},
    {'name': 'Full Platform Operational', 'week': 20, 'y': 1},
    {'name': 'Performance Optimization Complete', 'week': 24, 'y': 0}
]

# Create Gantt chart
for i, phase in enumerate(phases):
    ax.barh(i, phase['duration'], left=phase['start'], height=0.6, 
            color=phase['color'], alpha=0.8, edgecolor='black')
    
    # Add phase labels
    ax.text(phase['start'] + phase['duration']/2, i, phase['name'], 
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Add milestones
for milestone in milestones:
    ax.scatter(milestone['week'], milestone['y'], s=150, c='red', marker='D', 
              edgecolors='black', linewidth=2, zorder=5)
    ax.text(milestone['week'], milestone['y'] + 0.3, milestone['name'], 
            ha='center', va='bottom', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Customize the plot
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([f"Phase {i+1}" for i in range(len(phases))])
ax.set_xlabel('Implementation Timeline (Weeks)', fontsize=12, fontweight='bold')
ax.set_ylabel('Implementation Phases', fontsize=12, fontweight='bold')
ax.set_title('Implementation Timeline and Milestones\nSamaritan AI Deployment Roadmap', 
             fontsize=16, fontweight='bold', pad=20)

# Add grid
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(0, 26)

# Add timeline markers
for week in range(0, 27, 4):
    ax.axvline(x=week, color='gray', linestyle=':', alpha=0.5)
    ax.text(week, -0.8, f'Week {week}', ha='center', va='top', fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz14_implementation_timeline.png', dpi=300, bbox_inches='tight')
plt.close()

# Create Success Metrics Dashboard Mockup
fig = plt.figure(figsize=(16, 12))

# Create a 2x3 grid for different metrics
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# ROI Trend
ax1 = fig.add_subplot(gs[0, :2])
months = np.arange(1, 13)
roi_values = [0, 5, 15, 28, 45, 65, 88, 115, 145, 180, 220, 265]
ax1.plot(months, roi_values, 'o-', linewidth=3, markersize=8, color='#27AE60')
ax1.fill_between(months, roi_values, alpha=0.3, color='#27AE60')
ax1.set_title('ROI Progression (%)', fontweight='bold', fontsize=12)
ax1.set_xlabel('Months Since Implementation')
ax1.set_ylabel('ROI (%)')
ax1.grid(True, alpha=0.3)
ax1.text(6, 200, f'Current ROI: {roi_values[-1]}%', fontsize=14, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen'))

# Decision Speed Improvement
ax2 = fig.add_subplot(gs[0, 2])
categories = ['Before', 'After']
decision_times = [168, 15]  # hours
colors = ['#E74C3C', '#27AE60']
bars = ax2.bar(categories, decision_times, color=colors, alpha=0.8)
ax2.set_title('Decision Speed\n(Hours)', fontweight='bold', fontsize=12)
ax2.set_ylabel('Hours')
for bar, value in zip(bars, decision_times):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             f'{value}h', ha='center', va='bottom', fontweight='bold')

# Data Quality Score
ax3 = fig.add_subplot(gs[1, 0])
quality_score = 94
theta = np.linspace(0, 2*np.pi, 100)
r = np.ones_like(theta)
ax3 = plt.subplot(gs[1, 0], projection='polar')
ax3.fill_between(theta, 0, r, alpha=0.3, color='#3498DB')
ax3.plot(theta[:int(quality_score)], r[:int(quality_score)], linewidth=8, color='#27AE60')
ax3.set_ylim(0, 1)
ax3.set_title('Data Quality Score\n94%', fontweight='bold', fontsize=12, pad=20)
ax3.set_rticks([])
ax3.set_thetagrids([])

# User Adoption Rate
ax4 = fig.add_subplot(gs[1, 1])
adoption_data = [25, 45, 68, 82, 91, 95]
weeks = range(1, 7)
ax4.plot(weeks, adoption_data, 's-', linewidth=3, markersize=8, color='#9B59B6')
ax4.fill_between(weeks, adoption_data, alpha=0.3, color='#9B59B6')
ax4.set_title('User Adoption Rate (%)', fontweight='bold', fontsize=12)
ax4.set_xlabel('Weeks')
ax4.set_ylabel('Adoption (%)')
ax4.grid(True, alpha=0.3)
ax4.set_ylim(0, 100)

# Cost Savings
ax5 = fig.add_subplot(gs[1, 2])
cost_categories = ['Manual\nReporting', 'Data\nErrors', 'Delayed\nDecisions', 'IT\nMaintenance']
savings = [15000, 8500, 12000, 6500]
colors = ['#E74C3C', '#F39C12', '#3498DB', '#27AE60']
bars = ax5.bar(cost_categories, savings, color=colors, alpha=0.8)
ax5.set_title('Monthly Cost Savings ($)', fontweight='bold', fontsize=12)
ax5.set_ylabel('Savings ($)')
for bar, value in zip(bars, savings):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
             f'${value:,}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# System Performance Metrics
ax6 = fig.add_subplot(gs[2, :])
metrics = ['Query\nResponse', 'Data\nFreshness', 'System\nUptime', 'Report\nGeneration', 'Alert\nAccuracy']
current_values = [95, 98, 99.8, 92, 96]
target_values = [90, 95, 99.5, 85, 90]

x = np.arange(len(metrics))
width = 0.35

bars1 = ax6.bar(x - width/2, target_values, width, label='Target', color='#BDC3C7', alpha=0.8)
bars2 = ax6.bar(x + width/2, current_values, width, label='Current', color='#27AE60', alpha=0.8)

ax6.set_title('System Performance Metrics (%)', fontweight='bold', fontsize=12)
ax6.set_ylabel('Performance (%)')
ax6.set_xticks(x)
ax6.set_xticklabels(metrics)
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# Add values on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height}%',
                ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.suptitle('Success Metrics Dashboard\nSamaritan AI Performance Indicators', 
             fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig('/home/ubuntu/viz15_success_metrics.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations 13, 14, and 15 created successfully!")
print("- viz13_competitive_landscape.png: Competitive Landscape Positioning")
print("- viz14_implementation_timeline.png: Implementation Timeline and Milestones")
print("- viz15_success_metrics.png: Success Metrics Dashboard Mockup")

