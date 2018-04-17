#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  150 
#define SERVOMAX  700

// our servo # counter


void setup() {
  Serial.begin(115200); // use the same baud-rate as the python side

  pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  delay(10);
}

void setServoPulse(uint8_t n, double pos) {
  uint8_t servonum = n;
  uint16_t pulselength = SERVOMIN + pos/180*(SERVOMAX-SERVOMIN);
  pwm.setPWM(servonum, 0, pulselength);
  

  
}

void loop() {
  String str = "";
  String channel = "";
  String position = "";
  int success = 0;
  while (1){
  	if (Serial.available() > 0) 
  	{
  	  str = Serial.readStringUntil('\n');
  	  channel = Serial.readStringUntil('\,');
  	  position = Serial.readStringUntil('\n');
  	  
  	  Serial.print(channel+','+position);
  	  setServoPulse(channel.toInt(),position.toInt());
  
  	}
 }
}