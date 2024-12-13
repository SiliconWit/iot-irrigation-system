# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.signal import find_peaks
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Read and prepare data
Data = pd.read_csv('../data/Daily.csv', index_col=0, parse_dates=True)

# Basic statistical analysis
print("=== Basic Statistical Analysis ===")
print("\nData Overview:")
print(Data.describe())

# Calculate daily averages and variations
daily_stats = pd.DataFrame({
    'Beans_Moisture_Mean': Data.Mois_Beans.mean(),
    'Beans_Moisture_Std': Data.Mois_Beans.std(),
    'Maize_Moisture_Mean': Data.Mois_Maize.mean(),
    'Maize_Moisture_Std': Data.Mois_Maize.std(),
    'Onion_Moisture_Mean': Data.Mois_Onion.mean(),
    'Onion_Moisture_Std': Data.Mois_Onion.std(),
    'Rice_Moisture_Mean': Data.Mois_Rice.mean(),
    'Rice_Moisture_Std': Data.Mois_Rice.std()
}, index=[0])

print("\n=== Crop-wise Moisture Statistics ===")
print(daily_stats)

# Advanced Analysis: Control System Performance
def calculate_control_metrics(data, target, tolerance):
    """Calculate control system performance metrics"""
    deviation = np.abs(data - target)
    within_tolerance = np.mean(deviation <= tolerance) * 100
    rmse = np.sqrt(mean_squared_error([target]*len(data), data))
    return within_tolerance, rmse

# Define target values and tolerances for each crop
targets = {
    'Beans': {'moisture': 75, 'tolerance': 10},
    'Maize': {'moisture': 60, 'tolerance': 5},
    'Onion': {'moisture': 57.5, 'tolerance': 7.5},
    'Rice': {'moisture': 97.5, 'tolerance': 2.5}
}

print("\n=== Control System Performance Metrics ===")
for crop in ['Beans', 'Maize', 'Onion', 'Rice']:
    moisture_col = f'Mois_{crop}' if crop != 'Maize' else 'Mois_Maize'
    within_tol, rmse = calculate_control_metrics(
        Data[moisture_col],
        targets[crop]['moisture'],
        targets[crop]['tolerance']
    )
    print(f"\n{crop} Control Performance:")
    print(f"Time within tolerance: {within_tol:.2f}%")
    print(f"RMSE from target: {rmse:.2f}%")

# Visualization: Enhanced Moisture Content Analysis
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.regplot(x='Day_Index', y='Mois_beans', data=Data, scatter_kws={'alpha':0.5})
plt.title('Beans Moisture Content Trend')
plt.xlabel('Time (Days)')
plt.ylabel('Moisture Content (%)')

plt.subplot(2, 2, 2)
sns.regplot(x='Day_Index', y='Mois_Maize', data=Data, scatter_kws={'alpha':0.5}, color='red')
plt.title('Maize Moisture Content Trend')
plt.xlabel('Time (Days)')
plt.ylabel('Moisture Content (%)')

plt.subplot(2, 2, 3)
sns.regplot(x='Day_Index', y='Mois_Onion', data=Data, scatter_kws={'alpha':0.5}, color='green')
plt.title('Onion Moisture Content Trend')
plt.xlabel('Time (Days)')
plt.ylabel('Moisture Content (%)')

plt.subplot(2, 2, 4)
sns.regplot(x='Day_Index', y='Mois_Rice', data=Data, scatter_kws={'alpha':0.5}, color='orange')
plt.title('Rice Moisture Content Trend')
plt.xlabel('Time (Days)')
plt.ylabel('Moisture Content (%)')

plt.tight_layout()
plt.show()

# Temperature Analysis
print("\n=== Temperature Analysis ===")
temp_corr = Data[[col for col in Data.columns if 'Temp' in col]].corr()
print("\nTemperature Correlation Matrix:")
print(temp_corr)

# Visualize temperature relationships
plt.figure(figsize=(12, 8))
sns.heatmap(temp_corr, annot=True, cmap='coolwarm', center=0)
plt.title('Temperature Correlation Heatmap')
plt.show()

