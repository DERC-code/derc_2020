import RPi.GPIO as GPIO
import time
import sys
import ta7291
import Motor
import math

def main():
    
    setspeed = 100
    motor = Motor.Motor(18, 25, 24,13, 27, 17)
    motor.set_speed(-setspeed,setspeed) 
    time.sleep(10) #10秒動かす
   
    GPIO.cleanup()
    
    
if __name__ == "__main__":
    main()

    