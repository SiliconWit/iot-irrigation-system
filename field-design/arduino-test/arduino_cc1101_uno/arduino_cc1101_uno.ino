// Arduino Uno Code (Receiver)

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

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial port to be available
  
  Serial.println("Initializing CC110 on Uno...");
  if (!cc110.init()) {
    Serial.println("CC110 init failed");
    while (1); // If initialization fails, stop here
  }
  
  Serial.println("CC110 init succeeded");
  
  // Set frequency
  cc110.setFrequency(433.0);
  Serial.println("Frequency set to 433.0 MHz");
}

void loop() {
  Serial.println("Listening for messages...");
  
  uint8_t buf[RH_CC110_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
  
  if (cc110.waitAvailableTimeout(10000)) { // Wait for up to 10 seconds for a message
    if (cc110.recv(buf, &len)) {
      // Message received, print it
      Serial.print("Received: ");
      Serial.println((char*)buf);
      
      // Parse and display the data
      int temp_int, temp_frac, hum_int, hum_frac;
      if (sscanf((char*)buf, "T:%d.%d,H:%d.%d", &temp_int, &temp_frac, &hum_int, &hum_frac) == 4) {
        float temperature = temp_int + temp_frac / 100.0;
        float humidity = hum_int + hum_frac / 100.0;
        
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print("°C, Humidity: ");
        Serial.print(humidity);
        Serial.println("%");
      } else {
        Serial.println("Failed to parse data");
      }
    } else {
      Serial.println("Receive failed");
    }
  } else {
    Serial.println("No message received");
  }
}
