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

def find_arduino_ports():
    """
    Find all potential Arduino ports.
    
    Returns:
    list: A list of device names of USB ports found.
    """
    return [p.device for p in serial.tools.list_ports.comports() if 'USB' in p.device]

def clean_pressure(pressure_string):
    """
    Clean the pressure data by extracting only the valid pressure value.
    
    Args:
    pressure_string (str): The raw pressure string from the Arduino

    Returns:
    float: The cleaned pressure value
    """
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

    available_ports = find_arduino_ports()
    
    if not available_ports:
        print("[ERROR] No Arduino ports found. Please check your connections.")
        sys.exit(1)

    if args.port:
        if args.port in available_ports:
            arduino_port = args.port
        else:
            print(f"[WARNING] Specified port {args.port} not found.")
            print(f"Available ports: {', '.join(available_ports)}")
            arduino_port = input("Please enter the port to use from the available ports: ")
            if arduino_port not in available_ports:
                print("[ERROR] Invalid port selected. Exiting.")
                sys.exit(1)
    else:
        if len(available_ports) == 1:
            arduino_port = available_ports[0]
        else:
            print("Available ports:")
            for i, port in enumerate(available_ports):
                print(f"{i+1}. {port}")
            choice = int(input("Enter the number of the port to use: ")) - 1
            if 0 <= choice < len(available_ports):
                arduino_port = available_ports[choice]
            else:
                print("[ERROR] Invalid choice. Exiting.")
                sys.exit(1)

    print(f"[INFO] Using Arduino port: {arduino_port}")
    
    read_arduino_data(arduino_port, output_file=args.output)
    
    print(f"\n[INFO] Data collection complete. Data saved to {args.output}")

if __name__ == "__main__":
    main()