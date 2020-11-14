# pi@raspberrypi:~/work$ cat motor_test.py 
#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import ta7291

if __name__ == "__main__":
	d = ta7291.ta7291(18, 25, 24)
	'''
	18番ピン被るかもしれない
	'''
	d2 = ta7291.ta7291(13, 17, 27)

	print ("Max speed 3 seconds, and stop...")
	d.drive(100)
	d2.drive(100)
	time.sleep(3)
	d.drive(0)
	d2.drive(0)
	time.sleep(3)
	d.brake()
	d2.brake()
