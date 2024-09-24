#include <Arduino.h>
#include <HardwareSerial.h>

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

HardwareSerial A9GSerial(PA10, PA9);

const char* phone_number = "+254726240861";

unsigned long previousMillis = 0;
const unsigned long interval = 180000; // 3 minutes in milliseconds

void initA9G();
void initGPS();
bool testA9G();
String getGPSLocation();
bool sendSMS(float temp, float humidity, String location);
String sendATCommand(const String& command, int timeout);
void blinkLED(int times, int duration);
void resetA9G();

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LED_OFF);
  
  A9GSerial.begin(9600);  // Changed to 9600 baud rate
  
  delay(10000);  // Give A9G module time to start up
  
  initA9G();
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    if (testA9G()) {
      initGPS();
      String location = getGPSLocation();
      float temp = random(200, 350) / 10.0f;
      float humidity = random(300, 800) / 10.0f;
      if (sendSMS(temp, humidity, location)) {
        blinkLED(2, 500);  // Slow blink twice to indicate success
      } else {
        blinkLED(5, 50);  // Fast blink 5 times to indicate trouble
      }
    } else {
      resetA9G();
      blinkLED(10, 50);  // Indicate reset attempt with 10 very fast blinks
    }
  }
}

void initA9G() {
  sendATCommand("ATE0", 1000); // Disable command echo
  sendATCommand("AT+CGPSPWR=1", 2000); // Power on the GPS
  delay(2000);
  sendATCommand("AT+CGPSRST=1", 2000); // Reset GPS in hot mode
  delay(2000);
  sendATCommand("AT+CGPSIPR=9600", 2000); // Set GPS baud rate
  delay(2000);
  sendATCommand("AT+CGPSOUT=0", 2000); // Disable GPS NMEA output
}

void initGPS() {
  sendATCommand("AT+CGPS=1,1", 5000); // Turn on GPS with full power
  delay(5000); // Reduced wait time for GPS to initialize
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
  return "L:No Fix0";
}

bool sendSMS(float temp, float humidity, String location) {
  String message = "T:" + String(temp, 1) + "C,H:" + String(humidity, 1) + "%," + location;
  
  // Set SMS text mode
  if (sendATCommand("AT+CMGF=1", 2000).indexOf("OK") == -1) {
    return false;
  }
  
  // Set recipient number
  String setNumberCmd = "AT+CMGS=\"" + String(phone_number) + "\"";
  if (sendATCommand(setNumberCmd, 5000).indexOf(">") == -1) {
    return false;
  }
  
  // Send the message
  A9GSerial.print(message);
  A9GSerial.write(26);  // Ctrl+Z to end message
  
  // Wait for response
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
  sendATCommand("AT+CRESET", 5000); // Send reset command
  delay(10000); // Wait for A9G to restart
  initA9G(); // Re-initialize A9G after reset
}