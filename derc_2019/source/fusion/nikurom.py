#! /usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO # (1)
from time import sleep

GPIO.setmode(GPIO.BOARD) # (2)
GPIO.setup(36,GPIO.OUT)  # (3)
#while True: 
sleep(2)
print("on")
GPIO.output(36,GPIO.HIGH)  # (4)
sleep(3)

print("off")
GPIO.output(36,GPIO.LOW)  # (4)
GPIO.cleanup() # (5)
