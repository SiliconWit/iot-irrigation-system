import numpy as np
import pandas as pd
from tabulate import tabulate
from typing import Tuple, Dict, List, Optional, Union

"""
CROP WATER REQUIREMENTS CALCULATOR

This program calculates crop water requirements using FAO-56 methodology.
It incorporates crop coefficient (Kc) values for different growth stages:

Kc Values by Growth Stage:
- Ki (Initial stage): Crop coefficient during initial growth from planting to ~10% ground cover
- Kd (Development stage): Crop coefficient during rapid vegetative growth and canopy development
- Km (Mid-season stage): Crop coefficient during flowering and yield formation
- Kl (Late-season stage): Crop coefficient during ripening and senescence

The crop coefficient (Kc) represents the ratio of crop evapotranspiration to the 
reference evapotranspiration (ETo) and varies by crop type and growth stage.
"""

class SimplifiedETo:
    """
    Simplified calculation of reference evapotranspiration (ETo) with Nyeri-Kenya adaptations.

    This class implements a simplified Hargreaves-Samani equation for ETo calculation,
    with optional adjustments for Nyeri, Kenya's specific climatic conditions.

    Notes
    -----
    Nyeri Characteristics:
    * Altitude: ~1,750 meters above sea level
    * Location: Near equator (0°25'S)
    * Climate: Highland climate with two rainy seasons
    * Temperature range: 10-26°C typical
    * Relative Humidity: 60-84% typical
    """
    
    @staticmethod
    def calc_eto(temp: float, humidity: float, elevation: float = 100, 
                 fixed_eto: float = None, location_adjust: bool = False) -> Tuple[float, str]:
        """
        Calculate reference evapotranspiration (ETo) using simplified Hargreaves-Samani.

        Parameters
        ----------
        temp : float
            Mean temperature in Celsius
        humidity : float
            Relative humidity in percentage (0-100)
        elevation : float, optional
            Site elevation in meters above sea level, defaults to 100
        fixed_eto : float, optional
            Override calculated ETo with fixed value, defaults to None
        location_adjust : bool, optional
            Apply Nyeri-specific adjustments, defaults to False

        Returns
        -------
        Tuple[float, str]
            - ETo value in mm/day
            - Method used ('fixed' or 'calculated')
        """
        if fixed_eto is not None:
            return fixed_eto, "fixed"
            
        # Constants
        SOLAR_CONSTANT = 0.082  # MJ/m²/min
        
        # Estimate temperature range based on humidity
        min_temp_range = 8.0 if location_adjust else 5.0
        temp_range = max(min_temp_range, 12.0 * (1 - humidity/100))
        
        # Extra-terrestrial radiation (Ra) approximation
        if location_adjust:
            elevation_factor = 1 + (elevation/8000)  # Highland adjustment
        else:
            elevation_factor = 1 + elevation/10000   # Standard adjustment
            
        ra = SOLAR_CONSTANT * elevation_factor * 24 * 60 * 0.4  # MJ/m²/day
        ra_mm = ra * 0.408  # Convert to mm/day
        
        # Hargreaves-Samani equation
        eto = 0.0023 * (temp + 17.8) * (temp_range ** 0.5) * ra_mm
        
        # Humidity correction
        humidity_coef = 0.12 if location_adjust else 0.15
        humidity_factor = 1.0 - humidity_coef * (humidity/100)
        
        min_factor = 0.88 if location_adjust else 0.85
        eto *= max(min_factor, min(humidity_factor, 1.0))
        
        # Output constraints
        if location_adjust:
            return max(2.5, min(eto, 12.0)), "calculated"
        else:
            return max(2.0, min(eto, 15.0)), "calculated"

    @staticmethod
    def get_nyeri_seasonal_factor(month: int) -> float:
        """
        Get seasonal adjustment factor for Nyeri's climate patterns.

        Parameters
        ----------
        month : int
            Month of the year (1-12)

        Returns
        -------
        float
            Seasonal adjustment factor based on Nyeri's seasons
        """
        seasonal_factors = {
            1: 1.1, 2: 1.1,  # Hot dry
            3: 0.9, 4: 0.9, 5: 0.9,  # Long rains
            6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0,  # Cool dry
            10: 0.9, 11: 0.9, 12: 0.9  # Short rains
        }
        return seasonal_factors.get(month, 1.0)

    @staticmethod
    def is_valid_nyeri_conditions(temp: float, humidity: float, 
                                elevation: float) -> bool:
        """
        Validate if weather conditions are within typical Nyeri ranges.

        Parameters
        ----------
        temp : float
            Temperature in Celsius
        humidity : float
            Relative humidity in percentage
        elevation : float
            Site elevation in meters

        Returns
        -------
        bool
            True if all conditions are within Nyeri's typical ranges
        """
        return (10 <= temp <= 26 and 
                60 <= humidity <= 84 and 
                1400 <= elevation <= 2500)


