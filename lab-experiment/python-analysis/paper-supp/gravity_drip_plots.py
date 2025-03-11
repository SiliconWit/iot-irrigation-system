import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mtick
import os

# Set the style for publication-quality figures, using system fonts
plt.style.use('seaborn-whitegrid')
# Use a generic font family that's available on most systems
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18
plt.rcParams['figure.figsize'] = (10, 6)

def create_water_usage_data():
    """
    Create the water usage dataset for monoculture and intercropping systems
    using actual calculated values.
    """
    # Data from the program output (37-Day Experimental Period)
    systems = [
        "Beans (Monoculture)", 
        "Maize (Monoculture)", 
        "Onions (Monoculture)",
        "Maize + Beans (50:50)",
        "Onions + Beans (50:50)",
        "Maize + Onions (50:50)"
    ]
    
    # Actual calculated values from the program output
    initial_mm = [8.460, 12.750, 11.780, 10.194, 9.713, 11.738]
    dev_mm = [24.210, 21.280, 24.510, 19.476, 20.736, 19.405]
    total_mm = [32.670, 34.030, 36.290, 29.670, 30.449, 31.143]
    
    # Water savings percentages for intercropping systems
    water_savings = ["-", "-", "-", "11.0%", "11.7%", "11.4%"]
    
    data = {
        "System": systems,
        "Initial (mm)": initial_mm,
        "Development (mm)": dev_mm,
        "Total (mm)": total_mm,
        "Water Savings (%)": water_savings
    }
    
    return pd.DataFrame(data)

def create_gravity_drip_data():
    """
    Create data for standard vs gravity-fed drip irrigation systems
    using actual calculated values.
    """
    systems = [
        "Beans (Monoculture)", 
        "Maize (Monoculture)", 
        "Onions (Monoculture)",
        "Maize + Beans (50:50)",
        "Onions + Beans (50:50)",
        "Maize + Onions (50:50)",
        "Beans - GravityDrip (2.5m)", 
        "Maize - GravityDrip (2.5m)", 
        "Onions - GravityDrip (2.5m)",
        "Maize + Beans - GravityDrip (2.5m)",
        "Onions + Beans - GravityDrip (2.5m)",
        "Maize + Onions - GravityDrip (2.5m)"
    ]
    
    # Values from the program output
    initial_mm = [8.460, 12.750, 11.780, 10.194, 9.713, 11.738, 
                  6.599, 9.945, 9.188, 7.951, 7.576, 9.156]
    dev_mm = [24.210, 21.280, 24.510, 19.476, 20.736, 19.405,
              18.884, 16.598, 19.118, 15.191, 16.174, 15.136]
    total_mm = [32.670, 34.030, 36.290, 29.670, 30.449, 31.143,
                25.483, 26.543, 28.306, 23.143, 23.750, 24.292]
    
    water_savings = ["-", "-", "-", "11.0%", "11.7%", "11.4%",
                     "22.0%", "22.0%", "22.0%", "30.6%", "31.1%", "30.9%"]
    
    additional_savings = ["", "", "", "", "", "",
                         "", "", "", "+22.0%", "+22.0%", "+22.0%"]
    
    data = {
        "System": systems,
        "Initial (mm)": initial_mm,
        "Development (mm)": dev_mm,
        "Total (mm)": total_mm,
        "Water Savings (%)": water_savings,
        "Additional Savings": additional_savings,
        "Is GravityDrip": [False] * 6 + [True] * 6
    }
    
    return pd.DataFrame(data)

def create_operating_head_data():
    """
    Create data for operating head impact analysis
    using actual calculated values.
    """
    # Data from the program output
    heads = ["1.0m", "2.5m", "3.5m", "4.5m", "5.5m"]
    
    # Actual calculated values from the program output
    # "Impact of Operating Head on Water Savings (Maize + Beans):"
    savings = [27.0, 30.6, 31.5, 32.4, 33.3]
    
    data = {
        "Operating Head": heads,
        "Water Savings (%)": savings
    }
    
    return pd.DataFrame(data)

