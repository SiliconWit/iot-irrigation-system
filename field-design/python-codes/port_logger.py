#!/usr/bin/env python3
"""
Arduino Data Logger with CSV Output, Enhanced Terminal Output, and Data Cleaning

This script reads data from an Arduino board via serial communication,
parses and cleans the incoming data for temperature, humidity, and pressure readings,
logs this information to a CSV file, and provides professional terminal output.

Setup Instructions:
1. Install required library:
   pip install pyserial

2. Ensure you have permissions to access the serial port:
   sudo usermod -a -G dialout $USER
   (Log out and log back in for this to take effect)

3. Run the script:
   python arduino_data_logger.py

   Optional arguments:
   -p, --port: Specify the Arduino port (e.g., /dev/ttyUSB0)
   -o, --output: Specify the output CSV file (default: arduino_data.csv)

   Example: python arduino_data_logger.py -p /dev/ttyUSB0 -o my_data.csv
"""

import serial
import serial.tools.list_ports
import re
from datetime import datetime
import argparse
import sys
import csv
import time

def find_arduino_port():
    """
    Automatically find the Arduino port.
    
    Returns:
    str or None: The device name of the first USB port found, or None if no suitable port is found.
    """
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB' in p.device:
            return p.device
    return None

def clean_pressure(pressure_string):
    """
    Clean the pressure data by extracting only the valid pressure value.
    
    Args:
    pressure_string (str): The raw pressure string from the Arduino

    Returns:
    float: The cleaned pressure value
    """
    # Extract the first float value from the pressure string
    match = re.search(r'\d+\.\d+', pressure_string)
    if match:
        return float(match.group())
    return None

def read_arduino_data(port, baud_rate=9600, output_file='arduino_data.csv'):
    """
    Read data from Arduino, parse it, clean it, and save to a CSV file with enhanced terminal output.
    
    Args:
    port (str): Serial port to read from
    baud_rate (int): Baud rate for serial communication
    output_file (str): Name of the CSV file to save data
    """
    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser, \
             open(output_file, 'w', newline='') as csvfile:
            
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Temperature (°C)', 'Humidity (%)', 'Pressure (hPa)'])
            
            print(f"\n[INFO] Connected to {port}")
            print(f"[INFO] Logging data to {output_file}")
            print("[INFO] Press Ctrl+C to stop...")
            print("\n{:<19} {:<10} {:<12} {:<15}".format("Timestamp", "Temp(°C)", "Humidity(%)", "Pressure(hPa)"))
            print("-" * 60)
            
            last_data_time = time.time()
            while True:
                print("[STATUS] Listening for messages...", end='\r')
                line = ser.readline().decode('utf-8', errors='replace').strip()
                
                if line.startswith("Received:"):
                    match = re.search(r'T:(\d+\.\d+),H:(\d+\.\d+),P:(.+)', line)
                    if match:
                        temp, humidity, pressure_raw = match.groups()
                        pressure = clean_pressure(pressure_raw)
                        
                        if pressure is not None:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            csv_writer.writerow([timestamp, temp, humidity, pressure])
                            csvfile.flush()
                            
                            print(" " * 60, end='\r')  # Clear the "Listening for messages..." line
                            print("[RECEIVED] New data received")
                            print("{:<19} {:<10.2f} {:<12.2f} {:<15.2f}".format(
                                timestamp, float(temp), float(humidity), pressure))
                            
                            last_data_time = time.time()
                        else:
                            print("[WARNING] Invalid pressure data received", end='\r')
                elif time.time() - last_data_time > 10:  # No data received for 10 seconds
                    print(" " * 60, end='\r')  # Clear the "Listening for messages..." line
                    print("[WARNING] No data received in the last 10 seconds", end='\r')
                    time.sleep(1)  # Wait a bit before checking again
                
    except serial.SerialException as e:
        print(f"\n[ERROR] Serial communication error: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Stopping data collection...")

def main():
    """
    Main function to set up argument parsing and start the data logging process.
    """
    parser = argparse.ArgumentParser(description="Arduino Data Logger")
    parser.add_argument("-p", "--port", help="Specify the Arduino port (e.g., /dev/ttyUSB0)")
    parser.add_argument("-o", "--output", default="arduino_data.csv", help="Specify the output CSV file")
    args = parser.parse_args()

    if args.port:
        arduino_port = args.port
    else:
        arduino_port = find_arduino_port()
        if not arduino_port:
            print("[ERROR] Arduino port not found. Please specify the port using the -p option.")
            sys.exit(1)

    print(f"[INFO] Using Arduino port: {arduino_port}")
    
    read_arduino_data(arduino_port, output_file=args.output)
    
    print(f"\n[INFO] Data collection complete. Data saved to {args.output}")

if __name__ == "__main__":
    main()