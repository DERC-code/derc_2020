import RPi.GPIO as GPIO
import time
import sys
import ta7291
import Motor

motor = Motor.Motor(18, 25, 24,13, 17, 27)
print("setspeed")
motor.set_speed(-40, 40)
time.sleep(1.5)
motor.set_speed(-80, 80)
time.sleep(10000000.5)
# motor.set_speed(-100, 100)
# time.sleep(5)
# motor.set_speed(100, -100)
# time.sleep(3)
# motor.set_speed(-50, 50)
# time.sleep(3)   
# while True:
#     motor.set_speed(100, 100)
GPIO.cleanup()