def create_uniformity_data():
    """
    Create data for uniformity metrics at different operating heads
    using values from Martinez et al. (2023) research.
    """
    # Data from Martinez et al. (2023) as mentioned in the program output
    heads = [1.0, 2.5, 3.5, 4.5, 5.5]
    emission_uniformity = [95.5, 97.5, 97.8, 98.0, 98.1]
    christiansen_cu = [96.8, 98.2, 98.5, 98.6, 98.7]
    coefficient_variation = [0.052, 0.032, 0.028, 0.027, 0.026]
    
    data = {
        "Operating Head (m)": heads,
        "Emission Uniformity (%)": emission_uniformity,
        "Christiansen's CU (%)": christiansen_cu,
        "Coefficient of Variation": coefficient_variation
    }
    
    return pd.DataFrame(data)

def create_efficiency_matrix_data():
    """
    Create data for the water efficiency matrix using normalized values
    compared to standard beans monoculture.
    """
    # Define the systems and crops to evaluate
    irrigation_systems = ['Standard', 'GravityDrip (2.5m)']
    crop_combinations = [
        'Beans (Mono)',
        'Maize (Mono)',
        'Onions (Mono)',
        'Maize + Beans',
        'Onions + Beans',
        'Maize + Onions'
    ]
    
    # Create the efficiency matrix (% water saved compared to standard beans)
    # Higher values indicate greater water savings
    # These values are calculated as: (1 - water_req / reference) * 100
    efficiency_matrix = np.array([
        [0.0, 22.0],    # Beans (Mono)
        [-4.2, 18.8],   # Maize (Mono)
        [-11.1, 13.4],  # Onions (Mono)
        [9.2, 29.2],    # Maize + Beans
        [6.8, 27.3],    # Onions + Beans
        [4.7, 25.6]     # Maize + Onions
    ])
    
    # Create a DataFrame for easier handling
    df = pd.DataFrame(efficiency_matrix, 
                    index=crop_combinations,
                    columns=irrigation_systems)
    
    return df

def create_synergistic_data():
    """
    Create data for comparing synergistic benefits of intercropping 
    and gravity-fed drip irrigation using actual calculated values.
    """
    # Data from the program output
    systems = [
        "Maize (Mono)",
        "Beans (Mono)",
        "Average Mono",
        "Maize + Beans\n(Intercrop)",
        "Maize + Beans\n(GravityDrip)"
    ]
    
    # Actual values from the program output
    water_req = [34.030, 32.670, 33.350, 29.670, 23.143]
    
    # Calculate water savings relative to average monoculture
    avg_mono = 33.350  # As stated in the detailed calculation example
    savings = [(1 - req / avg_mono) * 100 for req in water_req]
    savings[0:2] = [0, 0]  # No savings for individual monocultures compared to average
    
    data = {
        "System": systems,
        "Water Requirement (mm)": water_req,
        "Water Savings (%)": savings
    }
    
    return pd.DataFrame(data)

def create_ratio_prediction_data():
    """
    Create data for different crop ratios predictions
    using actual calculated values.
    """
    # Data from the program output
    ratios = ["50:50", "70:30"]
    water_usage = [29.670, 29.993]
    water_savings = [11.0, 10.8]
    
    data = {
        "Ratio (Maize:Beans)": ratios,
        "Water Usage (mm)": water_usage,
        "Water Savings (%)": water_savings
    }
    
    return pd.DataFrame(data)

