#include <Arduino.h>
#include <RH_CC110.h>
#include <SPI.h>
#include <HardwareSerial.h>

// Pin Definitions for CC1101 connection to STM32 BluePill
#define CC1101_CS_PIN PA4   // Chip Select (CSN) pin
#define CC1101_GDO0_PIN PB0 // General Digital Output 0 pin

/* Complete CC1101 to STM32 BluePill Connection Guide:
 * CC1101 Pin | BluePill Pin | Function
 * -----------|--------------|----------
 * 1 (GND)    | GND          | Ground
 * 2 (VCC)    | 3.3V         | Power (3.3V only!)
 * 3 (GDO0)   | PB0          | General Digital Output 0 (Configurable)
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

#define SMS_INTERVAL 1800000 // 30 minutes in milliseconds
#define MQTT_INTERVAL 60000 //1800000 // 30 minutes in milliseconds
#define RESET_INTERVAL 2400000 // 40 minutes in milliseconds

// Initialize CC1101 radio module
RH_CC110 cc110(CC1101_CS_PIN, CC1101_GDO0_PIN);

// Initialize UART for A9G module
HardwareSerial A9GSerial(PA10, PA9);

const char* phone_number = "+254726240861";

// MQTT Configuration
const char* APN = "safaricom";
const char* MQTT_BROKER = "test.mosquitto.org";
const int MQTT_PORT = 1883;
const char* MQTT_CLIENT_ID = "STM32Client";
const char* MQTT_TOPIC = "/test/stm32/sensors";

unsigned long previousSMSMillis = 0;
unsigned long previousMQTTMillis = 0;
unsigned long previousResetMillis = 0;
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
void resetBluePill();
bool setupGPRS();
bool publishMQTT(const String& message);

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LED_OFF);
  
  SPI.begin();
  initCC1101();
  
  A9GSerial.begin(9600);
  delay(10000);  // Give A9G module time to start up
  
  initA9G();
  setupGPRS();

  // Indicate setup completion
  blinkLED(3, 200);  // 3 quick blinks
}

void loop() {
  uint8_t buf[RH_CC110_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
  
  if (cc110.waitAvailableTimeout(10000)) { // Wait for up to 10 seconds for a message
    if (cc110.recv(buf, &len)) {
      String receivedString = String((char*)buf);
      
      // Parse and process the data
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
  } else {
    // No data received, ensure lastReceivedData contains default values
    lastReceivedData = {9999.0, 9999.0, 9999.0};
  }
  
  unsigned long currentMillis = millis();
  
  // Check if it's time to send MQTT data
  if (currentMillis - previousMQTTMillis >= MQTT_INTERVAL) {
    previousMQTTMillis = currentMillis;
    
    if (testA9G()) {
      String location = getGPSLocation();
      String sensorDataString = formatSensorData(lastReceivedData);
      String message = sensorDataString + "," + location;
      if (publishMQTT(message)) {
        blinkLED(4, 100);  // 4 quick blinks indicate successful MQTT publish
      } else {
        blinkLED(4, 250);  // 4 medium blinks indicate MQTT publish failure
      }
    } else {
      resetA9G();
      blinkLED(10, 50);  // 10 quick blinks indicate A9G reset attempt
    }
  }
  
  // Check if it's time to send an SMS
  if (currentMillis - previousSMSMillis >= SMS_INTERVAL) {
    previousSMSMillis = currentMillis;
    
    if (testA9G()) {
      initGPS();
      String location = getGPSLocation();
      String sensorDataString = formatSensorData(lastReceivedData);
      String message = sensorDataString + "," + location;
      
      if (sendSMS(message)) {
        blinkLED(2, 500);  // 2 long blinks indicate successful SMS
        // Reset data to default after successful sending
        lastReceivedData = {9999.0, 9999.0, 9999.0};
        newDataReceived = false;
      } else {
        blinkLED(5, 50);  // 5 quick blinks indicate SMS sending failure
      }
    } else {
      resetA9G();
      blinkLED(10, 50);  // 10 quick blinks indicate A9G reset attempt
    }
  }
  
  // Check if it's time to reset the Blue Pill
  if (currentMillis - previousResetMillis >= RESET_INTERVAL) {
    resetBluePill();
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
  setupGPRS();
}

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
  int temp_int, temp_frac, hum_int, hum_frac, pres_int, pres_frac;
  
  if (sscanf(dataString.c_str(), "T:%d.%d,H:%d.%d,P:%d.%d", 
             &temp_int, &temp_frac, &hum_int, &hum_frac, &pres_int, &pres_frac) == 6) {
    
    data.temperature = temp_int + temp_frac / 100.0;
    data.humidity = hum_int + hum_frac / 100.0;
    data.pressure = pres_int + pres_frac / 100.0;
    
    return true;
  } else {
    // If parsing fails, set to default values
    data = {9999.0, 9999.0, 9999.0};
    return false;
  }
}

String formatSensorData(const SensorData& data) {
  // Convert each float to a string with 2 decimal places
  String tempStr = String(data.temperature, 2);
  String humStr = String(data.humidity, 2);
  String presStr = String(data.pressure, 2);

  // Replace any empty strings with "9999.00"
  if (tempStr.length() == 0 || tempStr == "nan") tempStr = "9999.00";
  if (humStr.length() == 0 || humStr == "nan") humStr = "9999.00";
  if (presStr.length() == 0 || presStr == "nan") presStr = "9999.00";

  // Construct the final string
  String result = "T:" + tempStr + ",H:" + humStr + ",P:" + presStr;

  return result;
}

void resetBluePill() {
  // Use the NVIC_SystemReset() function to reset the Blue Pill
  NVIC_SystemReset();
}

bool setupGPRS() {
  bool success = true;

  // Set up PDP context with APN
  success &= sendATCommand("AT+CGDCONT=1,\"IP\",\"" + String(APN) + "\",\"0.0.0.0\",0,0", 5000).indexOf("OK") != -1;

  // Activate PDP context
  success &= sendATCommand("AT+CGACT=1,1", 10000).indexOf("OK") != -1;

  return success;
}

bool publishMQTT(const String& message) {
  bool success = true;

  // Connect to MQTT broker
  String mqttConn = sendATCommand("AT+MQTTCONN=\"" + String(MQTT_BROKER) + "\"," + String(MQTT_PORT) + ",\"" + String(MQTT_CLIENT_ID) + "\",120,0", 15000);
  success &= mqttConn.indexOf("OK") != -1;

  if (success) {
    // Publish the message to the MQTT topic
    success &= sendATCommand("AT+MQTTPUB=\"" + String(MQTT_TOPIC) + "\",\"" + message + "\",0,0,0", 10000).indexOf("OK") != -1;
    
    // Disconnect from MQTT broker
    sendATCommand("AT+MQTTDISCONN", 5000);
  }

  return success;
}

/* LED Blink Status Guide:
 * 3 quick blinks (setup): Setup completed successfully
 * 2 quick blinks (loop): Successful data reception and parsing from CC1101
 * 1 long blink (loop): Data parsing failure
 * 3 very quick blinks (loop): CC1101 reception failure
 * 4 medium blinks (loop): MQTT publish failure
 * 2 long blinks (loop): Successful SMS sent
 * 5 quick blinks (loop): SMS sending failure
 * 10 quick blinks (loop): A9G reset attempt
 * 5 medium blinks (initCC1101): CC1101 initialization failure
 */