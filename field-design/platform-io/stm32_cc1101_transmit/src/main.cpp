#include <Arduino.h>
#include <RH_CC110.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

// Pin Definitions for CC1101 connection to STM32 BluePill
#define CC1101_CS_PIN PA4   // Chip Select (CSN) pin
#define CC1101_GDO0_PIN PA3 // General Digital Output 0 pin

/* Complete CC1101 to STM32 BluePill Connection Guide:
 * CC1101 Pin | BluePill Pin | Function
 * -----------|--------------|----------
 * 1 (GND)    | GND          | Ground
 * 2 (VCC)    | 3.3V         | Power (3.3V only!)
 * 3 (GDO0)   | PA3          | General Digital Output 0 (Configurable)
 * 4 (CSN)    | PA4          | SPI Chip Select
 * 5 (SCK)    | PA5          | SPI Clock
 * 6 (MOSI)   | PA7          | SPI Master Out Slave In
 * 7 (MISO)   | PA6          | SPI Master In Slave Out
 * 8 (GDO2)   | Not Connected| General Digital Output 2 (Not used in this code)
 */

/* AHT20 and BMP280 to STM32 BluePill Connection Guide:
 * Sensor Pin | BluePill Pin | Function
 * -----------|--------------|----------
 * VCC        | 3.3V         | Power (3.3V)
 * GND        | GND          | Ground
 * SDA        | PB7          | I2C Data
 * SCL        | PB6          | I2C Clock
 */

// Create an instance of the CC110 driver
RH_CC110 cc110(CC1101_CS_PIN, CC1101_GDO0_PIN);

// Define the onboard LED pin for visual feedback
#define LED_PIN PC13 // BluePill onboard LED is on PC13 and is active LOW

// Create instances of the sensor objects
Adafruit_AHTX0 aht;
Adafruit_BMP280 bmp;

// Function to read sensor data
void getSensorData(float &temperature, float &humidity, float &pressure) {
  sensors_event_t humidity_event, temp_event;
  
  if (aht.getEvent(&humidity_event, &temp_event)) {
    temperature = temp_event.temperature;
    humidity = humidity_event.relative_humidity;
  } else {
    temperature = humidity = -999.99;  // Error value
  }

  pressure = bmp.readPressure() / 100.0;  // Convert Pa to hPa
  if (isnan(pressure)) {
    pressure = -999.99;  // Error value
  }
}

void setup() {
  // Initialize the LED pin for status indication
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  // Turn off LED (it's active LOW)
  
  // Initialize I2C communication
  Wire.begin();
  
  // Initialize SPI communication
  SPI.begin();
  
  // Initialize the CC110 module
  while (!cc110.init()) {
    // If initialization fails, blink LED rapidly
    for (int i = 0; i < 10; i++) {
      digitalWrite(LED_PIN, LOW);  // LED on
      delay(100);
      digitalWrite(LED_PIN, HIGH); // LED off
      delay(100);
    }
  }
  
  // Set the transmitter frequency to 433 MHz
  cc110.setFrequency(433.0);
  
  // Set transmit power to maximum
  cc110.setTxPower(RH_CC110::TransmitPower10dBm);
  
  // Initialize sensors
  aht.begin();
  bmp.begin(0x77);  // BMP280 I2C address is typically 0x76 or 0x77
  
  // Configure BMP280 settings for weather monitoring
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);
  
  // Blink LED three times to indicate successful setup
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);  // LED on
    delay(200);
    digitalWrite(LED_PIN, HIGH); // LED off
    delay(200);
  }
}

void loop() {
  float temperature, humidity, pressure;
  
  // Get real sensor data
  getSensorData(temperature, humidity, pressure);
  
  // Prepare the message to be sent
  // Format: "T:XX.XX,H:YY.YY,P:ZZZZ.ZZ" where XX.XX is temperature, YY.YY is humidity, and ZZZZ.ZZ is pressure
  char msg[48];
  snprintf(msg, sizeof(msg), "T:%d.%02d,H:%d.%02d,P:%d.%02d", 
           (int)temperature, abs((int)(temperature*100)%100), 
           (int)humidity, abs((int)(humidity*100)%100),
           (int)pressure, abs((int)(pressure*100)%100));
  
  // Turn on LED to indicate transmission attempt
  digitalWrite(LED_PIN, LOW);
  
  // Send the message using the CC110 transmitter
  cc110.send((uint8_t *)msg, strlen(msg));
  cc110.waitPacketSent();
  
  // Turn off LED to indicate end of transmission
  digitalWrite(LED_PIN, HIGH);
  
  // Wait for 5 seconds before sending the next message
  delay(5000);
}