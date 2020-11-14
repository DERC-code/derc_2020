import RPi.GPIO as GPIO
import time
import numpy as np
import math
import threading

L1 = 180
L2 = 140
locationX=100
locationY=100
locationZ=0

def calc(x, y, z):
        Ld = np.sqrt((x ** 2)+(y ** 2)+(z ** 2))
        rad1 = math.atan2(y, x)
        radFor2=((L1 ** 2)+(Ld **2)-(L2 ** 2))/(2*L1*Ld)
        if radFor2 > 1:
                radFor2 = 1
        elif radFor2 <-1:
                radFor2 = -1
        radFor3 = ((Ld ** 2)-(L1 ** 2)-(L2 ** 2))/(2*L1*L2)
        if radFor3 > 1:
                radFor3 = 1
        elif radFor3 < -1:
                radFor3 = -1
        rad2 = math.acos(radFor2)+math.atan2(z,np.sqrt((x ** 2)+(y ** 2)))
        rad3 = math.asin(radFor3)+(np.pi/2)
        if 0<=rad2 and rad2<(np.pi/2):
                servorad2 = (np.pi/2)-rad2
        elif (np.pi/2)<= rad2 and rad2 <=np.pi:
                servorad2 = -(np.pi-rad2)
        else:
                servorad2 = 0
                #連続で動かす際は前回の値がいいけどな
        if 0<=rad3 and rad3<(np.pi/2):
                servorad3 = (np.pi/2)-rad3
        elif (np.pi/2)<= rad3 and rad3 <=np.pi:
                servorad3 = -(np.pi-rad2)
        else:
                servorad3 = 0
                #これも連続の際は前回の値がいい
        return [rad1, servorad2, servorad3]

def runServo1(servo1,arg1):
        servo1.start(0.0)
        servo1.ChangeDutyCycle(arg1*(9.5/np.pi)+7.25)
        time.sleep(0.3)
        servo1.stop()

def runServo2(servo2,arg2):
        servo2.start(0.0)
        servo2.ChangeDutyCycle(arg2*(9.5/np.pi)+7.25)
        time.sleep(0.3)
        servo2.stop()

def runServo3(servo3,arg3):
        servo3.start(0.0)
        servo3.ChangeDutyCycle(arg3*(9.5/np.pi)+7.25)
        time.sleep(0.3)
        servo3.stop()

def main():
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
        args = calc(locationX,locationY,locationZ-20)
        args2= calc(50,50,30)
        print(args)
        print(args[0]*57.2958)
        print(args[1]*57.2958)
        print(args[2]*57.2958)
        thread_1 = threading.Thread(target=runServo1(servo1,args[0]))
        thread_2 = threading.Thread(target=runServo2(servo2,args[1]))
        thread_3 = threading.Thread(target=runServo3(servo3,args[2]))
        thread_1.start()
        thread_2.start()
        thread_3.start()
        time.sleep(1)
        #print(args2[0]*57.2958)
        #print(args2[1]*57.2958)
        #print(args2[2]*57.2958)
        #thread_4 = threading.Thread(target=runServo1(servo1,args2[0]))
        #thread_5 = threading.Thread(target=runServo2(servo2,args2[1]))
        #thread_6 = threading.Thread(target=runServo3(servo3,args2[2]))
        #thread_4.start()
        #thread_5.start()
        #thread_6.start()
        servo1.stop()
        servo2.stop()
        servo3.stop()
        GPIO.cleanup()

if __name__ == "__main__":
        main()
