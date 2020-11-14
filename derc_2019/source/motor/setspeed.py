import RPi.GPIO as GPIO
import time
import sys
import ta7291

if __name__ == "__main__":
    d = ta7291.ta7291(18, 24, 25)

class motor:
    def __init__(self, pwm, in1, in2):
        leftmotor = ta7291.ta7291(18, 24, 25)
        rightmotor = ta7291.ta7291(18, 24, 25)

    def setspeed(self, leftmotor, rightmotor):
        leftmotor.drive(leftspeed)
        rightmotor.drive(rightspeed) 