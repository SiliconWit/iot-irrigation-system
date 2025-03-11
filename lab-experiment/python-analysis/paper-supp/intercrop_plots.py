import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Set the style - using a more generic style for compatibility
try:
    plt.style.use('seaborn-whitegrid')  # Try older style name
except:
    try:
        plt.style.use('seaborn')  # Try just seaborn
    except:
        pass  # Default style if others fail

# Set colors manually for better compatibility
sns.set_palette("colorblind")

# Create data for the visualizations based on the provided results
# Results data from intercropping experiment
def create_results_data():
    # System water usage data
    systems = [
        "IoT Beans (Monoculture)", 
        "IoT Maize (Monoculture)", 
        "IoT Onions (Monoculture)",
        "IoT Rice (Monoculture)",
        "IoT Maize + Beans (50:50)",
        "IoT Onions + Beans (50:50)",
        "IoT Maize + Onions (50:50)"
    ]
    
    initial_mm = [8.460, 12.750, 11.780, 346.180, 10.194, 9.713, 11.738]
    dev_mm = [24.210, 21.280, 24.510, 0.000, 19.476, 20.736, 19.405]
    total_mm = [32.670, 34.030, 36.290, 346.180, 29.670, 30.449, 31.143]
    water_savings = ["-", "-", "-", "-", "11.0%", "11.7%", "11.4%"]
    
    # Convert percentage strings to float values for plotting
    water_savings_float = []
    for saving in water_savings:
        if saving == "-":
            water_savings_float.append(0)
        else:
            water_savings_float.append(float(saving.strip("%")))
    
    data = {
        "System": systems,
        "Initial (mm)": initial_mm,
        "Development (mm)": dev_mm,
        "Total (mm)": total_mm,
        "Water Savings (%)": water_savings,
        "Water Savings Value": water_savings_float
    }
    
    return pd.DataFrame(data)

# Create the interaction factors data
def create_interaction_factors_data():
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
    
    return pd.DataFrame(data)

# Create data for the detailed example
def create_example_data():
    stages = ["Initial", "Development", "Total"]
    
    # Example data for Maize + Beans (50:50)
    intercrop_values = [10.194, 19.476, 29.670]
    mono_avg_values = [10.605, 22.745, 33.350]  # Average of monoculture values
    savings_percent = [(1 - intercrop_values[i]/mono_avg_values[i])*100 for i in range(3)]
    
    data = {
        "Stage": stages,
        "Intercrop (mm)": intercrop_values,
        "Monoculture Avg (mm)": mono_avg_values,
        "Savings (%)": savings_percent
    }
    
    return pd.DataFrame(data)

# Create data for ratio prediction
def create_ratio_prediction_data():
    ratios = ["50:50", "70:30"]
    water_usage = [29.670, 29.993]
    water_savings = [11.0, 10.8]
    
    data = {
        "Ratio (Maize:Beans)": ratios,
        "Water Usage (mm)": water_usage,
        "Water Savings (%)": water_savings
    }
    
    return pd.DataFrame(data)

