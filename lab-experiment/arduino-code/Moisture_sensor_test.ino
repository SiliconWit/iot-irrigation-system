//sensor and relay pins 
int readPin = A0;
int readPin1 = A1;
int readPin2 = A2;
int relay = 2;
int relay1 = 3;
int Mb;
int Mb1;
int Mb2;
void setup() {
  // put your setup code here, to run once:
pinMode(relay,OUTPUT);
pinMode(relay1, OUTPUT);
pinMode(readPin, INPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
Mb=analogRead(readPin); //read analog value from sensor 1
Mb1= analogRead(readPin1); //read analog value from sensor 2
Mb2 = analogRead(readPin2); //read analog value from sensor 3

//Change the readings into percentage
Mb=map(Mb,1023,340,0,100);
Mb1 =map(Mb1,1023,200,0,100);
Mb2 =map(Mb2,1023,170,0,100);
Serial.print("M1: "); 
Serial.print(Mb1);
Serial.print("  M2: "); 
Serial.print(Mb2);
Serial.print("  M3: "); 
Serial.println(Mb);

//Function to check limits and turn ON the pump
if(Mb<=30){
   digitalWrite(relay,HIGH);
   delay(2000);
   digitalWrite(relay1,HIGH);
   if(Mb>70){
    digitalWrite(relay1,LOW);
    delay(2000);
    digitalWrite(relay, LOW);
  }
}
else{
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}

delay(5000);
}
