import mpu92_test
import RPi.GPIO as GPIO
import time
import sys
import ta7291
import Motor

def main():
    maxX = -10000
    maxY = -10000
    minX = 10000
    minY = 10000
    t_end = time.time() + 30
    setspeed = 100
    motor = Motor.Motor(18, 25, 24,13, 27, 17)
    #time.sleep(5)
    while time.time() < t_end:     
        magnet = mpu92_test.get_magnet()
        print(magnet)
        if(maxX < magnet[0]):
            maxX = magnet[0]
        if(minX > magnet[0]):
            minX = magnet[0]
        if(maxY < magnet[1]):
            maxY = magnet[1]
        if(minY > magnet[1]):
            minY = magnet[1]
#         print("maxx",maxX)
#         print("minx",minX)
#         print()
#         print("maxy",maxY)
#         print("miny",minY)
#         print()
        motor.set_speed(setspeed,setspeed) 
        time.sleep(1) 

if __name__ == '__main__':
    main()