# 1. Visualization: Water usage comparison between monoculture and intercropping
def plot_water_usage_comparison(results_df):
    # Filter out rice (which has much higher values) and focus on the relevant crops
    plot_df = results_df[~results_df['System'].str.contains('Rice')].copy()
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create positions for the bars
    systems = plot_df['System']
    x = np.arange(len(systems))
    width = 0.35
    
    # Create the stacked bars
    ax.bar(x, plot_df['Initial (mm)'], width, label='Initial Stage')
    ax.bar(x, plot_df['Development (mm)'], width, bottom=plot_df['Initial (mm)'], label='Development Stage')
    
    # Add water savings annotations for intercropping systems
    for i, system in enumerate(systems):
        if 'Monoculture' not in system:
            height = plot_df.iloc[i]['Total (mm)']
            savings = plot_df.iloc[i]['Water Savings (%)']
            ax.annotate(f'{savings} savings', 
                        xy=(i, height + 1), 
                        xytext=(0, 0),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
    
    # Customize the plot
    ax.set_ylabel('Water Usage (mm)')
    ax.set_title('Water Usage Comparison: Monoculture vs. Intercropping Systems')
    ax.set_xticks(x)
    ax.set_xticklabels(systems, rotation=45, ha='right')
    ax.legend()
    
    # Add a horizontal line for average monoculture water usage
    mono_beans = plot_df[plot_df['System'] == 'IoT Beans (Monoculture)']['Total (mm)'].values[0]
    mono_maize = plot_df[plot_df['System'] == 'IoT Maize (Monoculture)']['Total (mm)'].values[0]
    mono_onions = plot_df[plot_df['System'] == 'IoT Onions (Monoculture)']['Total (mm)'].values[0]
    
    # Add lines for the expected average of each intercropping combination
    mb_avg = (mono_maize + mono_beans) / 2
    ob_avg = (mono_onions + mono_beans) / 2
    mo_avg = (mono_maize + mono_onions) / 2
    
    # Identify positions of intercropping systems
    mb_pos = list(systems).index('IoT Maize + Beans (50:50)')
    ob_pos = list(systems).index('IoT Onions + Beans (50:50)')
    mo_pos = list(systems).index('IoT Maize + Onions (50:50)')
    
    # Draw horizontal lines for expected water usage
    ax.hlines(y=mb_avg, xmin=mb_pos-0.3, xmax=mb_pos+0.3, colors='red', linestyles='dashed', label='Expected avg.')
    ax.hlines(y=ob_avg, xmin=ob_pos-0.3, xmax=ob_pos+0.3, colors='red', linestyles='dashed')
    ax.hlines(y=mo_avg, xmin=mo_pos-0.3, xmax=mo_pos+0.3, colors='red', linestyles='dashed')
    
    plt.tight_layout()
    plt.savefig('water_usage_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. Visualization: Interaction factors by crop and growth stage
def plot_interaction_factors(factors_df):
    # Create a melted dataframe for easier plotting
    melted_df = pd.melt(factors_df, id_vars=['Combination', 'Crop'], 
                         value_vars=['Initial Stage', 'Development Stage'],
                         var_name='Growth Stage', value_name='Interaction Factor')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the grouped bar chart
    sns.barplot(x='Crop', y='Interaction Factor', hue='Growth Stage', data=melted_df, ax=ax)
    
    # Add a horizontal line at y=1.0 to indicate the baseline
    ax.axhline(y=1.0, color='r', linestyle='-', alpha=0.3, linewidth=2)
    ax.annotate('Baseline: No interaction effect', xy=(0.5, 1.01), xycoords='data',
                ha='center', va='bottom', color='red')
    
    # Customize the plot
    ax.set_title('Interaction Factors by Crop and Growth Stage')
    ax.set_ylim(0.8, 1.02)  # Set y-axis limits to highlight the differences
    
    # Add value labels on top of bars
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.annotate(f'{height:.4f}', 
                    xy=(p.get_x() + p.get_width()/2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('interaction_factors.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Visualization: Detailed example of water savings calculation
def plot_example_calculation(example_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create positions for the bars
    stages = example_df['Stage']
    x = np.arange(len(stages))
    width = 0.35
    
    # Create the bars
    ax.bar(x - width/2, example_df['Intercrop (mm)'], width, label='Intercrop Usage')
    ax.bar(x + width/2, example_df['Monoculture Avg (mm)'], width, label='Monoculture Avg')
    
    # Add savings annotations
    for i, stage in enumerate(stages):
        savings = example_df.iloc[i]['Savings (%)']
        ax.annotate(f'{savings:.1f}% savings', 
                    xy=(i, example_df.iloc[i]['Intercrop (mm)'] - 2),
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha='center', va='top',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
    
    # Customize the plot
    ax.set_ylabel('Water Usage (mm)')
    ax.set_title('Maize + Beans (50:50): Detailed Water Usage Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(stages)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('example_calculation.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. Visualization: Prediction for different crop ratios
def plot_ratio_prediction(ratio_df):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    
    # Bar plot for water usage
    x = np.arange(len(ratio_df['Ratio (Maize:Beans)']))
    width = 0.4
    bars = ax1.bar(x, ratio_df['Water Usage (mm)'], width, color='steelblue', label='Water Usage')
    
    # Add a secondary y-axis for the water savings percentage
    ax2 = ax1.twinx()
    line = ax2.plot(x, ratio_df['Water Savings (%)'], 'ro-', label='Water Savings')
    
    # Customize the primary axis
    ax1.set_ylabel('Water Usage (mm)', color='steelblue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(ratio_df['Ratio (Maize:Beans)'])
    ax1.tick_params(axis='y', labelcolor='steelblue')
    
    # Customize the secondary axis
    ax2.set_ylabel('Water Savings (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 15)  # Set a reasonable y-axis limit for percentages
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Add value labels for the line
    for i, value in enumerate(ratio_df['Water Savings (%)']):
        ax2.text(i, value + 0.1, f'{value:.1f}%', ha='center', va='bottom', color='red')
    
    ax1.set_title('Effect of Crop Ratio on Water Usage and Savings (Maize + Beans)')
    
    # Add a combined legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper center')
    
    plt.tight_layout()
    plt.savefig('ratio_prediction.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. Visualization: Water savings heatmap for all combinations
def plot_water_savings_heatmap(results_df):
    # Extract only the intercropping systems
    intercrop_df = results_df[results_df['System'].str.contains('\+')].copy()
    
    # Extract crop pairs and water savings
    crop_pairs = [system.split('IoT ')[1].split(' (50:50)')[0] for system in intercrop_df['System']]
    savings_values = intercrop_df['Water Savings Value'].values
    
    # Create a pivot table-like structure for the heatmap
    heatmap_data = []
    
    for pair, saving in zip(crop_pairs, savings_values):
        crops = pair.split(' + ')
        heatmap_data.append([crops[0], crops[1], saving])
        # Add reverse combination for a complete matrix
        heatmap_data.append([crops[1], crops[0], saving])
    
    # Convert to DataFrame
    heatmap_df = pd.DataFrame(heatmap_data, columns=['Crop 1', 'Crop 2', 'Water Savings (%)'])
    
    # Create a pivot table
    pivot_df = heatmap_df.pivot(index='Crop 1', columns='Crop 2', values='Water Savings (%)')
    
    # Create the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_df, annot=True, cmap='YlGnBu', fmt='.1f', 
                linewidths=.5, cbar_kws={'label': 'Water Savings (%)'})
    
    plt.title('Water Savings (%) by Crop Combination')
    plt.tight_layout()
    plt.savefig('water_savings_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

# Main function to generate all visualizations
def generate_visualizations():
    # Create the dataframes
    results_df = create_results_data()
    factors_df = create_interaction_factors_data()
    example_df = create_example_data()
    ratio_df = create_ratio_prediction_data()
    
    # Generate all plots
    plot_water_usage_comparison(results_df)
    plot_interaction_factors(factors_df)
    plot_example_calculation(example_df)
    plot_ratio_prediction(ratio_df)
    plot_water_savings_heatmap(results_df)
    
    print("All visualizations have been generated successfully.")

# Execute the main function
if __name__ == "__main__":
    generate_visualizations()