def calculate_crop_water(ETo, Kc, days, area, stage_name, additional_params=None):
    """
    Calculate water requirements for a crop stage
    
    Parameters:
    - ETo: Reference evapotranspiration (mm/day)
    - Kc: Crop coefficient:
         - Ki (Initial stage coefficient) typically 0.3-0.5
         - Kd (Development stage coefficient) typically 0.7-0.8
         - Km (Mid-season stage coefficient) typically 1.0-1.2
         - Kl (Late-season stage coefficient) typically 0.6-0.8
    - days: Number of days in stage
    - area: Cultivation area (m²)
    - stage_name: Name of growth stage ('Initial', 'Development', 'Mid-Season', 'Late-Season')
    - additional_params: Dictionary of additional parameters (for rice cultivation)
    
    Returns:
    - Dictionary containing daily and total water requirements
    """
    ETcrop = ETo * Kc * days  # Total crop evapotranspiration for stage (mm)
    ETcrop_stage = ETcrop * area  # Total volume (mm × m²) = water volume
    
    daily_water = ETcrop_stage / days  # Daily water volume
    
    # Additional calculations for rice
    if additional_params:
        sat = additional_params.get('SAT', 0) / 30  # SAT in mm/day
        parc = additional_params.get('PARC', 0)     # PARC already in mm/day
        wl = additional_params.get('WL', 0) / 30    # WL in mm/day
        daily_water = daily_water + sat + parc + wl  # Add all daily needs
    
    total_water = daily_water * days  # Total water over the entire stage
    
    # Add the specific Kc type to the result for better readability
    kc_type = ""
    if stage_name == "Initial":
        kc_type = "Ki"
    elif stage_name == "Development":
        kc_type = "Kd"
    elif stage_name == "Mid-Season":
        kc_type = "Km"
    elif stage_name == "Late-Season":
        kc_type = "Kl"
    
    return {
        'stage': stage_name,
        'kc_type': kc_type,
        'kc_value': Kc,
        'daily_water': daily_water,
        'total_water': total_water,
        'days': days
    }

def calculate_experimental_water(crop_results, initial_days, development_days=0):
    """
    Calculate water requirements for the experimental period, handling crops with or without development stage
    
    Parameters:
    - crop_results: List of dictionaries containing crop stage results
    - initial_days: Days in initial stage
    - development_days: Days in development stage
    
    Returns:
    - Tuple of (initial_water, development_water, total_water, ki_value, kd_value)
    """
    try:
        initial_stage = next(r for r in crop_results if r['stage'] == 'Initial')
        initial_water = initial_stage['daily_water'] * initial_days
        ki_value = initial_stage['kc_value']
        
        development_water = 0
        kd_value = 0.0
        if development_days > 0:
            try:
                development_stage = next(r for r in crop_results if r['stage'] == 'Development')
                development_water = development_stage['daily_water'] * development_days
                kd_value = development_stage['kc_value']
            except StopIteration:
                print(f"Note: Development stage not found - calculating with initial stage only")
        
        total_water = initial_water + development_water
        return initial_water, development_water, total_water, ki_value, kd_value
    except StopIteration:
        raise ValueError("Initial stage data not found in crop results")

def calculate_crop_results(stages, ETo, area):
    """
    Calculate water requirements for all stages of a crop
    
    Parameters:
    - stages: List of dictionaries defining crop stages
    - ETo: Reference evapotranspiration (mm/day)
    - area: Cultivation area (m²)
    
    Returns:
    - List of dictionaries containing results for each stage
    """
    results = []
    for stage in stages:
        params = stage.get('params', None)
        result = calculate_crop_water(ETo, stage['Kc'], stage['days'], area, 
                                    stage['name'], params)
        results.append(result)
    return results

