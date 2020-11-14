import RPi.GPIO as GPIO
import time
import sys
import ta7291

class Motor():
    def __init__(self, pwmpin_L, in1_L, in2_L,pwmpin_R, in1_R, in2_R):
        self.leftmotor = ta7291.ta7291(pwmpin_L, in1_L, in2_L)
        self.rightmotor = ta7291.ta7291(pwmpin_R, in1_R, in2_R)

    def set_speed(self, leftspeed, rightspeed):
        self.leftmotor.drive(leftspeed)
        self.rightmotor.drive(rightspeed)
        
if __name__ == "__main__":
	pass