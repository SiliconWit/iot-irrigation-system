// Arduino Nano Code (Transmitter)

#include <RH_CC110.h>

// Create an instance of the CC110 driver
RH_CC110 cc110;

// Pin definitions for CC1101 v2 connection to Arduino Uno
// CSN (pin 4) -> D10 (Arduino Uno)
// SCK (pin 5) -> D13
// MOSI (pin 6) -> D11
// MISO (pin 7) -> D12
// GDO0 (pin 3) -> D2
// GND (pin 1) -> GND 
// VCC (pin 2) -> 3.3 V
// GDO2 (pin 8) -> Not Used

// Function to simulate temperature and humidity readings
void getRandomSensorData(float &temperature, float &humidity) {
  temperature = random(2000, 3100) / 100.0; // Random temp between 20.00 and 30.99
  humidity = random(3000, 8100) / 100.0; // Random humidity between 30.00 and 80.99
}

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial port to be available
  
  Serial.println("Initializing CC110 on Nano...");
  if (!cc110.init()) {
    Serial.println("CC110 init failed");
    while (1); // If initialization fails, stop here
  }
  
  Serial.println("CC110 init succeeded");
  
  // Set frequency
  cc110.setFrequency(433.0);
  Serial.println("Frequency set to 433.0 MHz");

  // Initialize random seed for sensor simulation
  randomSeed(analogRead(0));
}

void loop() {
  float temperature, humidity;
  getRandomSensorData(temperature, humidity);
  
  // Prepare the message
  char msg[32];
  snprintf(msg, sizeof(msg), "T:%d.%02d,H:%d.%02d", 
           (int)temperature, (int)(temperature*100)%100, 
           (int)humidity, (int)(humidity*100)%100);
  
  // Send the message
  cc110.send((uint8_t *)msg, strlen(msg));
  cc110.waitPacketSent();
  
  Serial.print("Sent: ");
  Serial.println(msg);
  
  delay(5000); // Wait for 5 seconds before sending the next message
}
