#include <Arduino.h>
#include <RH_CC110.h>
#include <SPI.h>

// Pin Definitions for CC1101 connection to STM32 BluePill
// These definitions make it easier to change pins if needed
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
 * 
 * Note: The SPI pins (SCK, MOSI, MISO) are handled automatically by the SPI library
 * and don't need to be explicitly defined in the code.
 */

// Create an instance of the CC110 driver
// Parameters: Chip Select pin, GDO0 pin
RH_CC110 cc110(CC1101_CS_PIN, CC1101_GDO0_PIN);

// Define the onboard LED pin for visual feedback
#define LED_PIN PC13 // BluePill onboard LED is on PC13 and is active LOW

// Function to simulate temperature and humidity readings
// This function generates random values for demonstration purposes
void getRandomSensorData(float &temperature, float &humidity) {
  temperature = random(2000, 3100) / 100.0; // Random temp between 20.00 and 30.99
  humidity = random(3000, 8100) / 100.0;    // Random humidity between 30.00 and 80.99
}

void setup() {
  // Initialize the LED pin for status indication
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  // Turn off LED (it's active LOW)
  
  // Initialize SPI communication
  // This is necessary for communication with the CC1101 module
  SPI.begin();
  
  // Initialize the CC110 module
  while (!cc110.init()) {
    // If initialization fails, blink LED rapidly
    // This provides a visual indicator of initialization failure
    for (int i = 0; i < 10; i++) {
      digitalWrite(LED_PIN, LOW);  // LED on
      delay(100);
      digitalWrite(LED_PIN, HIGH); // LED off
      delay(100);
    }
  }
  
  // Set the transmitter frequency to 433 MHz
  // Note: Ensure this frequency is legal for use in your region
  cc110.setFrequency(433.0);
  
  // Set transmit power to maximum
  // TransmitPower10dBm is typically the highest setting
  // Adjust if needed based on your requirements and local regulations
  cc110.setTxPower(RH_CC110::TransmitPower10dBm);
  
  // Initialize random seed for sensor simulation
  // Using analogRead of an unconnected pin for randomness
  randomSeed(analogRead(PA0));
  
  // Blink LED three times to indicate successful setup
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);  // LED on
    delay(200);
    digitalWrite(LED_PIN, HIGH); // LED off
    delay(200);
  }
}

void loop() {
  float temperature, humidity;
  
  // Get simulated sensor data
  getRandomSensorData(temperature, humidity);
  
  // Prepare the message to be sent
  // Format: "T:XX.XX,H:YY.YY" where XX.XX is temperature and YY.YY is humidity
  char msg[32];
  snprintf(msg, sizeof(msg), "T:%d.%02d,H:%d.%02d", 
           (int)temperature, (int)(temperature*100)%100, 
           (int)humidity, (int)(humidity*100)%100);
  
  // Turn on LED to indicate transmission attempt
  digitalWrite(LED_PIN, LOW);
  
  // Send the message using the CC110 transmitter
  cc110.send((uint8_t *)msg, strlen(msg));
  cc110.waitPacketSent();
  
  // Turn off LED to indicate end of transmission
  digitalWrite(LED_PIN, HIGH);
  
  // Wait for 5 seconds before sending the next message
  // This delay can be adjusted based on your requirements
  delay(5000);
}