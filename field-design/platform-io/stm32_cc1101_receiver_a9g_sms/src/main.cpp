#include <Arduino.h>
#include <RH_CC110.h>
#include <SPI.h>
#include <HardwareSerial.h>

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

/* A9G to STM32 BluePill Connection Guide:
 * A9G Pin    | BluePill Pin | Function
 * -----------|--------------|----------
 * TXD        | PA10         | UART RX (connect to BluePill's UART1 RX)
 * RXD        | PA9          | UART TX (connect to BluePill's UART1 TX)
 * GND        | GND          | Ground
 * VCC        | Not Connected| Power (A9G powered separately via USB)
 */

#define LED_PIN PC13
#define LED_ON LOW
#define LED_OFF HIGH

#define SMS_INTERVAL 180000 // 3 minutes in milliseconds

// Initialize CC1101 radio module
RH_CC110 cc110(CC1101_CS_PIN, CC1101_GDO0_PIN);

// Initialize UART for A9G module
HardwareSerial A9GSerial(PA10, PA9);

const char* phone_number = "+254726240861";

unsigned long previousMillis = 0;
unsigned long lastDataReceivedTime = 0;

// Structure to hold sensor data
struct SensorData {
  float temperature;
  float humidity;
  float pressure;
};

SensorData lastReceivedData = {9999.0, 9999.0, 9999.0};
bool newDataReceived = false;

// Function prototypes
void initCC1101();
void initA9G();
void initGPS();
bool testA9G();
String getGPSLocation();
bool sendSMS(const String& message);
String sendATCommand(const String& command, int timeout);
void blinkLED(int times, int duration);
void resetA9G();
bool parseSensorData(const String& dataString, SensorData& data);
String formatSensorData(const SensorData& data);
float parseFloat(const String& str);

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LED_OFF);
  
  SPI.begin();
  initCC1101();
  
  A9GSerial.begin(9600);
  delay(10000);  // Give A9G module time to start up
  
  initA9G();

  // Indicate setup completion
  blinkLED(3, 200);  // 3 quick blinks
}

void loop() {
  uint8_t buf[RH_CC110_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
  
  if (cc110.available()) {
    if (cc110.recv(buf, &len)) {
      String receivedString = String((char*)buf);
      if (parseSensorData(receivedString, lastReceivedData)) {
        newDataReceived = true;
        lastDataReceivedTime = millis();
        blinkLED(2, 100);  // 2 quick blinks indicate successful data reception and parsing
      } else {
        blinkLED(1, 500);  // 1 long blink indicates data parsing failure
      }
    } else {
      blinkLED(3, 50);  // 3 very quick blinks indicate reception failure
    }
  }
  
  unsigned long currentMillis = millis();
  
  // Check if it's time to send an SMS
  if (currentMillis - previousMillis >= SMS_INTERVAL) {
    previousMillis = currentMillis;
    
    // Check if data is stale (no new data for more than 5 minutes)
    if (currentMillis - lastDataReceivedTime > 300000) {
      lastReceivedData = {9999.0, 9999.0, 9999.0};
    }
    
    if (testA9G()) {
      initGPS();
      String location = getGPSLocation();
      String sensorDataString = formatSensorData(lastReceivedData);
      String message = sensorDataString + "," + location;
      
      if (sendSMS(message)) {
        blinkLED(2, 500);  // 2 long blinks indicate successful SMS
        newDataReceived = false;
      } else {
        blinkLED(5, 50);  // 5 quick blinks indicate SMS sending failure
      }
    } else {
      resetA9G();
      blinkLED(10, 50);  // 10 quick blinks indicate A9G reset attempt
    }
  }
}

void initCC1101() {
  if (!cc110.init()) {
    blinkLED(5, 100);  // 5 medium blinks indicate CC1101 init failure
    while (1);  // Halt if CC1101 init fails
  }
  cc110.setFrequency(433.0);
  cc110.setModeRx();
}

void initA9G() {
  sendATCommand("ATE0", 1000);
  sendATCommand("AT+CGPSPWR=1", 2000);
  delay(2000);
  sendATCommand("AT+CGPSRST=1", 2000);
  delay(2000);
  sendATCommand("AT+CGPSIPR=9600", 2000);
  delay(2000);
  sendATCommand("AT+CGPSOUT=0", 2000);
}

void initGPS() {
  sendATCommand("AT+CGPS=1,1", 5000);
  delay(5000);
}

bool testA9G() {
  String response = sendATCommand("AT", 2000);
  return response.indexOf("OK") != -1;
}

String getGPSLocation() {
  String response = sendATCommand("AT+CGPSINFO", 10000);
  if (response.indexOf("+CGPSINFO:") != -1) {
    int start = response.indexOf("+CGPSINFO:");
    int end = response.indexOf("\r", start);
    String gpsData = response.substring(start + 10, end);
    gpsData.trim();
    if (gpsData != ",,,,,,,," && gpsData.length() > 0) {
      return "L:" + gpsData;
    }
  }
  return "L:9999.0";
}

bool sendSMS(const String& message) {
  if (sendATCommand("AT+CMGF=1", 2000).indexOf("OK") == -1) {
    return false;
  }
  
  String setNumberCmd = "AT+CMGS=\"" + String(phone_number) + "\"";
  if (sendATCommand(setNumberCmd, 5000).indexOf(">") == -1) {
    return false;
  }
  
  A9GSerial.print(message);
  A9GSerial.write(26);  // Ctrl+Z to end message
  
  String response = sendATCommand("", 10000);
  return response.indexOf("+CMGS:") != -1;
}

String sendATCommand(const String& command, int timeout) {
  A9GSerial.println(command);
  
  unsigned long startTime = millis();
  String response = "";
  
  while (millis() - startTime < static_cast<unsigned long>(timeout)) {
    if (A9GSerial.available()) {
      char c = A9GSerial.read();
      response += c;
      if (response.indexOf("OK") != -1 || response.indexOf("ERROR") != -1 || response.indexOf(">") != -1) {
        break;
      }
    }
  }
  
  return response;
}

void blinkLED(int times, int duration) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, LED_ON);
    delay(duration);
    digitalWrite(LED_PIN, LED_OFF);
    delay(duration);
  }
}

