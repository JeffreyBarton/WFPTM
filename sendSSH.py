import serial,time
import numpy as np
arduino = serial.Serial('COM3',115200,timeout=.1)

MAX = 180
min = MAX - 180
max = MAX - 0


def setServo(channel,pos):
    if pos >= max:
        pos = max
    elif pos < min:
        pos = min
    command = "Sending\n".encode() + str(channel).encode() + ",".encode() + str(pos).encode() + "\n".encode()
    print(command)
    done = False
    while not done:
        arduino.write(command)
        data = arduino.readline()
        print(data)
        if data:
            a = data.decode("utf-8").split(',')
            if int(a[0]) ==  channel and int(a[1]) == pos:
                done = True
                print("Success")

Servos = [0,1,2,3,8]

setServo(15,180)
#setServo(15,90)


## Here is the arduino code for ya'll
# # include <Wire.h>
# # include <Adafruit_PWMServoDriver.h>
#
# Adafruit_PWMServoDriver
# pwm = Adafruit_PWMServoDriver();
#
# // Depending
# on
# your
# servo
# make, the
# pulse
# width
# min and max
# may
# vary, you
# // want
# these
# to
# be as small / large as possible
# without
# hitting
# the
# hard
# stop
# // for max range.You'll have to tweak them as necessary to match the servos you
# // have!
# # define SERVOMIN  150
# # define SERVOMAX  600
#
# // our
# servo  # counter
#
# void
# setup()
# {
#     Serial.begin(115200); // use
# the
# same
# baud - rate as the
# python
# side
#
# pwm.begin();
#
# pwm.setPWMFreq(60); // Analog
# servos
# run
# at
# ~60
# Hz
# updates
#
# delay(10);
# }
#
# void
# setServoPulse(uint8_t
# n, double
# pos) {
#     uint8_t
# servonum = n;
# uint16_t
# pulselength = SERVOMIN + pos / 180 * (SERVOMAX - SERVOMIN);
# pwm.setPWM(servonum, 0, pulselength);
#
# }
#
# void
# loop()
# {
#     String
# str = "";
# String
# channel = "";
# String
# position = "";
# int
# success = 0;
# while (1){
# if (Serial.available() > 0)
# {
# str = Serial.readStringUntil('\n');
# channel = Serial.readStringUntil('\,');
# position = Serial.readStringUntil('\n');
#
# Serial.print(channel+','+position);
# setServoPulse(channel.toInt(), position.toInt());
#
# }
# }
# }