def plot_water_usage_comparison(save_path=None):
    """
    Create a bar chart comparing water usage between monoculture and intercropping systems.
    """
    df = create_water_usage_data()
    
    # Filter out relevant systems
    df_filtered = df.copy()
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create positions for the bars
    systems = df_filtered['System']
    x = np.arange(len(systems))
    width = 0.55
    
    # Create the stacked bars
    ax.bar(x, df_filtered['Initial (mm)'], width, label='Initial Stage')
    ax.bar(x, df_filtered['Development (mm)'], width, bottom=df_filtered['Initial (mm)'], label='Development Stage')
    
    # Add water savings annotations for intercropping systems
    for i, system in enumerate(systems):
        if 'Monoculture' not in system:
            height = df_filtered.iloc[i]['Total (mm)']
            savings = df_filtered.iloc[i]['Water Savings (%)']
            ax.annotate(f'{savings} savings', 
                        xy=(i, height + 0.8), 
                        xytext=(0, 0),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
    
    # Customize the plot
    ax.set_ylabel('Water Usage (mm)')
    ax.set_title('Water Usage Comparison: Monoculture vs. Intercropping Systems')
    ax.set_xticks(x)
    ax.set_xticklabels(systems, rotation=30, ha='right')
    ax.legend(loc='upper left')
    
    # Add a horizontal line for average monoculture water usage
    mono_beans = df_filtered[df_filtered['System'] == 'Beans (Monoculture)']['Total (mm)'].values[0]
    mono_maize = df_filtered[df_filtered['System'] == 'Maize (Monoculture)']['Total (mm)'].values[0]
    mono_onions = df_filtered[df_filtered['System'] == 'Onions (Monoculture)']['Total (mm)'].values[0]
    
    # Add lines for the expected average of each intercropping combination
    mb_avg = (mono_maize + mono_beans) / 2
    ob_avg = (mono_onions + mono_beans) / 2
    mo_avg = (mono_maize + mono_onions) / 2
    
    # Identify positions of intercropping systems
    mb_pos = list(systems).index('Maize + Beans (50:50)')
    ob_pos = list(systems).index('Onions + Beans (50:50)')
    mo_pos = list(systems).index('Maize + Onions (50:50)')
    
    # Draw horizontal lines for expected water usage
    ax.hlines(y=mb_avg, xmin=mb_pos-0.4, xmax=mb_pos+0.4, colors='red', linestyles='dashed')
    ax.hlines(y=ob_avg, xmin=ob_pos-0.4, xmax=ob_pos+0.4, colors='red', linestyles='dashed')
    ax.hlines(y=mo_avg, xmin=mo_pos-0.4, xmax=mo_pos+0.4, colors='red', linestyles='dashed')
    
    # Add annotation for the dashed lines
    ax.annotate('Expected average\n(no interaction effect)', 
                xy=(mb_pos+0.8, mb_avg + 0.5), 
                xytext=(1, 0),
                textcoords="offset points",
                ha='center', va='bottom',
                color='red', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_operating_head_impact(save_path=None):
    """
    Create a bar chart showing the effect of operating head on water savings.
    """
    df = create_operating_head_data()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['Operating Head'], df['Water Savings (%)'], color='skyblue', width=0.5)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom')
    
    # Customize the plot
    ax.set_xlabel('Operating Head')
    ax.set_ylabel('Water Savings (%)')
    ax.set_title('Effect of Operating Head on Water Savings\n(Maize + Beans with Gravity-Fed Drip)')
    ax.set_ylim(0, max(df['Water Savings (%)']) * 1.15)  # Add space above for labels
    
    # Add a horizontal line at the 2.5m recommended operating head
    recommended_savings = df.loc[df['Operating Head'] == '2.5m', 'Water Savings (%)'].values[0]
    ax.axhline(y=recommended_savings, xmin=0.2, xmax=0.3, color='red', linestyle='--')
    
    # Add annotation for recommended operating head
    ax.annotate('Recommended\noperating head', 
                xy=(1, recommended_savings), 
                xytext=(15, 0),
                textcoords="offset points",
                ha='left', va='center',
                color='red',
                arrowprops=dict(arrowstyle="->", color='red'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_uniformity_metrics(save_path=None):
    """
    Create a dual y-axis plot showing uniformity metrics at different operating heads.
    """
    df = create_uniformity_data()
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot EU and CU on primary y-axis
    line1 = ax1.plot(df['Operating Head (m)'], df['Emission Uniformity (%)'], 'b-o', 
              linewidth=2, markersize=8, label='Emission Uniformity (EU)')
    line2 = ax1.plot(df['Operating Head (m)'], df['Christiansen\'s CU (%)'], 'g-^', 
              linewidth=2, markersize=8, label='Christiansen\'s CU')
    
    ax1.set_xlabel('Operating Head (m)')
    ax1.set_ylabel('Uniformity (%)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(94, 100)  # Set y-axis limits for uniformity metrics
    
    # Create secondary y-axis for CV
    ax2 = ax1.twinx()
    line3 = ax2.plot(df['Operating Head (m)'], df['Coefficient of Variation'], 'r-s', 
              linewidth=2, markersize=8, label='Coefficient of Variation (CV)')
    ax2.set_ylabel('Coefficient of Variation', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 0.06)  # Set y-axis limits for CV
    
    # Add a shaded region for recommended range
    plt.axvspan(2.5, 4.0, alpha=0.2, color='green')
    plt.text(3.25, 0.048, 'Recommended\nRange', ha='center', va='center', 
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
    
    # Add vertical line at 2.5m
    plt.axvline(x=2.5, color='green', linestyle='--', alpha=0.7)
    
    # Combine legends
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower right')
    
    plt.title('Effect of Operating Head on Gravity-Fed Drip Irrigation Uniformity')
    plt.grid(linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_efficiency_heatmap(save_path=None):
    """
    Create a heatmap visualizing the water efficiency matrix.
    """
    df = create_efficiency_matrix_data()
    
    # Create a custom colormap from red to green
    colors = ["#FF0000", "#FFFF00", "#00FF00"]
    cmap = LinearSegmentedColormap.from_list("RdYlGn", colors, N=100)
    
    plt.figure(figsize=(10, 8))
    
    # Create the heatmap
    ax = sns.heatmap(df, annot=True, cmap=cmap, fmt=".1f", linewidths=.5,
                cbar_kws={'label': 'Water Savings (%)'})
    
    # Customize the plot
    plt.title('Water Efficiency Matrix\n(% water saved compared to standard beans monoculture)')
    plt.ylabel('Crop System')
    plt.xlabel('Irrigation Method')
    
    # Format colorbar ticks as percentages
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([-10, 0, 10, 20, 30])
    cbar.set_ticklabels(['-10%', '0%', '10%', '20%', '30%'])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_synergistic_benefits(save_path=None):
    """
    Create a bar chart showing the synergistic benefits of combined approaches.
    """
    df = create_synergistic_data()
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot water requirements as bars
    bars = ax1.bar(df['System'], df['Water Requirement (mm)'], color=['blue', 'blue', 'blue', 'green', 'purple'])
    
    # Highlight the average monoculture with a different pattern
    bars[2].set_hatch('///')
    
    # Add a second y-axis for water savings
    ax2 = ax1.twinx()
    
    # Plot water savings as a line with points
    savings_data = df[df['Water Savings (%)'] > 0]
    ax2.plot(savings_data.index, savings_data['Water Savings (%)'], 'ro-', linewidth=2, markersize=10)
    
    # Format y-axis with percentage
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom')
    
    # Add water savings annotations
    for i, row in savings_data.iterrows():
        ax2.annotate(f"{row['Water Savings (%)']:.1f}%", 
                    xy=(i, row['Water Savings (%)']),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center', va='bottom',
                    color='red')
    
    # Customize the plot
    ax1.set_ylabel('Water Requirement (mm)')
    ax2.set_ylabel('Water Savings (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Set the range for the second y-axis
    ax2.set_ylim(0, 35)
    
    # Add annotations for key comparisons
    plt.annotate('', xy=(3, 15), xytext=(2, 15),
                arrowprops=dict(arrowstyle='<->', color='black'))
    plt.text(2.5, 16, '11.0% savings\nfrom intercropping', ha='center')
    
    plt.annotate('', xy=(4, 22), xytext=(3, 22),
                arrowprops=dict(arrowstyle='<->', color='black'))
    plt.text(3.5, 23, '22.0% additional savings\nfrom gravity-fed drip', ha='center')
    
    plt.title('Synergistic Benefits of Intercropping and Gravity-Fed Drip Irrigation\n(Maize + Beans System)')
    
    # Adjust layout and grid
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_ratio_prediction(save_path=None):
    """
    Create a chart showing the effect of different crop ratios on water usage and savings.
    """
    df = create_ratio_prediction_data()
    
    fig, ax1 = plt.subplots(figsize=(9, 6))
    
    # Bar plot for water usage
    x = np.arange(len(df['Ratio (Maize:Beans)']))
    width = 0.4
    bars = ax1.bar(x, df['Water Usage (mm)'], width, color='steelblue', label='Water Usage')
    
    # Add a secondary y-axis for the water savings percentage
    ax2 = ax1.twinx()
    line = ax2.plot(x, df['Water Savings (%)'], 'ro-', label='Water Savings')
    
    # Customize the primary axis
    ax1.set_ylabel('Water Usage (mm)', color='steelblue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['Ratio (Maize:Beans)'])
    ax1.tick_params(axis='y', labelcolor='steelblue')
    
    # Customize the secondary axis
    ax2.set_ylabel('Water Savings (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 15)  # Set a reasonable y-axis limit for percentages
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}', ha='center', va='bottom')
    
    # Add value labels for the line
    for i, value in enumerate(df['Water Savings (%)']):
        ax2.text(i, value + 0.1, f'{value:.1f}%', ha='center', va='bottom', color='red')
    
    ax1.set_title('Effect of Crop Ratio on Water Usage and Savings (Maize + Beans)')
    
    # Add a combined legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
        
def plot_interaction_factors(save_path=None):
    """
    Create a visualization of the interaction factors for different crop combinations.
    """
    # Create dataframe from the interaction factors data
    combinations = ["Maize+Beans", "Maize+Beans", "Onions+Beans", "Onions+Beans", "Maize+Onions", "Maize+Onions"]
    crops = ["Maize", "Beans", "Onions", "Beans", "Maize", "Onions"]
    initial = [0.9612, 0.9612, 0.9598, 0.9598, 0.9570, 0.9570]
    development = [0.8563, 0.8563, 0.8512, 0.8512, 0.8476, 0.8476]
    
    data = {
        "Combination": combinations,
        "Crop": crops,
        "Initial Stage": initial,
        "Development Stage": development
    }
    
    df = pd.DataFrame(data)
    
    # Create a melted dataframe for easier plotting
    melted_df = pd.melt(df, id_vars=['Combination', 'Crop'], 
                        value_vars=['Initial Stage', 'Development Stage'],
                        var_name='Growth Stage', value_name='Interaction Factor')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create the grouped bar chart
    sns.barplot(x='Crop', y='Interaction Factor', hue='Growth Stage', data=melted_df, ax=ax)
    
    # Add a horizontal line at y=1.0 to indicate the baseline
    ax.axhline(y=1.0, color='r', linestyle='-', alpha=0.3, linewidth=2)
    ax.annotate('Baseline: No interaction effect', xy=(2.5, 1.01), 
                ha='center', va='bottom', color='red')
    
    # Add value labels on top of bars
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.annotate(f'{height:.4f}', 
                    xy=(p.get_x() + p.get_width()/2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # Customize the plot
    ax.set_title('Interaction Factors by Crop and Growth Stage')
    ax.set_ylim(0.8, 1.02)  # Set y-axis limits to highlight the differences
    ax.legend(title='Growth Stage')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_water_savings_heatmap(save_path=None):
    """
    Create a heatmap showing water savings for all crop combinations.
    """
    # Create a dataframe with the water savings data
    systems = ["IoT Maize + Beans (50:50)", "IoT Onions + Beans (50:50)", "IoT Maize + Onions (50:50)"]
    water_savings = [11.0, 11.7, 11.4]
    
    # Convert to a format suitable for a heatmap
    crop_pairs = [tuple(system.split('IoT ')[1].split(' (50:50)')[0].split(' + ')) for system in systems]
    
    # Create a pivot table-like structure for the heatmap
    crops = ["Maize", "Beans", "Onions"]
    heatmap_data = np.zeros((len(crops), len(crops)))
    
    # Fill in the matrix
    for (crop1, crop2), saving in zip(crop_pairs, water_savings):
        i = crops.index(crop1)
        j = crops.index(crop2)
        heatmap_data[i, j] = saving
        heatmap_data[j, i] = saving  # Make it symmetric
    
    # Set diagonal to NaN (we don't have monoculture "savings")
    for i in range(len(crops)):
        heatmap_data[i, i] = np.nan
    
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    mask = np.isnan(heatmap_data)
    
    # Use a custom colormap for water savings
    cmap = plt.cm.YlGnBu
    
    # Create the heatmap
    ax = sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap=cmap, 
                    xticklabels=crops, yticklabels=crops, 
                    mask=mask, linewidths=.5,
                    cbar_kws={'label': 'Water Savings (%)'})
    
    # Customize the plot
    plt.title('Water Savings (%) by Crop Combination')
    
    # Rotate the x-axis labels
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_consumption_comparison(save_path=None):
    """
    Create a bar chart comparing theoretical vs actual water consumption.
    """
    # Theoretical water usage from "Consumption Calculations (ETo = 4.81 mm/day)"
    theoretical_crops = ["Beans", "Maize", "Onions"]
    theoretical_initial = [9.084, 13.843, 12.978]
    theoretical_dev = [26.647, 23.533, 26.647]
    theoretical_total = [35.732, 37.376, 39.625]
    
    # Actual water usage from IoT measurements
    actual_crops = ["Beans", "Maize", "Onions"]  
    actual_initial = [8.460, 12.750, 11.780]
    actual_dev = [24.210, 21.280, 24.510]
    actual_total = [32.670, 34.030, 36.290]
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Positions for the bars
    x = np.arange(len(theoretical_crops))
    width = 0.35
    
    # Create the grouped bars
    rects1 = ax.bar(x - width/2, theoretical_total, width, label='Theoretical')
    rects2 = ax.bar(x + width/2, actual_total, width, label='Actual (IoT)')
    
    # Add labels, title and custom x-axis tick labels
    ax.set_xlabel('Crop')
    ax.set_ylabel('Water Consumption (mm)')
    ax.set_title('Theoretical vs. Actual Water Consumption by Crop')
    ax.set_xticks(x)
    ax.set_xticklabels(theoretical_crops)
    ax.legend()
    
    # Add value labels on top of bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # Add percentages showing the difference
    for i, (theo, act) in enumerate(zip(theoretical_total, actual_total)):
        diff_pct = (1 - act/theo) * 100
        ax.annotate(f'{diff_pct:.1f}%',
                    xy=(i, min(theo, act) - 2),
                    ha='center', va='top',
                    color='green' if diff_pct > 0 else 'red',
                    fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def generate_all_plots(output_dir='.'):
    """Generate all plots and save them to the specified directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and save all plots
    print("Generating water usage comparison plot...")
    plot_water_usage_comparison(os.path.join(output_dir, 'water_usage_comparison.pdf'))
    
    print("Generating operating head impact plot...")
    plot_operating_head_impact(os.path.join(output_dir, 'operating_head_impact.pdf'))
    
    print("Generating uniformity metrics plot...")
    plot_uniformity_metrics(os.path.join(output_dir, 'uniformity_metrics.pdf'))
    
    print("Generating efficiency heatmap...")
    plot_efficiency_heatmap(os.path.join(output_dir, 'efficiency_heatmap.pdf'))
    
    print("Generating synergistic benefits plot...")
    plot_synergistic_benefits(os.path.join(output_dir, 'synergistic_benefits.pdf'))
    
    print("Generating ratio prediction plot...")
    plot_ratio_prediction(os.path.join(output_dir, 'ratio_prediction.pdf'))
    
    print("Generating interaction factors plot...")
    plot_interaction_factors(os.path.join(output_dir, 'interaction_factors.pdf'))
    
    print("Generating water savings heatmap...")
    plot_water_savings_heatmap(os.path.join(output_dir, 'water_savings_heatmap.pdf'))
    
    print("Generating consumption comparison plot...")
    plot_consumption_comparison(os.path.join(output_dir, 'consumption_comparison.pdf'))
    
    print(f"All plots have been generated and saved to {output_dir}.")

if __name__ == "__main__":
    # Generate all plots at once
    generate_all_plots('./plots')