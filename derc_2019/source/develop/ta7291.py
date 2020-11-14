# pi@raspberrypi:~/work$ cat ta7291.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

class ta7291:
	'''
	Motor driver TA7291 class
	'''
	def __init__(self, pwm, in1, in2):
		# GPIOセットアップ
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pwm, GPIO.OUT)
		GPIO.setup(in1, GPIO.OUT)
		GPIO.setup(in2, GPIO.OUT)
		# ピンを保存
		self.in1 = in1
		self.in2 = in2
		self.p = GPIO.PWM(pwm, 50)#GPIOのチャンネルが被らないために引数を修正しました。

	def drive(self, speed):
		'''
		モーターを回転させる。
		speed : -100から100の数値。正の数なら正回転、負の数なら逆回転。
		'''
		GPIO.setmode(GPIO.BCM)
		if speed > 0:
			GPIO.output(self.in1, 1)
			GPIO.output(self.in2, 0)
			self.p.start(speed)
		if speed < 0:
			GPIO.output(self.in1, 0)
			GPIO.output(self.in2, 1)
			self.p.start(-speed)
		if speed == 0:
			GPIO.output(self.in1, 0)
			GPIO.output(self.in2, 0)
			
	def brake(self):
		GPIO.output(self.in1, 1)
		GPIO.output(self.in2, 1)
		time.sleep(0.5)

	def cleanup(self):
		'''
		最後は正面に戻して終了する
		'''
		self.brake()
		GPIO.cleanup()

if __name__ == "__main__":
	pass
