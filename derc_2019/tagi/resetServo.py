import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
gp_out1 = 17
gp_out2 = 27
gp_out3 = 22
GPIO.setup(gp_out1, GPIO.OUT)
GPIO.setup(gp_out2, GPIO.OUT)
GPIO.setup(gp_out3, GPIO.OUT)
servo1 = GPIO.PWM(gp_out1, 50)
servo2 = GPIO.PWM(gp_out2, 50)
servo3 = GPIO.PWM(gp_out3, 50)
servo1.start(0.0)
servo2.start(0.0)
servo3.start(0.0)
servo1.ChangeDutyCycle(7.5)
time.sleep(0.5)
servo1.stop()
servo2.ChangeDutyCycle(7.5)
time.sleep(0.5)
servo2.stop()
servo3.ChangeDutyCycle(7.5)
time.sleep(0.5)
servo3.stop()
GPIO.cleanup()
