"""
Smart Irrigation Control System
------------------------------
A comprehensive system for automated irrigation control incorporating:
- FAO Penman-Monteith equation for ETo calculation
- Real-time sensor feedback with uncertainty handling
- Growth stage-based water requirements
- Automated valve control
- Data logging and monitoring
- Safety checks and error handling
"""

import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import time
import json
import logging
import sqlite3
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('irrigation_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('IrrigationSystem')

@dataclass
class SensorSpecs:
    """Sensor specifications including uncertainty parameters"""
    range_min: float
    range_max: float
    accuracy: float
    sampling_rate: float  # in seconds

@dataclass
class SensorData:
    """Container for sensor readings with timestamp"""
    soil_moisture: float
    temperature: float
    humidity: float
    water_level: Optional[float]
    flow_rate: float
    # TODO: Future improvements
    # - Add solar_radiation (W/m²) for more accurate ETo calculation
    # - Add wind_speed (m/s) for improved evaporation estimates
    # - Consider adding rainfall sensor for precipitation tracking
    # - Add soil temperature sensor for root zone monitoring
    timestamp: datetime

class SensorConfig:
    """Sensor configuration and specifications"""
    SPECS = {
        "soil_moisture": SensorSpecs(0, 100, 2.0, 10),
        "temperature": SensorSpecs(-55, 125, 0.5, 10),
        "humidity": SensorSpecs(0, 100, 4.5, 10),
        "water_level": SensorSpecs(0, 100, 1.0, 1),
        "flow_rate": SensorSpecs(1, 30, 0.02, 1),
        # TODO: Future sensor additions
        # "solar_radiation": SensorSpecs(0, 1500, 10, 10),
        # "wind_speed": SensorSpecs(0, 50, 0.5, 10),
        # "rainfall": SensorSpecs(0, 500, 0.2, 1),
        # "soil_temp": SensorSpecs(-10, 50, 0.5, 10)
    }

class DatabaseManager:
    """Handles all database operations for sensor data and irrigation events"""
    def __init__(self, db_path: str = "irrigation_data.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """
        Initialize database tables
        TODO: Future improvements
        - Add sensor calibration table
        - Add system configuration table
        - Implement data archiving
        - Add error log table
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    timestamp DATETIME,
                    soil_moisture REAL,
                    temperature REAL,
                    humidity REAL,
                    water_level REAL,
                    flow_rate REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS irrigation_events (
                    timestamp DATETIME,
                    crop_type TEXT,
                    duration REAL,
                    water_volume REAL,
                    reason TEXT
                )
            """)
            conn.commit()

    def log_sensor_data(self, data: SensorData):
        """Log sensor readings to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.timestamp, data.soil_moisture, data.temperature,
                data.humidity, data.water_level, data.flow_rate
            ))
            conn.commit()

    def log_irrigation_event(self, crop_type: str, duration: float, 
                           water_volume: float, reason: str):
        """Log irrigation event to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO irrigation_events VALUES (?, ?, ?, ?, ?)
            """, (datetime.now(), crop_type, duration, water_volume, reason))
            conn.commit()

