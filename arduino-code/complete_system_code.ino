#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Pin assignments
const int moistureSensorPins[] = {A0, A1, A2, A3};  // Pins for moisture sensors in blocks 1 to 3
const int dhtPins[] = {11, 12, 13};  // Pins for DHT11 humidity sensors in blocks 1 to 3
const int ds18b20Pins[] = {7, 8, 9, 10};  // Pins for DS18B20 temperature sensors in blocks 1 to 3
const int solenoidPins[] = {3, 4, 5, 6};  // Pins for solenoid valves
int X[4];
int Y[4];
float TIME[4] = {0};
float FREQUENCY[4] = {0};
float WATER[4];
float TOTAL[4] = {0};
float LS[4] = {0};
const int inputPins[] = {15, 16, 17, 18};
const int pumpPin = 2;  // Pin for irrigation pump
const int surroundingDHTPin = 21; // Pin for the DHT11 sensor measuring surrounding temperature and humidity
const int water1Read = A5;
const int water2Read = A6;
float moistureLevel[4];
float humidityLevel[3];
float temperatureLevel[4];


// Thresholds for blocks 1 to 3
const int moistureMinThresholds[] = {40, 81, 40};  // Min Moisture thresholds for blocks 1 to 3
const int humidityMinThresholds[] = {65, 55, 70};  // Min Humidity thresholds for blocks 1 to 3
const int temperatureMinThresholds[] ={21, 15, 13};  // Min Temperature thresholds for blocks 1 to 3
const int moistureMaxThresholds[] = {60, 95, 75};  // Max Moisture thresholds for blocks 1 to 3
const int humidityMaxThresholds[] = {95, 90, 70};  // Max Humidity thresholds for blocks 1 to 3
const int temperatureMaxThresholds[] = {26, 30, 25};  // Max Temperature thresholds for blocks 1 to 3

// Thresholds for block 4
const int moistureMinThreshold = 60;  // Minimum moisture threshold for block 4
const int moistureMaxThreshold = 80;  // Maximum moisture threshold for block 4
const int temperatureMinThreshold = 20;  // Minimum temperature threshold for block 4
const int temperatureMaxThreshold = 37;  // Maximum temperature threshold for block 4
const int waterLevelMinThreshold = 2;  // Minimum water level threshold for block 4
const int waterLevelMaxThreshold = 4;  // Maximum water level threshold for block 4

int trigPin = 19;
int echoPin = 20;
long duration;
float radius = 15;
int distance;
int higher = 0;
int lower = 13;
int waterLevel;
float currentWaterLevel;


int surroundingTemperature;
int surroundingHumidity;

// Initialize DHT sensors
DHT dhtBlocks[] = {DHT(dhtPins[0], DHT11), DHT(dhtPins[1], DHT11), DHT(dhtPins[2], DHT11), DHT(dhtPins[3], DHT11)};
DHT dhtSurrounding (surroundingDHTPin, DHT11);

// Initialize DS18B20 sensors
OneWire oneWire[] = {OneWire(ds18b20Pins[0]), OneWire(ds18b20Pins[1]), OneWire(ds18b20Pins[2]), OneWire(ds18b20Pins[3])};
DallasTemperature ds18b20[] = {DallasTemperature(&oneWire[0]), DallasTemperature(&oneWire[1]), DallasTemperature(&oneWire[2]), DallasTemperature(&oneWire[3])};

// Number of sensors in each block
const int numSensors = 3;

// Sensor readings array
//float sensorReadings[5][4];
float sensorReadings[19];

