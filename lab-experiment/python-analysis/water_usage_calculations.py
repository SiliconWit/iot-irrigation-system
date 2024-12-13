import numpy as np
import pandas as pd
from tabulate import tabulate

def calculate_crop_water(ETo, Kc, days, area, stage_name, additional_params=None):
    """
    Calculate water requirements for a crop stage
    
    Parameters:
    - ETo: Reference evapotranspiration
    - Kc: Crop coefficient
    - days: Number of days in stage
    - area: Cultivation area
    - stage_name: Name of growth stage
    - additional_params: Dictionary of additional parameters (for rice cultivation)
    
    Returns:
    - Dictionary containing daily and total water requirements
    """
    ETcrop = ETo * Kc * days
    ETcrop_stage = ETcrop * area
    
    daily_water = ETcrop_stage / days
    
    # Additional calculations for rice
    if additional_params:
        sat = additional_params.get('SAT', 0) / 30
        parc = additional_params.get('PARC', 0)
        wl = additional_params.get('WL', 0) / 30
        daily_water = daily_water + sat + parc + wl
    
    total_water = daily_water * days
    
    return {
        'stage': stage_name,
        'daily_water': daily_water,
        'total_water': total_water,
        'days': days
    }

def calculate_experimental_water(crop_results, initial_days, development_days=0):
    """
    Calculate water requirements for the experimental period, handling crops with or without development stage
    """
    try:
        initial_stage = next(r for r in crop_results if r['stage'] == 'Initial')
        initial_water = initial_stage['daily_water'] * initial_days
        
        development_water = 0
        if development_days > 0:
            try:
                development_stage = next(r for r in crop_results if r['stage'] == 'Development')
                development_water = development_stage['daily_water'] * development_days
            except StopIteration:
                print(f"Note: Development stage not found - calculating with initial stage only")
        
        total_water = initial_water + development_water
        return initial_water, development_water, total_water
    except StopIteration:
        raise ValueError("Initial stage data not found in crop results")

# Common parameters
ETo = 6.5
area = 0.36

# Define crop stages
onion_stages = [
    {'Kc': 0.5, 'days': 15, 'name': 'Initial'},
    {'Kc': 0.7, 'days': 25, 'name': 'Development'},
    {'Kc': 1.05, 'days': 70, 'name': 'Mid-Season'},
    {'Kc': 0.85, 'days': 40, 'name': 'Late-Season'}
]

beans_stages = [
    {'Kc': 0.35, 'days': 15, 'name': 'Initial'},
    {'Kc': 0.7, 'days': 25, 'name': 'Development'},
    {'Kc': 1.1, 'days': 35, 'name': 'Mid-Season'},
    {'Kc': 0.3, 'days': 20, 'name': 'Late-Season'}
]

maize_stages = [
    {'Kc': 0.4, 'days': 20, 'name': 'Initial'},
    {'Kc': 0.8, 'days': 35, 'name': 'Development'},
    {'Kc': 1.15, 'days': 40, 'name': 'Mid-Season'},
    {'Kc': 0.7, 'days': 30, 'name': 'Late-Season'}
]

rice_stages = [
    {
        'Kc': 1.1, 'days': 60, 'name': 'Initial',
        'params': {'PARC': 6, 'SAT': 60, 'WL': 10}
    },
    {
        'Kc': 1.2, 'days': 60, 'name': 'Mid-Season',
        'params': {'PARC': 6, 'SAT': 0, 'WL': 10}
    },
    {
        'Kc': 1.0, 'days': 30, 'name': 'Late-Season',
        'params': {'PARC': 6, 'SAT': 0, 'WL': 10}
    }
]

# Calculate results for each crop
def calculate_crop_results(stages):
    results = []
    for stage in stages:
        params = stage.get('params', None)
        result = calculate_crop_water(ETo, stage['Kc'], stage['days'], area, 
                                    stage['name'], params)
        results.append(result)
    return results

# Calculate and store results
crop_results = {
    'Onion': calculate_crop_results(onion_stages),
    'Beans': calculate_crop_results(beans_stages),
    'Maize': calculate_crop_results(maize_stages),
    'Rice': calculate_crop_results(rice_stages)
}

# Calculate experimental period water requirements
print("=== 37-DAY EXPERIMENTAL PERIOD WATER REQUIREMENTS ===")

experimental_periods = {
    'Onion': {'initial': 15, 'development': 22},
    'Beans': {'initial': 15, 'development': 22},
    'Maize': {'initial': 20, 'development': 17},
    'Rice': {'initial': 37, 'development': 0}  # Rice has no development stage
}

# Format the experimental period results 
def print_experimental_results(crop_results, experimental_periods):
    """
    Print experimental water requirements in a professional tabular format
    """
    print("\n" + "="*80)
    print("{:^80}".format("IRRIGATION WATER REQUIREMENTS ANALYSIS"))
    print("{:^80}".format("37-Day Experimental Period"))
    print("="*80 + "\n")

    # Prepare data for the table
    table_data = []
    for crop_name, days in experimental_periods.items():
        results = crop_results[crop_name]
        init_water, dev_water, total = calculate_experimental_water(
            results, days['initial'], days['development'])
        
        row = [
            crop_name,
            f"{days['initial']} days",
            f"{init_water:.3f}",
            f"{days['development']} days" if days['development'] > 0 else "N/A",
            f"{dev_water:.3f}" if days['development'] > 0 else "N/A",
            f"{total:.3f}"
        ]
        table_data.append(row)

    # Create and print the table
    headers = [
        "Crop Type",
        "Initial\nPeriod",
        "Initial Stage\nWater (mm)",
        "Development\nPeriod",
        "Development Stage\nWater (mm)",
        "Total Water\nRequirement (mm)"
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid",
                  numalign="right", stralign="center"))
    
    print("\nNotes:")
    print("1. All water measurements are in millimeters (mm)")
    print("2. Calculations based on ETo = 6.5 mm/day and cultivation area = 0.36 m²")
    print("3. Rice values include additional water requirements for saturation and standing water")
    
    print("\n" + "="*80)

# Calculate and display results
print_experimental_results(crop_results, experimental_periods)