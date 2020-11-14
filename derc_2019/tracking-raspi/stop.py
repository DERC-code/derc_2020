
import serial
import time
import pigpio

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)


pi = pigpio.pi()
#X_MAX = 1500 #下向き
#X_MIN = 800　#上向き
#X_HOME = 1300
# 
#Y_HOME = 1300
#Y_MAX = 1700 #左向き
#Y_MIN = 900 #右向き
#
def move(x_move, y_move):
    print('x_move: ', x_move)
    print('y_move: ', y_move)
    pi.set_servo_pulsewidth(4, x_move)
    pi.set_servo_pulsewidth(17, y_move)

ser.write(str.encode('m0:0\n'))
ser.write(str.encode('m1:0\n'))
move(1300,1300)
ser.close() 

