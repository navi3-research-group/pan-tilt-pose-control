
#include <Servo.h> 

Servo panServo;
Servo tiltServo;

const int maxPan = 170;
const int minPan = 10;
const int maxTilt = 130;
const int minTilt = 50;

int pan = 90;
int tilt = 90;

int pos = 0;
int panRead = 90;
int tiltRead = 90;

void setup() {
  panServo.attach(8);  
  tiltServo.attach(9);
  panServo.write(pan);
  tiltServo.write(tilt);

  Serial.begin(9600);
  Serial.println("READY");


  Serial.setTimeout(150);
}

void loop() {

  
  if (Serial.find("p")) {
    panRead = Serial.parseInt(); 
    tiltRead = Serial.parseInt();


    if (panRead > maxPan){
      panRead = maxPan;
      }

    if (panRead < minPan){
      panRead = minPan;
      }

    if (tiltRead > maxTilt){
      tiltRead = maxTilt;
      }

    if (tiltRead < minTilt){
      tiltRead = minTilt;
      }      

    //Serial.print("Pan servo: " );
    //Serial.print(panRead);
    //Serial.print(", Tilt servo: ");
    //Serial.println(tiltRead);

    if (panRead > pan){
      for (pos = pan; pos <= panRead; pos += 1) {
        panServo.write(pos);              
        delay(10); 
        //Serial.println(pos);
          }
      
      }


    if (panRead < pan){
      for (pos = pan; pos >= panRead; pos -= 1) { 
        panServo.write(pos);              
        delay(10);
        //Serial.println(pos);
          }
      
      }


    if (tiltRead > tilt){
      for (pos = tilt; pos <= tiltRead; pos += 1) { 
        tiltServo.write(pos);              
        delay(10); 
        //Serial.println(pos);
          }
      
      }




    if (tiltRead < tilt){
      for (pos = tilt; pos >= tiltRead; pos -= 1) { 
        tiltServo.write(pos);              
        delay(10);
        //Serial.println(pos);
          }
      
      }

      
    pan = panRead;
    tilt = tiltRead;

    Serial.flush();  

    //Serial.print("Pan servo: " );
    //Serial.print(pan);
    //Serial.print(", Tilt servo: ");
    //Serial.println(tilt);

  }
}