class SimplifiedETo:
    """Simplified ETo calculation with flexible options
    
    Calculations with optional Nyeri-Kenya-specific adjustments through location_adjust parameter.
    
    Nyeri Characteristics (for reference):
    - Altitude: ~1,750 meters
    - Location: Near equator (0°25'S)
    - Climate: Highland climate with two rainy seasons
    - Temperature range: 10-26°C typical
    - Relative Humidity: 60-84% typical
    """
    
    @staticmethod
    def calc_eto(temp: float, humidity: float, elevation: float = 100, 
                 fixed_eto: float = None, location_adjust: bool = False) -> float:
        """
        Calculate or return reference evapotranspiration (ETo)
        
        Parameters:
        -----------
        temp : float
            Mean temperature in Celsius
        humidity : float
            Relative humidity in %
        elevation : float, optional
            Site elevation in meters
        fixed_eto : float, optional
            Optional fixed ETo value (if provided, calculation is skipped)
        location_adjust : bool, optional
            Whether to apply Nyeri-specific adjustments (default False)
            
        Returns:
        --------
        tuple(float, str)
            - ETo in mm/day
            - Calculation method used
        """
        if fixed_eto is not None:
            return fixed_eto, "fixed"
            
        # Constants
        SOLAR_CONSTANT = 0.082  # MJ/m²/min
        
        # Estimate temperature range based on humidity
        # For Nyeri: Use 8.0°C minimum during location_adjust
        min_temp_range = 8.0 if location_adjust else 5.0
        temp_range = max(min_temp_range, 12.0 * (1 - humidity/100))
        
        # Extra-terrestrial radiation (Ra) approximation
        # For Nyeri: Adjust elevation factor for highland conditions
        if location_adjust:
            elevation_factor = 1 + (elevation/8000)  # Highland adjustment
        else:
            elevation_factor = 1 + elevation/10000   # Standard adjustment
            
        ra = SOLAR_CONSTANT * elevation_factor * 24 * 60 * 0.4  # MJ/m²/day
        ra_mm = ra * 0.408  # Convert to mm/day
        
        # Hargreaves-Samani equation
        eto = 0.0023 * (temp + 17.8) * (temp_range ** 0.5) * ra_mm
        
        # Humidity correction
        # For Nyeri: Use 0.12 factor during location_adjust
        humidity_coef = 0.12 if location_adjust else 0.15
        humidity_factor = 1.0 - humidity_coef * (humidity/100)
        
        min_factor = 0.88 if location_adjust else 0.85
        eto *= max(min_factor, min(humidity_factor, 1.0))
        
        # Output constraints
        # For Nyeri: Use 2.5-12.0 range during location_adjust
        if location_adjust:
            return max(2.5, min(eto, 12.0)), "calculated"
        else:
            return max(2.0, min(eto, 15.0)), "calculated"

    # Helper methods for Nyeri-specific calculations
    @staticmethod
    def get_nyeri_seasonal_factor(month: int) -> float:
        """Optional seasonal adjustment factor for Nyeri
        
        Can be used to post-process ETo values:
        adjusted_eto = eto * get_nyeri_seasonal_factor(month)
        
        Seasonal factors based on Nyeri's climate pattern:
        - Hot dry (Jan-Feb): 1.1
        - Long rains (Mar-May): 0.9
        - Cool dry (Jun-Sep): 1.0
        - Short rains (Oct-Dec): 0.9
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
        """Check if conditions are within typical Nyeri ranges
        
        Returns True if conditions are within typical ranges:
        - Temperature: 10-26°C
        - Humidity: 60-84%
        - Elevation: 1400-2500m
        """
        return (10 <= temp <= 26 and 
                60 <= humidity <= 84 and 
                1400 <= elevation <= 2500)


class ValveController:
    """Controls irrigation valves with safety checks"""
    def __init__(self):
        self.valve_states = {}
        self.max_open_time = 3600  # Maximum time a valve can stay open (1 hour)
        
    def open_valve(self, valve_id: str):
        """Open specified irrigation valve with safety check"""
        if valve_id in self.valve_states:
            if datetime.now() - self.valve_states[valve_id] > timedelta(seconds=self.max_open_time):
                logger.warning(f"Valve {valve_id} has been open too long - forcing close")
                self.close_valve(valve_id)
                return False
        
        # In real implementation, add hardware control code here
        self.valve_states[valve_id] = datetime.now()
        logger.info(f"Opened valve {valve_id}")
        return True
        
    def close_valve(self, valve_id: str):
        """Close specified irrigation valve"""
        # In real implementation, add hardware control code here
        if valve_id in self.valve_states:
            del self.valve_states[valve_id]
        logger.info(f"Closed valve {valve_id}")

class CropManager:
    """Manages crop-specific parameters and growth stages"""
    def __init__(self, crop_type: str, planting_date: datetime):
        self.crop_type = crop_type
        self.planting_date = planting_date
        
        # Crop parameters
        self.parameters = {
            "beans": {
                "moisture_min": 65,
                "moisture_max": 85,
                "temp_max": 26,
                "humidity_target": 85,
                "water_level": None
            },
            "maize": {
                "moisture_min": 55,
                "moisture_max": 65,
                "temp_max": 30,
                "humidity_target": 55,
                "water_level": None
            },
            "onions": {
                "moisture_min": 50,
                "moisture_max": 65,
                "temp_max": 24,
                "humidity_target": 70,
                "water_level": None
            },
            "rice": {
                "moisture_min": 95,
                "moisture_max": 100,
                "temp_max": 37,
                "humidity_target": 60,
                "water_level": (15, 45)
            }
        }
        
        # Growth stages and crop coefficients
        self.stages = {
            "beans": {
                "initial": (0.35, 15),
                "development": (0.7, 25),
                "mid_season": (1.1, 35),
                "late_season": (0.3, 20)
            },
            "maize": {
                "initial": (0.4, 20),
                "development": (0.8, 35),
                "mid_season": (1.15, 40),
                "late_season": (0.7, 30)
            },
            "onions": {
                "initial": (0.5, 15),
                "development": (0.8, 25),
                "mid_season": (1.05, 70),
                "late_season": (0.85, 40)
            },
            "rice": {
                "initial": (1.1, 60),
                "development": (0, 0),
                "mid_season": (1.2, 60),
                "late_season": (1.0, 30)
            }
        }

    def get_current_stage(self) -> Tuple[str, float]:
        """Determine current growth stage and crop coefficient"""
        days_since_planting = (datetime.now() - self.planting_date).days
        cumulative_days = 0
        
        for stage, (kc, duration) in self.stages[self.crop_type].items():
            cumulative_days += duration
            if days_since_planting <= cumulative_days:
                return stage, kc
        
        # If beyond all stages, return last stage
        return "late_season", self.stages[self.crop_type]["late_season"][0]

class IrrigationController:
    """Main irrigation control system"""
    def __init__(self, crop_type: str, plot_dimensions: Tuple[float, float],
                 planting_date: datetime, valve_id: str):
        self.crop_manager = CropManager(crop_type, planting_date)
        self.valve_controller = ValveController()
        self.db_manager = DatabaseManager()
        self.plot_area = plot_dimensions[0] * plot_dimensions[1]
        self.valve_id = valve_id
        
        # Initialize uncertainty handling
        self.measurement_window = []
        self.window_size = 5  # Number of measurements to consider for uncertainty
        
    def read_sensors(self) -> SensorData:
        """
        Read all sensors with uncertainty handling
        TODO: Future improvements
        - Add integration with actual hardware sensors
        - Implement sensor calibration routines
        - Add sensor health monitoring
        - Include data quality checks
        - Add support for wireless sensors
        - Implement sensor redundancy
        """
        base_moisture = np.random.normal(
            (self.crop_manager.parameters[self.crop_manager.crop_type]["moisture_min"] +
            self.crop_manager.parameters[self.crop_manager.crop_type]["moisture_max"]) / 2,
            SensorConfig.SPECS["soil_moisture"].accuracy
        )
        
        data = SensorData(
            soil_moisture=base_moisture,
            temperature=np.random.normal(25, SensorConfig.SPECS["temperature"].accuracy),
            humidity=np.random.normal(60, SensorConfig.SPECS["humidity"].accuracy),
            water_level=np.random.normal(30, SensorConfig.SPECS["water_level"].accuracy),
            flow_rate=np.random.normal(15, SensorConfig.SPECS["flow_rate"].accuracy),
            timestamp=datetime.now()
        )
        
        return data

    def handle_measurement_uncertainty(self, data: SensorData) -> SensorData:
        """
        Apply moving average filter to handle measurement uncertainty
        TODO: Future improvements
        - Add outlier detection
        - Implement Kalman filtering
        - Add sensor drift compensation
        - Include cross-sensor validation
        """
        self.measurement_window.append(data)
        if len(self.measurement_window) > self.window_size:
            self.measurement_window.pop(0)
        
        # Calculate moving averages
        avg_data = SensorData(
            soil_moisture=np.mean([d.soil_moisture for d in self.measurement_window]),
            temperature=np.mean([d.temperature for d in self.measurement_window]),
            humidity=np.mean([d.humidity for d in self.measurement_window]),
            water_level=np.mean([d.water_level for d in self.measurement_window]) if data.water_level is not None else None,
            flow_rate=np.mean([d.flow_rate for d in self.measurement_window]),
            timestamp=data.timestamp
        )
        
        return avg_data


    def calculate_irrigation_need(self, sensor_data: SensorData) -> Tuple[bool, float, float]:
        """
        Determine if irrigation is needed and calculate duration
        TODO: Future improvements
        - Add weather forecast integration
        - Implement soil type adjustments
        - Add crop stress indicators
        - Include historical irrigation patterns
        - Add machine learning for optimization
        """
        # Get current growth stage and crop coefficient
        stage, kc = self.crop_manager.get_current_stage()
        
        # Calculate ETo using simplified method - extract just the ETo value, not the tuple
        eto, _ = SimplifiedETo.calc_eto(
            sensor_data.temperature,
            sensor_data.humidity
        )
        
        # Calculate base water requirement
        daily_requirement = float(eto) * float(kc) * float(self.plot_area)  # Ensure float multiplication
        
        # Adjust based on soil moisture
        params = self.crop_manager.parameters[self.crop_manager.crop_type]
        target_moisture = (params["moisture_min"] + params["moisture_max"]) / 2
        moisture_deficit = target_moisture - sensor_data.soil_moisture
        
        # Decision making
        if moisture_deficit > 0:
            # Calculate irrigation duration based on flow rate
            # Ensure all values are floats
            duration = (float(daily_requirement) * float(moisture_deficit) / 100.0) / float(sensor_data.flow_rate)
            return True, min(float(duration), 3600.0), moisture_deficit  # Cap at 1 hour
        
        return False, 0.0, moisture_deficit

    def control_loop(self):
        """Main control loop"""
        while True:
            try:
                # Read sensors
                raw_data = self.read_sensors()
                sensor_data = self.handle_measurement_uncertainty(raw_data)
                
                # Check irrigation need and get moisture deficit
                need_irrigation, duration, moisture_deficit = self.calculate_irrigation_need(sensor_data)
                
                if need_irrigation:
                    # Safety checks before irrigation
                    if self._safety_checks(sensor_data):
                        logger.info(f"Starting irrigation for {duration:.1f} seconds")
                        
                        # Open valve
                        if self.valve_controller.open_valve(self.valve_id):
                            irrigation_start_time = datetime.now()
                            
                            # Monitor irrigation
                            try:
                                self._monitor_irrigation(duration, sensor_data)
                            finally:
                                # Ensure valve is closed
                                self.valve_controller.close_valve(self.valve_id)
                                
                            # Calculate actual water volume
                            actual_duration = (datetime.now() - irrigation_start_time).total_seconds()
                            water_volume = actual_duration * sensor_data.flow_rate / 60  # L
                            
                            # Log irrigation event with the moisture deficit
                            self.db_manager.log_irrigation_event(
                                self.crop_manager.crop_type,
                                actual_duration,
                                water_volume,
                                f"Moisture deficit: {moisture_deficit:.1f}%"
                            )
                
                # Wait for next cycle
                time.sleep(SensorConfig.SPECS["soil_moisture"].sampling_rate)
                
            except Exception as e:
                logger.error(f"Error in control loop: {str(e)}")
                # Ensure valve is closed in case of error
                self.valve_controller.close_valve(self.valve_id)
                time.sleep(60)  # Wait before retrying

    def _safety_checks(self, sensor_data: SensorData) -> bool:
        """Perform safety checks before irrigation"""
        try:
            # Check sensor readings are within valid ranges
            for param, value in {
                "soil_moisture": sensor_data.soil_moisture,
                "temperature": sensor_data.temperature,
                "humidity": sensor_data.humidity,
                "flow_rate": sensor_data.flow_rate
            }.items():
                specs = SensorConfig.SPECS[param]
                if not specs.range_min <= value <= specs.range_max:
                    logger.warning(f"Invalid {param} reading: {value}")
                    return False
            
            # Special checks for rice
            if (self.crop_manager.crop_type == "rice" and 
                sensor_data.water_level is not None):
                min_level, max_level = self.crop_manager.parameters["rice"]["water_level"]
                if sensor_data.water_level > max_level:
                    logger.warning(f"Water level too high: {sensor_data.water_level}mm")
                    return False
            
            # Check for extreme temperature conditions
            max_temp = self.crop_manager.parameters[self.crop_manager.crop_type]["temp_max"]
            if sensor_data.temperature > max_temp + 5:  # 5°C buffer
                logger.warning(f"Temperature too high: {sensor_data.temperature}°C")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in safety checks: {str(e)}")
            return False

    def _monitor_irrigation(self, planned_duration: float, initial_data: SensorData):
        """Monitor irrigation process and adjust if needed"""
        start_time = datetime.now()
        check_interval = 5  # seconds
        
        while (datetime.now() - start_time).total_seconds() < planned_duration:
            try:
                # Read sensors
                current_data = self.read_sensors()
                
                # Check for abnormal conditions
                if self._detect_abnormal_conditions(current_data, initial_data):
                    logger.warning("Abnormal conditions detected during irrigation")
                    break
                
                # For rice, monitor water level
                if (self.crop_manager.crop_type == "rice" and 
                    current_data.water_level is not None):
                    _, max_level = self.crop_manager.parameters["rice"]["water_level"]
                    if current_data.water_level >= max_level:
                        logger.info("Target water level reached for rice")
                        break
                
                time.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error during irrigation monitoring: {str(e)}")
                break

    def _detect_abnormal_conditions(self, current: SensorData, 
                                  initial: SensorData) -> bool:
        """Detect abnormal conditions during irrigation"""
        try:
            # Check for sudden changes in flow rate
            if abs(current.flow_rate - initial.flow_rate) > 5:  # L/min
                logger.warning("Abnormal flow rate change detected")
                return True
            
            # Check for excessive moisture increase
            moisture_change = current.soil_moisture - initial.soil_moisture
            if moisture_change > 20:  # %
                logger.warning("Excessive moisture increase detected")
                return True
            
            # Check for flooding conditions
            if current.water_level is not None:
                if current.water_level > 95:  # mm
                    logger.warning("Flooding condition detected")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in abnormal condition detection: {str(e)}")
            return True

class IrrigationSystem:
    """Main system class for managing multiple irrigation controllers"""
    def __init__(self):
        self.controllers: Dict[str, IrrigationController] = {}
        self.db_manager = DatabaseManager()
        
    def add_plot(self, plot_id: str, crop_type: str, 
                 dimensions: Tuple[float, float], 
                 planting_date: datetime,
                 valve_id: str):
        """Add a new plot to the irrigation system"""
        self.controllers[plot_id] = IrrigationController(
            crop_type, dimensions, planting_date, valve_id)
        logger.info(f"Added new plot {plot_id} with crop type {crop_type}")
        
    def start_system(self):
        """Start the irrigation system"""
        logger.info("Starting irrigation system")
        
        # Create threads for each controller
        import threading
        threads = []
        
        for plot_id, controller in self.controllers.items():
            thread = threading.Thread(
                target=controller.control_loop,
                name=f"Controller-{plot_id}"
            )
            thread.daemon = True
            threads.append(thread)
            
        # Start all threads
        for thread in threads:
            thread.start()
            
        try:
            # Keep main thread alive
            while True:
                time.sleep(60)
                self._system_health_check()
                
        except KeyboardInterrupt:
            logger.info("Shutting down irrigation system")
            # Cleanup will happen automatically as threads are daemonic
            
    def _system_health_check(self):
        """Perform system-wide health check"""
        for plot_id, controller in self.controllers.items():
            try:
                # Check valve states
                if len(controller.valve_controller.valve_states) > 0:
                    logger.info(f"Plot {plot_id} has active irrigation")
                
                # Check sensor readings
                sensor_data = controller.read_sensors()
                if not controller._safety_checks(sensor_data):
                    logger.warning(f"Safety check failed for plot {plot_id}")
                
            except Exception as e:
                logger.error(f"Health check failed for plot {plot_id}: {str(e)}")



def calculate_water_volume(crop_type: str, stage: str, kc: float, duration: int, 
                         eto: float, plot_area: float, eto_source: str) -> float:
    """Calculate water volume requirement for a growth stage"""
    # Base water requirement
    water_req = eto * kc * plot_area * duration
    logger.info(f"Using {eto_source} ETo value: {eto:.2f} mm/day for {crop_type} {stage}")
    
    # Additional requirements for rice
    if crop_type == "rice":
        if stage == "initial":
            water_req += 2 * duration  # Saturation water
        if stage != "development":
            water_req += 6 * duration  # Percolation
            water_req += (1/3) * duration  # Water layer maintenance
    
    return water_req



class TestDataGenerator:
    """Generates test data for irrigation system validation"""
    def __init__(self, system: IrrigationSystem, fixed_eto: float = None):
        self.system = system
        self.results = {}
        self.fixed_eto = fixed_eto
        
    def generate_stage_requirements(self):
        """Calculate water requirements for all crops and growth stages"""
        logger.info("Generating stage-wise water requirements")
        
        test_conditions = {
            'temperature': 25.0,
            'humidity': 60.0,
            'soil_moisture': 70.0,
            'water_level': 30.0,
            'flow_rate': 15.0
        }
        
        # Get ETo value (fixed or calculated)
        eto, eto_source = SimplifiedETo.calc_eto(
            test_conditions['temperature'],
            test_conditions['humidity'],
            fixed_eto=self.fixed_eto
        )
        
        # Collect results for all crops
        crops_data = {}
        for plot_id, controller in self.system.controllers.items():
            crop_type = controller.crop_manager.crop_type
            stage_reqs = []
            
            for stage in ['initial', 'development', 'mid_season', 'late_season']:
                kc, duration = controller.crop_manager.stages[crop_type][stage]
                water_req = calculate_water_volume(
                    crop_type, stage, kc, duration, 
                    eto, controller.plot_area, eto_source
                )
                stage_reqs.append(water_req)
            
            # Add total to stage requirements
            stage_reqs.append(sum(stage_reqs))
            crops_data[crop_type] = stage_reqs
            self.results[crop_type] = dict(zip(
                ['initial', 'development', 'mid_season', 'late_season', 'total'], 
                stage_reqs
            ))
        
        # Print formatted table with units
        print("\nCalculated Water Requirements by Growth Stage:")
        print("-" * 82)
        print(f"{'Crop':<10} {'Initial':>12} {'Development':>12} {'Mid-Season':>12} {'Late-Season':>12} {'Total':>12}")
        print(f"{'':10} {'(L)':>12} {'(L)':>12} {'(L)':>12} {'(L)':>12} {'(L)':>12}")
        print("-" * 82)
        
        # Sort crops alphabetically
        for crop in sorted(crops_data.keys()):
            values = [f"{val:>12.2f}" for val in crops_data[crop]]
            print(f"{crop:<10} {' '.join(values)}")
        
        print("-" * 82)
        return self.results

class IntercroppingAnalyzer:
    """Analyzes water requirements for intercropping combinations"""
    def __init__(self, test_generator: TestDataGenerator):
        self.test_generator = test_generator
        # Define interaction factors - water reduction due to beneficial interactions
        self.interaction_factors = {
            ('maize', 'beans'): 0.85,  # 15% water reduction
            ('beans', 'maize'): 0.85,
            ('onions', 'maize'): 0.95,  # 5% water reduction
            ('maize', 'onions'): 0.95,
            ('beans', 'onions'): 0.90,  # 10% water reduction
            ('onions', 'beans'): 0.90
        }

    def analyze_combinations(self):
        """Analyze water requirements for different intercropping combinations"""
        logger.info("Analyzing intercropping combinations")
        
        try:
            # Get base requirements
            print("\nWater Requirements Summary:")
            print("-" * 90)
            base_reqs = self.test_generator.generate_stage_requirements()
            
            # Print intercropping analysis header
            print("\nIntercropping Analysis Results:")
            print("-" * 100)
            print(f"{'Crop Combination':<20} {'Individual Sum':>15} {'Combined Req':>15} {'Water Saving':>15} {'Saving %':>15}")
            print(f"{'':20} {'(L)':>15} {'(L)':>15} {'(L)':>15} {'(%)':>15}")
            print("-" * 100)
            
            # Analyze common intercropping combinations
            combinations = [
                ('maize', 'beans'),
                ('maize', 'onions'),
                ('beans', 'onions')
            ]
            
            total_savings = 0
            for crop1, crop2 in combinations:
                # Calculate individual total requirements
                total1 = base_reqs[crop1]['total']
                total2 = base_reqs[crop2]['total']
                individual_sum = total1 + total2
                
                if individual_sum > 0:
                    # Calculate combined requirement with interaction factor
                    interaction_factor = self.interaction_factors.get((crop1, crop2), 1.0)
                    combined_req = individual_sum * interaction_factor
                    
                    # Calculate savings
                    water_saving = individual_sum - combined_req
                    saving_percent = (water_saving / individual_sum) * 100
                    total_savings += water_saving
                    
                    # Print results with crop names properly formatted
                    combo_name = f"{crop1}+{crop2}"
                    print(f"{combo_name:<20} {individual_sum:>15.2f} {combined_req:>15.2f} "
                          f"{water_saving:>15.2f} {saving_percent:>14.1f}%")
            
            print("-" * 100)
            print(f"{'Total potential savings':>50}: {total_savings:>15.2f} L")
            print("-" * 100)
            
            # Print explanatory notes
            print("\nNotes:")
            print("- Individual Sum: Total water requirement if crops are grown separately")
            print("- Combined Req: Water requirement when crops are intercropped")
            print("- Water Saving: Reduction in water use due to intercropping")
            print("- Saving %: Percentage of water saved through intercropping")
            
        except Exception as e:
            logger.error(f"Error in intercropping analysis: {str(e)}")
            print("Error occurred during analysis. Check logs for details.")



def main():
    """Main function to run the irrigation system"""
    try:
        # Initialize system
        system = IrrigationSystem()
        
        # Add plots
        plots = [
            ("plot1", "rice", (0.6, 0.6), datetime(2024, 3, 1), "valve1"),
            ("plot2", "maize", (0.6, 0.6), datetime(2024, 3, 15), "valve2"),
            ("plot3", "beans", (0.6, 0.6), datetime(2024, 3, 10), "valve3"),
            ("plot4", "onions", (0.6, 0.6), datetime(2024, 3, 5), "valve4")
        ]
        
        for plot_id, crop_type, dimensions, planting_date, valve_id in plots:
            system.add_plot(plot_id, crop_type, dimensions, planting_date, valve_id)
        
        while True:
            print("\nIrrigation System Options:")
            print("1. Run water requirement analysis")
            print("2. Run intercropping analysis")
            print("3. Start real-time monitoring")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                # Ask for ETo preference
                eto_choice = input("Use fixed ETo value? (y/n): ").lower()
                fixed_eto = float(input("Enter ETo value (mm/day): ")) if eto_choice == 'y' else None
                
                # Generate test data
                test_generator = TestDataGenerator(system, fixed_eto)
                test_generator.generate_stage_requirements()
                
            elif choice == '2':
                # Ask for ETo preference
                eto_choice = input("Use fixed ETo value? (y/n): ").lower()
                fixed_eto = float(input("Enter ETo value (mm/day): ")) if eto_choice == 'y' else None
                
                # Generate test data and analyze intercropping
                test_generator = TestDataGenerator(system, fixed_eto)
                intercrop_analyzer = IntercroppingAnalyzer(test_generator)
                intercrop_analyzer.analyze_combinations()
                
            elif choice == '3':
                logger.info("Starting real-time monitoring")
                system.start_system()
                break
                
            elif choice == '4':
                logger.info("Exiting system")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()