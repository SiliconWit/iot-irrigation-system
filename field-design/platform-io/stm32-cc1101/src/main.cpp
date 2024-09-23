#include <Arduino.h>
#define TINY_GSM_MODEM_SIM800
#include <TinyGsmClient.h>

// The phone number you want to send SMS to
const char phoneNumber[] = "+254726240861";

// Define LED pin
#define LED_PIN PC13

// Use the pre-defined Serial1 for USART1 (PA9/PA10)
TinyGsm modem(Serial1);

void setup() {
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH); // Turn off LED (it's active low)

  // Set GSM module baud rate
  Serial1.begin(9600);
  delay(3000);

  // Initialize modem
  while (!modem.isNetworkConnected()) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN)); // Toggle LED
    modem.restart();
    delay(2000);
    modem.waitForNetwork();
  }

  // Network connected, turn on LED
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // Send SMS
  if (modem.sendSMS(phoneNumber, "Test SMS from BluePill")) {
    digitalWrite(LED_PIN, HIGH); // Turn off LED to indicate success
  } else {
    digitalWrite(LED_PIN, LOW); // Turn on LED to indicate failure
  }

  delay(3000); // Wait for 3 seconds before sending the next SMS
}