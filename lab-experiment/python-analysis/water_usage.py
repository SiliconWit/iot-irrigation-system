import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style
sns.set_style("whitegrid")

# Data
stages = ['Initial', 'Development', 'Mid-Season', 'Late-Season']
estimated_water = [452.33, 103.9, 0, 0]
utilized_water = [432.15, 76, 0, 0]

# Set figure size and DPI for high quality output
plt.figure(figsize=(12, 7), dpi=300)

# Configure plot style
ax = plt.gca()
ax.set_axisbelow(True)

# Create graph paper effect
# Major grid (darker lines)
plt.grid(which='major', color='#E0E0E0', linestyle='-', linewidth=0.8)

# Minor grid (lighter lines)
ax.grid(which='minor', color='#F5F5F5', linestyle='-', linewidth=0.5)
ax.minorticks_on()

# Create the plot
x = np.arange(len(stages))
plt.plot(x, estimated_water, marker='o', linewidth=2.5, markersize=10, 
         label='Estimated Water', color='#2E86C1', linestyle='-')
plt.plot(x, utilized_water, marker='s', linewidth=2.5, markersize=10,
         label='Utilized Water', color='#E67E22', linestyle='-')

# Add labels and title with adjusted positioning
plt.xlabel('Growth Stages', fontsize=12, fontweight='bold')
plt.ylabel('Water Usage (mm)', fontsize=12, fontweight='bold')
plt.title('Water Usage Comparison Across Growth Stages\n(37-Experimental Days)', 
         fontsize=14, fontweight='bold', y=1.05)

# Customize x-axis
plt.xticks(x, stages, fontsize=11)
plt.yticks(fontsize=11)

# Add value labels
for i, (est, util) in enumerate(zip(estimated_water, utilized_water)):
    if est > 0:
        plt.annotate(f'{est}', (i, est), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=10)
    if util > 0:
        plt.annotate(f'{util}', (i, util), textcoords="offset points", 
                    xytext=(0,-15), ha='center', fontsize=10)

# Customize legend
plt.legend(loc='upper right', fontsize=11, framealpha=0.95, 
          edgecolor='gray', fancybox=True)

# Set y-axis limits with padding
plt.ylim(-20, max(max(estimated_water), max(utilized_water)) + 50)

# Set background color
ax.set_facecolor('white')
plt.gcf().set_facecolor('white')

# Add border
for spine in ax.spines.values():
    spine.set_color('gray')
    spine.set_linewidth(0.5)

# Adjust layout and margins
plt.subplots_adjust(top=0.9, bottom=0.15, left=0.1, right=0.95)

# Save the plot as a high-resolution PNG
plt.savefig('water_usage_comparison.png', dpi=300, bbox_inches='tight')
plt.close()