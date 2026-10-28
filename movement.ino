#include <Servo.h>




const int joy = A0;
const int trigPin = 3;
const int echoPin = 2;


Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;




void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  motor1.attach(6);
  motor2.attach(9);
  motor3.attach(10);
  motor4.attach(11);
  Serial.begin(115200);




  pinMode(joy, INPUT);




  motor1.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  Serial.begin(9600);
  delay(3000);
}




void loop() {
  long duration, cm;

  if (Serial.available() > 0){
    String control_output = Serial.readStringUntil('\n');

  }


  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);


  duration = pulseIn(echoPin, HIGH);


  // convert the time into a distance
  cm = microsecondsToCentimetres(duration);
 
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();  
  delay(100);



  int speed = map(analogRead(joy), 0, 1023, 0, 2000);
  int speeds=(speed-10*cm);
  Serial.println(speeds);
  if(cm>150){
    while(cm>150){
      speeds--;
      motor1.writeMicroseconds(speeds);
      motor2.writeMicroseconds(speeds);
      motor3.writeMicroseconds(speeds);
      motor4.writeMicroseconds(speeds);

      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

      duration = pulseIn(echoPin, HIGH);
      cm = microsecondsToCentimetres(duration);
    }

  }
  else{

    if (control_ouput > 0){
      motor1.writeMicroseconds(speeds);
      motor2.writeMicroseconds(speeds);
      motor3.writeMicroseconds(speeds-(0.1*control_output));
      motor4.writeMicroseconds(speeds-(0.1*control_output));
    }
      
    
    elif (control output < 0){
      motor1.writeMicroseconds(speeds-(0.1*control_output));
      motor2.writeMicroseconds(speeds-(0.1*control_output));
      motor3.writeMicroseconds(speeds);
      motor4.writeMicroseconds(speeds);

    }

    else{
      motor1.writeMicroseconds(speeds);
      motor2.writeMicroseconds(speeds);
      motor3.writeMicroseconds(speeds);
      motor4.writeMicroseconds(speeds);
    }

  }



  
  
}


long microsecondsToCentimetres(long microseconds)
{
  return microseconds / 29 / 2;
}
