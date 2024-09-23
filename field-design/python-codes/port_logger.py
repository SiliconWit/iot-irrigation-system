"""
Simplified Arduino Data Logger with CSV Output

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

def find_arduino_port():
    """
    Automatically find the Arduino port.
    Returns the first USB port found, or None if no suitable port is found.
    """
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB' in p.device:
            return p.device
    return None

def read_arduino_data(port, baud_rate=9600, output_file='arduino_data.csv'):
    """
    Read data from Arduino and save to CSV file.
    
    Args:
    port (str): Serial port to read from
    baud_rate (int): Baud rate for serial communication
    output_file (str): Name of the CSV file to save data
    """
    try:
        # Open serial connection and CSV file
        with serial.Serial(port, baud_rate, timeout=1) as ser, \
             open(output_file, 'w', newline='') as csvfile:
            
            # Set up CSV writer
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Temperature (°C)', 'Humidity (%)'])
            
            print(f"Connected to {port}")
            print(f"Logging data to {output_file}")
            print("Press Ctrl+C to stop...")
            
            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8', errors='replace').strip()
                if line.startswith("Received:"):
                    # Extract temperature and humidity using regex
                    match = re.search(r'T:(\d+\.\d+),H:(\d+\.\d+)', line)
                    if match:
                        temp, humidity = map(float, match.groups())
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Write data to CSV
                        csv_writer.writerow([timestamp, temp, humidity])
                        csvfile.flush()  # Ensure data is written immediately
                        
                        print(f"Recorded: Timestamp: {timestamp}, Temperature: {temp}°C, Humidity: {humidity}%")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopping data collection...")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Arduino Data Logger")
    parser.add_argument("-p", "--port", help="Specify the Arduino port (e.g., /dev/ttyUSB0)")
    parser.add_argument("-o", "--output", default="arduino_data.csv", help="Specify the output CSV file")
    args = parser.parse_args()

    # Determine which port to use
    if args.port:
        arduino_port = args.port
    else:
        arduino_port = find_arduino_port()
        if not arduino_port:
            print("Error: Arduino port not found. Please specify the port using the -p option.")
            sys.exit(1)

    print(f"Using Arduino port: {arduino_port}")
    
    # Start reading data
    read_arduino_data(arduino_port, output_file=args.output)
    
    print(f"\nData collection complete. Data saved to {args.output}")

if __name__ == "__main__":
    main()