def print_experimental_results(crop_results, experimental_periods, ETo, area, eto_info=""):
    """
    Print experimental water requirements in a professional tabular format
    
    Parameters:
    - crop_results: Dictionary of crop results by crop name
    - experimental_periods: Dictionary defining experimental periods
    - ETo: Reference evapotranspiration value used (mm/day)
    - area: Cultivation area (m²)
    - eto_info: Optional information about ETo method used
    """
    print("\n" + "="*80)
    print("{:^80}".format("IRRIGATION WATER REQUIREMENTS ANALYSIS"))
    print("{:^80}".format("37-Day Experimental Period"))
    
    if eto_info:
        print("{:^80}".format(eto_info))
    
    print("="*80 + "\n")

    # Prepare data for the table
    table_data = []
    for crop_name, days in experimental_periods.items():
        results = crop_results[crop_name]
        init_water, dev_water, total, ki_value, kd_value = calculate_experimental_water(
            results, days['initial'], days['development'])
        
        # Create a formatted string for Kc values
        kc_info = f"Ki={ki_value:.2f}"
        if days['development'] > 0:
            kc_info += f", Kd={kd_value:.2f}"
        
        row = [
            crop_name,
            f"{days['initial']} days",
            f"{init_water:.3f}",
            f"{days['development']} days" if days['development'] > 0 else "N/A",
            f"{dev_water:.3f}" if days['development'] > 0 else "N/A",
            f"{total:.3f}",
            kc_info
        ]
        table_data.append(row)

    # Create and print the table
    headers = [
        "Crop Type",
        "Initial\nPeriod",
        "Initial Stage\nWater (mm)",
        "Development\nPeriod",
        "Development Stage\nWater (mm)",
        "Total Water\nRequirement (mm)",
        "Crop Coefficients"
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid",
                  numalign="right", stralign="center"))
    
    print("\nNotes:")
    print("1. All water measurements are in millimeters (mm) of water depth × area (m²)")
    print(f"2. Calculations based on ETo = {ETo:.2f} mm/day and cultivation area = {area} m²")
    print("3. Rice values include additional water requirements for saturation and standing water")
    print("4. Unit explanation: 1 mm depth over 1 m² = 1 liter of water")
    print("5. Crop coefficients: Ki = Initial stage, Kd = Development stage")
    
    print("\n" + "="*80)

def calculate_nyeri_eto(temp=17.0, humidity=80.0, elevation=1750.0, month=7):
    """
    Calculate ETo specifically for Nyeri, Kenya with seasonal adjustments
    Default values represent cool season (June-September)
    
    Parameters:
    - temp: Temperature in Celsius
    - humidity: Relative humidity (%)
    - elevation: Elevation (m)
    - month: Month of the year (1-12)
    
    Returns:
    - Tuple of (ETo value, valid conditions flag)
    """
    eto_calculator = SimplifiedETo()
    
    # Calculate base ETo
    nyeri_eto_base, method = eto_calculator.calc_eto(
        temp=temp,
        humidity=humidity,
        elevation=elevation,
        fixed_eto=None,
        location_adjust=True
    )
    
    # Apply seasonal adjustment
    seasonal_factor = eto_calculator.get_nyeri_seasonal_factor(month)
    nyeri_eto = nyeri_eto_base * seasonal_factor
    
    # Validate conditions
    valid_conditions = eto_calculator.is_valid_nyeri_conditions(
        temp, humidity, elevation
    )
    
    return nyeri_eto, valid_conditions

