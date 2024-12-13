# %%
"""
Gravity Fed Irrigation System Design Tool

Analyzes and visualizes gravity-fed irrigation systems, calculating key parameters 
like pipe sizing, flow rates and pressure drops based on elevation differences.
Uses interactive widgets for real-time system design optimization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
import math
from matplotlib.gridspec import GridSpec

# Set style for better visualization 
plt.style.use('seaborn')
sns.set_palette("husl")

# %%
def calculate_drip_irrigation_parameters(
    tank_volume_liters=2000,
    emitter_flow_rate_lph=2.0,
    number_of_plants=None,
    field_size_m2=None,
    tank_elevation_m=None,
    emitter_spacing_m=0.3,
    row_spacing_m=1.0,
    pipe_diameter_mm=16,
    friction_factor=0.015,
    efficiency=0.9
    ):
    """
    Calculate design parameters for a gravity-fed drip irrigation system.

    This function performs hydraulic calculations for drip irrigation systems,
    analyzing either field coverage possibilities given an elevation, or required
    elevation given desired coverage.

    Parameters
    ----------
    tank_volume_liters : float, optional
        Water storage tank capacity in liters (default: 2000)
    emitter_flow_rate_lph : float, optional
        Flow rate per emitter in liters per hour (default: 2.0)
    number_of_plants : int, optional
        Total number of plants to irrigate (default: None)
    field_size_m2 : float, optional
        Total field area in square meters (default: None)
    tank_elevation_m : float, optional
        Height of water tank above field level in meters (default: None)
    emitter_spacing_m : float, optional
        Distance between emitters along the line in meters (default: 0.3)
    row_spacing_m : float, optional
        Distance between rows in meters (default: 1.0)
    pipe_diameter_mm : float, optional
        Diameter of main distribution pipe in millimeters (default: 16)
    friction_factor : float, optional
        Pipe friction coefficient (default: 0.015)
    efficiency : float, optional
        System efficiency factor between 0 and 1 (default: 0.9)

    Returns
    -------
    dict
        Dictionary containing calculated system parameters:
            - elevation_needed_m: Required tank elevation
            - recommended_elevation_m: Suggested elevation with safety factor
            - max_coverage_area_m2: Maximum field size possible
            - current_field_size_m2: Actual field size being used
            - field_length_m: Approximate field length
            - total_emitters: Number of emitters/plants in system
            - flow_rate_total_lph: Total system flow rate
            - operating_time_hours: Runtime per tank volume
            - friction_loss_m: Head loss due to friction
            - water_velocity_ms: Flow velocity in main pipe
            - daily_refills_needed: Tank refills needed for 8-hour operation
            - operating_pressure_kpa: System operating pressure
            - pressure_adequate: Boolean indicating if pressure meets requirements
            - slope_impact_m: Head loss due to field slope

    Notes
    -----
    - Assumes a 2% field slope for conservative design
    - Uses Darcy-Weisbach equation for friction loss calculations
    - Minimum pressure requirement is 50 kPa at emitters
    - Either number_of_plants or field_size_m2 should be provided
    """
    try:
        GRAVITY = 9.81
        WATER_DENSITY = 1000
        MIN_PRESSURE_KPA = 50
        
        # Input validation
        if any(param <= 0 for param in [tank_volume_liters, emitter_flow_rate_lph, 
                                      emitter_spacing_m, row_spacing_m, pipe_diameter_mm]):
            return None
            
        # Calculate field parameters based on available inputs
        if number_of_plants and not field_size_m2:
            field_size_m2 = number_of_plants * emitter_spacing_m * row_spacing_m
            total_emitters = number_of_plants
        elif field_size_m2 and not number_of_plants:
            total_emitters = math.floor(field_size_m2 / (emitter_spacing_m * row_spacing_m))
            number_of_plants = total_emitters
        elif field_size_m2 and number_of_plants:
            # Use provided number of plants but verify it fits in field
            max_possible_plants = math.floor(field_size_m2 / (emitter_spacing_m * row_spacing_m))
            total_emitters = min(number_of_plants, max_possible_plants)
        else:
            # If neither is provided, use a default small field size
            field_size_m2 = 100
            total_emitters = math.floor(field_size_m2 / (emitter_spacing_m * row_spacing_m))
            number_of_plants = total_emitters

        # Calculate flow requirements
        total_flow_rate_lph = total_emitters * emitter_flow_rate_lph * (1/efficiency)
        flow_rate_m3s = total_flow_rate_lph / (3600 * 1000)
        
        # Pipe calculations
        pipe_radius_m = pipe_diameter_mm / 2000
        pipe_area_m2 = math.pi * pipe_radius_m ** 2
        velocity = flow_rate_m3s / pipe_area_m2
        
        # Calculate field dimensions and losses
        field_length = math.sqrt(field_size_m2)
        
        # Calculate friction losses using Darcy-Weisbach
        kinematic_viscosity = 1e-6
        reynolds = velocity * (pipe_diameter_mm/1000) / kinematic_viscosity
        if reynolds > 0:
            if reynolds < 2300:
                friction_factor = 64 / reynolds
            else:
                friction_factor = 0.316 / (reynolds ** 0.25)
                
            minor_loss_coefficient = 2.5
            head_loss = (friction_factor * field_length * velocity**2 / 
                        (2 * GRAVITY * (pipe_diameter_mm/1000)) +
                        minor_loss_coefficient * velocity**2 / (2 * GRAVITY))
        else:
            head_loss = 0
            
        # Calculate minimum pressure head needed
        min_pressure_head = MIN_PRESSURE_KPA * 1000 / (WATER_DENSITY * GRAVITY)
        field_slope_factor = 0.02 * field_length  # 2% slope assumption
        
        if tank_elevation_m:
            # Calculate achievable pressure with given elevation
            available_pressure_kpa = (tank_elevation_m * WATER_DENSITY * GRAVITY) / 1000
            pressure_adequate = available_pressure_kpa >= MIN_PRESSURE_KPA
            
            # Calculate maximum possible field size with this elevation
            max_field_size = field_size_m2 if pressure_adequate else (field_size_m2 * available_pressure_kpa / MIN_PRESSURE_KPA)
            
            elevation_needed = tank_elevation_m
            recommended_elevation = (min_pressure_head + head_loss + field_slope_factor) * 1.1
        else:
            # Calculate required elevation
            elevation_needed = (min_pressure_head + head_loss + field_slope_factor) * 1.1
            recommended_elevation = elevation_needed
            available_pressure_kpa = (elevation_needed * WATER_DENSITY * GRAVITY) / 1000
            max_field_size = field_size_m2
            pressure_adequate = True
        
        # Operating parameters
        operating_time_hours = tank_volume_liters / total_flow_rate_lph
        daily_refills = 8 / operating_time_hours if operating_time_hours > 0 else float('inf')
        
        return {
            'elevation_needed_m': round(elevation_needed, 1),
            'recommended_elevation_m': round(recommended_elevation, 1),
            'max_coverage_area_m2': round(max_field_size, 1),
            'current_field_size_m2': round(field_size_m2, 1),
            'field_length_m': round(field_length, 1),
            'total_emitters': total_emitters,
            'flow_rate_total_lph': round(total_flow_rate_lph, 2),
            'operating_time_hours': round(operating_time_hours, 1),
            'friction_loss_m': round(head_loss, 2),
            'water_velocity_ms': round(velocity, 2),
            'daily_refills_needed': round(daily_refills, 1),
            'operating_pressure_kpa': round(available_pressure_kpa, 1),
            'pressure_adequate': pressure_adequate,
            'slope_impact_m': round(field_slope_factor, 2)
        }
    except Exception as e:
        print(f"Error in calculations: {str(e)}")
        return None

# %%
def plot_comprehensive_analysis(df, selected_volume):
   """
   Create a comprehensive visualization of gravity-fed irrigation system parameters.

   Generates a figure with 5 subplots analyzing different aspects of the irrigation
   system performance based on tank height variations.

   Parameters
   ----------
   df : pandas.DataFrame
       DataFrame containing the analysis results with columns:
       - tank_volume: Tank size in liters
       - height: Tank elevation in meters
       - max_coverage_area_m2: Maximum irrigable area
       - operating_time_hours: System runtime
       - head_loss_m: Friction and minor losses
       - daily_refills_needed: Required tank refills
       - water_velocity_ms: Flow velocity
       - recommended_height_m: Optimal tank elevation
   selected_volume : float
       Tank volume in liters to analyze

   Returns
   -------
   matplotlib.figure.Figure
       Figure containing 5 subplots:
       1. Coverage Area vs Height (with 10% variance band)
       2. Operating Time vs Height (with 8-hour workday reference)
       3. System Efficiency (Head Loss)
       4. Daily Refills Needed
       5. Water Velocity (with min/max reference lines)

   Notes
   -----
   - Uses GridSpec for optimized subplot layout
   - Main title includes practical height recommendation range
   - Reference lines indicate key operational thresholds
   """
   fig = plt.figure(figsize=(15, 12))
   gs = GridSpec(3, 2, figure=fig)

   # Main title with practical interpretation
   practical_height = df[df['tank_volume'] == selected_volume]['recommended_height_m'].mean()
   fig.suptitle(f'Gravity Fed Drip Irrigation Analysis - {selected_volume}L Tank\n' +
               f'Recommended Height Range: {practical_height-1:.1f}m - {practical_height+1:.1f}m',
               fontsize=16, y=0.95)

   # Filter data
   data = df[df['tank_volume'] == selected_volume]

   # Plot 1: Coverage Area vs Height (larger plot)
   ax1 = fig.add_subplot(gs[0, :])
   ax1.plot(data['height'], data['max_coverage_area_m2'], 'b-', linewidth=2)
   ax1.fill_between(data['height'], data['max_coverage_area_m2']*0.9,
                   data['max_coverage_area_m2']*1.1, alpha=0.2)
   ax1.set_xlabel('Tank Height (m)')
   ax1.set_ylabel('Coverage Area (m²)')
   ax1.set_title('Coverage Area vs Tank Height (with 10% variance)')
   ax1.grid(True)

   # Plot 2: Operating Time vs Height
   ax2 = fig.add_subplot(gs[1, 0])
   ax2.plot(data['height'], data['operating_time_hours'], 'g-', linewidth=2)
   ax2.axhline(y=8, color='r', linestyle='--', label='Typical work day')
   ax2.set_xlabel('Tank Height (m)')
   ax2.set_ylabel('Operating Time (hours)')
   ax2.set_title('Operating Time vs Tank Height')
   ax2.grid(True)
   ax2.legend()

   # Plot 3: System Efficiency
   ax3 = fig.add_subplot(gs[1, 1])
   ax3.plot(data['height'], data['head_loss_m'], 'm-', linewidth=2)
   ax3.set_xlabel('Tank Height (m)')
   ax3.set_ylabel('Head Loss (m)')
   ax3.set_title('System Efficiency (Head Loss)')
   ax3.grid(True)

   # Plot 4: Daily Refills Needed
   ax4 = fig.add_subplot(gs[2, 0])
   ax4.plot(data['height'], data['daily_refills_needed'], 'r-', linewidth=2)
   ax4.set_xlabel('Tank Height (m)')
   ax4.set_ylabel('Refills Needed per Day')
   ax4.set_title('Tank Refills Required (8-hour operation)')
   ax4.grid(True)

   # Plot 5: Water Velocity
   ax5 = fig.add_subplot(gs[2, 1])
   ax5.plot(data['height'], data['water_velocity_ms'], 'y-', linewidth=2)
   ax5.axhline(y=0.5, color='r', linestyle='--', label='Min velocity')
   ax5.axhline(y=3.0, color='r', linestyle='--', label='Max velocity')
   ax5.set_xlabel('Tank Height (m)')
   ax5.set_ylabel('Water Velocity (m/s)')
   ax5.set_title('Water Velocity in Pipes')
   ax5.grid(True)
   ax5.legend()

   plt.tight_layout()
   return fig

# %%
def generate_analysis_data():
   """
   Generate comprehensive analysis data for irrigation system configurations.

   Creates a dataset exploring various combinations of tank heights and volumes, 
   calculating system performance parameters for each combination.

   Parameters
   ----------
   None - Uses internal constants for analysis ranges:
       - Heights: 1m to 10m in 0.5m increments
       - Volumes: 1000L, 2000L, 3000L, 5000L tanks

   Returns
   -------
   pandas.DataFrame
       DataFrame containing analysis results with columns:
       - tank_volume: Tank size in liters
       - height: Tank elevation in meters
       - All parameters from calculate_drip_irrigation_parameters()
       - daily_refills_needed: Number of tank refills needed for 8h operation

   Notes
   -----
   - Uses calculate_drip_irrigation_parameters() for each configuration
   - Skips invalid configurations (where parameters calculation returns None)
   - Assumes 8-hour working day for refill calculations
   - Pressure is calculated using rho*g*h (hydrostatic pressure)
   """
   heights = np.arange(1, 11, 0.5)  # Heights from 1m to 10m
   volumes = [1000, 2000, 3000, 5000]  # Standard tank volumes
   results = []

   for volume in volumes:
       for height in heights:
           params = calculate_drip_irrigation_parameters(
               tank_volume_liters=volume,
               desired_pressure_kpa=height * 9.81
           )
           if params:  # Only add valid results
               params['tank_volume'] = volume
               params['height'] = height
               results.append(params)

   df = pd.DataFrame(results)
   # Calculate additional metrics for analysis
   df['daily_refills_needed'] = 8 / df['operating_time_hours']  # Assuming 8-hour working day
   return df

# %%
def create_interactive_analysis():
   """
   Create an interactive dashboard for gravity-fed irrigation system analysis.

   Generates a widget-based interface allowing users to dynamically adjust system
   parameters and see real-time analysis results.

   Parameters
   ----------
   None - Uses internal widgets with the following ranges:
       - Tank Volume: 500L, 1000L, 2000L, 3000L
       - Elevation: Any positive float value
       - Field Size: Any positive float value
       - Plant Count: Any positive integer
       - Plant Spacing: 0.2m to 1.0m

   Returns
   -------
   ipywidgets.interactive
       Interactive widget containing:
       - Input controls for system parameters
       - Real-time calculation output displaying:
           • Field specifications
           • Elevation and pressure analysis
           • System performance metrics
           • Warning indicators for sub-optimal conditions
           • Recommendations for limited elevation scenarios

   Notes
   -----
   - Uses calculate_drip_irrigation_parameters() for computations
   - Row spacing automatically set to 2x plant spacing
   - Provides warnings for:
       • Water velocity (<0.5 m/s or >2.0 m/s)
       • Frequent refills (>3 per 8h day)
       • Low pressure (<50 kPa)
       • Insufficient elevation
   """
   tank_volume_widget = widgets.Dropdown(
       options=[500, 1000, 2000, 3000],
       value=1000,
       description='Tank Volume (L):',
       style={'description_width': 'initial'}
   )
   
   # Add elevation input
   elevation_widget = widgets.FloatText(
       value=None,
       description='Available Elevation (m):',
       placeholder='Enter elevation or leave blank',
       style={'description_width': 'initial'}
   )
   
   # Modified field size input
   field_size_widget = widgets.FloatText(
       value=None,
       description='Field Size (m²):',
       placeholder='Enter size or leave blank',
       style={'description_width': 'initial'}
   )
   
   # Modified plant count input
   plant_count_widget = widgets.IntText(
       value=None,
       description='Number of Plants:',
       placeholder='Enter count or leave blank',
       style={'description_width': 'initial'}
   )
   
   plant_spacing_widget = widgets.FloatSlider(
       value=0.3,
       min=0.2,
       max=1.0,
       step=0.1,
       description='Plant Spacing (m):',
       style={'description_width': 'initial'}
   )
   
   def update_analysis(tank_volume, elevation, field_size, plant_count, plant_spacing):
       """
       Update the analysis display based on user inputs.
       
       Parameters
       ----------
       tank_volume : int
           Selected tank volume in liters
       elevation : float or None
           Available elevation in meters
       field_size : float or None
           Field area in square meters
       plant_count : int or None
           Number of plants to irrigate
       plant_spacing : float
           Distance between plants in meters
       """
       clear_output(wait=True)
       
       params = calculate_drip_irrigation_parameters(
           tank_volume_liters=tank_volume,
           tank_elevation_m=elevation if elevation else None,
           field_size_m2=field_size if field_size else None,
           number_of_plants=plant_count if plant_count else None,
           emitter_spacing_m=plant_spacing,
           row_spacing_m=plant_spacing * 2
       )
       
       if params:
           print("=== GRAVITY-FED IRRIGATION SYSTEM ANALYSIS ===\n")
           
           print("FIELD SPECIFICATIONS:")
           print(f"• Current field size: {params['current_field_size_m2']} m²")
           print(f"• Maximum possible field size: {params['max_coverage_area_m2']} m²")
           print(f"• Number of irrigation outlets: {params['total_emitters']}")
           print(f"• Approximate field length: {params['field_length_m']} m")
           
           print(f"\nELEVATION AND PRESSURE:")
           if elevation:
               print(f"• Available elevation: {elevation} m")
               print(f"• Recommended elevation: {params['recommended_elevation_m']} m")
               if not params['pressure_adequate']:
                   print("⚠️ Warning: Available elevation may not provide adequate pressure")
           else:
               print(f"• Recommended elevation: {params['recommended_elevation_m']} m")
           print(f"• Operating pressure: {params['operating_pressure_kpa']} kPa")
           print(f"• Friction losses: {params['friction_loss_m']} m")
           print(f"• Slope impact: {params['slope_impact_m']} m")
           
           print(f"\nSYSTEM PERFORMANCE:")
           print(f"• Flow rate: {params['flow_rate_total_lph']} L/hour")
           print(f"• Water velocity: {params['water_velocity_ms']} m/s")
           print(f"• Operating time per tank: {params['operating_time_hours']} hours")
           print(f"• Daily refills needed (8h): {params['daily_refills_needed']}")
           
           print("\nSYSTEM CHECKS:")
           if params['water_velocity_ms'] < 0.5:
               print("⚠️ Warning: Water velocity too low - may cause sediment buildup")
           if params['water_velocity_ms'] > 2.0:
               print("⚠️ Warning: Water velocity too high - may cause pipe wear")
           if params['daily_refills_needed'] > 3:
               print("⚠️ Warning: High number of refills needed - consider larger tank")
           if params['operating_pressure_kpa'] < 50:
               print("⚠️ Warning: Low pressure - emitters may not function properly")
           
           if elevation and elevation < params['recommended_elevation_m']:
               print("\nRECOMMENDATIONS FOR LIMITED ELEVATION:")
               print("1. Consider dividing field into smaller zones")
               print("2. Use lower flow-rate emitters")
               print("3. Increase emitter spacing")
               print("4. Consider timing irrigation during cooler hours")
   
   return widgets.interactive(
       update_analysis,
       tank_volume=tank_volume_widget,
       elevation=elevation_widget,
       field_size=field_size_widget,
       plant_count=plant_count_widget,
       plant_spacing=plant_spacing_widget
   )


# %%
def main():
   """
   Launch the Gravity Fed Drip Irrigation Planner interactive dashboard.

   Displays a welcome message and creates an interactive interface for designing 
   and analyzing gravity-fed irrigation systems.

   Parameters
   ----------
   None

   Returns
   -------
   ipywidgets.interactive
       Interactive dashboard widget with system design controls and real-time analysis.
       See create_interactive_analysis() for detailed widget specifications.

   Notes
   -----
   - Entry point for the irrigation planner application
   - Creates user-friendly interface for system parameter adjustment
   - Provides immediate feedback on system performance
   """
   print("Welcome to the Gravity Fed Drip Irrigation Planner!")
   print("This tool helps you optimize your irrigation system design based on tank height and volume.")
   print("\nAdjust the parameters below to see how they affect your irrigation system:")
   return create_interactive_analysis()

if __name__ == "__main__":
   dashboard = main()
   display(dashboard)


