//The program to print data in array
//Sensor pins
int sensorPin1 = A0;
int sensorPin2 = A1;
int sensorPin3 = A2;
int sensorPin4 = A3;

//number of sensors to be printed in array
int sensorReadings[4];

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read sensor values
  sensorReadings[0] = analogRead(sensorPin1);
  sensorReadings[1] = analogRead(sensorPin2);
  sensorReadings[2] = analogRead(sensorPin3);
  sensorReadings[3] = analogRead(sensorPin4);

  // Print sensor values
  Serial.print("Sensor Readings: [");
  for (int i = 0; i < 4; i++) {
    Serial.print(sensorReadings[i]);
    if (i < 3) {
      Serial.print(", ");
    }
  }
  Serial.println("]");

  delay(1000); // wait for 1 second
}