def run_analysis(eto_mode, custom_eto=None, custom_params=None):
    """
    Run the crop water analysis with the selected ETo mode
    
    Parameters:
    - eto_mode: 'fixed', 'nyeri', or 'custom'
    - custom_eto: Custom ETo value (used only if eto_mode is 'custom')
    - custom_params: Dictionary with custom Nyeri parameters (used only if eto_mode is 'nyeri')
    """
    # Common parameters
    area = 0.36  # m²
    
    # Define crop stages with Kc values
    # Note: 
    # - Ki = Crop coefficient for the initial stage
    # - Kd = Crop coefficient for the development stage
    # - Km = Crop coefficient for the mid-season stage
    # - Kl = Crop coefficient for the late-season stage
    
    onion_stages = [
        {'Kc': 0.5, 'days': 15, 'name': 'Initial'},      # Ki = 0.5
        {'Kc': 0.7, 'days': 25, 'name': 'Development'},   # Kd = 0.7
        {'Kc': 1.05, 'days': 70, 'name': 'Mid-Season'},   # Km = 1.05
        {'Kc': 0.85, 'days': 40, 'name': 'Late-Season'}   # Kl = 0.85
    ]

    beans_stages = [
        {'Kc': 0.35, 'days': 15, 'name': 'Initial'},      # Ki = 0.35
        {'Kc': 0.7, 'days': 25, 'name': 'Development'},    # Kd = 0.7
        {'Kc': 1.1, 'days': 35, 'name': 'Mid-Season'},     # Km = 1.1
        {'Kc': 0.3, 'days': 20, 'name': 'Late-Season'}     # Kl = 0.3
    ]

    maize_stages = [
        {'Kc': 0.4, 'days': 20, 'name': 'Initial'},       # Ki = 0.4
        {'Kc': 0.8, 'days': 35, 'name': 'Development'},    # Kd = 0.8
        {'Kc': 1.15, 'days': 40, 'name': 'Mid-Season'},    # Km = 1.15
        {'Kc': 0.7, 'days': 30, 'name': 'Late-Season'}     # Kl = 0.7
    ]

    rice_stages = [
        {   # Ki = 1.1 plus additional water requirements
            'Kc': 1.1, 'days': 60, 'name': 'Initial',
            'params': {'PARC': 6, 'SAT': 60, 'WL': 10}
        },
        {   # Km = 1.2 plus additional water requirements
            'Kc': 1.2, 'days': 60, 'name': 'Mid-Season',
            'params': {'PARC': 6, 'SAT': 0, 'WL': 10}
        },
        {   # Kl = 1.0 plus additional water requirements
            'Kc': 1.0, 'days': 30, 'name': 'Late-Season',
            'params': {'PARC': 6, 'SAT': 0, 'WL': 10}
        }
    ]
    
    experimental_periods = {
        'Onion': {'initial': 15, 'development': 22},
        'Beans': {'initial': 15, 'development': 22},
        'Maize': {'initial': 20, 'development': 17},
        'Rice': {'initial': 37, 'development': 0}  # Rice has no development stage
    }
    
    # Determine which ETo to use
    eto_info = ""
    if eto_mode.lower() == 'fixed':
        ETo = 6.5
        eto_info = f"Using Fixed ETo = {ETo:.2f} mm/day"
    
    elif eto_mode.lower() == 'nyeri':
        # Default Nyeri parameters for cool season (or use custom if provided)
        params = custom_params or {
            'temp': 17.0,      # Cool season temperature
            'humidity': 80.0,  # Cool season humidity
            'elevation': 1750.0,
            'month': 7         # July (cool dry season)
        }
        
        ETo, valid_conditions = calculate_nyeri_eto(
            temp=params['temp'],
            humidity=params['humidity'],
            elevation=params['elevation'],
            month=params['month']
        )
        
        validity_note = "within typical range" if valid_conditions else "outside typical range"
        eto_info = (f"Using Nyeri ETo = {ETo:.2f} mm/day (Calculated for cool season)\n"
                  f"Parameters: T={params['temp']}°C, RH={params['humidity']}%, "
                  f"Elev={params['elevation']}m, Month={params['month']} - {validity_note}")
    
    elif eto_mode.lower() == 'custom':
        if custom_eto is None:
            try:
                custom_eto = float(input("Enter custom ETo value (mm/day): "))
            except ValueError:
                print("Invalid input, using default value of 5.0 mm/day")
                custom_eto = 5.0
        
        ETo = custom_eto
        eto_info = f"Using Custom ETo = {ETo:.2f} mm/day"
    
    else:
        print(f"Unknown ETo mode '{eto_mode}', using fixed ETo")
        ETo = 6.5
        eto_info = f"Using Fixed ETo = {ETo:.2f} mm/day"
    
    # Calculate with the selected ETo
    crop_results = {
        'Onion': calculate_crop_results(onion_stages, ETo, area),
        'Beans': calculate_crop_results(beans_stages, ETo, area),
        'Maize': calculate_crop_results(maize_stages, ETo, area),
        'Rice': calculate_crop_results(rice_stages, ETo, area)
    }
    
    # Print results
    print(f"=== 37-DAY EXPERIMENTAL PERIOD WATER REQUIREMENTS ({eto_mode.upper()} ETo) ===")
    print_experimental_results(crop_results, experimental_periods, ETo, area, eto_info)
    
    return ETo, crop_results

