import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gp_out1 = 4
gp_out2 = 17
GPIO.setup(gp_out1, GPIO.OUT)
GPIO.setup(gp_out2, GPIO.OUT)

servo1 = GPIO.PWM(gp_out1, 50)
servo2 = GPIO.PWM(gp_out2, 50)

servo1.start(0.0)
servo2.start(0.0)

#servo1.ChangeDutyCycle(12.0)
time.sleep(0.5)

#servo1.ChangeDutyCycle(7.75)
time.sleep(0.5)

servo2.ChangeDutyCycle(4.75)
time.sleep(0.5)

#servo2.ChangeDutyCycle(7.75)
time.sleep(0.5)

#servo2.ChangeDutyCycle(2.5)
time.sleep(0.5)

#servo1.ChangeDutyCycle(2.5)
time.sleep(0.5)

servo2.stop()
servo1.stop()
GPIO.cleanup()