# System Response Analysis
def analyze_system_response(data, column, threshold):
    """Analyze system response characteristics"""
    # Find peaks in the data
    peaks, _ = find_peaks(data[column])
    response_times = np.diff(peaks)
    
    return {
        'avg_response_time': np.mean(response_times),
        'std_response_time': np.std(response_times),
        'num_adjustments': len(peaks)
    }

# Analyze system response for each crop
print("\n=== System Response Analysis ===")
for crop in ['beans', 'Maize', 'Onion', 'Rice']:
    moisture_col = f'Mois_{crop}'
    response_metrics = analyze_system_response(Data, moisture_col, threshold=0.5)
    print(f"\n{crop} Response Characteristics:")
    print(f"Average response time: {response_metrics['avg_response_time']:.2f} time units")
    print(f"Response time std: {response_metrics['std_response_time']:.2f}")
    print(f"Number of control adjustments: {response_metrics['num_adjustments']}")

# Environmental Coupling Analysis
print("\n=== Environmental Coupling Analysis ===")
# Calculate correlation between humidity and temperature for each crop
for crop in ['beans', 'Maize', 'Onion']:
    humid_col = f'Humid_{crop}'
    temp_col = f'Temp_{crop}'
    correlation = Data[humid_col].corr(Data[temp_col])
    print(f"\n{crop} Temperature-Humidity Correlation: {correlation:.3f}")

# Water Management Analysis for Rice
print("\n=== Rice Water Management Analysis ===")
water_stats = Data['water_level'].describe()
print("\nWater Level Statistics:")
print(water_stats)

# Efficiency Analysis
def calculate_efficiency_metrics(data, moisture_col, target):
    """Calculate system efficiency metrics"""
    error = data[moisture_col] - target
    mae = np.mean(np.abs(error))
    mse = np.mean(error**2)
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': np.sqrt(mse)
    }

print("\n=== System Efficiency Metrics ===")
for crop in ['beans', 'Maize', 'Onion', 'Rice']:
    moisture_col = f'Mois_{crop}'
    target = targets[crop]['moisture']
    metrics = calculate_efficiency_metrics(Data, moisture_col, target)
    print(f"\n{crop} Efficiency Metrics:")
    print(f"Mean Absolute Error: {metrics['MAE']:.2f}%")
    print(f"Root Mean Square Error: {metrics['RMSE']:.2f}%")

# Plot key findings
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
Data[[col for col in Data.columns if 'Mois' in col]].boxplot()
plt.title('Moisture Distribution by Crop')
plt.xticks(rotation=45)
plt.ylabel('Moisture Content (%)')

plt.subplot(1, 3, 2)
Data[[col for col in Data.columns if 'Temp' in col]].boxplot()
plt.title('Temperature Distribution by Crop')
plt.xticks(rotation=45)
plt.ylabel('Temperature (°C)')

plt.subplot(1, 3, 3)
Data[[col for col in Data.columns if 'Humid' in col]].boxplot()
plt.title('Humidity Distribution by Crop')
plt.xticks(rotation=45)
plt.ylabel('Humidity (%)')

plt.tight_layout()
plt.show()

# Final Summary Statistics
print("\n=== Final System Performance Summary ===")
summary_stats = pd.DataFrame({
    'Metric': ['Average Moisture Control Accuracy (%)', 
               'Temperature Stability (Std Dev)',
               'Humidity Control Precision (%)',
               'Water Level Control Accuracy (mm)'],
    'Value': [
        np.mean([calculate_control_metrics(Data[f'Mois_{crop}'], 
                targets[crop]['moisture'], 
                targets[crop]['tolerance'])[0] 
                for crop in ['beans', 'Maize', 'Onion', 'Rice']]),
        np.mean([Data[f'Temp_{crop}'].std() 
                for crop in ['beans', 'Maize', 'Onion', 'Rice']]),
        np.mean([Data[f'Humid_{crop}'].std() 
                for crop in ['beans', 'Maize', 'Onion']]),
        Data['water_level'].std()
    ]
})

print(summary_stats)