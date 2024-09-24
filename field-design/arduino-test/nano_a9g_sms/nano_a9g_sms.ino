#include <SoftwareSerial.h>

const int RX_PIN = 2;  // Connect this to TX of A9G
const int TX_PIN = 3;  // Connect this to RX of A9G
SoftwareSerial A9G(RX_PIN, TX_PIN);

const char* phone_number = "+254726240861";

unsigned long previousMillis = 0;
const unsigned long interval = 180000; // 3 minutes in milliseconds

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect
  }
  Serial.println("Serial communication started");
  
  A9G.begin(9600);
  Serial.println("A9G communication started at 9600 baud");
  
  delay(10000);  // Give A9G module more time to start up
  
  initA9G();
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    Serial.println("Starting data transmission...");
    if (testA9G()) {
      initGPS();
      String location = getGPSLocation();
      float temp = random(200, 350) / 10.0;  // Random temp between 20.0 and 35.0
      float humidity = random(300, 800) / 10.0;  // Random humidity between 30.0 and 80.0
      Serial.println("Got location: " + location);
      sendSMS(temp, humidity, location);
      Serial.println("SMS sent. Waiting for next interval...");
    } else {
      Serial.println("Failed to communicate with A9G. Will retry at next interval.");
    }
  }
}

void initA9G() {
  Serial.println("Initializing A9G...");
  sendATCommand("ATE0", 1000); // Disable echo
  sendATCommand("AT+CGPSPWR=1", 2000); // Power on GPS
  delay(2000);
  sendATCommand("AT+CGPSRST=1", 2000); // Reset GPS in hot mode
  delay(2000);
  sendATCommand("AT+CGPSIPR=9600", 2000); // Set GPS baud rate
  delay(2000);
  sendATCommand("AT+CGPSOUT=0", 2000); // Disable GPS NMEA output
  Serial.println("A9G initialization complete");
}

void initGPS() {
  Serial.println("Initializing GPS...");
  sendATCommand("AT+CGPS=1,1", 5000); // Turn on GPS with full power
  delay(15000); // Wait longer for GPS to initialize
}

boolean testA9G() {
  Serial.println("Testing A9G communication...");
  return sendATCommand("AT", 2000);
}

String getGPSLocation() {
  Serial.println("Getting GPS location...");
  if (sendATCommand("AT+CGPSINFO", 10000)) {
    String response = A9G.readString();
    Serial.println("GPS Response: " + response);
    if (response.indexOf("+CGPSINFO:") != -1) {
      // Parse the GPS data here
      int start = response.indexOf("+CGPSINFO:");
      int end = response.indexOf("\r", start);
      String gpsData = response.substring(start + 10, end);
      gpsData.trim();
      if (gpsData != ",,,,,,,," && gpsData.length() > 0) {
        return "L:" + gpsData;
      } else {
        return "L:No Fix";
      }
    } else if (response.indexOf("+CME ERROR:") != -1) {
      Serial.println("GPS Error: " + response);
      return "L:GPS Error";
    } else {
      return "L:No Data";
    }
  }
  return "L:Timeout";
}

void sendSMS(float temp, float humidity, String location) {
  String message = "T:" + String(temp, 1) + "C,H:" + String(humidity, 1) + "%," + location;
  
  Serial.println("Sending SMS...");
  Serial.println("Message content: " + message);
  
  if (sendATCommand("AT+CMGF=1", 2000) && // Set SMS text mode
      sendATCommand("AT+CMGS=\"" + String(phone_number) + "\"", 5000)) {
    A9G.print(message);
    A9G.write(26); // Ctrl+Z to end SMS
    delay(60000); // Wait for SMS to be sent
    Serial.println("SMS sent successfully");
  } else {
    Serial.println("Failed to send SMS");
  }
}

boolean sendATCommand(String command, int timeout) {
  Serial.println("Sending command: " + command);
  A9G.println(command);
  
  long int time = millis();
  String response = "";
  
  while((time+timeout) > millis()) {
    while(A9G.available()) {
      char c = A9G.read();
      response += c;
      Serial.write(c); // Print each character as it's received
    }
    if (response.indexOf("OK") != -1 || response.indexOf(">") != -1) {
      Serial.println("\nCommand successful");
      return true;
    }
    if (response.indexOf("ERROR") != -1) {
      Serial.println("\nCommand failed");
      return false;
    }
  }
  
  Serial.println("\nCommand timed out");
  return false;
}