void resetA9G() {
  sendATCommand("AT+CRESET", 5000);
  delay(10000);
  initA9G();
}

// Helper function to parse float values, returning 9999.0 for invalid inputs
float parseFloat(const String& str) {
  if (str.length() == 0) return 9999.0;
  
  for (unsigned int i = 0; i < str.length(); i++) {
    if (isdigit(str[i]) || str[i] == '.' || str[i] == '-') {
      return str.toFloat();
    }
  }
  
  return 9999.0;
}

bool parseSensorData(const String& dataString, SensorData& data) {
  // Initialize data to error values
  data = {9999.0, 9999.0, 9999.0};

  int t_index = dataString.indexOf("T:");
  int h_index = dataString.indexOf("H:");
  int p_index = dataString.indexOf("P:");
  
  if (t_index == -1 || h_index == -1 || p_index == -1) {
    return false;
  }
  
  String temp = dataString.substring(t_index + 2, h_index);
  String hum = dataString.substring(h_index + 2, p_index);
  String pres = dataString.substring(p_index + 2);
  
  // Remove any non-numeric characters except for the decimal point and minus sign
  temp.replace(String('\r'), "");
  hum.replace(String('\r'), "");
  pres.replace(String('\r'), "");
  
  // Parse the values using the helper function
  data.temperature = parseFloat(temp);
  data.humidity = parseFloat(hum);
  data.pressure = parseFloat(pres);
  
  // Check if any valid data was parsed (not all values are 9999.0)
  return (data.temperature != 9999.0 || data.humidity != 9999.0 || data.pressure != 9999.0);
}

String formatSensorData(const SensorData& data) {
  char buffer[50];
  snprintf(buffer, sizeof(buffer), "T:%.2f,H:%.2f,P:%.2f", 
           data.temperature, data.humidity, data.pressure);
  return String(buffer);
}

/* LED Blink Status Guide:
 * 3 quick blinks (setup): Setup completed successfully
 * 2 quick blinks (loop): Successful data reception and parsing from CC1101
 * 1 long blink (loop): Data parsing failure
 * 3 very quick blinks (loop): CC1101 reception failure
 * 2 long blinks (loop): Successful SMS sent
 * 5 quick blinks (loop): SMS sending failure
 * 10 quick blinks (loop): A9G reset attempt
 * 5 medium blinks (initCC1101): CC1101 initialization failure
 */