def main():
    """
    Main function with interactive mode selection
    """
    print("CROP WATER REQUIREMENTS CALCULATOR")
    print("==================================")
    print("\nThis program calculates crop water requirements based on different ETo methods.")
    print("ETo = Reference Evapotranspiration (mm/day)")
    print("\nCROP COEFFICIENTS:")
    print("- Ki = Initial stage coefficient (early growth)")
    print("- Kd = Development stage coefficient (vegetative growth)")
    print("- Km = Mid-season stage coefficient (flowering/fruiting)")
    print("- Kl = Late-season stage coefficient (ripening/harvesting)")
    print("\nUNIT EXPLANATION:")
    print("- Water requirements are measured in mm × m²")
    print("- 1 mm of water over 1 m² equals 1 liter")
    print("- Example: 10 mm over 0.36 m² = 3.6 liters of water")
    
    while True:
        print("\nSelect ETo calculation method:")
        print("1. Fixed ETo (6.5 mm/day)")
        print("2. Nyeri, Kenya (cool season - calculated)")
        print("3. Custom ETo value")
        print("4. Compare all methods")
        print("5. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            
            if choice == 1:
                run_analysis('fixed')
            
            elif choice == 2:
                run_analysis('nyeri')
            
            elif choice == 3:
                try:
                    eto = float(input("Enter custom ETo value (mm/day): "))
                    run_analysis('custom', custom_eto=eto)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            
            elif choice == 4:
                # Run all methods for comparison
                print("\n--- COMPARING ALL ETo METHODS ---")
                
                # 1. Fixed ETo
                fixed_eto, fixed_results = run_analysis('fixed')
                
                # 2. Nyeri cool season ETo
                nyeri_eto, nyeri_results = run_analysis('nyeri')
                
                # 3. Custom ETo (using an example value)
                try:
                    custom_value = float(input("\nEnter custom ETo value for comparison (mm/day): "))
                    custom_eto, custom_results = run_analysis('custom', custom_eto=custom_value)
                except ValueError:
                    print("Invalid input, using example value of 5.0 mm/day")
                    custom_eto, custom_results = run_analysis('custom', custom_eto=5.0)
                
                # Print summary comparison
                print("\n" + "="*80)
                print("{:^80}".format("ETo METHOD COMPARISON SUMMARY"))
                print("="*80)
                print(f"Fixed ETo: {fixed_eto:.2f} mm/day")
                print(f"Nyeri ETo: {nyeri_eto:.2f} mm/day")
                print(f"Custom ETo: {custom_eto:.2f} mm/day")
                print("-"*80)
                
                # Compare water requirements for maize as an example
                maize_fixed = fixed_results['Maize']
                maize_nyeri = nyeri_results['Maize']
                maize_custom = custom_results['Maize']
                
                init_fixed, dev_fixed, fixed_total, ki_fixed, kd_fixed = calculate_experimental_water(
                    maize_fixed, 20, 17
                )
                
                init_nyeri, dev_nyeri, nyeri_total, ki_nyeri, kd_nyeri = calculate_experimental_water(
                    maize_nyeri, 20, 17
                )
                
                init_custom, dev_custom, custom_total, ki_custom, kd_custom = calculate_experimental_water(
                    maize_custom, 20, 17
                )
                
                print(f"Example: Maize total water requirements for 37-day period:")
                print(f"  - Fixed ETo: {fixed_total:.2f} mm × m² (~ {fixed_total:.2f} liters) with Ki={ki_fixed:.2f}, Kd={kd_fixed:.2f}")
                print(f"  - Nyeri ETo: {nyeri_total:.2f} mm × m² (~ {nyeri_total:.2f} liters) with Ki={ki_nyeri:.2f}, Kd={kd_nyeri:.2f}")
                print(f"  - Custom ETo: {custom_total:.2f} mm × m² (~ {custom_total:.2f} liters) with Ki={ki_custom:.2f}, Kd={kd_custom:.2f}")
                print("="*80)
            
            elif choice == 5:
                print("Exiting program. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
