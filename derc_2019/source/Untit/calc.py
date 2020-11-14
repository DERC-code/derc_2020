import mpu92_test
import RPi.GPIO as GPIO
import time
import sys
import ta7291
import Motor
import threading

def calc():
    maxX = -100
    maxY = -100
    minX = 100
    minY = 100
    t_end = time.time() + 10
    setspeed = 100
    motor = Motor.Motor(18, 25, 24,13, 27, 17)
    time.sleep(5)
    while time.time() < t_end:     
        magnet = mpu92_test.get_magnet()
        if(maxX < magnet[0]):
            maxX = magnet[0]
        if(minX > magnet[0]):
            minX = magnet[0]
        if(maxY < magnet[1]):
            maxY = magnet[1]
        if(minY > magnet[1]):
            minY = magnet[1]
        #print("magnet[%+4.2f, %+4.2f, %+4.2f]" % (magnet[0], magnet[1], magnet[2]), end="\t")
        print("maxx",maxX)
        print("minx",minX)
        print()
        print("maxy",maxY)
        print("miny",minY)
        print()
        motor.set_speed(-100,100) 
        time.sleep(1)

def rot():
    setspeed = 100
    motor = Motor.Motor(18, 25, 24,13, 27, 17)
    motor.set_speed(-setspeed,setspeed) 
    time.sleep(10) #10秒動かす    

def main():
    calc()
#     thread_1=threading.Thread(target=calc)
#     thread_2=threading.Thread(target=rot)
    
#     thread_1.start()
#     thread_2.start()

if __name__ == '__main__':
    main()