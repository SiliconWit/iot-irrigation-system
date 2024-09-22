# 8-Pin CC1101 Wireless Transceiver Module Guide

This document provides a guide on using the 8-pin CC1101 wireless transceiver module with Arduino boards. 

## CC1101 Overview

The CC1101 is a low-power sub-1GHz RF transceiver designed for very low-power wireless applications. Key features include:

- Frequency range: 300-348 MHz, 387-464 MHz and 779-928 MHz
- High sensitivity (-116 dBm at 0.6 kBaud, 433 MHz, 1% packet error rate)
- Low current consumption (14.7 mA in RX, 1.2 kBaud, 433 MHz)
- Programmable data rate from 0.6 to 600 kBaud
- OOK, 2-FSK, GFSK, and MSK modulation
- Built-in support for packet handling, data buffering, burst transmissions, and clear channel assessment

## Hardware Setup

### Pin Configuration

The 8-pin CC1101 module typically has the following pinout:

1. VCC
2. GND
3. MOSI
4. MISO
5. SCK
6. CSN
7. GDO0
8. GDO2 (not used in this setup)

### Connections

Connect the CC1101 to the Arduino as follows:

| CC1101 Pin | Arduino Pin |
|------------|-------------|
| VCC        | 3.3V        |
| GND        | GND         |
| MOSI       | D11         |
| MISO       | D12         |
| SCK        | D13         |
| CSN        | D10         |
| GDO0       | D2          |

**Note**: Ensure you're using a 3.3V Arduino or a logic level converter, as the CC1101 operates at 3.3V.

## Software Implementation

For testing, we created a simple system where one Arduino (Nano) acts as a transmitter, sending simulated temperature and humidity data, and another Arduino (Uno) acts as a receiver, displaying the received data.

### Transmitter Code (Arduino Nano)

```cpp
#include <RH_CC110.h>

RH_CC110 cc110;

void getRandomSensorData(float &temperature, float &humidity) {
  temperature = random(2000, 3100) / 100.0;
  humidity = random(3000, 8100) / 100.0;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Initializing CC110 on Nano...");
  if (!cc110.init()) {
    Serial.println("CC110 init failed");
    while (1);
  }
  
  Serial.println("CC110 init succeeded");
  cc110.setFrequency(433.0);
  Serial.println("Frequency set to 433.0 MHz");
  
  randomSeed(analogRead(0));
}

void loop() {
  float temperature, humidity;
  getRandomSensorData(temperature, humidity);
  
  char msg[32];
  snprintf(msg, sizeof(msg), "T:%.2f,H:%.2f", temperature, humidity);
  
  cc110.send((uint8_t *)msg, strlen(msg));
  cc110.waitPacketSent();
  
  Serial.print("Sent: ");
  Serial.println(msg);
  
  delay(5000);
}
```

### Receiver Code (Arduino Uno)

```cpp
#include <RH_CC110.h>

RH_CC110 cc110;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Initializing CC110 on Uno...");
  if (!cc110.init()) {
    Serial.println("CC110 init failed");
    while (1);
  }
  
  Serial.println("CC110 init succeeded");
  cc110.setFrequency(433.0);
  Serial.println("Frequency set to 433.0 MHz");
}

void loop() {
  Serial.println("Listening for messages...");
  
  uint8_t buf[RH_CC110_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
  
  if (cc110.waitAvailableTimeout(10000)) {
    if (cc110.recv(buf, &len)) {
      Serial.print("Received: ");
      Serial.println((char*)buf);
      
      float temperature, humidity;
      if (sscanf((char*)buf, "T:%f,H:%f", &temperature, &humidity) == 2) {
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
```

## Testing and Verification

1. Upload the transmitter code to the Arduino Nano and the receiver code to the Arduino Uno.
2. Open Serial Monitors for both devices (set to 9600 baud).
3. You should see the Nano sending temperature and humidity data every 5 seconds.
4. The Uno should receive these messages, parse them correctly, and display the parsed data.
5. Verify that the received data on the Uno matches the sent data from the Nano.

## Troubleshooting

1. **No data received**: 
   - Check all wiring connections.
   - Ensure both modules are powered and on the same frequency.
   - Verify that antennas are properly connected (if using external antennas).

2. **Garbled data**:
   - Check for interference sources nearby.
   - Try adjusting the frequency slightly.
   - Ensure proper grounding of both Arduino boards.

3. **Inconsistent reception**:
   - Reduce the distance between modules.
   - Check power supply stability.
   - Ensure the baud rates match on both the transmitter and receiver.

## Additional Information to Remember

1. **Range**: The effective range of the CC1101 module depends on various factors including antenna type, environmental conditions, and transmission power. Typical ranges can vary from 100 meters to several kilometers in ideal conditions.

2. **Frequency Selection**: While this guide uses 433 MHz, the CC1101 supports other frequencies. Ensure you're using a legally allowed frequency for your region.

3. **Power Consumption**: The CC1101 is designed for low-power applications. Implement sleep modes and efficient transmission schedules for battery-powered projects.

4. **Error Handling**: For real-world applications, implement error checking (e.g., CRC) and packet acknowledgment for more reliable communication.

5. **Encryption**: If security is a concern, implement data encryption before transmission.

6. **Multiple Nodes**: The CC1101 can be used in networks with multiple nodes. Implement addressing schemes for more complex setups.

7. **Antenna Selection**: The choice of antenna can significantly affect performance. Experiment with different antenna types for optimal results.

