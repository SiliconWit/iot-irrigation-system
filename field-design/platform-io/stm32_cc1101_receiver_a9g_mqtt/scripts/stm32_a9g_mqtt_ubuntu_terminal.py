import paho.mqtt.client as mqtt
import csv
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CSV file to log the received data
CSV_FILE = "sensor_data_log.csv"
CSV_HEADER = ["Timestamp", "Temperature (°C)", "Humidity (%)", "Pressure (hPa)", "Location"]

# MQTT configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "/test/stm32/sensors"

def setup_csv_file():
    """Set up the CSV file with headers if it doesn't exist."""
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when the client connects to the broker."""
    if rc == 0:
        logging.info(f"Connected to MQTT broker: {MQTT_BROKER}")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        logging.error(f"Failed to connect to MQTT broker. Error code: {rc}")

def parse_sensor_data(message):
    """Parse sensor data from the message in the format T:21.24,H:69.37,P:814.87,L:9999.0."""
    try:
        # Split the message by commas and then by colons to get key-value pairs
        data_parts = message.split(',')
        data = {}
        for part in data_parts:
            key, value = part.split(':')
            data[key.strip()] = float(value.strip())

        return {
            'temperature': data.get('T', 9999.0),
            'humidity': data.get('H', 9999.0),
            'pressure': data.get('P', 9999.0),
            'location': data.get('L', 'Unknown') 
        }
    except Exception as e:
        logging.error(f"Failed to parse sensor data: {message}. Error: {e}")
        return None

def on_message(client, userdata, msg):
    """Callback when a message is received from the broker."""
    try:
        message = msg.payload.decode()
        logging.info(f"Received message on topic {msg.topic}: {message}")

        # Parse the sensor data
        parsed_data = parse_sensor_data(message)
        if parsed_data is None:
            return

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format the data for logging
        formatted_message = (
            f"Temp: {parsed_data['temperature']:.2f} °C, "
            f"Humid: {parsed_data['humidity']:.2f} %, "
            f"Press: {parsed_data['pressure']:.2f} hPa, "
            f"Location: {parsed_data['location']}"
        )
        logging.info(f"Formatted Data -> {formatted_message}")

        # Append the data to CSV file without the raw message column
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                parsed_data['temperature'],
                parsed_data['humidity'],
                parsed_data['pressure'],
                parsed_data['location']
            ])

    except Exception as e:
        logging.error(f"Error processing message: {e}")

def main():
    """Main function to set up and run the MQTT client."""
    setup_csv_file()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"Error connecting to MQTT broker: {e}")

if __name__ == "__main__":
    main()

