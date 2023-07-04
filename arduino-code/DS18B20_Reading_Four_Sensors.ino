//Rquired Libraries 
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is connected to individual pins
#define block1Temperature 7
#define block2Temperature 8
#define block3Temperature 9
#define block4Temperature 10

// Define the number of sensors
#define NUM_SENSORS 4

// Setup oneWire instances for each sensor
OneWire oneWireSensor1(block1Temperature);
OneWire oneWireSensor2(block2Temperature);
OneWire oneWireSensor3(block3Temperature);
OneWire oneWireSensor4(block4Temperature);

// Pass oneWire references to DallasTemperature library
DallasTemperature sensor1(&oneWireSensor1);
DallasTemperature sensor2(&oneWireSensor2);
DallasTemperature sensor3(&oneWireSensor3);
DallasTemperature sensor4(&oneWireSensor4);

// Array to store the addresses of the sensors
DeviceAddress sensor1Address;
DeviceAddress sensor2Address;
DeviceAddress sensor3Address;
DeviceAddress sensor4Address;

void setup() {
  // Start serial communication
  Serial.begin(9600);

  // Initialize the DS18B20 sensors
  sensor1.begin();
  sensor2.begin();
  sensor3.begin();
  sensor4.begin();

  // Get the addresses of the sensors
  sensor1.getAddress(sensor1Address, 0);
  sensor2.getAddress(sensor2Address, 0);
  sensor3.getAddress(sensor3Address, 0);
  sensor4.getAddress(sensor4Address, 0);
}

void loop() {
  // Request temperature from each sensor
  sensor1.requestTemperatures();
  sensor2.requestTemperatures();
  sensor3.requestTemperatures();
  sensor4.requestTemperatures();

  // Read and display the temperature for each sensor
  float temperatureC;

  // Sensor 1
  temperatureC = sensor1.getTempC(sensor1Address);
  displayTemperature(1, temperatureC);

  // Sensor 2
  temperatureC = sensor2.getTempC(sensor2Address);
  displayTemperature(2, temperatureC);

  //Sensor 3
  temperatureC = sensor3.getTempC(sensor3Address);
  displayTemperature(3, temperatureC);

  // Sensor 4
  temperatureC = sensor4.getTempC(sensor4Address);
  displayTemperature(4, temperatureC);

  // Wait for a second before reading the temperatures again
  delay(1000);
}

// Function to display temperature on the serial monitor
void displayTemperature(int sensorNumber, float temperature) {
  // Check if the temperature is valid (not an error value)
  if (temperature != DEVICE_DISCONNECTED_C) {
    // Display the temperature on the serial monitor
    Serial.print("Sensor ");
    //Serial.print(sensorNumber);
    Serial.print(" Temperature: ");
    Serial.print(temperature);
    Serial.println("°C");
  } else {
    // If an error occurred, display an error message
    Serial.print("Error: Could not read temperature data from Sensor ");
    Serial.println(sensorNumber);
  }
}