// Water level in tank
int waterLevelTank;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set solenoid and pump pins as outputs
  for (int i = 0; i < 4; i++) {
    pinMode(solenoidPins[i], OUTPUT);
    pinMode(inputPins[i], INPUT);
  }
  pinMode(pumpPin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Start DHT sensors for blocks 1 to 3
  for (int i = 0; i < 3; i++) {
    dhtBlocks[i].begin();
  }

  // Start DHT sensor for surrounding temperature and humidity
  dhtSurrounding.begin();

  // Start DS18B20 sensors
  for (int i = 0; i < 3; i++) {
    ds18b20[i].begin();
  }
  digitalWrite(pumpPin, HIGH);
  for (int i = 0; i < 4; i++) {
    digitalWrite(solenoidPins[i], HIGH);
  }
  
  // Check sensor readings in blocks 1 to 3 during setup
  for (int i = 0; i < 3; i++) {
    int moistureLevel = map(analogRead(moistureSensorPins[i]), 1023, 300, 0, 100);
    float humidityLevel = dhtBlocks[i].readHumidity();
    ds18b20[i].requestTemperatures();
    float temperatureLevel = ds18b20[i].getTempCByIndex(0);
    
    // Store the sensor readings in the array
    sensorReadings[2] = map(analogRead(moistureSensorPins[0]), 1023, 300, 0, 100);
    sensorReadings[6] = map(analogRead(moistureSensorPins[1]), 1023, 300, 0, 100);
    sensorReadings[10] = map(analogRead(moistureSensorPins[2]), 1023, 300, 0, 100);
    sensorReadings[3] = dhtBlocks[0].readHumidity();
    sensorReadings[7] = dhtBlocks[1].readHumidity();
    sensorReadings[11] = dhtBlocks[2].readHumidity();
    ds18b20[0].requestTemperatures();
    sensorReadings[1] = ds18b20[0].getTempCByIndex(0);
    ds18b20[1].requestTemperatures();
    sensorReadings[5] = ds18b20[1].getTempCByIndex(0);
    ds18b20[2].requestTemperatures();
    sensorReadings[9] = ds18b20[2].getTempCByIndex(0);
    

    // Check if any sensor reading is below the thresholds
    if(waterLevelTank > 20){
      if (moistureLevel < moistureMinThresholds[i] || humidityLevel < humidityMinThresholds[i] || temperatureLevel > temperatureMaxThresholds[i]){
        for (int i = 0; i < 3; i++) {
          openValveAndStartPump(i);// Open solenoid valve and start pump for the block
          X[i] = pulseIn(inputPins[i], HIGH);
          Y[i] = pulseIn(inputPins[i], LOW);
          TIME[i] = X[i] + Y[i];
          FREQUENCY[i] = 1000000 / TIME[i];
          WATER[i] = FREQUENCY[i] / 7.5;
          LS[i] = WATER[i] / 60;

          if (FREQUENCY[i] >= 0) {
             if(isinf(FREQUENCY[i])){
               calculateTotal(i);
               sensorReadings[4] = TOTAL[0];
               sensorReadings[8] = TOTAL[1];
               sensorReadings[12] = TOTAL[2];
              } else {
              TOTAL[i] += LS[i];
              calculateTotal(i);
              sensorReadings[4] = TOTAL[0];
              sensorReadings[8] = TOTAL[1];
              sensorReadings[12] = TOTAL[2];
            }
          }
        }
      
      } 
      else {
      closeValveAndStopPump(i);  // Close solenoid valve and stop pump for the block
      }
    } 
    else {
      closeValveAndStopPump(i);
    }
    
  }
  //delay(200);

  // Check sensor readings in block 4 during setup
  int moistureLevelRice = map(analogRead(moistureSensorPins[3]), 1023, 300, 0, 100);
  float surroundingHumidity = dhtBlocks[3].readHumidity();
  float surroundingTemperature = dhtBlocks[3].readTemperature();
  ds18b20[3].requestTemperatures();
  float temperatureLevelRice = ds18b20[3].getTempCByIndex(0);
  // TODO: Read water level sensor for block 4
  int water1 = analogRead(water1Read);
  int water2 = analogRead(water2Read);
  int waterLevel = (water1 + water2)/20;

  // Store the sensor readings in the array
 
  sensorReadings[14] = moistureLevelRice;
  sensorReadings[13] = temperatureLevelRice;
  sensorReadings[15] = waterLevel;
  sensorReadings[17] = surroundingTemperature;
  sensorReadings[18] = surroundingHumidity;

  

  // Check if any sensor reading is below the thresholds
  if(waterLevelTank >20){
    if(moistureLevelRice < moistureMinThreshold || temperatureLevelRice > temperatureMaxThreshold || waterLevel < waterLevelMinThreshold){
      openValveAndStartPump(3);  // Open solenoid valve and start pump for block 4
      
      X[3] = pulseIn(inputPins[3], HIGH);
      Y[3] = pulseIn(inputPins[3], LOW);
      TIME[3] = X[3] + Y[3];
      FREQUENCY[3] = 1000000 / TIME[3];
      WATER[3] = FREQUENCY[3] / 7.5;
      LS[3] = WATER[3] / 60;

      if (FREQUENCY[3] >= 0) {
        if (isinf(FREQUENCY[3])) {
          calculateTotal(3);
          sensorReadings[16] = TOTAL[3];
        } else {
          TOTAL[3] = LS[3];
          calculateTotal(3);
          sensorReadings[16] = TOTAL[3];
        }
      }
      
    } else {
    closeValveAndStopPump(3);  // Close solenoid valve and stop pump for block 4
    }
  }
  else {
      closeValveAndStopPump(3);
    }
  

  // Initialize water level in tank
  digitalWrite(trigPin, LOW);  
  delayMicroseconds(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration*0.034/2;
  currentWaterLevel = map(distance,lower,higher,13,0);
  waterLevelTank = (3.14*radius*radius*currentWaterLevel)/1000;
  waterLevelTank = map(waterLevelTank,20,0,0,100);
  sensorReadings[0] = waterLevelTank;
  

  // Update water level in tank
  waterLevelTank = currentWaterLevel;
  for (int i =0; i<19; i++) {
  Serial.print(sensorReadings[i]);
  if (i<18) {
    Serial.print(", ");
  }
}
Serial.println("");
  
  

}

void loop() {
  //Read surrounding temperature and humidity
  float surroundingTemperature = dhtSurrounding.readTemperature();
  float surroundingHumidity = dhtSurrounding.readHumidity();

  sensorReadings[17] = surroundingTemperature;
  sensorReadings[18] = surroundingHumidity;

  digitalWrite(trigPin, LOW);  
  delayMicroseconds(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration*0.034/2;
  currentWaterLevel = map(distance,lower,higher,13,0);
  waterLevelTank = (3.14*radius*radius*currentWaterLevel)/1000;
  waterLevelTank = map(waterLevelTank,20,0,0,100);
  sensorReadings[0] = waterLevelTank;

  // Check sensor readings in blocks 1 to 3
  for (int i = 0; i < 3; i++) {
    int moistureLevel = map(analogRead(moistureSensorPins[i]), 1023, 300, 0, 100);
    float humidityLevel = dhtBlocks[i].readHumidity();
    ds18b20[i].requestTemperatures();
    float temperatureLevel = ds18b20[i].getTempCByIndex(0);

   
    sensorReadings[2] = map(analogRead(moistureSensorPins[0]), 1023, 300, 0, 100);
    sensorReadings[6] = map(analogRead(moistureSensorPins[1]), 1023, 300, 0, 100);
    sensorReadings[10] = map(analogRead(moistureSensorPins[2]), 1023, 300, 0, 100);
    sensorReadings[3] = dhtBlocks[0].readHumidity();
    sensorReadings[7] = dhtBlocks[1].readHumidity();
    sensorReadings[11] = dhtBlocks[2].readHumidity();
    ds18b20[0].requestTemperatures();
    sensorReadings[1] = ds18b20[0].getTempCByIndex(0);
    ds18b20[1].requestTemperatures();
    sensorReadings[5] = ds18b20[1].getTempCByIndex(0);
    ds18b20[2].requestTemperatures();
    sensorReadings[9] = ds18b20[2].getTempCByIndex(0);


    // Check if any sensor reading is below the thresholds
    if(waterLevelTank > 20){
      if (moistureLevel < moistureMinThresholds[i] || humidityLevel < humidityMinThresholds[i] || temperatureLevel > temperatureMaxThresholds[i]){
      for (int i = 0; i < 3; i++) {
          openValveAndStartPump(i);// Open solenoid valve and start pump for the block
          X[i] = pulseIn(inputPins[i], HIGH);
          Y[i] = pulseIn(inputPins[i], LOW);
          TIME[i] = X[i] + Y[i];
          FREQUENCY[i] = 1000000 / TIME[i];
          WATER[i] = FREQUENCY[i] / 7.5;
          LS[i] = WATER[i] / 60;

          if (FREQUENCY[i] >= 0) {
            if (isinf(FREQUENCY[i])) {
              calculateTotal(i);
              sensorReadings[4] = TOTAL[0];
              sensorReadings[8] = TOTAL[1];
              sensorReadings[12] = TOTAL[2];
            } else {
              TOTAL[i] += LS[i];
              calculateTotal(i);
              sensorReadings[4] = TOTAL[0];
              sensorReadings[8] = TOTAL[1];
              sensorReadings[12] = TOTAL[2];
            }
          }
        }
      } else {
        closeValveAndStopPump(i);  // Close solenoid valve and stop pump for the block
       
      }
    }  
    else {
      closeValveAndStopPump(i);
    }  
  }
  //delay(200);

  // Check sensor readings in block 4
  int moistureLevel = map(analogRead(moistureSensorPins[3]), 1023, 300, 0, 100);
  float humidityLevel = dhtBlocks[3].readHumidity();
  ds18b20[2].requestTemperatures();
  float temperatureLevel = ds18b20[2].getTempCByIndex(0);
  // TODO: Read water level sensor for block 4
  int water1 = analogRead(water1Read);
  int water2 = analogRead(water2Read);
  int waterLevel = (water1 + water2)/20;

  sensorReadings[14] = moistureLevel;
  sensorReadings[13] = temperatureLevel;
  sensorReadings[15] = waterLevel;
  

  // Check if any sensor reading is below the thresholds
  if(waterLevelTank > 20){
    if(moistureLevel < moistureMinThreshold || temperatureLevel > temperatureMaxThreshold || waterLevel < waterLevelMinThreshold){
      openValveAndStartPump(3);  // Open solenoid valve and start pump for block 4
      
      X[3] = pulseIn(inputPins[3], HIGH);
      Y[3] = pulseIn(inputPins[3], LOW);
      TIME[3] = X[3] + Y[3];
      FREQUENCY[3] = 1000000 / TIME[3];
      WATER[3] = FREQUENCY[3] / 7.5;
      LS[3] = WATER[3] / 60;

      if (FREQUENCY[3] >= 0) {
        if (isinf(FREQUENCY[3])) {
          calculateTotal(3);
          sensorReadings[16] = TOTAL[3];
        } else {
          TOTAL[3] = LS[3];
          calculateTotal(3);
          sensorReadings[16] = TOTAL[3];
        }
      }
      
    } else {
      closeValveAndStopPump(3);  // Close solenoid valve and stop pump for block 4
    }
  }
  else {
      closeValveAndStopPump(3);
    }

  // Print all sensor readings

  for (int i =0; i<19; i++) {
  Serial.print(sensorReadings[i]);
  if (i<18) {
    Serial.print(", ");
  }
}
Serial.println("");


  delay(10000);  // Adjust the delay as needed
}

void openValveAndStartPump(int block) {
  digitalWrite(solenoidPins[block], LOW);  // Open solenoid valve for the block
  digitalWrite(pumpPin, LOW);  // Start pump
  
}

void closeValveAndStopPump(int block) {
  digitalWrite(pumpPin, HIGH);  // Stop pump
  digitalWrite(solenoidPins[block], HIGH);  // Close solenoid valve for the block  
  
}

void calculateTotal(int block)
{
  
  TOTAL[block];


}



