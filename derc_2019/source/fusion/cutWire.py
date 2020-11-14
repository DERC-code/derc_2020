#! /usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO # (1)

print("high voltage")
GPIO.setmode(GPIO.BOARD) # (2)
GPIO.setup(16,GPIO.OUT)  # (3)
GPIO.output(16,GPIO.HIGH)  # (4)
time.sleep(5)
GPIO.output(16,GPIO.LOW)  # (4)
print("low voltage")
GPIO.cleanup() # (5)